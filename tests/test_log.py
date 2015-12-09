#!/usr/bin/env python

from cmddocs import Cmddocs

def test_do_log(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_log("10")
    out, err = capsys.readouterr()
    assert out.startswith("Last 10 commits\n")

def test_do_log_10_file(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_log("10 testfile1")
    out, err = capsys.readouterr()
    assert out.startswith("Last 10 commits for testfile1.md\n")

def test_do_log_20_file(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_log("20 testfile1")
    out, err = capsys.readouterr()
    assert out.startswith("Last 20 commits for testfile1.md\n")

def test_do_log_file(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_log("testfile2")
    out, err = capsys.readouterr()
    assert out.startswith("Last 10 commits for testfile2.md\n")

def test_do_log_commitmsg(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_log("testfile2")
    out, err = capsys.readouterr()
    assert out.endswith("init\n")
