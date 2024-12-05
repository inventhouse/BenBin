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

- DONE: Start with _only_ stdin, no files; `cat` in whatever you want
- Handle stdout closing (e.g. `lines ... | head`)

- Add file args; file names may be useful context when doing multi-file processing

- Parse args
    - `lines COMMAND ... -- FILE ...` or `lines -e COMMAND -e... FILE ...`?
        - Leaning toward the former, but latter is more standard
    - Commands are command + separator (`(?P<cmd>[a-z]+)(?P<sep>[^a-z])`), fields split by separator, command options
        - Separator is a single character following the command, used through the rest of the command; no escape sequence, use onethat doesn't appear; recommend bullet (`•`) - not used in regex, easy to type (`opt-8`)
        - Short and long commands? - YES, quick vs. readability/maintainability uses for both with commands and options
        - Short and long options? - YES
            - Option syntax?
                - Maybe something like`(?P<short_letters_block>[\w-]*);?(?P<long_opt>[\w-]+(:(?P<opt_arg>[\w-]+(,...)?)?;?...)`
                - Definitely want option-parser utility, operations should get kwargs
                    - Should common options like RE flags be parsed here?

- Top-level options
    - Add `argparse`
    - Script file option
    - Trace/verbose/debug
    - Default pass/drop?
    - Help
        - Build command help from `CMD_MAP` and Operation class docstrings

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
        - Indentation level?
    - If/else?
    - Global `else`?  (i.e. all the lines that were simply passed by other operations)
    - Operate on file-change?

### Doneyard


---