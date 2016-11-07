import os
from abc import ABCMeta

import yaml

import finding
from whitelist_helper import Whitelist_helper


class Script:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.finding = finding.Finding()
        self.config = self.get_config()
        self.result = []
        self.whitelist = self.get_whitelist()

    def get_config(self):
        module_name = self.__module__
        abs_path = os.path.abspath(__file__)
        filename = os.path.dirname(abs_path) + "/../config/" + module_name + ".yaml"
        try:
            stream = open(filename, "r")
            return yaml.load(stream)
        except IOError:
            pass

    def get_whitelist(self):
        module_name = self.__module__
        helper = Whitelist_helper.Instance()
        return helper.get_config_for_module(module_name)

    def is_finding_on_whitelist(self, finding):
        whitelist = self.get_whitelist()
        if whitelist is None:
            return False
        for el in whitelist:
            if finding['address'] == el:
                # if there is only ip on whitelist without ports specified
                if whitelist[finding['address']] is None:
                    return True
                ports = whitelist[finding['address']].split(',')
                if str(finding['port']) in ports:
                    return True
            if '*' == el and whitelist[el] is not None:
                if str(finding['port']) in whitelist['*']:
                    return True
        return False

    def enumerate(self, finding):
        self.finding = finding
        if self.assess_finding() is False:
            return False

    def add_result(self, result, level):
        self.result.append(level.upper() + ': ' + str(result))

    def get_result(self):
        return self.result
