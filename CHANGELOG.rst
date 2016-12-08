Changelog
=========

0.17.0 (2016-11-15)
-------------------

- Python 3.5 compatibility in setup and tests. [Florian Baumann]

- Python3 compatibility: raw_input =&gt; input. [lonetwin]

- Python3 compatibility: relative imports. [lonetwin]

- Python3 compatibility: File mode changes. [lonetwin]

  Use text mode instead of binary to avoid unnecesary bytes-to-string
  conversions

- Python3 compatibility: subprocess stdout bytes =&gt; utf-8 strings. [lonetwin]

- Python3 compatibility: ConfigParser =&gt; configparser. [lonetwin]

- Badges. [Florian Baumann]

- Codecoverage for tests. [Florian Baumann]

- Codecoverage for tests. [Florian Baumann]

0.16.2 (2016-04-12)
-------------------

- Version bump. [Florian Baumann]

- Fix mail with no parameters #32. [Florian Baumann]

0.16.1 (2016-04-12)
-------------------

- Version bump. [Florian Baumann]

- Fix for editorflags. [Florian Baumann]

- Changelog update. [Florian Baumann]

0.16.0 (2016-04-12)
-------------------

Fix
~~~

- No [Colors] section is also okay for config parser now. #29. [Florian Baumann]

- Catch error when accessing git objects with diff. [Florian Baumann]

Documentation
~~~~~~~~~~~~~

- Documentation: Screenshot in Readme. [Florian Baumann]

- Documentation: Screenshot in Readme. [Florian Baumann]

- Documentation: Readme format update. [Florian Baumann]

- Documentation: Screenshot in Readme. [Florian Baumann]

- Documentation: Screenshot in Readme. [Florian Baumann]

Other
~~~~~

- Version bump. [Florian Baumann]

- Implemented editorflags #31. [Florian Baumann]

- Merge branch &#x27;master&#x27; of github.com:noqqe/cmddocs. [Florian Baumann]

- Changelog update. [Florian Baumann]

0.15.0 (2015-12-13)
-------------------

Feature
~~~~~~~

- Feature: Added more tests for dir, log, search. [Florian Baumann]

- Feature: Added more tests. [Florian Baumann]

Fix
~~~

- Status and Initialization tests. [Florian Baumann]

- Fixed broken tree call for directories and added tests. [Florian Baumann]

- Stats test. [Florian Baumann]

- Catch exception when dir or file in list not found. [Florian Baumann]

- Tests for pwd and properly change to datadir. [Florian Baumann]

- Tests imporved. [Florian Baumann]

- Make checks work in travis. [Florian Baumann]

Documentation
~~~~~~~~~~~~~

- Documentation: Fixed directory checks. [Florian Baumann]

- Documentation: more tests. [Florian Baumann]

- Documentation: directory checks. [Florian Baumann]

- Documentation: undo, version, status Tests. [Florian Baumann]

- Documentation: new tests and new testenv. [Florian Baumann]

- Documentation: info command tests. [Florian Baumann]

- Documentation: Restructured Tests. [Florian Baumann]

- Documentation: reformat readme. [Florian Baumann]

- Documentation: Docs for each command in Readme. [Florian Baumann]

- Documentation: new sections for changelog. [Florian Baumann]

- Documentation: new help messages. [Florian Baumann]

- Documentation: Readme updated. [Florian Baumann]

Other
~~~~~

- Release version 0.15.0. [Florian Baumann]

- Edit tests. [Florian Baumann]

- Removed pypy build from travis. [Florian Baumann]

- Added user and mail for tests. [Florian Baumann]

- Fix readme. [Florian Baumann]

- Fix readme. [Florian Baumann]

- Markup fix. [Florian Baumann]

- Applied pylint changes. [Florian Baumann]

- Version bump. [Florian Baumann]

0.14.0 (2015-12-08)
-------------------

Feature
~~~~~~~

- Feature: Configurable colors for md to ascii #22. [Florian Baumann]

- Feature: Configure pager flags - #20. [Florian Baumann]

Documentation
~~~~~~~~~~~~~

- Documentation: updated Readme for Pagerflags. [Florian Baumann]

Other
~~~~~

- More robust config in completions. [Florian Baumann]

