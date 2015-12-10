#!/usr/bin/env python

from cmddocs import Cmddocs

def test_do_edit(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_edit("testfile1", test=True)
    out, err = capsys.readouterr()
    assert out.startswith("automatic change done")

