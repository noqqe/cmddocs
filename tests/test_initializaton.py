#!/usr/bin/env python

from cmddocs import Cmddocs

def test_do_initializaton(emptyenv, capsys):
    c, d = emptyenv
    Cmddocs(c).do_status("test")
    out, err = capsys.readouterr()
    assert "On branch master" in out
