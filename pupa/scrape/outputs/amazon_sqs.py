import boto3
import os
import json
import uuid
from collections import OrderedDict

from pupa import utils
from pupa.scrape.outputs.output import Output

MAX_BYTE_LENGTH = 230000


class AmazonSQS(Output):

    def __init__(self, scraper):
        super().__init__(scraper)

        self.sqs = boto3.resource('sqs')
        # The modifications being made here to push the caching layer closer to the
        # scrape allow us to publish messages based on different scrape type (e.g.,
        # vote event vs. bill)... so the AMAZON_SQS_QUEUE_PREFIX env var functions
        # as queue prefix, assuming the pattern $QUEUE_PREFIX$TYPE
        self.queue_prefix = os.environ.get('AMAZON_SQS_QUEUE_PREFIX', '')
        self.queue_sep = os.environ.get('AMAZON_SQS_QUEUE_SEP', '')
        self.default_queue_name = os.environ.get('AMAZON_SQS_QUEUE')
        self.queues = {}

        self.s3 = boto3.resource('s3')
        self.bucket_name = os.environ.get('AMAZON_S3_BUCKET')
        self.always_use_s3 = os.environ.get('AMAZON_S3_ALWAYS', False)
        self.always_use_s3 = bool(self.always_use_s3)

    def handle_output(self, obj, **kwargs):
        name = self.queue_prefix + self.queue_sep + kwargs.get('type', self.default_queue_name)
        queue = self._get_queue(name)

        self.scraper.info('send %s %s to queue %s', obj._type, obj, name)
        self.debug_obj(obj)

        self.add_output_name(obj, name)
        obj_str = self.stringify_obj(obj, True, True)
        encoded_obj_str = obj_str.encode('utf-8')

        if self.always_use_s3 or len(encoded_obj_str) > MAX_BYTE_LENGTH:
            key = 'S3:{}'.format(str(uuid.uuid4()))

            self.scraper.info('put %s %s to bucket %s/%s', obj._type, obj,
                              self.bucket_name, key)

            self.s3.Object(self.bucket_name, key).put(Body=encoded_obj_str)
            queue.send_message(MessageBody=key)
        else:
            queue.send_message(MessageBody=obj_str)

    def _get_queue(self, name):
        queue = self.queues.get(name)

        if queue is not None:
            return queue

        queue = self.sqs.get_queue_by_name(QueueName=name)
        self.queues[name] = queue

        return queue
