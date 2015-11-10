#!/usr/bin/env python

from cmddocs import Cmddocs
from cmddocs import *
import sys
import pytest
import os


@pytest.fixture(scope="session", autouse=True)
def setup_environment(tmpdir_factory):
    d = tmpdir_factory.mktemp("demodocs")

def test_do_exit(setup_environment):
    assert Cmddocs().do_exit('exit') == True

def test_do_help(capsys):
    Cmddocs().do_help('exit')
    out, err = capsys.readouterr()
    assert out == "Exit cmddocs\n"

#def test_do_list(capsys):
#    Cmddocs().do_list('SSL')
#    out, err = capsys.readouterr()
#    assert out.startswith("SSL")
