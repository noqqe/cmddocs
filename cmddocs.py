#!/usr/bin/env python

import os
import sys
import cmd
import git
import re
from subprocess import call

datadir = "/home/noqqe/Code/cmddocs/data/"
exclude = ".git/"
os.chdir(datadir)

try:
    repo = git.Repo(datadir)
except:
    repo = git.Repo.init(datadir)
    repo.git.add(".")
    repo.git.commit("init")
    print("Successfully created and initialized empty repo at " % datadir)


def list_articles(dir):
    d = os.path.relpath(os.getcwd(),dir)
    call(["tree", d ])

def change_directory(dir):
    """ switch directory within docs dir """
    d = os.path.join(os.getcwd(),dir)

    # dont cd out of datadir
    if not datadir in d:
        d = datadir

    # switch to dir
    try:
        os.chdir(d)
    except:
        print("Directory %s not found" % dir)

def edit_article(article,dir):
    # set paths
    a = os.path.join(dir,article)
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

def search_article(keyword,dir):
    c = 0 
    r = re.compile(keyword)
    for dirpath, dirs, files in os.walk(dir):
        dirs[:] = [d for d in dirs if d not in exclude]
        for fname in files:
            path = os.path.join(dirpath, fname)
            f = open(path, "rt")
            for i, line in enumerate(f):
                if r.search(line):
                    c = c + 1
                    print "* \033[92m%s\033[39m: %s" % (os.path.relpath(path, datadir),
                            line.rstrip('\n'))
    return "Results: %s" % c


def path_complete(self, text, line, begidx, endidx):
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

class Prompt(cmd.Cmd):
    """ Basic commandline interface class """

    prompt = "\033[1m\033[37mcmddocs> \033[0m"
    intro = "Welcome to cmddocs"

    ### list
    def do_list(self, cwd):
        if not cwd:
            cwd = os.getcwd()
        return list_articles(cwd)

    def complete_list(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def do_l(self, cwd):
        if not cwd:
            cwd = os.getcwd()
        return list_articles(cwd)

    def complete_l(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def do_cd(self,dir):
        return change_directory(dir)

    def complete_cd(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def do_pwd(self,line):
        print os.path.relpath(os.getcwd(),datadir)

    ### edit
    def do_edit(self, article):
        return edit_article(article, os.getcwd())

    def complete_edit(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def do_e(self, article):
        return edit_article(article, os.getcwd())

    def complete_e(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    ### search 
    def do_search(self, keyword):
        print search_article(keyword, os.getcwd())

    ### misc
    def do_status(self, line):
        repo.git.status()

    def do_log(self, count):
        if not count:
            count = 10
        print repo.git.log(oneline=True,n=count)

    ### exit
    def do_exit(self, line):
        return True

    def do_EOF(self, line):
        print "exit"
        return True


if __name__ == '__main__':
    Prompt().cmdloop()
