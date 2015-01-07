import os
import sys
import cmd
import git
import re
import tempfile
import subprocess
import ConfigParser
from os.path import expanduser

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
