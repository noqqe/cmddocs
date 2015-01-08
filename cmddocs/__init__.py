#!/usr/bin/env python

import os
import cmd
import git
import ConfigParser
from os.path import expanduser
from articles import *
from completions import *

class Cmddocs(cmd.Cmd):
    """ Basic commandline interface class """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.read_config(self)
        self.initialize_docs(self)
        self.prompt = '\033[1m\033[37m{} \033[0m'.format(self.prompt)

    def read_config(self, conf):
        config = ConfigParser.ConfigParser()
        if not config.read(expanduser("~/.cmddocsrc")):
            print "Error: your ~/.cmddocsrc could not be read"
            exit(1)
        try:
            self.datadir = expanduser(config.get("General", "Datadir"))
            self.exclude = expanduser(config.get("General", "Excludedir"))
            self.default_commit_msg = config.get("General", "Default_Commit_Message")
            self.editor = config.get("General", "Editor")
            self.pager = config.get("General", "Pager")
            self.prompt = config.get("General", "Prompt")
            self.intro = config.get("General", "Intro_Message")
        except ConfigParser.NoSectionError:
            print "Error: Config wrong formatted"
            exit(1)
        return 
        
    def initialize_docs(self, docs):
        # Read or initialize git repository
        try:
            self.repo = git.Repo(self.datadir)
        except git.exc.InvalidGitRepositoryError:
            self.repo = git.Repo.init(self.datadir)
            self.repo.git.add(".")
            self.repo.git.commit("init")
            print("Successfully created and initialized empty repo at %s" % self.datadir)
        # Change to datadir
        try:
            os.chdir(self.datadir)
            self.cwd = os.getcwd()
        except OSError:
            print "Error: Switching to Datadir %s not possible" % self.datadir
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
        print os.path.relpath(os.getcwd(),self.datadir)

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
        print search_article(keyword,os.getcwd(), self.datadir, self.exclude)

    ### status
    def do_status(self, line):
        "Show git repo status of your docs"
        print self.repo.git.status()

    def do_log(self, args):
        """
        Show git logs of your docs.

        Usage: log                      # default loglines: 10)
               log 20                   # show 20 loglines
               log 20 article           # show log for specific article
               log databases/mongodb 3  # same
        """
        show_log(args,self.repo)

    ### exit
    def do_exit(self, line):
        "Exit cmddocs"
        return True

    def do_EOF(self, line):
        "Exit cmddocs"
        print "exit"
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

