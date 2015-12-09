#!/usr/bin/env python

from cmddocs import Cmddocs

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

def test_do_cd_fail(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_cd("dir7")
    out, err = capsys.readouterr()
    assert out == "Error: Directory dir7 not found\n"
