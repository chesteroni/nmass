from string import Template


class Result:
    template_raw = Template(
        '$module'
        + ',class: ' + '$classname'
        + ' on IP: ' + '$address'
        + ', port: ' + '$port'
        + ' | ' + '$description')
    template_csv = Template(
        '"'
        + '$module' + '";"'
        + '$classname' + '";"'
        + '$address' + '";"'
        + '$port' + '";"'
        + '$description' + '"'
        + "\n")

    def __init__(self):
        self.finding = None
        self.module = None
        self.classname = None
        self.description = None

    def get_data(self):
        return dict(module=str(self.module),
                    classname=str(self.classname),
                    address=str(self.finding['address']),
                    port=str(self.finding['port']),
                    description=str(self.description))

    def get_result(self):
        if bool(self) is False:
            return None
        return self.template_raw.safe_substitute(self.get_data())

    def get_result_csv(self):
        if bool(self) is False:
            return None
        return self.template_csv.safe_substitute(self.get_data())

    def __bool__(self):
        if self.finding is not None and self.module is not None and self.classname is not None and self.description is not None:
            return True;
        return False

    __nonzero__ = __bool__

    def __str__(self):
        dictionary = {"finding": self.finding, "module": self.module, "class": self.classname,
                      "desc": self.description}
        return str(dictionary)
