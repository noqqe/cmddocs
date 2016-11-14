import os
import configparser
from os.path import expanduser
from .utils import *

def path_complete(self, text, line, begidx, endidx):
    """
    Path completition function used in various places for tab completion
    when using cmd
    """
    arg = line.split()[1:]

    # this is a workaround to get default extension into the completion function
    # may (hopefully) gets replaced.
    try:
        config = configparser.ConfigParser()
        if not config.read(expanduser("~/.cmddocsrc")):
            print("Error: your config %s could not be read" % conf)
            exit(1)
        extension = config.get("General", "Default_Extension")
    except configparser.NoOptionError:
        self.extension = "md"

    if not arg:
        completions = os.listdir('./')
        completions[:] = [d for d in completions if d not in self.exclude]
    else:
        dir, part, base = arg[-1].rpartition('/')
        if part == '':
            dir = './'
        elif dir == '':
            dir = '/'

        completions = []
        for f in os.listdir(dir):
            if f.startswith(base):
                if os.path.isfile(os.path.join(dir, f)):
                    f = remove_fileextension(f, extension)
                    completions.append(f)
                else:
                    completions.append(f+'/')
    return completions
