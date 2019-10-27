def _it(args, stdin=None):
    "Easily pipe to and from $it"
    if stdin is None:  # No input, output $it
        return "{}".format(${...}.get("it", ""))
    else:  # Stash input into $it
        $it = stdin.read()
        return $it

aliases["it"] = _it
aliases["ag"] = "allgit"

###
