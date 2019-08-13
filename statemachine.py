#!/usr/bin/env python3
# Copyright (c) 2019 Benjamin Holt -- MIT License

"""
State machine engine that makes minimal, but convenient, assumptions.

This is a stripped-down [Mealy](https://en.wikipedia.org/wiki/Mealy_machine) state machine engine (output depends on state and input.)  Good for writing parsers, but makes no assumptions about text parsing, and doesn't make any unnecessary assumptions about the states, tests, or actions that make up the transitions that wire up the machines it can run.
"""

import re
#####


###  Main  ###
def main(args, env):
    "BJH: TODO: do something useful"
    pass
#####


###  State Machine  ###
class StateMachine(object):
    def __init__(self, start, unrecognized=lambda s,i: None, tracer=None):
        """Creates a state machine in the start state with an optional unrecognized input handler and debug tracer

        If an input does not match any transition the `unrecognized` handler is called with the state and input; by default this just returns `None`.

        An optional `tracer` gets called after each transition's test with `(state, i, test, result, action, dst, tag)`; this can be set to `printTrace` for a verbose log of the operation of your state machine.
        """
        self.transitions = {start:[], None:[],}  # {state: [(test, action, dst, tag), ...], ...}
        self.state = start
        self.unrecognized = unrecognized
        self.tracer = tracer


    def add(self, state, test, action, dst, tag=None):
        """Add transition from `state` to `dst` with `test`, `action`, and optional debugging `tag`.  Transitions will be tested in the order they added.

        `state` and `dst` must be hashable and are automatically added.  If `state` is `None`, this transition will be implictly added to all states, and evaluated after any explict transitions.  If `dst` is `None`, the machine will remain in the same state (self-transition).

        If `test` is callable, it will be called as described below, otherwise it will be compared against the input (`test == input`)

        If `action` is callable, it will be called as described below, otherwise it will be returned when the transition is followed.
        """
        if state not in self.transitions:
            self.transitions[state] = []
        if dst not in self.transitions:
            self.transitions[dst] = []
        self.transitions[state].append((test, action, dst, tag))  # BJH: auto-tag "global" transitions?


    # BJH: is an 'action' decorator useful?
    # def action(self, state, test, dst, tag=None):
    #     def decor(f):
    #         self.add(state, test, f, dst, tag)
    #         return f  # HACK: don't actually decorate f, just attach to the state machine
    #     return decor


    def input(self, i):
        """Tests input `i` against current state's transitions, changes state, and returns the output of the first matching transition's action.

        Transitions are tested in the order they were added to their originating state and the first one with a truish result is followed.  Transitions starting from `None` are implicitly added to all states and evaluated in order after the current state's explict transitions.

        If `test` is callable, it will be called with the input and an `info` tuple containing `(state, dst)`; a truish result will cause this transition's action to be called and the machine will go to `dst`.  If `test` is not callable will be compared against the input (`test == input`).

        If the test result is truish and `action` is callable, it will be called with the input and an `info` tuple containing `(state, result, dst)` and the output will be returned.  Otherwise, the `action` itself will be returned when the transition is followed.
        """
        tlist = self.transitions[self.state]
        for (test, action, dst, tag) in tlist + self.transitions[None]:
            result = test(i, (self.state, dst)) if callable(test) else test == i
            if self.tracer:
                self.tracer(self.state, i, test, result, action, dst, tag)
            if result:
                out = action(i, (self.state, result, dst)) if callable(action) else action
                if dst is not None:
                    self.state = dst
                return out
        return self.unrecognized(self.state, i)


    def parse(self, inputs):
        "Feeds items from the `inputs` iterable into the state machine and yields truish outputs"
        for i in inputs:
            out = self.input(i)
            if out:
                yield out
#####


###  Tests  ###
def trueTest(i, _):
    "Always returns `True`"
    return True


def inTest(l):
    "Creates a test closure that returns true if an input is in `l`"
    def t(i, _):
        return i in l
    return t


def matchTest(pattern):
    "Creates a test closure that returns true if an input matches `pattern` using `re.match`"
    r = re.compile(pattern)
    def t(i, _):
        return r.match(i)
    return t
#####


###  Actions  ###
def inputAction(i, _):
    """Returns the input that matched this transition"""
    return i
#####


###  Utilities  ###
def printTrace(state, i, test, result, action, dst, tag):
    label = f"{tag}:" if tag else ''
    if result:
        print(f"T:{state}->{dst}: {label}(input:{i}, test:{test}, result:{result}, {action})")
    else:
        print(f"T:\t{label}({state}, input:{i}, test:{test}, result:{result}, {dst})")
#####


#####
if __name__ == "__main__":
    # import os, sys
    # _xit = main(sys.argv, os.environ)  # pylint: disable=invalid-name
    # sys.exit(_xit)
    pass
#####
