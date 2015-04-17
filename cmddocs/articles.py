import os
import re
import git
import tempfile
import subprocess

# Function definitions
def list_articles(dir):
    "lists all articles in current dir and below"
    subprocess.call(["tree", dir])

def list_directories(dir):
    "lists all directories in current dir and below"
    subprocess.call(["tree", "-d", dir])

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
    try:
        subprocess.call([editor, a])
    except OSError:
        print "'%s' No such file or directory" % editor

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
    try:
        subprocess.call([pager, "-fr", tmp.name])
    except OSError:
        print "'%s' No such file or directory" % pager

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
    Search for a keyword in every article within your current directory and
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

def show_diff(args,repo):
    """
    Shows diffs for files or whole article directory
    """
    colorization = "always"
    unifiedopt = "0"

    args = args.split()
    if len(args) > 1:
        if os.path.isfile(os.path.join(os.getcwd(), args[1])):
            try:
                print repo.git.diff('HEAD~'+args[0],args[1],
                        unified=unifiedopt, color=colorization)
            except git.exc.GitCommandError:
                print "ERROR: Not a valid git commit reference"
        else:
            print "ERROR: Wrong Usage. See help diff"
    elif len(args) == 1:
        try:
            print repo.git.diff('HEAD~'+args[0],
                        unified=unifiedopt, color=colorization)
        except git.exc.GitCommandError:
            print "ERROR: Not a valid git commit reference"
    else:
        print repo.git.diff('HEAD~5', unified="0", color="always")

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

