#!/usr/bin/env python

import os
import sys
import cmd
import git
import re
from subprocess import call

datadir = "/home/noqqe/Code/cmddocs/data/"
datadir = "/home/noqqe/Docs"
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

def list_directories(dir):
    d = os.path.relpath(os.getcwd(),dir)
    call(["tree", "-d", d ])

def change_directory(dir):
    """ switch directory within docs dir """
    d = os.path.join(os.getcwd(),dir)

    # dont cd out of datadir
    if not datadir in d:
        d = datadir

    # if empty, switch to datadir
    if not dir:
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

def delete_article(article,dir):
    a = os.path.join(dir,article)
    try:
        repo.git.rm(a)
        repo.git.commit(m="%s deleted" % article)
    except:
        if os.path.isdir(a):
            os.rmdir(a)
            print("Removed directory %s which was not under version control" % a)
        else:
            os.remove(a)
            print("Removed file %s which was not under version control" % a)

    return "%s deleted" % article

def move_article(article,dir,dest):
    a = os.path.join(dir,article)
    e = os.path.join(dir,dest)
    d = os.path.dirname(e)

    # create dir(s)
    if not os.path.isdir(d):
        os.makedirs(d)

    # move file in git and commit
    repo.git.mv(a,e)
    repo.git.commit(m="Moved %s to %s" % (article,dest))
    return "Moved %s to %s" % (article,dest)

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
        "Show files in current working dir"
        if not cwd:
            cwd = os.getcwd()
        return list_articles(cwd)

    def complete_list(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def do_l(self, cwd):
        "Show files in current working dir"
        if not cwd:
            cwd = os.getcwd()
        return list_articles(cwd)

    def do_ls(self, cwd):
        "Show files in current working dir"
        if not cwd:
            cwd = os.getcwd()
        return list_articles(cwd)

    def do_d(self, cwd):
        "Show only directories in current working dir"
        if not cwd:
            cwd = os.getcwd()
        return list_directories(cwd)

    def do_dirs(self, cwd):
        "Show only directories in current working dir"
        if not cwd:
            cwd = os.getcwd()
        return list_directories(cwd)

    def complete_l(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def complete_ls(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def do_cd(self,dir):
        "Change directory"
        return change_directory(dir)

    def complete_cd(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def do_pwd(self,line):
        "Show current directory"
        print os.path.relpath(os.getcwd(),datadir)

    ### edit
    def do_edit(self, article):
        "Edit an article. edit path/to/article"
        return edit_article(article, os.getcwd())

    def complete_edit(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def do_e(self, article):
        "Edit an article. e path/to/article"
        return edit_article(article, os.getcwd())

    def complete_e(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    ### delete
    def do_delete(self, article):
        "Delete an article"
        delete_article(article, os.getcwd())

    def complete_delete(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def do_rm(self, article):
        "Delete an article"
        delete_article(article, os.getcwd())

    def complete_rm(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    ### move
    def do_move(self, line):
        "Move an article"
        args = line.split()
        if len(args)!=2:
            print "Invalid usage\nUse: move source dest"
            return
        move_article(args[0], os.getcwd(), args[1])

    def complete_move(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def do_mv(self, line):
        "Move an article"
        args = line.split()
        if len(args)!=2:
            print "Invalid usage\nUse: mv source dest"
            return
        move_article(args[0], os.getcwd(), args[1])

    def complete_mv(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    ### search 
    def do_search(self, keyword):
        "Search for keyword in current directory. Example: search mongodb"
        print search_article(keyword, os.getcwd())

    ### misc
    def do_status(self, line):
        "Show git repo status of your docs"
        repo.git.status()

    def do_log(self, count):
        "Show git logs of your docs. Use log 10 to show 10 entries"
        if not count:
            count = 10
        #print repo.git.log(pretty="format:%h%x09%an%x09%ad%x09%s",date="short",n=count)
        print repo.git.log(pretty="format:%C(blue)%h %Cgreen%C(bold)%ad %Creset%s", n=count, date="short") 

    ### exit
    def do_exit(self, line):
        "Exit cmddocs"
        return True

    def do_EOF(self, line):
        "Exit cmddocs"
        print "exit"
        return True


if __name__ == '__main__':
    Prompt().cmdloop()
