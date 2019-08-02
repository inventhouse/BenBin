#!/bin/sh
git config --global alias.pra 'pull -r --autostash'
git config --global alias.ss 'status -s'
git config --global alias.l1 'log -n1'
git config --global alias.l5 'log -n5'
git config --global alias.l3 'log -n 3'
git config --global alias.lo 'log -n 10 --oneline'
git config --global alias.co 'checkout'
git config --global alias.cp 'cherry-pick'
git config --global alias.cm 'commit -m'
git config --global alias.cam 'commit -am'
git config --global alias.sb '! setupb'
git config --global alias.lb '! listb'
git config --global alias.nb '! newb'
git config --global alias.gb '! getb'
git config --global alias.killb '! killb'
git config --global alias.db '! dropb'
git config --global alias.sq '! squashbranch'
git config --global alias.rbm 'rebase origin/master'
git config --global alias.prl '! hub pr list'
git config --global alias.prm '! hub pull-request --browse -m'
git config --global alias.rau 'remote add upstream'
git config --global alias.fu 'fetch upstream'
git config --global alias.rbu 'rebase upstream/master'