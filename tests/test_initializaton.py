#!/usr/bin/env python

from cmddocs import Cmddocs

def test_do_initializaton(emptyenv, capsys):
    c, d = emptyenv
    Cmddocs(c).do_status("test")
    out, err = capsys.readouterr()
    assert out.startswith("On branch master\n\nInitial commit\n\nnothing to commit")
