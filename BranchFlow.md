BranchFlow
==========
easier branch workflow

`$ ag -m -- newb JIRA-123-my-feature f` ==> checkout -b f ; push -u bjh/JIRA-123-my-feature (maybe also something to add jira tik after-the-fact? or generalized rename?)
_( work with f like normal )_
`$ ag -b f -- rebase` ==> rebase from parent branch (can I get this automagically or just assume master?)
`$ ag -b f -- pr` ==> create PR for branch
_( incorporate feedback )_
`$ ag -b f -- squashbranch -cp` ==> squash, re-commit with original message + squash-hashes, force-push (maybe be clever about only squash if there are multiple commits to squash)
`$ ag -b f -- killb` ==> check out parent branch and delete local and remote (or rebase-done?)

`$ ag -a -- listb` ==> list alias branches in repos that have them

- DONE: $ALLGIT_BRANCH - mechanism for helpers that expect to be on the desired branch so they can enforce that?

`$ ag -cb f -- squashbranch [-c|-m message] [-p?]` ==> squash, re-commit with original message + squash-hashes or message + squash-hashes, force-push (pre-commit check in here somewhere?) - or maybe `squashpush` does squashbranch + extras  (Does git support precommit hook? yes, also look into https://pre-commit.com)


$ git push -u origin thing:bjh/thing
Total 0 (delta 0), reused 0 (delta 0)
remote:
remote: Create a pull request for 'bjh/thing' on GitHub by visiting:
remote:      https://github.com/inventhouse/Test/pull/new/bjh/thing
remote:
To github.com:inventhouse/Test.git
 * [new branch]      thing -> bjh/thing
Branch 'thing' set up to track remote branch 'bjh/thing' from 'origin'.
Inara:Test bjh$
Inara:Test bjh$ git rev-parse --abbrev-ref @{upstream}
origin/bjh/thing
Inara:Test bjh$ git rev-parse --abbrev-ref HEAD
thing
Inara:Test bjh$ git remote
origin
Inara:Test bjh$


- short "alias" local names, longer descriptive remote names
    - easy as possible to create - programmatic prefix (maybe git-config setting?), jira tix integration? slug?
    - easy-or-automatic to avoid/deal with alias conflicts
    - easy to push/create PR  (probably need access token for that?)
    - easy to clean up
    - easy to alias-checkout remote branches

- easy to list "alias" branches
    - DONE: `listb` - lists branches that don't match their upstream (including local branches)
    - allgit -a/--alias-branches? - run in repos with local branches that don't "match" upstream - needs to be a "pre-filter" in allgit though
    - should it include "pure local" branches? - probably

- DONE: `newb` - create a local branch with short name & upstream with longer composed name
    - DONE: need `setupb SLUG` for composing upstream name after-the-fact - need to guard for already tracking?
- DONE: `killb` - clean up local and upstream branches
    - DONE: need a good way to delete just local branch but with $ALLGIT_BRANCH - `dropb`?
- DONE: `getb` - check out remote branch as alias

- need an allgit utils module or something

---