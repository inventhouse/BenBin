Xonsh Notes
===========


To Do
-----
- `re` glob issues
    - DONE: split [original issue](https://github.com/xonsh/xonsh/issues/3372), [new issue](https://github.com/xonsh/xonsh/issues/3381)
        - research & document current behavior
        - implement better error messages
    - research better `re` matching algorithm
        - DONE: can it be done with standard `re` library
            - NO.  `match` implemented in C, hides VM error code: [_sre_SRE_Pattern_match_impl](https://github.com/python/cpython/blob/d0e0f5bf0c07ca025f54df21fd1df55ee430d9fc/Modules/_sre.c#L589)
            - doesn't have to be that way, `match_impl` is pretty small, could be hoisted to python allowing access to underlying machine
            - https://stackoverflow.com/questions/58599729/programmatically-determine-where-pythons-re-match-stopped-matching
        - find pure-python `re` library
- create issue & pr to make `ret_code_color` configurable
    - [code](https://github.com/xonsh/xonsh/blob/master/xontrib/prompt_ret_code.xsh)
- create issue for "python redirection": `<(py_exp)`, `>(py_name)`, `>>(py_name)`


### Doneyard

---
