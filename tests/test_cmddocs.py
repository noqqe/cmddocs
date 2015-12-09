#!/usr/bin/env python

from cmddocs import Cmddocs
import sys
import pytest
import os
import tempfile
import git

# generate environment for each test
@pytest.fixture(scope="session", autouse=True)
def demoenv():

    # init demo dir
    d = tempfile.mkdtemp(dir="/tmp/", prefix="demodocs-")

    # create test files
    for x in range(1,5):
       x = str(x)
       f = open(d + "/testfile" + x + ".md", "ab+")
       f.write("Test " + x)
       f.close()

    # create test dirs
    for x in range(1,3):
        x = str(x)
        os.mkdir(d + "/dir" + x)

    repo = git.Repo.init(d)
    repo.git.add(".")
    repo.git.commit(m=" init")

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
Mail = mail@example.com
Default_Extension = md

[Colors]
Header12 = 37
Header345 = 37
Codeblock = 92
    """ % d

    config.write(content)
    config.close()

    c = config.name

    return c, d

def test_do_exit(demoenv):
    c, d = demoenv
    assert Cmddocs(c).do_exit('exit') == True

def test_do_help(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_help('exit')
    out, err = capsys.readouterr()
    assert out.startswith("\n        Exit cmddocs\n")

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
    assert "/tmp/demodocs" in out

def test_do_cd(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_cd("dir2")
    out, err = capsys.readouterr()
    assert "" in out

def test_do_stats_start(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_stats("test")
    out, err = capsys.readouterr()
    assert out.startswith("Newest Commit:")

def test_do_stats_end(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_stats("test")
    out, err = capsys.readouterr()
    assert "Characters" in out

def test_do_log(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_log("test")
    out, err = capsys.readouterr()
    assert out.startswith("Last test commits")

def test_do_search(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_search("test")
    out, err = capsys.readouterr()
    assert out.startswith("Articles:")

def test_do_search_results(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_search("test")
    out, err = capsys.readouterr()
    assert out.endswith("Results: 4\n")

def test_do_mv_fail(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_mv("dir1/testfileX dir1/testfileX")
    out, err = capsys.readouterr()
    assert out == ("Error: File could not be moved\n")
