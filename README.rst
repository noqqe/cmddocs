.. image:: https://travis-ci.org/noqqe/cmddocs.svg?branch=master
       :target: https://travis-ci.org/noqqe/cmddocs

.. image:: https://codecov.io/gh/noqqe/cmddocs/branch/master/graph/badge.svg
     :target: https://codecov.io/gh/noqqe/cmddocs

cmddocs
=======

``cmddocs`` is an interactive commandline wiki. It
lets you easily maintain your docs/cheetsheets/notes using:

- Plain Text Files
- Write ``markdown`` in your local Editor
- View in your local Pager
- Versioning with ``git``

cmddocs is like a framework around your plaintext files.

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

After switching to just plaintext files using
``vim`` and ``git`` it was also a bit annoying. So I wrote
``cmddocs`` to make it easier for me to handle my plaintext files.

Markdown Rendering
------------------

``cmddocs`` uses the `mistune <https://github.com/lepture/mistune>`__ lexer to
wrap markdown with ansi control sequences instead of html tags.

It looks something like this.

.. image:: https://raw.github.com/noqqe/cmddocs/master/cmddocs-md2ascii.png

Demo
----

To give you an idea what it looks/feels like I created a short terminal
recording.

`asciinema cmddocs demo <https://asciinema.org/a/15168>`__

Installation
------------

::

    pip install cmddocs

Also make sure you have `tree` installed.


Configuration
-------------

Create ``.cmddocsrc`` file in your $HOME with the following content
(adjust to your needs):

::

    [General]
    Datadir = /home/noqqe/Docs
    Default_Commit_Message = small changes
    Excludedir = .git/
    Editor = /usr/local/bin/vim
    # EditorFlags = -C
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

Quick Start
-----------

At first, create a very minimal config, like

::

    [General]
    Datadir = /home/noqqe/Docs
    Editor = /usr/local/bin/vim
    Pager = /usr/bin/less

Then you can start using cmddocs.

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

Command Documentation
---------------------

``cd``
------

Change directory

::

        Usage:
            cd Programming/
            cd

``delete``, ``rm``
------------------

Delete an article

::

        Usage:
            delete databases/mongodb
            rm databases/mssql


``dirs``, ``d``
---------------

Show directories in current working dir

::

        Usage:
            dirs
            d
            dirs Databases/


``e``, ``edit``
---------------

Edit or create new article.

::

        Usage:
            edit databases/mongodb
            edit intro



``list``, ``l``, ``ls``
-----------------------

Show files in current working dir

::

        Usage:
            list
            l
            list Databases/


``move``, ``mv``
----------------

Move an article to a new location

::

        Usage:
            move databases/mongodb databases/MongoDB
            move life/foo notes/foo
            mv life/foo notes/foo

``view``
--------

View an article. Creates temporary file with converted markdown to
ansi colored output. Opens your PAGER. (Only less supported atm)

::

        Usage:
            view databases/mongodb
            view intro

``mail``
--------

Mail an article to a friend

::

        Usage:
            mail databases/mongodb
            Recipient: mail@example.net

            mail programming/r/loops
            mail intro

``pwd``
-------

Show current directory

::

        Usage:
            pwd

``search``
----------

Search for keyword in current directory

::

        Usage:
            search mongodb
            search foo

``undo``, ``revert``
-------------------

You can revert your changes (use revert from git)

::


        Usage:
            undo HEAD
            undo 355f375

        Will ask for confirmation.

``diff``
--------

Show git diffs between files and commits

::

        Usage:
            diff 7                   # show diff for last 7 changes
            diff 1 article           # show diff for last change to article
            diff                     # show last 5 diffs

``info``
--------

Show infos for an article

::

        Usage:
            info article
            info Databases/mongodb
            Created: 2014-01-18 11:18:03 +0100
            Updated: 2015-10-23 14:14:44 +0200
            Commits: 26
            Lines: 116
            Words: 356
            Characters: 2438

``log``
--------

Show git logs of your docs.

::

        Usage:
            log                      # default loglines: 10)
            log 20                   # show 20 loglines
            log 20 article           # show log for specific article
            log databases/mongodb 3  # same

``status``
----------

Show git repo status of your docs

::

        Usage:
            status

``stats``
---------

Calculate some statistics on your docs

::

        Usage:
            stats

``exit``, ``EOF``
-----------------

Exit cmddocs

::

        Usage:
            exit


``help``
--------

List available commands with "help" or detailed help with "help cmd".

``version``
-----------

Show version of cmddocs

::

        Usage:
            version


Changelog
---------

See Changelog_.

.. _Changelog: https://github.com/noqqe/cmddocs/blob/master/CHANGELOG.rst

License
-------

See License_.

.. _License: https://github.com/noqqe/cmddocs/blob/master/License.txt

