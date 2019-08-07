import copy
import hashlib
import json


def get_obj_attrs(obj):
    """Get object attributes

    :param obj: scrape object as modified dict (@see Output#get_obj_as_dict)
    :type obj: dict
    :returns obj_attrs: object attributes
    :rtype: dict
    """

    try:
        obj_type = obj.get('type')
    except AttributeError:
        return dict(key=None, type=None)

    # TODO: Not important, but could probably come up with a better key format
    if obj_type == 'bill':
        obj_key = '{type}-{jurisdiction}-{session}-{id}'.format(
            type=obj_type,
            jurisdiction=obj['jurisdiction'],
            session=_format_key_chunk(obj['legislative_session']),
            id=_format_key_chunk(obj['identifier']))
        return dict(key=obj_key, type=obj_type)
    if obj_type == 'event':
        obj_key = '{type}-{jurisdiction}-{start_date}-{id}'.format(
            type=obj_type,
            jurisdiction=obj['jurisdiction'],
            start_date=obj['start_date'].replace(':00+00:00', '').replace(':', ''),
            id=hashlib.md5(obj['name'].encode('utf-8')).hexdigest())
        return dict(key=obj_key, type=obj_type)
    if obj_type == 'vote_event':
        # NOTE: `obj['bill']` looks like '~{"identifier": "SR 3"}'
        bill = json.loads(obj['bill'][1:]) if 'bill' in obj else dict()
        obj_key = '{type}-{jurisdiction}-{session}-{id}-{motion_text}-{start_date}'.format(
            type=obj_type,
            jurisdiction=obj['jurisdiction'],
            session=_format_key_chunk(obj['legislative_session']),
            # TODO: Do we want to use a default ID?
            id=_format_key_chunk(bill.get('identifier', 'EMPTY_BILL_NAME')),
            motion_text=_format_key_chunk(obj['motion_text']),
            start_date=obj['start_date'])
        return dict(key=obj_key, type=obj_type)
    return dict(key=None, type=None)


def get_obj_hash(obj):
    """Get object hash

    :param obj: scrape object as modified dict (@see Output#get_obj_as_dict)
    :type obj: dict
    :returns obj_hash: object hash
    :rtype: string
    """

    # TODO: Do we need to deep copy? Is _id key required anywhere else?
    deep_obj_copy = copy.deepcopy(obj)
    deep_obj_copy.pop('_id', None)

    stringified_obj = json.dumps(_get_deep_sorted_obj(deep_obj_copy))
    return hashlib.md5(stringified_obj.encode('utf-8')).hexdigest()


def _format_key_chunk(key_chunk):
    """Format key chunk

    :param key_chunk: key chunk
    :type key_chunk: string
    :return formatted_key_chunk: formatted key chunk
    :type formatted_key_chunk: string
    """

    return ' '.join(key_chunk.upper().split())


def _get_deep_sorted_obj(obj):
    """Helper to deep sorted scrape object, _including_ nested lists and tuples

    :see: https://stackoverflow.com/a/25851972/1858091

    :param obj: scrape object
    :type obj: dict
    :returns deep_sorted_obj: deep sorted scrape object
    :rtype: dict
    """

    if isinstance(obj, dict):
        return sorted((k, _get_deep_sorted_obj(v)) for k, v in obj.items())
    if isinstance(obj, (list, tuple,)):
        return sorted(_get_deep_sorted_obj(v) for v in obj)
    return obj
