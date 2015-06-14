#!/usr/bin/env python

import os
import cmd
import git
import sys
import signal
import ConfigParser
import pkg_resources
from os.path import expanduser
from articles import *
from completions import *

class Cmddocs(cmd.Cmd):
    """ Basic commandline interface class """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.reset = '\033[0m'
        self.read_config(self)
        self.initialize_docs(self)
        self.prompt = '\033[1m\033[' + self.promptcol + 'm' + self.prompt + " " + self.reset

    def read_config(self, conf):
        config = ConfigParser.ConfigParser()
        if not config.read(expanduser("~/.cmddocsrc")):
            print("Error: your ~/.cmddocsrc could not be read")
            exit(1)
        try:
            self.datadir = expanduser(config.get("General", "Datadir"))
        except ConfigParser.NoOptionError:
            print("Error: Please set a Datadir in ~/.cmddocsrc")
            exit(1)
        try:
            self.exclude = expanduser(config.get("General", "Excludedir"))
        except ConfigParser.NoOptionError:
            self.exclude = expanduser('.git/')
        try:
            self.default_commit_msg = config.get("General", "Default_Commit_Message")
        except ConfigParser.NoOptionError:
            self.default_commit_msg = "small changes"
        try:
            self.editor = config.get("General", "Editor")
        except ConfigParser.NoOptionError:
            if os.environ.get('EDITOR') is not None:
                self.editor = os.environ.get('EDITOR')
            else:
                print("Error: Could not find usable editor.")
                print("Please specify one in config or set EDITOR in your \
                OS Environment")
                exit(1)
        try:
            self.pager = config.get("General", "Pager")
        except ConfigParser.NoOptionError:
            if os.environ.get('PAGER') is not None:
                self.editor = os.environ.get('PAGER')
            else:
                print("Error: Could not find usable Pager.")
                print("Please specify one in config or set PAGER in your\
                OS Environment")
                exit(1)
        try:
            self.prompt = config.get("General", "Prompt")
        except ConfigParser.NoOptionError:
            self.prompt = "cmddocs>"
        try:
            self.promptcol = config.get("General", "Promptcolor")
        except ConfigParser.NoOptionError:
            self.promptcol = "37"
        try:
            self.intro = config.get("General", "Intro_Message")
        except ConfigParser.NoOptionError:
            self.intro = "cmddocs - press ? for help"
        return

    def initialize_docs(self, docs):
        # Read or initialize git repository
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

    ### list
    def do_list(self, dir):
        "Show files in current working dir"
        if not dir:
            dir = "."
        return list_articles(dir)

    # Aliases
    do_l = do_list
    do_ls = do_list

    def do_dirs(self, dir):
        "Show only directories in cwd"
        if not dir:
            dir = "."
        return list_directories(dir)

    do_d = do_dirs

    ### directories
    def do_cd(self,dir):
        "Change directory"
        cwd = change_directory(dir,self.datadir)

    def do_pwd(self,line):
        "Show current directory"
        print(os.path.relpath(os.getcwd(),self.datadir))

    ### edit
    def do_edit(self, article):
        """
        Edit or create new article.

        > edit databases/mongodb
        > edit intro
        """
        return edit_article(article, os.getcwd(), self.editor, self.repo, self.default_commit_msg)

    do_e = do_edit

    ### view
    def do_view(self, article):
        """
        View an article. Creates temporary file with converted markdown to
        ansi colored output. Opens your PAGER. (Only less supported atm)

        > view databases/mongodb
        > view intro
        """
        return view_article(article, os.getcwd(), self.pager)

    ### delete
    def do_delete(self, article):
        "Delete an article"
        delete_article(article, os.getcwd(),self.repo)

    do_rm = do_delete

    ### move
    def do_move(self, args):
        "Move an article"
        move_article(os.getcwd(),args,self.repo)

    do_mv = do_move

    ### search
    def do_search(self, keyword):
        "Search for keyword in current directory. Example: search mongodb"
        print(search_article(keyword,os.getcwd(), self.datadir,
            self.exclude))

    ### status
    def do_status(self, line):
        "Show git repo status of your docs"
        print(self.repo.git.status())

    def do_log(self, args):
        """
        Show git logs of your docs.

        Usage: log                      # default loglines: 10)
               log 20                   # show 20 loglines
               log 20 article           # show log for specific article
               log databases/mongodb 3  # same
        """
        show_log(args,self.repo)

    def do_diff(self, args):
        """
        Show git diffs (Gruesse von deiner Suessen!)

        Usage: log                      # default diff to last
        """
        show_diff(args,self.repo)


    ### undo / revert
    def do_undo(self, args):
        """
        You can revert your changes (use revert from git)

        Usage:
        > undo HEAD
        > undo 355f375

        Will ask for confirmation.
        """
        undo_change(args, self.repo)

    do_revert = do_undo

    ### exit
    def do_exit(self, line):
        "Exit cmddocs"
        return True

    def do_EOF(self, line):
        "Exit cmddocs"
        print("exit")
        return True

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

    complete_mv = path_complete
    complete_move = path_complete

    complete_log = path_complete

def ctrlc(sig, frame):
    print("\n")
    sys.exit(0)

signal.signal(signal.SIGINT, ctrlc)

def main():
    Cmddocs().cmdloop()

if __name__ == '__main__':
    main()
