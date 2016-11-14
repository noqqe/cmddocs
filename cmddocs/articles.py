""" Article class """

import os
import re
import subprocess
import socket
import smtplib
import tempfile
import datetime
from builtins import input
from email.mime.text import MIMEText
import mistune
import git
from cmddocs.utils import *
from cmddocs.rendering import md_to_ascii


# Function definitions
def list_articles(dir, extension):
    "lists all articles in current dir and below"
    try:
        DEVNULL = open(os.devnull, 'wb')
        listing = subprocess.check_output(["tree", dir], stderr=DEVNULL)
        listing = remove_fileextension(listing.decode('utf-8'), extension)
        print(listing)
    except OSError:
        print("Error: tree not installed")
        return False
    except subprocess.CalledProcessError:
        print("Error: File or Directory not found")

def list_directories(dir):
    "lists all directories in current dir and below"
    try:
        DEVNULL = open(os.devnull, 'wb')
        listing = subprocess.check_output(["tree", "-d", dir], stderr=DEVNULL)
        print(listing.decode('utf-8'))
    except OSError:
        print("Error: tree not installed")
        return False
    except subprocess.CalledProcessError:
        print("Error: File or Directory not found")

def change_directory(dir, datadir):
    "changes directory"
    d = os.path.join(os.getcwd(), dir)

    # dont cd out of datadir
    if datadir not in d:
        d = datadir

    # if empty, switch to datadir
    if not dir:
        d = datadir

    # switch to dir
    try:
        os.chdir(d)
        return d
    except OSError:
        print("Error: Directory %s not found" % dir)

def edit_article(article, directory, editor, repo, default_commit_msg, extension, test, editorflags):
    """edit an article within your docs"""
    # set paths
    a = add_fileextension(article, extension)
    a = os.path.join(directory, a)
    d = os.path.dirname(a)

    # create dir(s)
    if not os.path.isdir(d):
        try:
            os.makedirs(d)
        except OSError:
            print("Error: Creation of path %s is not possible" % d)
            return False

    # start editor
    if test is False:
        try:
            if editorflags is False:
                subprocess.call([editor, a])
            else:
                subprocess.call([editor, editorflags, a])
        except OSError:
            print("Error: '%s' No such file or directory" % editor)
            return False
    else:
        try:
            with open(a, "a") as fp:
                content = "TEST CHANGE"
                fp.write(content)
        except OSError:
            print("Error: '%s' No such file or directory" % editor)


    # commit into git
    try:
        repo.git.add(a)
        if repo.is_dirty():
            if test is False:
                try:
                    msg = input("Commit message: ")
                    if not msg:
                        msg = default_commit_msg
                except OSError:
                    print("Error: Could not create commit")
            else:
                msg = default_commit_msg
                print("automatic change done")
            try:
                repo.git.commit(m=msg)
            except OSError:
                print("Error: Could not create commit")

        else:
            print("Nothing to commit")
    except (OSError, git.exc.GitCommandError) as e:
        print("Error: Could not create commit")



def info_article(article, dir, repo, extension):
    "get info for an article within your docs"
    a = add_fileextension(article, extension)
    a = os.path.join(dir, a)

    # Create commit list
    try:
        commits = repo.git.log(a, follow=True, format="%H")
        commits = commits.split()
        n = len(commits)
    except git.exc.GitCommandError:
        print("Error: File not found")
        return False

    # Article create date
    created = repo.git.show(commits[n-1], quiet=True, pretty="format:%ci")
    print("Created: %s" % created)

    # Article last updated
    updated = repo.git.show(commits[0], quiet=True, pretty="format:%ci")
    print("Updated: %s" % updated)

    # Number of commits
    print("Commits: %s" % n)

    # Collect textual informations
    num_lines = 0
    num_words = 0
    num_chars = 0

    with open(a, 'r') as f:
        for line in f:
            words = line.split()

            num_lines += 1
            num_words += len(words)
            num_chars += len(line)

    # Print textual informations
    print("Lines: %s" % num_lines)
    print("Words: %s" % num_words)
    print("Characters: %s" % num_chars)

