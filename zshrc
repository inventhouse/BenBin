#!/bin/zsh

###  Environment Variables  ###
export PATH="$HOME/.local/bin:${PATH}:$HOME/inventhub/allgit:$HOME/inventhub/bettergit:$HOME/inventhub/BenBin"

# Go lang
export PATH="$PATH:$HOME/go/bin"

# Rust
export PATH="$PATH:$HOME/.cargo/bin"

# Homebrew
if `which brew 2>&1 >> /dev/null`; then
    eval "$(brew shellenv)"
fi
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
