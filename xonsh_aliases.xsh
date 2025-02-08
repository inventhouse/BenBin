def _it(args, stdin=None):
    "Easily pipe to and from $it"
    if stdin is None:  # No input, output $it
        return "{}".format(${...}.get("it", ""))
    else:  # Stash input into $it
        $it = stdin.read()
        return $it if "-q" not in args else ""
aliases["it"] = _it

# alias pbq='pbpaste | sed -e "s/^/> /" | pbcopy'
def _pbq(args, stdin=None):
    "Adds '> ' to the lines in the pasteboard so they can be pasted as a Markdown block quote"
    lines = [ f"> {s}" for s in !(pbpaste) ]
    echo -n @("".join(lines)) | pbcopy
    return None
aliases["pbq"] = _pbq

# Rewraps lines in the pasteboard so they are at most 72 characters long
# alias pbw='pbpaste | fmt -72 | pbcopy'
aliases["pbw"] = lambda: $[pbpaste | fmt | pbcopy]  # pipelines in aliases are tricky

# Sorts lines in the pasteboard
# alias pbs='pbpaste | wc'
aliases["pbwc"] = lambda: $[pbpaste | wc]

# Sorts lines in the pasteboard
# alias pbs='pbpaste | sort | pbcopy'
aliases["pbs"] = lambda: $[pbpaste | sort | pbcopy]

# Format json with jq - brew install jq
# alias pbw='pbpaste | jq "." | pbcopy'
aliases["pbjq"] = lambda: $[pbpaste | jq '.' | pbcopy]

# alias pbdotpath='pbpaste | sed -e "s/\\.[^.]*$//" | tr "/" "." | pbcopy'
aliases["pbdotpath"] = lambda: $[pbpaste | sed -e 's/\\.[^.]*$//' | tr "/" "." | pbcopy]

# alias pbc='pbpaste | sed -e "s/ # .*//" -e "s/^#.*//" -e "/^ *$/d" | pbcopy'
# aliases["pbc"] = lambda: $[pbpaste | sed -e "s/ # .*//" -e "s/^#.*//" -e "/^ *$/d" | pbcopy]
def _pbc(args, stdin=None):
    "Strips #-style comments from the lines in the pasteboard so they can be pasted"
    lines = !(pbpaste)
    lines = ( re.sub(r"(^#.*$)|(\s+#\s.*$)", "", l) for l in lines )
    lines = ( l for l in lines if re.search(r"\S", l))
    echo -n @("".join(lines)) | pbcopy
    return None
aliases["pbc"] = _pbc

# alias pbl='pbpaste | tr 'A-Z' 'a-z' | pbcopy'
def _pbl(args, stdin=None):
    "Lowercase text on the pasteboard"
    lines = [ s.lower() for s in !(pbpaste) ]
    echo -n @("".join(lines)) | pbcopy
    return None
aliases["pbl"] = _pbl

# alias pbu='pbpaste | tr 'a-z' 'A-Z' | pbcopy'
def _pbu(args, stdin=None):
    "Uppercase text on the pasteboard"
    lines = [ s.upper() for s in !(pbpaste) ]
    echo -n @("".join(lines)) | pbcopy
    return None
aliases["pbu"] = _pbu

# alias pbsqlfix='pbpaste | sqlfluff fix --dialect postgres - | pbcopy'  # FIXME: translate fix-or-lint/format into standard alias
aliases["pbsqlfix"] = lambda: $[pbpaste | sqlfluff fix --dialect postgres - | pbcopy] or $[pbpaste | sqlfluff lint --dialect postgres -]

# alias pbxmlfix='pbpaste | xmllint --format - | pbcopy'
aliases["pbxmlfix"] = lambda: $[pbpaste | xmllint --format - | pbcopy]

aliases["adb"] = "~/Library/Android/sdk/platform-tools/adb"

aliases["ag"] = "allgit"
if !(which allgit_dev):  # Special symlink to keep uing the dev version
    aliases["ag"] = "allgit_dev"

aliases["dkr"] = "docker"
aliases["dkc"] = "docker-compose"
aliases["tf"] = "terraform"
aliases["per"] = "pipenv run"

# Snippets:
aliases["snip-clog"] = lambda: $[echo 'console.log({ "": {}, })  // BJH: NOCOMMIT    ' | pbcopy]

aliases["snip-eslint"] = lambda: $[echo '// eslint-disable-next-line ' | pbcopy]

###