- Referenced Changelog in README.rst. [Florian Baumann]

- Now using gitchangelog for python to provide proper changelog. [Florian Baumann]

0.13.0 (2015-12-08)
-------------------

- Implemented version command #21. [Florian Baumann]

- Count files and ignore .git. [Florian Baumann]

- Implemented stats command - fixes #24. [Florian Baumann]

- Fixed diff function and help message. [Florian Baumann]

- Created info command to display informations about an article. [Florian Baumann]

- Comma code style for arguments. [Florian Baumann]

- Fixed bugs in log and diff because of missing file extensions. [Florian Baumann]

- More py3 removals. [Florian Baumann]

0.12.3 (2015-11-11)
-------------------

- Reverted py3 compatibility. Its fucked. [Florian Baumann]

- Tree as dep in test build. [Florian Baumann]

- Config example mail in tests. [Florian Baumann]

- Added more tests. [Florian Baumann]

0.12.2 (2015-11-10)
-------------------

- Bugfix default-extension when creating a new file. [Florian Baumann]

- Switch to pytest. [Florian Baumann]

- Added test and some restructuring. [Florian Baumann]

- Made .cmddocsrc a class parameter. [Florian Baumann]

- Deleted cache. [Florian Baumann]

- Cache dir ignore. [Florian Baumann]

- Tests init. [Florian Baumann]

- Gitpython is broken with 3.2. [Florian Baumann]

- Fixes py3.1-py3.4 setup py. [Florian Baumann]

- Removed requirements due to fully compatible py3 py2 pip. [Florian Baumann]

- Testing travis. [Florian Baumann]

0.12.1 (2015-11-08)
-------------------

- Fixes for python3 install with pip. [Florian Baumann]

0.12.0 (2015-11-08)
-------------------

- Python 3 compatibility - fixes #17. [Florian Baumann]

- Fixes #11 - Default Filetype introduced! [Florian Baumann]

0.11.0 (2015-11-08)
-------------------

- Fixes #11 - Default Filetype introduced! [Florian Baumann]

- Readme update. [Florian Baumann]

- Mail function #14. [Florian Baumann]

- Merge pull request #19 from agundy/master. [Florian Baumann]

  Added exception catch for log.

- Added exception catch for log. [Aaron Gunderson]

0.10.6 (2015-06-14)
-------------------

- Added handler for tree dependency. [Florian Baumann]

- Catch missing tree, converted all print statements. [Florian Baumann]

0.10.5 (2015-06-06)
-------------------

- Version bump. [Florian Baumann]

- Crtl-c signal handling. [Florian Baumann]

0.10.4 (2015-06-06)
-------------------

- Version bump. [Florian Baumann]

- Bug fixes, print syntax, return values. [Florian Baumann]

0.10.3 (2015-06-06)
-------------------

- Version bump. [Florian Baumann]

- Catch datadir not existing error. [Florian Baumann]

0.10.2 (2015-06-06)
-------------------

- Repo init fix. [Florian Baumann]

- Mistune requirements. [Florian Baumann]

0.10.0 (2015-06-06)
-------------------

- Version bump. [Florian Baumann]

- Deleted setup. [Florian Baumann]

- Long description for pypi. [Florian Baumann]

- Fixed list items. [Florian Baumann]

- Readme to rst. [Florian Baumann]

- Added mistune to PROPERLY parse markdown to ascii. [Florian Baumann]

- Added mistune to PROPERLY parse markdown to ascii. [Florian Baumann]

- Created undo/revert. [Florian Baumann]

- Updated readme. [Florian Baumann]

- Added sane config default fallbacks #1. [Florian Baumann]

- Color prompt now configurable. [Florian Baumann]

- Catching errors when exec without valid config #13. [Florian Baumann]

- Article name search implemented #12. [Florian Baumann]

- Updated readme for pip. [Florian Baumann]

0.9.1 (2015-05-17)
------------------

- Fix long description. [Florian Baumann]

- Moved license. [Florian Baumann]

- Setup.cfg. [Florian Baumann]

- Ignores. [Florian Baumann]

- Pip preparations. [Florian Baumann]

0.9.0 (2015-05-17)
------------------

- Added setup.py. [Florian Baumann]

- Added diff functionality. [Florian Baumann]

