#!/usr/bin/env python

from cmddocs import Cmddocs
import sys
import pytest
import os
import tempfile

# generate environment for each test
@pytest.fixture(scope="session", autouse=True)
def demoenv():

    # init demo dir
    d = tempfile.mkdtemp(dir="/tmp/", prefix="demodocs-")

    # create test files
    for x in range(1,5):
       x = str(x)
       f = open(d + "/testfile" + x, "ab+")
       f.write("Test " + x)
       f.close()

    for x in range(1,3):
        x = str(x)
        os.mkdir(d + "/dir" + x)


    # create test config
    config = open(d + "/config", "ab+")

    # initialize test config
    content = """
    [General]
    Datadir = %s
    Default_Commit_Message = small changes
    Excludedir = .git/
    Editor = /usr/local/bin/vim
    Pager = /usr/bin/less
    Prompt = cmddocs>
    Promptcolor = 37
    Intro_Message = cmddocs - press ? for help
    Mail = flo@noqqe.de
    Default_Extension = md
    """ % d

    config.write(content)
    config.close()

    c = config.name

    return c, d

def test_do_exit(demoenv):
    c, d = demoenv
    assert Cmddocs(c).do_exit('exit') == True

def test_do_help(capsys):
    Cmddocs().do_help('exit')
    out, err = capsys.readouterr()
    assert out == "Exit cmddocs\n"

def test_do_list_end(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_list(d)
    out, err = capsys.readouterr()
    assert out.endswith("5 files\n\n")

def test_do_list_start(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_list(d)
    out, err = capsys.readouterr()
    assert out.startswith(d)

def test_do_pwd(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_pwd(d)
    out, err = capsys.readouterr()
    assert out == '.\n'

def test_do_cd(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_cd("dir2",True)
    out, err = capsys.readouterr()
    assert out == "Changed to %s" % d + "dir2"

# Test default-extension when called on a new file