def mail_article(article, dir, mailfrom, extension):
    "mail an article to a friend"
    a = add_fileextension(article, extension)
    a = os.path.join(dir, a)

    # Create a text/plain message
    try:
        fp = open(a, 'r')
        msg = MIMEText(fp.read())
        fp.close()
    except IOError:
        print("Error: Please specify a document")
        return False


    mailto = input("Recipient: ")
    msg['Subject'] = article
    msg['From'] = mailfrom
    msg['To'] = mailto

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP()
    try:
        s.connect()
        s.sendmail(mailfrom, [mailto], msg.as_string())
        s.quit()
    except socket.error:
        print("Error: Apparently no mailer running on your system.")
        print("Error: Could not connect to localhost:25")
        return False
    except smtplib.SMTPRecipientsRefused:
        print("Error: Invalid recipient or sender")
        return False



def view_article(article, dir, pager, extension, pagerflags, colors):
    "view an article within your docs"
    a = add_fileextension(article, extension)
    a = os.path.join(dir, a)
    # read original file
    try:
        article = open(a, "r")
    except IOError:
        print("Error: Could not find %s" % article)
        return False

    content = article.read()
    article.close()

    # hand everything over to mistune lexer
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
        md = mistune.Markdown(renderer=md_to_ascii(colors))
        tmp.write(md.render(content))

    # start pager and cleanup tmp file afterwards
    # also parse flags for local pager
    try:
        if pagerflags is False:
            subprocess.call([pager, tmp.name])
        else:
            subprocess.call([pager, pagerflags, tmp.name])
    except OSError:
        print("Error: '%s' No such file or directory" % pager)

    try:
        os.remove(tmp.name)
    except OSError:
        print("Error: Could not remove %s" % tmp.name)

def delete_article(article, dir, repo, extension):
    """ delete an article """
    a = add_fileextension(article, extension)
    a = os.path.join(dir, a)
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

def move_article(dir, args, repo, extension):
    "move an article from source to destination"
    args = args.split()
    if len(args) != 2:
        print("Invalid usage\nUse: mv source dest")
        return False

    a = os.path.join(dir, args[0])
    a = add_fileextension(a, extension)
    e = os.path.join(dir, args[1])
    e = add_fileextension(e, extension)
    d = os.path.dirname(e)

    # create dir(s)
    if not os.path.isdir(d):
        os.makedirs(d)

    # move file in git and commit
    try:
        repo.git.mv(a, e)
        repo.git.commit(m="Moved %s to %s" % (a, e))
        print("Moved %s to %s" % (a, e))
    except git.exc.GitCommandError:
        print("Error: File could not be moved")

def search_article(keyword, directory, datadir, exclude):
    """
    Search for a keyword in every article within your current directory and
    below. Much like recursive grep.
    """
    c = 0
    r = re.compile(keyword)
    print("Articles:")
    for dirpath, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclude]
        for fname in files:
            path = os.path.join(dirpath, fname)
            if r.search(path) is not None:
                print("* \033[92m%s\033[39m" %
                      os.path.relpath(path, datadir))
                c = c + 1
    print("Content:")
    for dirpath, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclude]
        for fname in files:
            path = os.path.join(dirpath, fname)
            f = open(path, "rt")
            for i, line in enumerate(f):
                if r.search(line):
                    c = c + 1
                    print("* \033[92m%s\033[39m: %s" % (os.path.relpath(path, datadir),
                                                        line.rstrip('\n')))
    return "Results: %s" % c

def show_diff(args, repo, extension):
    """
    Shows diffs for files or whole article directory
    """
    colorization = "always"
    unifiedopt = "0"

    args = args.split()
    if len(args) > 1:
        if os.path.isfile(os.path.join(os.getcwd(), add_fileextension(args[1], extension))):
            # diff 7 article
            try:
                print(repo.git.diff('HEAD~'+args[0], add_fileextension(args[1], extension),
                                    unified=unifiedopt, color=colorization))
            except git.exc.GitCommandError:
                print("Error: Not a valid git commit reference")
        else:
            print("Error: Wrong Usage. See help diff")
    elif len(args) == 1:
        # diff 7
        try:
            print(repo.git.diff('HEAD~'+args[0],
                                unified=unifiedopt, color=colorization))
        except git.exc.GitCommandError:
            print("Error: Not a valid git commit reference")
    else:
        try:
            print(repo.git.diff('HEAD~1', unified="0", color="always"))
        except git.exc.GitCommandError:
            print("Error: Not a valid git commit reference")

