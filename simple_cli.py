#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# simple_cli: Copyright © 2025 Benjamin Holt - MIT License

import re
from typing import Callable, Dict, List, Tuple
import unittest
from unittest.mock import Mock
#####


###  Example  ###
_USAGE = f"""
Usage: {__file__} [options] [--] [args]
Options:
  -t, --test      Run tests
  -h, --help      Show this help message and exit

Prints parsed arguments and options, also runs the test suite if -t or --test is given.

This is intended as a self-hosted example of the `parse_args` command-line argument parser in this module, not as a useful program.
"""

def _usage():
    print(_USAGE)
    return 0

def _main(*args, **opts):
    print(f"{args = }")
    print(f"{opts = }")
    if opts.get("test", opts.get("t", False)):
        print("Running tests...")
        unittest.main()  # FIXME: this also tries to parse sys.argv and errors on -t
    return 0
#####


###  Run Main  ###
OptionValue = str | bool | int | float
ArgsOpts = Tuple[List[str], Dict[str, OptionValue]]
ExitCode = None | int | str

def run_main(
        arg_list: List[str],
        main: Callable[..., ExitCode],
        usage: Callable[[], ExitCode] | None = None
    ) -> ExitCode:
    """
    Parse command-line arguments and options with parse_args, then call a main function with the results; given a usage function, if -h or --help is given, call that instead.
    """
    args, opts = parse_args(arg_list)
    if usage and opts.get("help", opts.get("h", False)):
        return usage()
    return main(*args, **opts)

def parse_args(arg_list: List[str]) -> ArgsOpts:
    """
    A simple parser that translates command-line arguments and options into a Python list and dict suitable for *args and **kwargs.

    Features:
    - Parses options and arguments from a list of strings with no setup needed
    - Calls a main function, if given, and returns the exit value
    - Automatically recognizes -h / --help when given a usage function
    - Short and long boolean flags (-f / --foo)
    - Combined short flags (-abc == -a -b -c)
    - Negative flags (--foo / --no-foo)
    - Options with values (-f=bar / --foo=bar)
    - Items after arguments separator (--) are treated as arguments, not options

    Limitations:
    - Requires explicit '=' for options with values like --foo=bar; --foo bar is ambiguous without complex argument configuration
    - Does not automatically map short options to long options; use a pattern like opts.get("foo", opts.get("f", False))
    - Does not support options with multiple values like --foo=bar,baz (though "bar,baz" would come through and could be split)
    """
    args: List[str] = []
    options: Dict[str, OptionValue] = {}
    args_only = False
    for arg in arg_list:
        if args_only:
            args.append(arg)
            continue

        match arg:
            ## Separator
            case "--":
                args_only = True
            ## Long options
            case _ if re.match(r"--[^-]", arg):
                arg = arg.lstrip("-")
                v: OptionValue | None = None
                if "=" in arg:
                    k, _, v = arg.partition("=")
                else:
                    # no- --> False
                    v = not arg.startswith("no-")
                    k = arg.removeprefix("no-")
                options[k] = v
            ## Short options
            case _ if re.match(r"-[^-]", arg):
                arg = arg.lstrip("-")
                last_opt = None
                if "=" in arg:
                    opts, _, val = arg.partition("=")
                    arg, last_opt = opts[:-1], opts[-1]
                options.update({k: True for k in arg})
                if last_opt:
                    # Must process in-order
                    options[last_opt] = val
            ## Anything else is an argument
            case _:
                args.append(arg)
    return (args, options)
#####


###  Tests  ###
class TestRunMain(unittest.TestCase):
    def test_usage(self):
        main = Mock(return_value="main")
        usage = Mock(return_value="usage")

        r = run_main(("-h",), main, usage=usage)
        main.assert_not_called()
        usage.assert_called_once()
        self.assertEqual(r, "usage", "Should return usage return value")

        main.reset_mock()
        usage.reset_mock()

        run_main(("--help",), main, usage=usage)
        main.assert_not_called()
        usage.assert_called_once()

        main.reset_mock()
        usage.reset_mock()

        r = run_main(("-h",), main, usage=None)
        main.assert_called_once_with(h=True)
        usage.assert_not_called()
        self.assertEqual(r, "main", "Should return main return value")

class TestParseArgs(unittest.TestCase):
    def test_options(self):
        args, opts = parse_args(("-f", "--bar=baz"))
        self.assertEqual(args, [])
        self.assertEqual(opts, {"f": True, "bar": "baz"})

    def test_muli_word_options(self):
        args, opts = parse_args(("--stuff-thing", "--foo-bar=baz",))
        self.assertEqual(args, [])
        self.assertEqual(opts, {"stuff-thing": True, "foo-bar": "baz"})

    def test_args(self):
        args, opts = parse_args(("arg1", "arg2"))
        self.assertEqual(args, ["arg1", "arg2"])
        self.assertEqual(opts, {})

    def test_args_options(self):
        args, opts = parse_args(("-f", "--bar=baz", "arg1", "arg2"))
        self.assertEqual(args, ["arg1", "arg2"])
        self.assertEqual(opts, {"f": True, "bar": "baz"})

    def test_combined(self):
        args, opts = parse_args(["-abc"])
        self.assertEqual(args, [])
        self.assertEqual(opts, {"a": True, "b": True, "c": True})

    def test_negative(self):
        args, opts = parse_args(["--no-foo"])
        self.assertEqual(args, [])
        self.assertEqual(opts, {"foo": False})

    def test_value(self):
        args, opts = parse_args(["--foo=bar"])
        self.assertEqual(args, [])
        self.assertEqual(opts, {"foo": "bar"})

    def test_short_value(self):
        args, opts = parse_args(["-f=bar"])
        self.assertEqual(args, [])
        self.assertEqual(opts, {"f": "bar"})

    def test_short_combined_value(self):
        args, opts = parse_args(["-abc=bar"])
        self.assertEqual(args, [])
        self.assertEqual(opts, {"a": True, "b": True, "c": "bar"})

    def test_combined_short_last_wins(self):
        args, opts = parse_args(["-cc=bar"])
        self.assertEqual(args, [])
        self.assertEqual(opts, {"c": "bar"})

    def test_options_separator(self):
        args, opts = parse_args(["-a", "--", "-f"])
        self.assertEqual(args, ["-f"])
        self.assertEqual(opts, {"a": True})

    def test_weird_characters(self):
        args, opts = parse_args(("-?", "-b*", "-a%=wut", "--bar$=baz?", "arg1?"))
        self.assertEqual(args, ["arg1?"])
        self.assertEqual(opts, {"?": True, "b":True, "*": True, "a": True, "%": "wut", "bar$":"baz?"})

    def test_dash_value(self):
        args, opts = parse_args(("-i=-", "--input=-", "--foo=-bar-",))
        self.assertEqual(args, [])
        self.assertEqual(opts, {"i": "-", "input": "-", "foo": "-bar-"})
#####


###  Main  ###
if __name__ == "__main__":
    # import sys
    # xit = run_main(sys.argv[1:], _main, _usage)
    # sys.exit(xit)
    unittest.main()
#####
