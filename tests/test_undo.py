#!/usr/bin/env python

from cmddocs import Cmddocs

def test_do_undo_fail(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_undo('test')
    out, err = capsys.readouterr()
    assert out == "Error: Could not find given commit reference\n"

def test_do_revert_fail(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_revert('test')
    out, err = capsys.readouterr()
    assert out == "Error: Could not find given commit reference\n"

#def test_do_undo_head(demoenv, capsys):
#    c, d = demoenv
#    Cmddocs(c).do_undo('HEAD')
#    out, err = capsys.readouterr()
#    assert out == "Error: Could not find given commit reference\n"
