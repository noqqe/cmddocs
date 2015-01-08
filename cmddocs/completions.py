import os

def path_complete(self, text, line, begidx, endidx):
    """
    Path completition function used in various places for tab completion
    when using cmd
    """
    arg = line.split()[1:]

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
                if os.path.isfile(os.path.join(dir,f)):
                    completions.append(f)
                else:
                    completions.append(f+'/')
    return completions
