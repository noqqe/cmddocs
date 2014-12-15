#!/usr/bin/env python

import os
import sys
import cmd
import git

datadir = "/home/noqqe/Code/cmddocs/data"
exclude = ".git/"
os.chdir(datadir)

try:
    repo = git.Repo(datadir)
except:
    repo = git.Repo.init(datadir)
    repo.git.add(".")
    repo.git.commit("init")
    print("Successfully created and initialized empty repo")


def list_articles(cwd):
    for root, dirs, files in os.walk(cwd):
        # exclude .git/
        dirs[:] = [d for d in dirs if d not in exclude]
        # build tree view
        level = root.replace(cwd, '').count(os.sep)
        indent = ' ' * 2 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 2 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

def edit_article(article, datadir):
    # set paths
    a = os.path.join(datadir,article)
    d = os.path.dirname(a)

    # create dir(s)
    if not os.path.isdir(d):
        os.makedirs(d)

    # start editor
    os.system('%s %s' % (os.getenv('EDITOR'),a))

    # commit into git
    try:
        repo.git.add(a)
        if repo.is_dirty():
            msg = raw_input("Commit message: ")
            repo.git.commit(m=msg)
        else:
            print "Nothing to commit"
    except:
        pass

class Prompt(cmd.Cmd):
    """ Basic commandline interface class """

    prompt = "\033[1m\033[37mcmddocs> \033[0m"
    intro = "Welcome to cmddocs"

    ### list
    def do_list(self, line):
        return list_articles(datadir)

    def do_l(self, cwd):
        if not cwd:
            cwd = datadir
        return list_articles(cwd)

    def complete_l(self, text, line, begidx, endidx):
        arg = line.split()[1:]

        if not arg:
            completions = os.listdir('./')
            completions[:] = [d for d in completions if d not in exclude]
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


    ### edit
    def do_edit(self, article):
        edit_article(article, datadir)

    def do_e(self, article):
        return edit_article(article, datadir)

    ### misc
    def do_status(self, line):
        print repo.git.status()

    def do_log(self, line):
        print repo.git.log(oneline=True,n=5)

    ### exit
    def do_exit(self, line):
        return True

    def do_EOF(self, line):
        print "exit"
        return True


if __name__ == '__main__':
    Prompt().cmdloop()
