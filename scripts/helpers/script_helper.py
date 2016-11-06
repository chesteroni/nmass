import glob
import importlib
import os


def classesinmodule(module):
    md = module.__dict__
    return [md[c] for c in md if (isinstance(md[c], type) and md[c].__module__ == module.__name__)]


def get_scripts(scripts):
    import_list = []
    if scripts == "all":
        modules = glob.glob(os.path.dirname(os.path.abspath(__file__)) + "/scripts/*.py")
        list_modules = [os.path.basename(f)[:-3] for f in modules if os.path.isfile(f)]
        for mod in list_modules:
            mo = importlib.import_module(mod)
            classlist = classesinmodule(mo)
            for c in classlist:
                parts = [
                    mod,
                    c.__name__
                ]
                import_list.append(parts)
    else:
        for element in scripts.split(","):
            if '/' not in element:
                modulename = 'nmass_' + element
                mo = importlib.import_module(modulename)
                classlist = classesinmodule(mo)
                for c in classlist:
                    parts = [
                        modulename,
                        c.__name__
                    ]
                    import_list.append(parts)
            else:
                parts = str(element).split('/')
                parts[0] = 'nmass_' + parts[0]
                import_list.append(parts)
    return import_list
