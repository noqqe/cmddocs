#!/usr/bin/env python
""" cmddocs Class """

import os
import cmd
import sys
import signal
import configparser
import git
import pkg_resources
from cmddocs.articles import *
from cmddocs.completions import *
from cmddocs.version import __version__

class Cmddocs(cmd.Cmd):
    """ Basic commandline interface class """

    def __init__(self, conf="~/.cmddocsrc"):
        """
        Initialize the class
        Inherit from Cmd
        Read config, initialize Datadir, create Prompt
        """
        cmd.Cmd.__init__(self)
        self.reset = '\033[0m'
        self.read_config(self, conf)
        self.initialize_docs(self)
        self.prompt = '\033[1m\033[' + self.promptcol + 'm' + self.prompt + " " + self.reset
        self.do_cd(self.datadir)

    def read_config(self, sconf, conf):
        """
        All Config Options being read and defaulting
        """

        self.colors = {}
        config = configparser.ConfigParser()

        if not config.read(os.path.expanduser(conf)):
            print("Error: your config %s could not be read" % conf)
            exit(1)

        try:
            self.datadir = os.path.expanduser(config.get("General", "Datadir"))
        except configparser.NoOptionError:
            print("Error: Please set a Datadir in %s" % conf)
            exit(1)

        try:
            self.exclude = os.path.expanduser(config.get("General", "Excludedir"))
        except configparser.NoOptionError:
            self.exclude = os.path.expanduser('.git/')

        try:
            self.default_commit_msg = config.get("General", "Default_Commit_Message")
        except configparser.NoOptionError:
            self.default_commit_msg = "small changes"

        try:
            self.editor = config.get("General", "Editor")
        except configparser.NoOptionError:
            if os.environ.get('EDITOR') is not None:
                self.editor = os.environ.get('EDITOR')
            else:
                print("Error: Could not find usable editor.")
                print("Please specify one in config or set EDITOR in your \
                OS Environment")
                exit(1)

        try:
            self.pager = config.get("General", "Pager")
        except configparser.NoOptionError:
            if os.environ.get('PAGER') is not None:
                self.editor = os.environ.get('PAGER')
            else:
                print("Error: Could not find usable Pager.")
                print("Please specify one in config or set PAGER in your\
                OS Environment")
                exit(1)

        try:
            self.pagerflags = config.get("General", "PagerFlags")
        except configparser.NoOptionError:
            self.pagerflags = False

        try:
            self.editorflags = config.get("General", "EditorFlags")
        except configparser.NoOptionError:
            self.editorflags = False

        try:
            self.prompt = config.get("General", "Prompt")
        except configparser.NoOptionError:
            self.prompt = "cmddocs>"

        try:
            self.promptcol = config.get("General", "Promptcolor")
        except configparser.NoOptionError:
            self.promptcol = "37"

        try:
            self.intro = config.get("General", "Intro_Message")
        except configparser.NoOptionError:
            self.intro = "cmddocs - press ? for help"

        try:
            self.mailfrom = config.get("General", "Mail")
        except configparser.NoOptionError:
            self.mailfrom = "nobody"

        try:
            self.extension = config.get("General", "Default_Extension")
        except configparser.NoOptionError:
            self.extension = "md"

        try:
            self.colors['h1'] = config.get("Colors", "Header12")
        except (configparser.NoOptionError, configparser.NoSectionError):
            self.colors['h1'] = "37"

        try:
            self.colors['h2'] = config.get("Colors", "Header345")
        except (configparser.NoOptionError, configparser.NoSectionError):
            self.colors['h2'] = "92"

        try:
            self.colors['code'] = config.get("Colors", "Codeblock")
        except (configparser.NoOptionError, configparser.NoSectionError):
            self.colors['code'] = "92"

        return

    def initialize_docs(self, docs):
        """ Read or initialize git repository """
        try:
            self.repo = git.Repo(self.datadir)
        except git.exc.NoSuchPathError:
            print("Error: Specified datadir %s does not exist" % self.datadir)
            exit(1)
        except git.exc.InvalidGitRepositoryError:
            self.repo = git.Repo.init(self.datadir)
            try:
                self.repo.git.add(".")
                self.repo.git.commit(m=" init")
            except git.exc.GitCommandError:
                pass
            print("Successfully created and initialized empty repo at %s" % self.datadir)
        # Change to datadir
        try:
            os.chdir(self.datadir)
            self.cwd = os.getcwd()
        except OSError:
            print("Error: Switching to Datadir %s not possible" % self.datadir)
            exit(1)

    def do_list(self, dir):
        """
        Show files in current working dir

        Usage:
            list
            l
            list Databases/
        """
        if not dir:
            dir = "."
        return list_articles(dir, self.extension)

    do_l = do_list
    do_ls = do_list

    def do_dirs(self, dir):
        """
        Show directories in current working dir

        Usage:
            dirs
            d
            dirs Databases/
        """
        if not dir:
            dir = "."
        return list_directories(dir)

    do_d = do_dirs

    def do_cd(self, dir):
        """
        Change directory

        Usage:
            cd Programming/
            cd
        """
        change_directory(dir, self.datadir)

    def do_pwd(self, line):
        """
        Show current directory

        Usage:
            pwd
        """
        print(os.path.relpath(os.getcwd(), self.datadir))

    def do_edit(self, article, test=False):
        """
        Edit or create new article.

        Usage:
            edit databases/mongodb
            edit intro
        """
        return edit_article(article, os.getcwd(), self.editor, self.repo,
                            self.default_commit_msg, self.extension, test, self.editorflags)

    do_e = do_edit

    def do_view(self, article):
        """
        View an article. Creates temporary file with converted markdown to
        ansi colored output. Opens your PAGER. (Only less supported atm)

        Usage:
            view databases/mongodb
            view intro
        """
        return view_article(article, os.getcwd(), self.pager, self.extension,
                            self.pagerflags, self.colors)

    def do_mail(self, article):
        """
        Mail an article to a friend

        Usage:
            mail databases/mongodb
            Recipient: mail@example.net

            mail programming/r/loops
            mail intro
        """
        return mail_article(article, os.getcwd(), self.mailfrom, self.extension)

    def do_delete(self, article):
        """
        Delete an article

        Usage:
            delete databases/mongodb
            rm databases/mssql
        """
        delete_article(article, os.getcwd(), self.repo, self.extension)

    do_rm = do_delete

    def do_move(self, args):
        """
        Move an article to a new location

        Usage:
            move databases/mongodb databases/MongoDB
            move life/foo notes/foo
            mv life/foo notes/foo
        """
        move_article(os.getcwd(), args, self.repo, self.extension)

    do_mv = do_move

    def do_search(self, keyword):
        """
        Search for keyword in current directory

        Usage:
            search mongodb
            search foo
        """
        print(search_article(keyword, os.getcwd(), self.datadir,
                             self.exclude))

    def do_status(self, line):
        """
        Show git repo status of your docs

        Usage:
            status

        """
        print(self.repo.git.status())

    def do_log(self, args):
        """
        Show git logs of your docs.

        Usage:
            log                      # default loglines: 10)
            log 20                   # show 20 loglines
            log 20 article           # show log for specific article
            log databases/mongodb 3  # same
        """
        show_log(args, self.repo, self.extension)

    def do_info(self, article):
        """
        Show infos for an article

        Usage:
            info article
            info Databases/mongodb
            Created: 2014-01-18 11:18:03 +0100
            Updated: 2015-10-23 14:14:44 +0200
            Commits: 26
            Lines: 116
            Words: 356
            Characters: 2438
        """
        info_article(article, os.getcwd(), self.repo, self.extension)

    def do_diff(self, args):
        """
        Show git diffs between files and commits

        Usage:
            diff 7                   # show diff for last 7 changes
            diff 1 article           # show diff for last change to article
            diff                     # show last 5 diffs
        """
        show_diff(args, self.repo, self.extension)

    def do_undo(self, args):
        """
        You can revert your changes (use revert from git)

        Usage:
            undo HEAD
            undo 355f375

        Will ask for confirmation.
        """
        undo_change(args, self.repo)

    def do_stats(self, args):
        """
        Calculate some statistics on your docs

        Usage:
            stats

        """
        show_stats(args, self.repo, self.datadir)

    def do_version(self, args):
        """
        Show version of cmddocs

        Usage:
            version

        """
        print("cmddocs %s" % __version__)


    do_revert = do_undo

    ### exit
    def do_exit(self, args):
        """
        Exit cmddocs

        Usage:
            exit
        """
        return True

    do_EOF = do_exit

    ### completions
    complete_l = path_complete
    complete_ls = path_complete
    complete_list = path_complete

    complete_d = path_complete
    complete_dirs = path_complete

    complete_view = path_complete
    complete_cd = path_complete

    complete_e = path_complete
    complete_edit = path_complete

    complete_rm = path_complete
    complete_delete = path_complete

    complete_mail = path_complete
    complete_mv = path_complete
    complete_move = path_complete

    complete_log = path_complete
    complete_info = path_complete

def ctrlc(sig, frame):
    """ Handle Interrupts """
    print("\n")
    sys.exit(0)

signal.signal(signal.SIGINT, ctrlc)

def main():
    """ Call loop method """
    Cmddocs().cmdloop()

if __name__ == '__main__':
    main()
