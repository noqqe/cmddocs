from cmddocs import Cmddocs

def test_do_stats_start(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_stats("test")
    out, err = capsys.readouterr()
    assert out.startswith("Newest Commit:")

def test_do_stats_end(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_stats("test")
    out, err = capsys.readouterr()
    assert "Characters" in out

def test_do_stats_charcount(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_stats("test")
    out, err = capsys.readouterr()
    assert "Characters: 2892" in out

#def test_do_stats_linecount(demoenv, capsys):
#    c, d = demoenv
#    Cmddocs(c).do_stats("test")
#    out, err = capsys.readouterr()
#    assert "Lines: 35" in out

def test_do_stats_articlecount(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_stats("test")
    out, err = capsys.readouterr()
    assert "Articles: 14" in out
