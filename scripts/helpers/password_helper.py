class Password_helper:


    def __init__(self, config_node):
        self.config_node = config_node
        self.passwords = {}


    def get_passwords(self):
        if self.passwords == {}:
            users = self.config_node.keys()
            for user in users:
                config = self.get_config(self.config_node[user])
                try:
                    words = self.get_from_file(config["file"])
                except KeyError:
                    words = config["pass"].split(",")
                self.passwords[user] = self.reduce_list(words)
        return self.passwords


    def reduce_list(self,seq):
        already = set()
        already_add = already.add # to not call each time the objecta
        return [el for el in seq if not (el in already or already_add(el))]


    def get_from_file(self, filename):
        f = open(filename)
        content = f.read().splitlines()
        return content


    def get_config(self, config):
        try:
            ret = {}
            ret["type"] = config["type"]
            if ret["type"] != "dictionary":
                print "bad type"
                return self.get_empty_dictionary()
        except:
            print("Type is missing in config, assuming wordlist with empty password")
            return self.get_empty_dictionary()
        try:
            ret["file"] = config["file"]
        except:
            try:
                ret["pass"] = config["pass"]
            except:
                print("Unknown password file or passwordlist, assuming wordlist with empty password")
                ret["pass"] = [""]
        return ret


    def get_empty_dictionary(self):
        return {"type" : "dictionary", "pass" : [""]}
