#!/usr/bin/env python

from cmddocs import Cmddocs

def test_do_delete_edit(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_edit("testfile1", test=True)
    out, err = capsys.readouterr()
    assert out.startswith("automatic change done")

def test_do_delete_edit_commitmsg(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_log("")
    out, err = capsys.readouterr()
    assert "small changes" in out

def test_do_delete(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_delete("testfile1")
    out, err = capsys.readouterr()
    assert out == "testfile1 deleted\n"

def test_do_delete_log_commitmsg(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_log("")
    out, err = capsys.readouterr()
    assert "testfile1 deleted\n" in out
