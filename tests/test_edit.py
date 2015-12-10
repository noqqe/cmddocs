#!/usr/bin/env python

from cmddocs import Cmddocs

def test_do_edit(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_edit("testfile1", test=True)
    out, err = capsys.readouterr()
    assert out.startswith("automatic change done")

def test_do_edit_log_commitmsg(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_log("testfile1")
    out, err = capsys.readouterr()
    assert "small changes" in out

def test_do_e(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_e("testfile1", test=True)
    out, err = capsys.readouterr()
    assert out.startswith("automatic change done")
