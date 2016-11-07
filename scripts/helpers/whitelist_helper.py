import os

import yaml


"""
Merging dictionaries
If argument is list, not a dictionary, there is an assumption
that it is a list of dictionaries and should be merged recursively
If argument is a dictionary, there is assumption that the key is 
an ip, and the value is a comma-joined list of ports.
When two such lists are merged, the result is a union of both lists.
E.g. merging {'a.b.c.d':'1,2'} with {'a.b.c.d':'2,3'} should give
{'a.b.c.d':'1,2,3'} as a result
"""

def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        if dictionary is None:
            continue
        if isinstance(dictionary, list):
            merged = {}
            for d in dictionary: # the variable 'dictionary' so far is a list
                merged = merge_dicts(merged, d)
            dictionary = merged # and now it has been converted to a dict
        for k in dictionary.keys():
            if k not in result.keys():
                result[k] = dictionary[k]
            else:
                result[k] = merge_ports(result[k], dictionary[k])
    return result

def merge_ports(portx, porty):
    inportsx = portx.split(',')
    inportsy = porty.split(',')
    for p in inportsy:
        if p not in inportsx:
            inportsx.append(p)
    return ','.join(inportsx)

def convert_list_to_dict(list_arg):
    if isinstance(list_arg, list): # list of dicts {ip: 'port'}
        merged = {}
        for d in list_arg:
            merged = merge_dicts(merged, d)
        list_arg = merged
    return list_arg

"""
The Singleton class has been copied from:
http://stackoverflow.com/a/7346105
It is an unmodified code created by Paul Manta
The code has been licensed with Creative Commons CC-BY-SA
"""

class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class Whitelist_helper:

    def __init__(self):
        self.config = {}
        self.read = False

    def read_config(self):
        filename = os.path.dirname(os.path.abspath(__file__)) + "/../config/whitelist.yaml"
        try:
            stream = open(filename, "r")
            return yaml.load(stream)
        except IOError:
            pass

    def get_config(self):
        if self.read == False:
            self.config = self.read_config()
            self.read = True

    def get_config_for_module(self, module):
        self.get_config()
        if self.config is None:
            return None

        config = {}

        if module in self.config and self.config[module] is not None:
            config = self.config[module]

        config = convert_list_to_dict(config)

        if '*' in self.config and self.config['*'] is not None:
            if not isinstance(self.config['*'], dict):
                self.config['*'] = convert_list_to_dict(self.config['*'])
            config = merge_dicts(config, self.config['*'])

        return config
