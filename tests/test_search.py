from cmddocs import Cmddocs

def test_do_search(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_search("test")
    out, err = capsys.readouterr()
    assert out.startswith("Articles:")

def test_do_search_results(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_search("test")
    out, err = capsys.readouterr()
    assert out.endswith("Results: 4\n")

def test_do_search_content(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_search("test")
    out, err = capsys.readouterr()
    assert "Content:" in out

def test_do_search_noresults(demoenv, capsys):
    c, d = demoenv
    Cmddocs(c).do_search("SOMETHINGTHATWILLNEVERBEFOUND")
    out, err = capsys.readouterr()
    assert out == "Articles:\nContent:\nResults: 0\n"
