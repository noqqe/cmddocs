import os
import ConfigParser
from os.path import expanduser
from utils import *

def path_complete(self, text, line, begidx, endidx):
    """
    Path completition function used in various places for tab completion
    when using cmd
    """
    arg = line.split()[1:]

    # this is a workaround to get default extension into the completion function
    # may (hopefully) gets replaced.
    config = ConfigParser.ConfigParser()
    config.read(expanduser("~/.cmddocsrc"))
    extension = config.get("General", "Default_Extension")

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
