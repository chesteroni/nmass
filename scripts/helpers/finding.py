import xmltodict
import collections
from itertools import chain

# based on http://stackoverflow.com/posts/39375731/edit
# the code of finding contains modifications 
# Original code author is Aaron Hall http://stackoverflow.com/users/541136/aaron-hall
# The original code is licensed through CC-BY-SA https://creativecommons.org/licenses/by-sa/3.0/
# Therefore this file is licensed with the same conditions

items = 'iteritems'

def ensure_finding(maybe_str):
    if maybe_str not in ('port', 'address'):
        raise ValueError("Invalid key provided for finding, only port and address are allowed.")
    return maybe_str


class Finding_helper():


    """
    Example line:
    <host endtime="1473799051"><address addr="127.0.0.1" addrtype="ipv4"/><ports><port protocol="tcp" portid="80"><state state="open" reason="syn-ack" reason_ttl="244"/></port></ports></host>
    """
    def get_from_xml(self, line):
        if not line.startswith('<host '):
            return None
        line = '<?xml version="1.0" ?>' + line # line by line scanning, not as a whole XML
        dictionary = xmltodict.parse(line)
        ret = Finding()
        ret['port'] =  int(dictionary['host']['ports']['port']['@portid'])
        ret['address'] = dictionary['host']['address']['@addr']
        return ret


class Finding(dict):  # dicts take a mapping or iterable as their optional first argument

    __slots__ = () # no __dict__ - that would be redundant


    @staticmethod # because this doesn't make sense as a global function.
    def _process_args(mapping=(), **kwargs):
        if hasattr(mapping, items):
            mapping = getattr(mapping, items)()
        return ((ensure_finding(k), v) for k, v in chain(mapping, getattr(kwargs, items)()))


    def __init__(self, mapping=(), **kwargs):
        super(Finding, self).__init__(self._process_args(mapping, **kwargs))


    def __getitem__(self, k):
        return super(Finding, self).__getitem__(ensure_finding(k))


    def __setitem__(self, k, v):
        return super(Finding, self).__setitem__(ensure_finding(k), v)


    def __delitem__(self, k):
        return super(Finding, self).__delitem__(ensure_finding(k))


    def get(self, k, default=None):
        return super(Finding, self).get(ensure_finding(k), default)


    def setdefault(self, k, default=None):
        return super(Finding, self).setdefault(ensure_finding(k), default)


    def pop(self, k):
        return super(Finding, self).pop(ensure_finding(k))


    def update(self, mapping=(), **kwargs):
        super(Finding, self).update(self._process_args(mapping, **kwargs))


    def __contains__(self, k):
        return super(Finding, self).__contains__(ensure_finding(k))


    @classmethod
    def fromkeys(cls, keys):
        return super(Finding, cls).fromkeys(ensure_finding(k) for k in keys)
