#!/usr/bin/env python3
# Copyright (c) 2019 Benjamin Holt -- MIT License

"""
State machine engine that makes minimal, but convenient, assumptions.

This is a stripped-down [Mealy](https://en.wikipedia.org/wiki/Mealy_machine) state machine engine (output depends on state and input.)  Good for writing parsers, but makes no assumptions about text parsing, and doesn't make any unnecessary assumptions about the states, tests, or actions that make up the transitions that wire up the machines it can run.
"""

from collections import deque, namedtuple
import re
#####


###  Main  ###
def main(args, env):
    "BJH: TODO: do something useful"
    pass
#####


###  State Machine  ###
TransitionInfo = namedtuple("TransitionInfo", ("state", "dst", "count", "result"),)
TraceInfo = namedtuple("TraceInfo", ("t_info", "test", "action", "tag", "out"))


class StateMachine(object):
    def __init__(self, start, tracer=True, unrecognized=True):
        """Creates a state machine in the start state with an optional unrecognized input handler and debug tracer

        If an input does not match any transition the `unrecognized` handler is called with the input, state and input count; by default this just returns `None`.

        An optional `tracer` gets called after each transition tested with the input and a `TraceInfo`.  This can be set to a `Tracer` instance for a verbose log of the operation of your state machine.
        """
        self.transitions = {start:[], None:[],}  # {state: [(test, action, dst, tag), ...], ...}
        self.state = start
        self.i_count = 0

        # Baseline to no-ops, default behavior will override
        self.tracer = tracer if callable(tracer) else lambda *_: None
        self.unrecognized = unrecognized if callable(unrecognized) else lambda *_: None
        if unrecognized is True:
            # Use default tracer and unrecognized handler
            traceDepth = 5  # Each transition prints 4-5 lines of trace
            if type(tracer) == int:  # Tricksy, but really easy to set the depth
                traceDepth = tracer
            rt = RecentTracer(sm=self, depth=traceDepth)
            self.unrecognized = rt.throw
            self.tracer = rt
            if callable(tracer):
                # If another tracer was specified, use both of them
                def both(i, t):
                    tracer(i, t)
                    rt(i, t)
                self.tracer = both


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


    def input(self, i):
        """Tests input `i` against current state's transitions, changes state, and returns the output of the first matching transition's action.

        Transitions are tested in the order they were added to their originating state and the first one with a truish result is followed.  Transitions starting from `None` are implicitly added to all states and evaluated in order after the current state's explict transitions.

        If `test` is callable, it will be called with the input and a `TransitionInfo`; a truish result will cause this transition's action to be called and the machine will go to `dst`.  If `test` is not callable will be compared against the input (`test == input`).

        If the test result is truish and `action` is callable, it will be called with the input and a `TransitionInfo` and the output will be returned.  Otherwise, the `action` itself will be returned when the transition is followed.
        """
        self.i_count += 1
        tlist = self.transitions[self.state]
        for (test, action, dst, tag) in tlist + self.transitions[None]:
            t_info = TransitionInfo(self.state, dst, self.i_count, None)
            result = test(i, t_info) if callable(test) else test == i
            t_info = t_info._replace(result=result)
            if result:
                out = action(i, t_info) if callable(action) else action
                self.tracer(i, TraceInfo(t_info, test, action, tag, out))
                if dst is not None:
                    self.state = dst
                return out
            self.tracer(i, TraceInfo(t_info, test, action, tag, None))

        return self.unrecognized(i, self.state, self.i_count)


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
def format_transition_table(sm):
    pass
#####


###  Tracing  ###
class Tracer():
    def __init__(self, printer=print):
        self.input_count = 0
        self.printer = printer


    def __call__(self, i, t):
        (t_info, test, action, tag, out) = t
        if t_info.count != self.input_count:
            # New input, start a new block, number and print it
            self.input_count = t_info.count
            self.printer("")
            self.printer(f"=====  {t_info.state}  =====")
            self.printer(f"{t_info.count}: {i}")

        # Format and print tested transition
        t_string = f"\t[{tag}] " if tag else "\t"
        t_string += f"{t_info.result} <-- ({t_info.state}, {test}, {action}, {t_info.dst})"
        self.printer(t_string)

        if t_info.result:
            # Transition fired, print state change and output
            self.printer(f"\t    {t_info.state} --> {t_info.dst}")
            self.printer(f"\t    ==> '{out}'")


class RecentTracer(object):
    def __init__(self, sm=None, depth=10):
        self.sm = sm  # The state machine (for printing the transition table if desired)
        self.buffer = deque(maxlen=depth)  # [(t_info, (loop_count, t_count, i_count)), ...]
        self.t_count = 0  # Count of tested transitions since the last one that was followed


    def __call__(self, i, t):
        (t_info, *_) = t
        self.t_count += 1
        if not t_info.result:
            return

        loop_count = 1
        if len(self.buffer):
            (_, ((s, *_), *_), (lc, *_)) = self.buffer[-1]
            if t_info.state == s and (t_info.dst is None or t_info.state == t_info.dst):
                # if the state isn't changing, bump the loop count and replace the last entry
                loop_count = lc + 1
                self.buffer.pop()

        self.buffer.append((i, t, (loop_count, self.t_count)))
        self.t_count = 0


    def throw(self, i, s, c):
        traceLines = "\n".join(self.formatTrace())
        msg = f"Unrecognized input\nStateMachine Traceback (most recent transition last):\n{traceLines}\nValueError: '{s}' did not recognize {c}: '{i}'"
        raise ValueError(msg)


    def formatTrace(self):
        trace = []
        for (ti, (t_info, test, action, tag, out), (lc, tc)) in self.buffer:
            if lc > 1:
                trace.append(f"  ...(Looped {lc} times)")
            trace.append(f"  {t_info.count}: {ti}")
            t_string = f"      ({tc} tested) "
            if tag:
                t_string += f"[{tag}] "
            t_string += f"{t_info.result} <-- ({t_info.state}, {test}, {action}, {t_info.dst})"
            trace.append(t_string)
            trace.append(f"          {t_info.state} --> {t_info.dst}\n          ==> '{out}'")
        return trace
#####


#####
if __name__ == "__main__":
    # import os, sys
    # _xit = main(sys.argv, os.environ)  # pylint: disable=invalid-name
    # sys.exit(_xit)
    pass
#####
