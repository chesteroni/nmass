import sys

import MySQLdb
import _mysql_exceptions

from helpers.password_helper import Password_helper
from helpers.result import Result
from helpers.script import Script


class Nmass_mysql(Script):
    def __init__(self):
        super(Nmass_mysql, self).__init__()
        self.users = self.config["users"].keys()
        helper = Password_helper(self.config["users"])
        self.passwords = helper.get_passwords()

    def assess_finding(self):
        if not self.is_finding_on_whitelist(self.finding) and self.finding['port'] in [3306, 3307]:
            return True
        return False

    def enumerate(self, finding):
        check = super(Nmass_mysql, self).enumerate(finding)
        if check is False:
            return False

        r = Result()
        for u in self.users:
            for p in self.passwords[u]:
                conn_result = self.conn(self.finding["address"], self.finding["port"], u, p)

                if conn_result is not False:
                    r.module = sys.modules[__name__]
                    r.classname = self.__class__.__name__
                    r.finding = finding

                    message = "MySQL connection on user %s with password '%s', did not try further!"
                    r.description = message % (u, p)
                    return r
        return r

    def conn(self, host, port, user, passwd):
        try:
            c = MySQLdb.connect(host, user, passwd, '', port)
        except _mysql_exceptions.OperationalError:
            return False
        c.close()
        return True
