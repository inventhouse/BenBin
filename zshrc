#!/bin/zsh

###  Environment Variables  ###
export PATH="$HOME/.pyenv/bin:${PATH}:$HOME/inventhub/allgit:$HOME/inventhub/bettergit:$HOME/inventhub/BenBin"

# Added by `pipx`
export PATH="$PATH:/Users/bjh/.local/bin"

# pyenv setup
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
#####


###  Key Bindings  ###
bindkey "^[[A" history-beginning-search-backward
bindkey "^[[B" history-beginning-search-forward
#####


###  Prompt  ###
source ~/inventhub/BenBin/zsh-prompt
#####


###  Aliases  ###
source ~/inventhub/BenBin/zsh-aliases
#####