- Moved utils to compeltions. [Florian Baumann]

- Removed imports - thanks to pyflakes. [Florian Baumann]

- More structure. [Florian Baumann]

- Lol. [Florian Baumann]

- Gitignore. [Florian Baumann]

- Moved to package. [Florian Baumann]

- Better presentation of path. [Florian Baumann]

- Merge branch &#x27;posativ-patch-3&#x27; [Florian Baumann]

- Merged. [Florian Baumann]

- Use subprocess instead of os.system with string replacement. [Martin Zimmermann]

- T push origin master Merge branch &#x27;posativ-patch-4&#x27; [Florian Baumann]

- Merged. [Florian Baumann]

- Fix undefined behavior, mis-used classmethods. [Martin Zimmermann]

- Accidentially wrong mapped alias. [Florian Baumann]

- Merge pull request #3 from posativ/patch-2. [Florian Baumann]

  simplify command declaration

- Simplify command declaration. [Martin Zimmermann]

  Minor drawback: the docstring for aliases is no longer available
  (replaced with the actual function&#x27;s docstring).

- Merge pull request #2 from posativ/patch-1. [Florian Baumann]

  expanduser for configuration variables

- Expanduser for configuration variables. [Martin Zimmermann]

- Error handling for rm and fix for mv. [Florian Baumann]

- Prompt in new structure. [Florian Baumann]

- Repo referenced in functions. [Florian Baumann]

- Merged. [Florian Baumann]

- Bugfix cwd. [Florian Baumann]

- Fixed cwd problem. [Florian Baumann]

- More variable passing. [Florian Baumann]

- Merge branch &#x27;master&#x27; into noglobals. [Florian Baumann]

- Replaced dumb try with if. [Florian Baumann]

- First steps making config in class. [Florian Baumann]

- Just renaming. [Florian Baumann]

- Function definitions. [Florian Baumann]

- Small fix. [Florian Baumann]

- Added intro message configurable and readme update. [Florian Baumann]

- Prompt configurable. [Florian Baumann]

- Removed double check of datadir. [Florian Baumann]

- Merge branch &#x27;master&#x27; of github.com:noqqe/cmddocs. [Florian Baumann]

- Update LICENSE.md. [Florian Baumann]

- Pager and editor now configurable in config. [Florian Baumann]

- Merge branch &#x27;master&#x27; of github.com:noqqe/cmddocs. [Florian Baumann]

- Added license. [Florian Baumann]

- Embedding of asciinema does not work... :( added link instead. [Florian Baumann]

- Make config usergeneric. [Florian Baumann]

- Docs update and helptexts improvements. [Florian Baumann]

- Fixes for list dir. [Florian Baumann]

- Restructuring. [Florian Baumann]

- Readme added. [Florian Baumann]

- Configparser. [Florian Baumann]

- Arg parsing into functions, better error handling. [Florian Baumann]

- Better error handling. [Florian Baumann]

- Added check for EDITOR and PAGER. [Florian Baumann]

- Default commit message implemented. [Florian Baumann]

- Log messages. [Florian Baumann]

- Intelligent log function. [Florian Baumann]

- View mode with header and codeblock highlight. [Florian Baumann]

- Highlighted view mode. [Florian Baumann]

- Added basic pager, view mode. [Florian Baumann]

- Fix mv and colors for log. [Florian Baumann]

- Added comments, move and delete functionality. [Florian Baumann]

- Make cd able to switch to default. [Florian Baumann]

- Stopped experimenting with python made tree-like output. [Florian Baumann]

- Colored search. [Florian Baumann]

- Working search. [Florian Baumann]

- Var replacement and datadir. [Florian Baumann]

- Path completion for all functions. [Florian Baumann]

- Fix dir not found message. [Florian Baumann]

- Added &#x27;safe&#x27; cd function. [Florian Baumann]

- Implemented search function.. start.. [Florian Baumann]

- Log improvements and list replacement. [Florian Baumann]

- Huge steps, we make. [Florian Baumann]

- L can now take arguments. [Florian Baumann]

- Completion without .git directory. [Florian Baumann]

- Added completion to list. [Florian Baumann]

- Fixed edit with new subdirs. [Florian Baumann]

- Init. [Florian Baumann]


