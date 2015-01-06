#!/usr/bin/env python

import os
import sys
import cmd
import git
import re
import tempfile
import ConfigParser
from subprocess import call

# Initialize config
config = ConfigParser.ConfigParser()
if not config.read(os.path.expanduser('~') + "/.cmddocsrc"):
    print "Error: your ~/.cmddocsrc could not be read"
    exit(1)

try:
    datadir = config.get("General", "Datadir")
    exclude = config.get("General", "Excludedir")
    default_commit_msg = config.get("General", "Default_Commit_Message")
    editor = config.get("General", "Editor")
    pager = config.get("General", "Pager")
    prompt = config.get("General", "Prompt")
    intro = config.get("General", "Intro_Message")
except ConfigParser.NoSectionError:
    print "Error: Config wrong formatted"
    exit(1)

# Change to datadir
try:
    os.chdir(datadir)
except OSError:
    print "Error: Switching to Datadir %s not possible" % datadir
    exit(1)


# Read or initialize git repository
try:
    repo = git.Repo(datadir)
except git.exc.InvalidGitRepositoryError:
    repo = git.Repo.init(datadir)
    repo.git.add(".")
    repo.git.commit("init")
    print("Successfully created and initialized empty repo at %s" % datadir)

# Function definitions
def list_articles(dir):
    "lists all articles in current dir and below"
    d = os.path.join(os.getcwd(),dir)
    call(["tree", d ])

def list_directories(dir):
    "lists all directories in current dir and below"
    d = os.path.join(os.getcwd(),dir)
    call(["tree", "-d", d ])

def change_directory(dir):
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


def edit_article(article,dir):
    "edit an article within your docs"
    # set paths
    a = os.path.join(dir,article)
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

def view_article(article,dir):
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

def delete_article(article,dir):
    "delete an article"
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

def move_article(dir,args):
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
    repo.git.commit(m="Moved %s to %s" % (article,dest))
    return "Moved %s to %s" % (article,dest)

def search_article(keyword,dir):
    """
    search for a keyword in every article within your current directory and
    below. Much like recursive grep.
    """
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

def show_log(args):
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

    prompt = '\033[1m\033[37m{} \033[0m'.format(prompt)
    intro = intro
    cwd = datadir

    ### list
    def do_list(self, dir):
        "Show files in current working dir"
        if not dir: dir= os.getcwd()
        return list_articles(dir)

    def do_l(self, dir):
        "Alias for list"
        if not dir: dir= os.getcwd()
        return list_articles(dir)

    def do_ls(self, dir):
        "Alias for list"
        if not dir: dir= os.getcwd()
        return list_articles(dir)

    def do_d(self, dir):
        "Alias for dirs"
        if not dir: dir= os.getcwd()
        return list_directories(dir)

    def do_dirs(self, dir):
        "Show only directories in cwd"
        if not dir: dir= os.getcwd()
        return list_directories(dir)

    ### directories
    def do_cd(self,dir):
        "Change directory"
        cwd = change_directory(dir)

    def do_pwd(self,line):
        "Show current directory"
        print os.path.relpath(os.getcwd(),datadir)

    ### edit
    def do_edit(self, article):
        """ 
        Edit or create new article. 
        
        > edit databases/mongodb
        > edit intro
        """
        return edit_article(article, os.getcwd())

    def do_e(self, article):
        "Alias for edit"
        return edit_article(article, os.getcwd())

    ### view
    def do_view(self, article):
        """
        View an article. Creates temporary file with converted markdown to
        ansi colored output. Opens your PAGER. (Only less supported atm)

        > view databases/mongodb
        > view intro
        """
        return view_article(article, os.getcwd())

    ### delete
    def do_delete(self, article):
        "Delete an article"
        delete_article(article, os.getcwd())

    def do_rm(self, article):
        "Alias for delete"
        delete_article(article, os.getcwd())

    ### move
    def do_move(self, args):
        "Move an article"
        move_article(os.getcwd(),args)

    def do_mv(self, args):
        "Alias for move"
        move_article(os.getcwd(),args)

    ### search
    def do_search(self, keyword):
        "Search for keyword in current directory. Example: search mongodb"
        print search_article(keyword,os.getcwd())

    ### status
    def do_status(self, line):
        "Show git repo status of your docs"
        print repo.git.status()

    def do_log(self, args):
        """
        Show git logs of your docs.

        Usage: log                      # default loglines: 10)
               log 20                   # show 20 loglines
               log 20 article           # show log for specific article
               log databases/mongodb 3  # same
        """
        show_log(args)

    ### exit
    def do_exit(self, line):
        "Exit cmddocs"
        return True

    def do_EOF(self, line):
        "Exit cmddocs"
        print "exit"
        return True

    ### completions
    def complete_l(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def complete_d(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def complete_dirs(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def complete_view(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def complete_ls(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def complete_list(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def complete_cd(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def complete_e(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def complete_edit(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def complete_delete(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def complete_rm(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def complete_move(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def complete_mv(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

    def complete_log(self, text, line, begidx, endidx):
        return path_complete(self, text, line, begidx, endidx)

if __name__ == '__main__':
    cmddocs().cmdloop()
