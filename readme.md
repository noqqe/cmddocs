# cmddocs

`cmddocs` is an interactive commandline wiki-like python script. It lets
you easily maintain your wiki/docs/cheetsheets using:

* Python
* `cmd` module (for CLI)
* `git` for version control
* `markdown` for writing and viewing
* oldschool files and directories in your $HOME

### Why ?

I kind of started `cmddocs` because I couldn't find something like this on
the internet. Here's my usecase. Im working as a DevOps guy being in touch 
with various types of software, languages, tools, operating systems and
databases. To remember all those things I need a place to store commands,
workflows and short howtos. 

Most of the software I use (and love) runs on a OpenBSD Box on the internet
and are commandline-based. These are [mutt](http://www.mutt.org),
[taskwarrior](http://taskwarrior.org),
[jrnl](http://maebert.github.io/jrnl/), [weechat](http://weechat.org) and
so on...But i was missing a tool for documentation.

I was using [gitit](http://gitit.net) also for a long time, but I found that its way
too bloated for my needs. Compiling `ghc` and `gitit` was awful, too.
After switching to just plaintext files using my `vim` and `git` it was also
a bit annoying. So I wrote `cmddocs` to make it easier for me to handle my
plaintext files.

### Demo

To give you an idea what it looks/feels like I created a short terminal
recording.

[asciinema cmddocs demo](https://asciinema.org/a/15168)

### Installation and usage

Installation

```
git clone https://github.com/noqqe/cmddocs
cd cmddocs
pip install -r requirements.txt
```

Create `.cmddocsrc` file in your $HOME with the following content (adjust
to your needs):

```
[General]
Datadir = /home/noqqe/Docs
Default_Commit_Message = small changes
Excludedir = .git/
```

Once you start cmddocs.py the CLI will be shown. Use `help` for commands.

```
$ ./cmddocs.py
Welcome to cmddocs
cmddocs> help

Documented commands (type help <topic>):
========================================
EOF  d       dirs  edit  help  list  ls    mv   rm      status
cd   delete  e     exit  l     log   move  pwd  search  view

cmddocs> help l
Show files in current working dir
```

Exit cmddocs.py

* `CTRL+D`
* `exit`

### Correctness, feature-completeness and other weaknesses

Since I'm not a programmer and new to python there are serveral weaknesses.

* `tree` view for `ls` command is still produced by calling the external
  tool tree.
* markdown to ANSI Colors for `view` command is produced by RegEx matching
  on markdown format. Longterm goal is to replace it with pythons markdown
  module using `etree` function.
* At some point there will may be a `pip` package for it

If you like, please help me improving.
