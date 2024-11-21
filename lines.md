Lines
=====
_Lines Is Not Exactly Sed_

Sed-inspired line processor using modern Python regex and format syntaxes

Random Thoughts
---------------
- Keep common usage as simple as possible; Sled was too complicated
    - Make some sophisticated things possible, though, especially pre- and post-context lines
- How much should we enable `sed`-isms?  (e.g. `-e 's/foo/bar/g` as alias for `trans/foo/bar/all`?)


To Do
-----

- Use stdin, both as default and specified with `-`
- Handle stdout closing (e.g. `lines ... | tail`)

- Parse args
    - `lines COMMAND ... -- FILE ...` or `lines -e COMMAND -e... FILE ...`?
        - Leaning toward the former, but latter is more standard
    - Commands are command + separator (`(?P<cmd>[a-z]+)(?P<sep>[^a-z])`), fields split by separator, command options
        - Separator is a single character following the command, used through the rest of the command; no escape sequence, use onethat doesn't appear; recommend bullet (`•`) - not used in regex, easy to type (`opt-8`)
        - Short and long commands? - YES
        - Short and long options?

- Top-level options
    - Script file option
    - Trace/verbose/debug
    - Default pass/drop?

- Processors
    - Commands map to processors which form a pipeline
    - Init with parsed args and options
    - Called with `(line, context)`
        - Return `(line, context)` or `(None, context)`
        - If `line` is `None`, stop processing and read next

- Operations
    - `f` filter: pass only matching lines; option to invert
        - Match or search?  Easy enough to add `.*` or to anchor `^` to flip
        - Option to pass unmatched lines?  Explicitly drop unmatched lines?
            - drop / pass / pass-other-matches?  Any others?
    - `t` transform: match line pass formatted version; option to pass/drop unmatched lines
        - FIXME: use [sub/subn](https://docs.python.org/3/library/re.html#re.sub)
    - Others?  Mine sed: [Sed - An Introduction and Tutorial](https://www.grymoire.com/Unix/Sed.html)

- Meta-commands?
    - Macro definitions that can be used as arguments in other commands?
    - Buffering for pre-context?
    - Print control for post-context or to change default pass/drop?
    - Store/recall to move extracted values between lines?
    - If/else?
    - Global `else`?  (i.e. all the lines that were simply passed by other operations)

### Doneyard


---