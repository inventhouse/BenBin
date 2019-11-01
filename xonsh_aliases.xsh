def _it(args, stdin=None):
    "Easily pipe to and from $it"
    if stdin is None:  # No input, output $it
        return "{}".format(${...}.get("it", ""))
    else:  # Stash input into $it
        $it = stdin.read()
        return $it if "-q" not in args else ""
aliases["it"] = _it

# alias pbq='pbpaste | sed -e "s/^/> /" | pbcopy'
def _pbq(ars, stdin=None):
    "Adds '> ' to the lines in the pasteboard so they can be pasted as a Markdown block quote"
    lines = [ f"> {s}" for s in !(pbpaste) ]
    echo -n @("".join(lines)) | pbcopy
    return None
aliases["pbq"] = _pbq

# alias pbc='pbpaste | sed -e "s/ # .*//" -e "s/^#.*//" -e "/^ *$/d" | pbcopy'


aliases["ag"] = "allgit"
aliases["dkr"] = "docker"
aliases["dkc"] = "docker-compose"

###
