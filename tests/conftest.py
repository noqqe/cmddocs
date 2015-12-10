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

    doc = """
# Header 1

This is some test content
hopefully no one will ever read this

## Header 2

py.test rocks...

### Header 3

there will be some codeblock

```
foo=$(echo foo)
echo foo | sed -i 's#foo#bar#'
```

#### Header 4

Test Test test

##### Header 5

This is some test content
hopefully no one will ever read this
"""

    # create test dirs
    for x in range(1, 4):
        x = str(x)
        os.mkdir(d + "/dir" + x)

    # create test files
    for x in range(1, 6):
        x = str(x)
        f = open(d + "/testfile" + x + ".md", "ab+")
        f.write("Test " + x)
        f.close()

    for x in range(1, 4):
        x = str(x)
        f = open(d + "/dir1/testfile" + x + ".md", "ab+")
        f.write(doc)
        f.close()


    repo = git.Repo.init(d)
    repo.git.config("user.email", "mail@example.net")
    repo.git.config("user.name", "Charlie Root")
    repo.git.add(".")
    repo.git.commit(m=" init")

    # create new content
    for x in range(1, 4):
        x = str(x)
        f = open(d + "/dir2/testfile" + x + ".md", "ab+")
        f.write(doc)
        f.close()

    # create 2nd commit
    repo.git.add(".")
    repo.git.commit(m=" 2nd commit")

    # create new content
    for x in range(1, 4):
        x = str(x)
        f = open(d + "/dir3/testfile" + x + ".md", "ab+")
        f.write(doc)
        f.close()

    # create 3rd commit
    repo.git.add(".")
    repo.git.commit(m=" 3rd commit")

    # create test config
    confpath = tempfile.mkdtemp(dir="/tmp/", prefix="demodocsconf-")
    config = open(confpath + "/config", "ab+")

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
