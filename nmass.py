import importlib
import os
import sys

import click

from scripts.helpers import finding
from scripts.helpers.script_helper import get_scripts

sys.path.append("scripts")

NMASS_STATE_FILE = ".nmass_state"

INMASS_HELP = "Input file with results of masscan. When omitted, the default is stdin."
SCRIPTS_HELP = "List of modules and/or classes in modules that should be used.\n\
e.g. mysql,smtp/spoof,smtp/relay would use all the classes in mysql module and only spoof and relay classes from smtp module\n\
When omitted, the default is 'all' and nmass would fire all the tools available in the scripts directory"
INTYPE_HELP = "Type of input file. Available options are xml and grep for the default format and the -oG output"
OUT_HELP = "Type of output. Default format is human readable, usable for good understanding of findings, but there is also CSV format available"
IGNORE_SAVED_HELP = "Nmass can save its state into .nmass_state file. You can disable auto-resume behaviour with this option"


def get_file(inmass):
    if not isinstance(inmass, file):
        try:
            fp = open(inmass)
        except:
            print("Fatal error, cannot open file: " + inmass)
            sys.exit(1)
    else:
        fp = inmass
    return fp


@click.command()
@click.pass_context
@click.option('--inmass', default=sys.stdin, type=click.STRING, help=INMASS_HELP)
@click.option('--scripts', default="all", type=click.STRING, help=SCRIPTS_HELP)
@click.option('--intype', default="xml", type=click.Choice(['xml', 'grep']), help=INTYPE_HELP)
@click.option('--out', default="string", type=click.Choice(['string', 'csv']), help=OUT_HELP)
@click.option('--ignoresaved', default="no", type=click.Choice(['yes', 'no']),
              help=IGNORE_SAVED_HELP)
def sectest(
        ctx,
        inmass,
        scripts,
        intype,
        out,
        ignoresaved):
    if ignoresaved == "yes":
        delete_state_file()

    state_content = []
    if os.path.isfile(NMASS_STATE_FILE):
        print("Found saved state, resuming")
        f = open(NMASS_STATE_FILE)
        state_content = f.read().splitlines()
        if len(state_content) != 8:
            print("Invalid state file, ignoring")
        else:
            if state_content[4] == "<stdin>":
                inmass = sys.stdin
            else:
                inmass = state_content[4]
            scripts = state_content[5]
            intype = state_content[6]
            out = state_content[7]

    fp = get_file(inmass)
    f_helper = finding.Finding_helper()
    findings = []
    scripts_to_import = get_scripts(scripts)

    if intype == "xml":
        for line in fp:
            found = f_helper.get_from_xml(line)
            if found is not None:
                findings.append(found)
    else:
        print ("grep format is not yet supported")
        sys.exit()

    # Main loop: for each script: for each finding: enumerate()!
    for script in scripts_to_import:
        if not isinstance(script, list):
            print("Invalid script given, ignoring: %s" % str(script))
            continue
        module = script[0]
        classname = script[1][0].upper() + script[1][1:]
        state_content_size = len(state_content)
        if state_content_size == 8 and \
                (state_content[0] != module or state_content[1] != classname):
            continue

        try:
            m = importlib.import_module(module, classname)
            obj = getattr(m, classname)()
            for f in findings:
                if state_content_size == 8 and \
                        (state_content[2] != str(f['port']) or state_content[3] != f['address']):
                    continue
                state = open(NMASS_STATE_FILE, "w")

                first_line = \
                    module + "\n" + classname + "\n" + str(f['port']) + "\n" + f['address'] + "\n"
                state.write(first_line)

                second_line = inmass.name + "\n" + scripts + "\n" + intype + "\n" + out
                state.write(second_line)

                result = obj.enumerate(f)
                if bool(result) is True:
                    if out == "string":
                        print(result.get_result())
                    elif out == "csv":
                        print(result.get_result_csv())
                state.close()
        except ImportError as e:
            print ("no module %s or class %s ignoring" % (module, classname))
            continue
    delete_state_file()


def delete_state_file():
    try:
        if os.path.isfile(NMASS_STATE_FILE):
            os.remove(NMASS_STATE_FILE)
    except OSError:
        print("Could not remove nmass' state file")


if __name__ == '__main__':
    sectest()
