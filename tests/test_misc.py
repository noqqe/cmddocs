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


