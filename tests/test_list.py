
from cmddocs import Cmddocs

def test_do_list_end(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_list(d)
    out, err = capsys.readouterr()
    assert out.endswith("14 files\n\n")

def test_do_list_start(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_list(d)
    out, err = capsys.readouterr()
    assert "tmp/demodocs" in out

def test_do_l_start(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_l(d)
    out, err = capsys.readouterr()
    assert "tmp/demodocs" in out

def test_do_list_fail(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_list("NEVEREVER")
    out, err = capsys.readouterr()
    assert out.startswith("Error: File or Directory not found\n")

def test_do_l_fail(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_l("NEVEREVER")
    out, err = capsys.readouterr()
    assert out.startswith("Error: File or Directory not found\n")
