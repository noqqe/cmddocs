#!/usr/bin/env python

from cmddocs import Cmddocs

def test_do_exit(demoenv):
    c, d = demoenv
    assert Cmddocs(c).do_exit('exit') == True

def test_do_help(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_help('exit')
    out, err = capsys.readouterr()
    assert out.startswith("\n        Exit cmddocs\n")

def test_do_pwd(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_pwd(d)
    out, err = capsys.readouterr()
    assert ".\n" in out

def test_do_cd(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_cd("dir2")
    out, err = capsys.readouterr()
    assert "" in out


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

