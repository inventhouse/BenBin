#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# simple_cli: Copyright © 2025 Benjamin Holt - MIT License

import re
import unittest
from unittest.mock import Mock
#####


###  Run Main  ###
def run_main(main, arg_list, usage=None):
    """
    A simple command-line interface parser that is better than grubbing through sys.argv yourself when argparse is overkill

    Features:
    - Parses options and arguments from a list of strings and passes them to a main function with no setup needed
    - Automatically recognizes -h / --help when given a usage function
    - Long options are converted to snake_case (e.g. --foo-bar --> foo_bar, but other punctuation is preserved)
    - Short and long boolean flags (-f / --foo)
    - Combined short flags (-abc == -a -b -c)
    - Negative flags (--foo / --no-foo)
    - Options with values (-f=bar / --foo=bar)
    - Items after arguments separator (--) are treated as arguments, not options

    Limitations:
    - Requires explicit '=' for options with values like --foo=bar; --foo bar is ambiguous without complex argument configuration
    - Does not automatically map short options to long options; use a pattern like opts.get("foo", opts.get("f", False))
    - Does not support options with multiple values like --foo=bar,baz (though "bar,baz" would come through and could be split)

    Example:

        from simple_cli import run_main

        def usage(msg=""):
            print(f"Usage: {__file__} [options] [args]")

        def main(*args, **opts):
            print(f"{args = }")
            print(f"{opts = }")

        if __name__ == "__main__":
            import sys
            xit = run_main(main, sys.argv[1:], usage=usage)
            sys.exit(xit)

        # $ python3 my_script.py -a --foo=bar arg1 arg2

        # args = ('arg1', 'arg2')
        # opts = {'a': True', foo': 'bar'}
    """
    args = []
    options = {}
    args_only = False
    for arg in arg_list:
        if args_only:
            args.append(arg)
            continue
        if arg == "--":
            args_only = True
            continue
        if usage and arg in ("-h", "--help"):
            return usage()
        if re.match(r"--[^-]", arg):
            arg = arg.lstrip("-")
            if "=" in arg:
                # Only supports --foo=bar, not --foo bar
                k, _, v = arg.partition("=")
            else:
                # --foo --> {"foo": True}
                # --no-foo --> {"foo": False}
                v = not arg.startswith("no-")
                k = arg.removeprefix("no-")
            options[k.replace("-", "_")] = v
            continue
        if re.match(r"-[^-]", arg):
            arg = arg.lstrip("-")
            last_opt = None
            if "=" in arg:
                # Only supports -f=bar, not -f bar
                opts, _, val = arg.partition("=")
                arg, last_opt = opts[:-1], opts[-1]
            options.update({k: True for k in arg})
            if last_opt:
                # Must process in order
                options[last_opt] = val
            continue
        args.append(arg)

    return main(*args, **options)
#####


###  Tests  ###
class TestSimpleCLI(unittest.TestCase):
    def test_usage(self):
        main = Mock()
        usage = Mock(return_value=0)

        r = run_main(main, ("-h",), usage=usage)
        main.assert_not_called()
        usage.assert_called_once()
        self.assertEqual(r, 0, "Should return usage return value")

        main.reset_mock()
        usage.reset_mock()

        run_main(main, ("--help",), usage=usage)
        main.assert_not_called()
        usage.assert_called_once()

        main.reset_mock()
        usage.reset_mock()

        run_main(main, ("-h",), usage=None)
        main.assert_called_once_with(h=True)
        usage.assert_not_called()

    def test_options(self):
        main = Mock(return_value=0)
        r = run_main(main, ("-f", "--bar=baz"))
        main.assert_called_once_with(f=True, bar="baz")
        self.assertEqual(r, 0, "Should return main return value")

    def test_muli_word_options(self):
        main = Mock()
        run_main(main, ("--stuff-thing", "--foo-bar=baz",))
        main.assert_called_once_with(stuff_thing=True, foo_bar="baz")

    def test_weird_characters(self):
        main = Mock()
        run_main(main, ("-?", "-b*", "-a%=wut", "--bar$=baz?", "arg1?"))
        main.assert_called_once_with('arg1?', **{"?": True, "b":True, "*": True, "a": True, "%": "wut", "bar$":"baz?"})

    def test_dash_value(self):
        main = Mock()
        run_main(main, ("-i=-", "--input=-", "--foo=-bar-",))
        main.assert_called_once_with(i='-', input='-', foo='-bar-')

    def test_args(self):
        main = Mock()
        run_main(main, ("arg1", "arg2"))
        main.assert_called_once_with("arg1", "arg2")

    def test_args_options(self):
        main = Mock()
        run_main(main, ("-f", "--bar=baz", "arg1", "arg2"))
        main.assert_called_once_with("arg1", "arg2", f=True, bar="baz")

    def test_combined(self):
        main = Mock()
        run_main(main, ["-abc"])
        main.assert_called_once_with(a=True, b=True, c=True)

    def test_negative(self):
        main = Mock()
        run_main(main, ["--no-foo"])
        main.assert_called_once_with(foo=False)

    def test_value(self):
        main = Mock()
        run_main(main, ["--foo=bar"])
        main.assert_called_once_with(foo="bar")

    def test_short_value(self):
        main = Mock()
        run_main(main, ["-f=bar"])
        main.assert_called_once_with(f="bar")

    def test_short_combined_value(self):
        main = Mock()
        run_main(main, ["-abc=bar"])
        main.assert_called_once_with(a=True, b=True, c="bar")

    def test_combined_short_last_wins(self):
        main = Mock()
        run_main(main, ["-cc=bar"])
        main.assert_called_once_with(c="bar")

    def test_options_separator(self):
        main = Mock()
        run_main(main, ["-a", "--", "-f"])
        main.assert_called_once_with("-f", a=True)


if __name__ == "__main__":
    unittest.main()
#####
