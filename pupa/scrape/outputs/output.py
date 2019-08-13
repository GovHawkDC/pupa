import json

from abc import abstractmethod, ABCMeta
from collections import OrderedDict

from pupa import utils
from pupa.scrape.objects.objects import get_obj_attrs, get_obj_hash


class Output(metaclass=ABCMeta):

    def __init__(self, scraper):
        self.scraper = scraper

    def add_output_name(self, obj):
        filename = '{0}_{1}.json'.format(obj._type, obj._id).replace('/', '-')
        self.scraper.output_names[obj._type].add(filename)

    def debug_obj(self, obj):
        self.scraper.debug(json.dumps(OrderedDict(sorted(obj.as_dict().items())),
                           cls=utils.JSONEncoderPlus,
                           indent=4, separators=(',', ': ')))

    def get_obj_as_dict(self, obj, add_jurisdiction=False, add_type=False):
        obj_dict = obj.as_dict()
        if add_jurisdiction and self.scraper.jurisdiction:
            obj_dict['jurisdiction'] = self.scraper.jurisdiction.jurisdiction_id
        if add_type:
            obj_dict['type'] = obj._type
        return obj_dict

    @abstractmethod
    def handle_output(self, obj, **kwargs):
        pass

    def pre_handle_output(self, obj, **kwargs):
        cache_target = kwargs.get('cache_target')
        # Handle as normal if no cache target specified
        if cache_target is None:
            self.handle_output(obj)
            return

        obj_dict = self.get_obj_as_dict(obj, True, True)
        obj_attrs = get_obj_attrs(obj_dict)
        # Check for object key
        if obj_attrs.get('key') is None:
            self.scraper.info('no cache key found for %s; skipping', obj)
            return

        cached_obj_hash = cache_target.get(obj_attrs.get('key'))
        obj_hash = get_obj_hash(obj_dict)
        # Bail if object already processed and cached
        if cached_obj_hash and obj_hash == cached_obj_hash:
            self.scraper.info('%s already cached', obj)
            return

        # Cache and handle as normal
        cache_target.set(obj_attrs.get('key'), obj_hash, obj=obj)
        self.handle_output(obj, **obj_attrs)

    def save_object(self, obj, **kwargs):
        obj.pre_save(self.scraper.jurisdiction.jurisdiction_id)
        self.debug_obj(obj)
        self.add_output_name(obj)

        self.pre_handle_output(obj, **kwargs)

        # validate after writing, allows for inspection on failure
        try:
            obj.validate()
        except ValueError as ve:
            if self.scraper.strict_validation:
                raise ve
            else:
                self.scraper.warning(ve)

        # after saving and validating, save subordinate objects
        for obj in obj._related:
            self.save_object(obj)

    def stringify_obj(self, obj, add_jurisdiction=False, add_type=False):
        obj_dict = self.get_obj_as_dict(obj, add_jurisdiction, add_type)
        return self.stringify_obj_dict(obj_dict)

    def stringify_obj_dict(self, obj_dict):
        return json.dumps(obj_dict, cls=utils.JSONEncoderPlus,
                          separators=(',', ':'))
