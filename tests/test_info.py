from cmddocs import Cmddocs

def test_do_info_start(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_info("testfile1")
    out, err = capsys.readouterr()
    assert out.startswith("Created:")

def test_do_info_end(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_info("testfile1")
    out, err = capsys.readouterr()
    assert "Characters" in out

def test_do_info_charcount(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_info("testfile2")
    out, err = capsys.readouterr()
    assert "Characters: 6" in out

def test_do_info_linecount(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_info("testfile1")
    out, err = capsys.readouterr()
    assert "Lines: 1" in out

def test_do_info_wordcount(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_info("testfile1")
    out, err = capsys.readouterr()
    assert "Words: 2" in out

def test_do_info_commitcount(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_info("testfile1")
    out, err = capsys.readouterr()
    assert "Commits: 1" in out
