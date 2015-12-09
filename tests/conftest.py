import os
import tempfile
import pytest
import git

@pytest.fixture(scope="session", autouse=True)
def demoenv():
    """
    Initializes a test environment to make
    sure all tests can be applied properly
    """

    # init demo dir
    d = tempfile.mkdtemp(dir="/tmp/", prefix="demodocs-")

    # create test files
    for x in range(1, 5):
        x = str(x)
        f = open(d + "/testfile" + x + ".md", "ab+")
        f.write("Test " + x)
        f.close()

    # create test dirs
    for x in range(1, 3):
        x = str(x)
        os.mkdir(d + "/dir" + x)

    repo = git.Repo.init(d)
    repo.git.config("user.email", "mail@example.net")
    repo.git.config("user.name", "Charlie Root")
    repo.git.add(".")
    repo.git.commit(m=" init")

    # create test config
    config = open(d + "/config", "ab+")

    # initialize test config
    content = """
[General]
Datadir = %s
Default_Commit_Message = small changes
Excludedir = .git/
Editor = /usr/local/bin/vim
Pager = /usr/bin/less
Prompt = cmddocs>
Promptcolor = 37
Intro_Message = cmddocs - press ? for help
Mail = mail@example.com
Default_Extension = md

[Colors]
Header12 = 37
Header345 = 37
Codeblock = 92
    """ % d

    config.write(content)
    config.close()

    c = config.name
    print(d)

    return c, d
