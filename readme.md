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
and are commandline-based. There are [mutt](http://www.mutt.org), [taskwarrior](http://taskwarrior.org), [jrnl](http://maebert.github.io/jrnl/),
[weechat](http://weechat.org) and so on...But i was missing a tool for documentation

I was using [gitit](http://gitit.net) also for a long time, but I found that its way
too bloated for my needs. Also compiling `ghc` and `gitit` was awful.
After switching to just plain files using my `vim` and `git` it was also
a bit annoying. So I wrote `cmddocs` to make it easier for me to handle my
plaintext files.

If you like it - feel free using/improving it!

### Usage


