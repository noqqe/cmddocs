
from cmddocs import Cmddocs

def test_do_list_end(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_list(d)
    out, err = capsys.readouterr()
    assert out.endswith("5 files\n\n")

def test_do_list_start(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_list(d)
    out, err = capsys.readouterr()
    assert out.startswith(d)

def test_do_list_fail(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_list("NEVEREVER")
    out, err = capsys.readouterr()
    assert out.startswith(d)
