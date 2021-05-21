To Do
=====
- Add more readme about my `.xonsh*` configuation
- Add pointers to other repos
    - GitLab too?
- Add script for cleaning up copied command-lines
    - Hoist distinct right-prompts to comment-lines?
- Write-up `jira-open` and `JiraShortcut.zip`
- Write up something about my scripting style?
- `offmain` script for `ag --test` to find repos not on main/master/default
    - `git rev-parse --abbrev-ref HEAD | grep -Ev "^(main|master)$"`
    - e.g. `ag -t offmain - listb`: tell me what branches repos are on if they're not on main
    - Should this get packaged with `allgit` itself?
    - Should it allow a branch pattern argument?  Something like `offbranch "release-1.*"`
    - Or should it have an invert option `onbranch -v "release-1.*"`?
    - Should such options get passed on to grep?
    - Maybe the whole thing should be `headcheck [options for grep]`?

- recase: convert strings between upper, lower, camel, snake, kabob, ...

---
