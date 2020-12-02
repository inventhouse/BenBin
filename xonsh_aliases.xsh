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

# alias pbc='pbpaste | sed -e "s/ # .*//" -e "s/^#.*//" -e "/^ *$/d" | pbcopy'
# aliases["pbc"] = lambda: $[pbpaste | sed -e "s/ # .*//" -e "s/^#.*//" -e "/^ *$/d" | pbcopy]  # pipelines in aliases are tricky
def _pbc(args, stdin=None):
    "Strips #-style comments from the lines in the pasteboard so they can be pasted"
    lines = !(pbpaste)
    lines = ( re.sub(r"(^#.*$)|(\s+#\s.*$)", "", l) for l in lines )
    lines = ( l for l in lines if re.search(r"\S", l))
    echo -n @("".join(lines)) | pbcopy
    return None
aliases["pbc"] = _pbc


aliases["adb"] = "~/Library/Android/sdk/platform-tools/adb"
aliases["ag"] = "allgit"
aliases["dkr"] = "docker"
aliases["dkc"] = "docker-compose"

# Snippets:
aliases["snip-clog"] = lambda: $[echo 'console.log({ "": {}, })  // BJH: DELETEME    ' | pbcopy]

aliases["snip-eslint"] = lambda: $[echo '// eslint-disable-next-line ' | pbcopy]

###
