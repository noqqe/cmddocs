#!/usr/bin/env python

import os
import sys
import cmd
import git
import re
import tempfile
import ConfigParser

from subprocess import call
from os.path import expanduser

# Function definitions
def list_articles(dir):
    "lists all articles in current dir and below"
    d = os.path.join(os.getcwd(),dir)
    call(["tree", d ])

def list_directories(dir):
    "lists all directories in current dir and below"
    d = os.path.join(os.getcwd(),dir)
    call(["tree", "-d", d ])

def change_directory(dir,datadir):
    "changes directory"
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
        return d
    except OSError:
        print("Directory %s not found" % dir)

def edit_article(article, directory, editor, repo, default_commit_msg):
    """edit an article within your docs"""
    # set paths
    a = os.path.join(directory, article)
    d = os.path.dirname(a)

    # create dir(s)
    if not os.path.isdir(d):
        os.makedirs(d)

    # start editor
    os.system('%s %s' % (editor,a))

    # commit into git
    try:
        repo.git.add(a)
        if repo.is_dirty():
            msg = raw_input("Commit message: ")
            if not msg: 
                msg = default_commit_msg
            repo.git.commit(m=msg)
        else:
            print "Nothing to commit"
    except:
        pass

def view_article(article,dir,pager):
    "view an article within your docs"
    a = os.path.join(dir,article)
    # read original file
    try:
        article = open(a, "r")
    except IOError:
        print "Error: Could not find %s" % article
        return

    content = article.read()
    article.close()

    # create tmp file and convert markdown to ansi
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        h = re.compile('^#{3,5}\s*(.*)\ *$',re.MULTILINE)
        content = h.sub('\033[1m\033[37m\\1\033[0m', content)
        h = re.compile('^#{1,2}\s*(.*)\ *$',re.MULTILINE)
        content = h.sub('\033[4m\033[1m\033[37m\\1\033[0m', content)
        h = re.compile('^\ {4}(.*)',re.MULTILINE)
        content = h.sub('\033[92m\\1\033[0m', content)
        h = re.compile('~~~\s*([^~]*)~~~[^\n]*\n',re.DOTALL)
        content = h.sub('\033[92m\\1\033[0m', content)
        tmp.write(content)

    # start pager and cleanup tmp file afterwards
    # -fr is needed for showing binary+ansi colored files to 
    # be properly displayed
    os.system('%s -fr %s' % (pager,tmp.name))
    try:
        os.remove(tmp.name)
    except OSError:
        print "Error: Could not remove %s" % tmp.name

def delete_article(article,dir,repo):
    "delete an article"
    a = os.path.join(dir,article)
    try:
        repo.git.rm(a)
        repo.git.commit(m="%s deleted" % article)
        print("%s deleted" % article)
    except:
        if os.path.isdir(a):
            try:
                os.rmdir(a)
                print("Removed directory %s which was not under version control" % a)
            except OSError:
                print("Could not remove %s - its maybe not empty" % a)
        else:
            try:
                os.remove(a)
                print("Removed file %s which was not under version control" % a)
            except OSError:
                print("File %s could not be removed" % a)
    return

def move_article(dir,args,repo):
    "move an article from source to destination"
    args = args.split()
    if len(args)!=2:
        print "Invalid usage\nUse: mv source dest"
        return

    a = os.path.join(dir,args[0])
    e = os.path.join(dir,args[1])
    d = os.path.dirname(e)

    # create dir(s)
    if not os.path.isdir(d):
        os.makedirs(d)

    # move file in git and commit
    repo.git.mv(a,e)
    repo.git.commit(m="Moved %s to %s" % (a,e))
    print("Moved %s to %s" % (a,e))

def search_article(keyword, directory, datadir, exclude):
    """
    search for a keyword in every article within your current directory and
    below. Much like recursive grep.
    """
    c = 0
    r = re.compile(keyword)
    for dirpath, dirs, files in os.walk(directory):
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

def show_log(args,repo):
    """
    Show latest git logs with specified number of entries and maybe for a
    specific file.
    """
    args = args.split()
    format="format:%C(blue)%h %Cgreen%C(bold)%ad %Creset%s"
    dateformat="short"

    if len(args) >= 1:
        if os.path.isfile(os.path.join(os.getcwd(), args[0])):
            file = args[0]
            try:
                count = args[1]
                print "Last %s commits for %s" % (count, file)
                print repo.git.log(file, pretty=format, n=count, date=dateformat)
            except IndexError:
                count = 10
                print "Last %s commits for %s" % (count, file)
                print repo.git.log(file, pretty=format, n=count, date=dateformat)
        else:
            count = args[0]
            try:
                file = args[1]
                print "Last %s commits for %s" % (count, file)
                print repo.git.log(file, pretty=format, n=count, date=dateformat)
            except IndexError:
                print "Last %s commits" % count
                print repo.git.log(pretty=format, n=count, date=dateformat)

    elif len(args) == 0:
        count = 10
        print "Last %s commits" % count
        print repo.git.log(pretty=format, n=count,date=dateformat)

