#!/usr/bin/env python

import os 
import sys
import cmd
import git

datadir = "/home/noqqe/Code/cmddocs/data"
exclude = ".git/"

try: 
    repo = git.Repo(datadir)
except:
    repo = git.Repo.init(datadir)
    repo.git.add(".")
    repo.git.commit("init")
    print("Successfully created and initialized empty repo")


def list_articles(datadir):
    for root, dirs, files in os.walk(datadir):
        # exclude .git/
        dirs[:] = [d for d in dirs if d not in exclude]
        # build tree view
        level = root.replace(datadir, '').count(os.sep)
        indent = ' ' * 2 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 2 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

def edit_article(article, datadir):
    os.system('%s %s' % (os.getenv('EDITOR'),
        os.path.join(datadir,article)))
    repo.git.add(os.path.join(datadir,article))
    msg = raw_input("Commit message: ")
    repo.git.add(os.path.join(datadir,article))
    repo.git.commit(m=msg)

class Prompt(cmd.Cmd):
    """ Basic commandline interface class """

    prompt = "cmddocs> "
    intro = "Welcome to cmddocs"
    
    def do_greet(self, line):
        print "hello"
    
    def do_list(self, line):
        list_articles(datadir)

    def do_edit(self, article):
        edit_article(article, datadir)

    def do_status(self, line):
        print repo.git.status()

    def do_log(self, line):
        print repo.git.log()

    def do_exit(self, line):
        return True

    def do_EOF(self, line):
        print "exit"
        return True

if __name__ == '__main__':
    Prompt().cmdloop()
