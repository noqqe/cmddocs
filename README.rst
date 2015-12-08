cmddocs
=======

``cmddocs`` is an interactive commandline wiki-like python script. It
lets you easily maintain your wiki/docs/cheetsheets using:

-  Python
-  ``cmd`` module (for CLI)
-  ``git`` for version control
-  ``markdown`` for writing and viewing
-  oldschool files and directories in your $HOME

Why ?
-----

I kind of started ``cmddocs`` because I couldn't find something like
this on the internet. Here's my usecase. Im working as a DevOps guy
being in touch with various types of software, languages, tools,
operating systems and databases. To remember all those things I need a
place to store commands, workflows and short howtos.

Most of the software I use (and love) runs on a OpenBSD Box on the
internet and are commandline-based. These are
`mutt <http://www.mutt.org>`__,
`taskwarrior <http://taskwarrior.org>`__,
`jrnl <http://maebert.github.io/jrnl/>`__,
`weechat <http://weechat.org>`__ and so on...But i was missing a tool
for documentation.

I was using `gitit <http://gitit.net>`__ also for a long time, but I
found that its way too bloated for my needs. Compiling ``ghc`` and
``gitit`` was awful, too. After switching to just plaintext files using
my ``vim`` and ``git`` it was also a bit annoying. So I wrote
``cmddocs`` to make it easier for me to handle my plaintext files.

Demo
----

To give you an idea what it looks/feels like I created a short terminal
recording.

`asciinema cmddocs demo <https://asciinema.org/a/15168>`__

Installation and usage
----------------------

Installation

::

    pip install cmddocs

Also make sure you have `tree` installed.

Create ``.cmddocsrc`` file in your $HOME with the following content
(adjust to your needs):

::

    [General]
    Datadir = /home/noqqe/Docs
    Default_Commit_Message = small changes
    Excludedir = .git/
    Editor = /usr/local/bin/vim
    Pager = /usr/bin/less
    PagerFlags = -fr
    Prompt = cmddocs>
    Promptcolor = 37
    Intro_Message = cmddocs - press ? for help
    Mail = mail@example.org
    Default_Extension = md

    [Colors]
    Header12 = 37
    Header345 = 37
    Codeblock = 92

The only required option is "Datadir", everything else will be guessed
or defaults to a sane default value. Once you start cmddocs.py the CLI
will be shown. Use ``help`` for commands.

::

    $ cmddocs
    cmddocs - press ? for help
    cmddocs> help

    Documented commands (type help <topic>):
    ========================================
    EOF  delete  e     help  list  mail  pwd     search  undo
    cd   diff    edit  info  log   move  revert  stats   version
    d    dirs    exit  l     ls    mv    rm      status  view

    cmddocs> help l

        Show files in current working dir

    cmddocs> help log

        Show git logs of your docs.

        Usage: log                      # default loglines: 10)
               log 20                   # show 20 loglines
               log 20 article           # show log for specific article
               log databases/mongodb 3  # same

Exit cmddocs.py

-  ``CTRL+D``
-  ``exit``

Correctness, feature-completeness and other weaknesses
------------------------------------------------------

Since I'm not a programmer and new to python there are serveral
weaknesses.

-  ``tree`` view for ``ls`` command is still produced by calling the
   external tool tree.

If you like, please help me improving.

Changelog
---------

See Changelog_.

.. _Changelog: https://github.com/noqqe/cmddocs/blob/master/CHANGELOG.rst