def path_complete(self, text, line, begidx, endidx):
    """ 
    Path completition function used in various places for tab completion
    when using cmd
    """
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

class cmddocs(cmd.Cmd):
    """ Basic commandline interface class """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.read_config(self)
        self.initialize_docs(self)
        self.prompt = '\033[1m\033[37m{} \033[0m'.format(self.prompt)

    def read_config(self, conf):
        config = ConfigParser.ConfigParser()
        if not config.read(expanduser("~/.cmddocsrc")):
            print "Error: your ~/.cmddocsrc could not be read"
            exit(1)
        try:
            self.datadir = expanduser(config.get("General", "Datadir"))
            self.exclude = expanduser(config.get("General", "Excludedir"))
            self.default_commit_msg = config.get("General", "Default_Commit_Message")
            self.editor = config.get("General", "Editor")
            self.pager = config.get("General", "Pager")
            self.prompt = config.get("General", "Prompt")
            self.intro = config.get("General", "Intro_Message")
        except ConfigParser.NoSectionError:
            print "Error: Config wrong formatted"
            exit(1)
        return 
        
    def initialize_docs(self, docs):
        # Read or initialize git repository
        try:
            self.repo = git.Repo(self.datadir)
        except git.exc.InvalidGitRepositoryError:
            self.repo = git.Repo.init(self.datadir)
            self.repo.git.add(".")
            self.repo.git.commit("init")
            print("Successfully created and initialized empty repo at %s" % self.datadir)
        # Change to datadir
        try:
            os.chdir(self.datadir)
            self.cwd = os.getcwd()
        except OSError:
            print "Error: Switching to Datadir %s not possible" % self.datadir
            exit(1)

    ### list
    def do_list(self, dir):
        "Show files in current working dir"
        if not dir:
            dir= os.getcwd()
        return list_articles(dir)

    # Aliases
    do_l = do_list
    do_ls = do_list

    def do_dirs(self, dir):
        "Show only directories in cwd"
        if not dir:
            dir= os.getcwd()
        return list_directories(dir)

    do_d = do_dirs

    ### directories
    def do_cd(self,dir):
        "Change directory"
        cwd = change_directory(dir,self.datadir)

    def do_pwd(self,line):
        "Show current directory"
        print os.path.relpath(os.getcwd(),self.datadir)

    ### edit
    def do_edit(self, article):
        """ 
        Edit or create new article. 
        
        > edit databases/mongodb
        > edit intro
        """
        return edit_article(article, os.getcwd(), self.editor, self.repo, self.default_commit_msg)

    do_e = do_edit

    ### view
    def do_view(self, article):
        """
        View an article. Creates temporary file with converted markdown to
        ansi colored output. Opens your PAGER. (Only less supported atm)

        > view databases/mongodb
        > view intro
        """
        return view_article(article, os.getcwd(), self.pager)

    ### delete
    def do_delete(self, article):
        "Delete an article"
        delete_article(article, os.getcwd(),self.repo)

    do_rm = do_delete

    ### move
    def do_move(self, args):
        "Move an article"
        move_article(os.getcwd(),args,self.repo)

    do_mv = do_move

    ### search
    def do_search(self, keyword):
        "Search for keyword in current directory. Example: search mongodb"
        print search_article(keyword,os.getcwd(), self.datadir, self.exclude)

    ### status
    def do_status(self, line):
        "Show git repo status of your docs"
        print self.repo.git.status()

    def do_log(self, args):
        """
        Show git logs of your docs.

        Usage: log                      # default loglines: 10)
               log 20                   # show 20 loglines
               log 20 article           # show log for specific article
               log databases/mongodb 3  # same
        """
        show_log(args,self.repo)

    ### exit
    def do_exit(self, line):
        "Exit cmddocs"
        return True

    def do_EOF(self, line):
        "Exit cmddocs"
        print "exit"
        return True

    ### completions
    complete_l = path_complete
    complete_ls = path_complete
    complete_list = path_complete

    complete_d = path_complete
    complete_dirs = path_complete

    complete_view = path_complete
    complete_cd = path_complete

    complete_e = path_complete
    complete_edit = path_complete

    complete_rm = path_complete
    complete_delete = path_complete

    complete_mv = path_complete
    complete_move = path_complete

    complete_log = path_complete

if __name__ == '__main__':
    cmddocs().cmdloop()