def show_log(args, repo, extension):
    """
    Show latest git logs with specified number of entries and maybe for a
    specific file.
    """
    args = args.split()
    format = "format:%C(blue)%h %Cgreen%C(bold)%ad %Creset%s"
    dateformat = "short"

    if len(args) >= 1:
        if os.path.isfile(os.path.join(os.getcwd(), add_fileextension(args[0], extension))):
            file = add_fileextension(args[0], extension)

            # Command: log Article 12
            try:
                count = args[1]
                print("Last %s commits for %s" % (count, file))
                print(repo.git.log(file, pretty=format, n=count,
                                   date=dateformat, follow=True))
            # Command: log Article
            except IndexError:
                count = 10
                print("Last %s commits for %s" % (count, file))
                print(repo.git.log(file, pretty=format, n=count,
                                   date=dateformat, follow=True))
            except git.exc.GitCommandError:
                print("Error: git command resulted in an error")
        else:
            count = args[0]
            # Command: log 12 Article
            try:
                file = add_fileextension(args[1], extension)
                print("Last %s commits for %s" % (count, file))
                print(repo.git.log(file, pretty=format, n=count,
                                   date=dateformat, follow=True))
            # Command: log 12
            except IndexError:
                print("Last %s commits" % count)
                print(repo.git.log(pretty=format, n=count,
                                   date=dateformat))
            except git.exc.GitCommandError:
                print("Error: git command resulted in an error")

    # Command: log
    elif len(args) == 0:
        count = 10
        print("Last %s commits" % count)
        try:
            print(repo.git.log(pretty=format, n=count, date=dateformat))
        except git.exc.GitCommandError:
            print("Error: git may not be configured on your system.")

def undo_change(args, repo):
    """
    You can revert your changes (use revert from git)
    """
    args = args.split()
    if len(args) == 1:
        try:
            print(repo.git.show(args[0], '--oneline', '--patience'))
            msg = input("\nDo you really want to undo this? (y/n): ")
            if msg == "y":
                repo.git.revert(args[0], '--no-edit')

        except git.exc.GitCommandError:
            print("Error: Could not find given commit reference")

def show_stats(args, repo, datadir):
    """
    Show some statistics and other informations
    on your repos
    """
    # get time series of commits
    commits = repo.git.log(format="%ci")
    commits = commits.split('\n')
    n = len(commits)

    print("Newest Commit: %s" % commits[0])
    print("Oldest Commit: %s" % commits[n-1])
    print("Number of Commits: %s" % n)

    # Calculate Repo age
    f = commits[n-1].split()
    today = datetime.datetime.today()
    first = datetime.datetime.strptime(f[0], "%Y-%m-%d")
    days = today - first
    print("Repository Age: %s" % days.days)

    # Calculate commits per day
    cpd = float(days.days) / n
    print("Average Commits per Day: %s" % cpd)

    # Calculate size of docs
    folder_size = 0
    num_lines = 0
    num_words = 0
    num_chars = 0
    num_files = 0
    for (path, dirs, files) in os.walk(datadir):
        for file in files:
            filename = os.path.join(path, file)
            if ".git/" not in filename:
                num_files += 1
                folder_size += os.path.getsize(filename)
                with open(filename, 'r') as f:
                    for line in f:
                        words = line.split()
                        num_lines += 1
                        num_words += len(words)
                        num_chars += len(line)

    print("Size of your Docs: %0.1f MB" % (folder_size/(1024*1024.0)))
    print("Total Articles: %s" % num_files)
    print("Total Lines: %s" % num_lines)
    print("Total Words: %s" % num_words)
    print("Total Characters: %s" % num_chars)
