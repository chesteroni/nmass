from abc import ABCMeta
import yaml
import os
import finding


class Script:
    __metaclass__ = ABCMeta


    def __init__(self):
        self.finding = finding.Finding()
        self.config = self.get_config()
        self.result = []


    def get_config(self):
        module_name = self.__module__
        filename = os.path.dirname(os.path.abspath(__file__)) + "/../config/" + module_name + ".yaml"
        try:
            stream = open(filename, "r")
            return yaml.load(stream)
        except IOError:
            pass


    def enumerate(self, finding):
        self.finding = finding
        if self.assess_finding() is False:
            return False


    def add_result(self, result, level):
        self.result.append(level.upper() + ': ' + str(result))


    def get_result(self):
        return self.result
