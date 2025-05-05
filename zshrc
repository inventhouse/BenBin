#!/bin/zsh
###  Prompt  ###
parse_git_branch() {
    # Check if we are in a git repository (avoiding errors outside repos)
    git rev-parse --is-inside-work-tree >/dev/null 2>&1 || return

    # Get the abbreviated branch name
    local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    # Handle detached HEAD state
    if [ "$branch" = "HEAD" ]; then
        local commit_hash=$(git rev-parse --short HEAD 2>/dev/null)
        branch="($commit_hash)"
    fi

    local dirty_color=""
    if [[ -z "$(git status --porcelain --ignore-submodules -unormal)" ]]; then
        # No changes
        dirty_color="%F{green}"
    else
        # Changes present
        dirty_color="%F{red}"
    fi

    echo " ${dirty_color}${branch}%{%f%}"
}

get_virtualenv_name() {
    if [[ -n "$VIRTUAL_ENV" ]]; then
        # Add a leading space before the virtual env name
        echo " ($(basename "$VIRTUAL_ENV"))"
    else
        # Return empty string if no virtual environment is active
        echo ""
    fi
}

shorten_pwd() {
    local max_width=$1
    local pwd_path=$(print -P "%~")  # Use %~ to get the path with ~ abbreviation
    local path_length=${#pwd_path}

    if [[ $max_width -gt 0 && $path_length -gt $max_width ]]; then
        local truncate_len=$((path_length - max_width + 1)) # +1 for the single ellipsis character
        local start_len=$(( (path_length - truncate_len) / 2 ))
        local end_len=$(( path_length - start_len - truncate_len ))

        echo "${pwd_path:0:$start_len}…${pwd_path: -$end_len}"
    else
        echo "$pwd_path"
    fi
}

set_prompt() {
    local venv_name=$(get_virtualenv_name)
    local git_branch=$(parse_git_branch)

    PS1="%{%F{%(?.blue.red)}%}▶︎ %{%f%}"
    RPROMPT="%{%F{%(?.blue.red)}%}●%(?.. %?)%{%f%}$(get_virtualenv_name)$(parse_git_branch)%{%F{blue}%} $(shorten_pwd 30)%{%f%}"
}

typeset -ga precmd_functions
precmd_functions+=(set_prompt)  # Keep prompt updated
#####


###  Environment Variables  ###
export PATH="${PATH}:$HOME/inventhub/allgit:$HOME/inventhub/bettergit:$HOME/inventhub/BenBin"
#####


###  Aliases  ###
source ~/inventhub/BenBin/zsh-aliases
#####