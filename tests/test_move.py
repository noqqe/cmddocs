
from cmddocs import Cmddocs

def test_do_mv_fail(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_mv("testfileX testfileX")
    out, err = capsys.readouterr()
    assert out == ("Error: File could not be moved\n")

def test_do_mv_start(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_mv("testfile1 testfileX")
    out, err = capsys.readouterr()
    assert out.startswith("Moved /tmp/d")

def test_do_mv_ends(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_mv("testfileX testfile1")
    out, err = capsys.readouterr()
    assert out.endswith("testfile1.md\n")

def test_do_mv_commitcheck(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_log("testfile1")
    out, err = capsys.readouterr()
    assert "testfileX.md" in out
