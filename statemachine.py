#!/usr/bin/env python3
# Copyright (c) 2019 Benjamin Holt -- MIT License

"""General-purpose state machine engine with extras and tracing."""


from collections import deque, namedtuple
import re
#####


###  State Machine  ###
TransitionInfo = namedtuple("TransitionInfo", ("state", "dst", "count", "result"),)
TraceInfo = namedtuple("TraceInfo", ("t_info", "test", "action", "tag", "out", "end"))


class StateMachine(object):
    """State machine engine that makes minimal, but convenient, assumptions.

    This is a stripped-down [Mealy](https://en.wikipedia.org/wiki/Mealy_machine) (output depends on state and input) state machine engine.  Good for writing parsers, but makes no assumptions about text parsing, and doesn't make any unnecessary assumptions about the states, tests, or actions that make up the transitions that wire up the machines it can run.
    """
    def __init__(self, start, tracer=True, unrecognized=True):
        """Creates a state machine in the start state with an optional tracer and unrecognized input handler.

        An optional `tracer` gets called after each transition tested with the input and a `TraceInfo`.  By default, this uses `RecentTracer` to collect the last five significant transitions (self-transitions are counted but only the last of them is kept) to be raised by the default `unrecognized` handler.  An integer can be passed to set the trace depth.  This can be set to another callable, such as a `Tracer` instance, for a complete, quite verbose, log of the operation of your state machine; the recent trace will still be collected if the default unrecognized handler is being used.

        If an input does not match any transition the `unrecognized` handler is called with the input, state and input count.  By default this raises a `ValueError` with a short trace of recent transitions.  It can be set to `False` to disable the default tracing and ignore unrecognized input.
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
            rt = RecentTracer(depth=traceDepth)
            self.unrecognized = rt.throw
            self.tracer = rt
            if callable(tracer):
                # If another tracer was specified, use both of them
                def both(i, t):
                    tracer(i, t)
                    rt(i, t)
                self.tracer = both


    def add(self, state, test, dst, action=None, tag=None):
        """Add transition from `state` to `dst` with `test`, `action`, and optional debugging `tag`.  Transitions will be tested in the order they added.

        `state` and `dst` must be hashable and are automatically added.  If `state` is `None`, this transition will be implictly added to all states, and evaluated after any explict transitions.  If `dst` is `None`, the machine will remain in the same state (self-transition or the action could directly set a dynamic state).

        If `test` is callable, it will be called as described below, otherwise it will be compared against the input (`test == input`)

        If `action` is callable, it will be called as described below, otherwise it will be returned when the transition is followed.
        """
        if state not in self.transitions:
            self.transitions[state] = []
        if dst not in self.transitions:
            self.transitions[dst] = []
        self.transitions[state].append((test, dst, action, tag))  # REM: auto-tag "global" transitions?


    def input(self, i):
        """Tests input `i` against current state's transitions, changes state, and returns the output of the first matching transition's action.

        Transitions are tested in the order they were added to their originating state and the first one with a truish result is followed.  Transitions starting from `None` are implicitly added to all states and evaluated in order after the current state's explict transitions.

        If `test` is callable, it will be called with the input and a `TransitionInfo`; a truish result will cause the machine will go to `dst` and this transition's action to be called.  If `test` is not callable will be compared against the input (`test == input`).

        If the test result is truish and `action` is callable, it will be called with the input and a `TransitionInfo` and the output will be returned.  Otherwise, the `action` itself will be returned when the transition is followed.
        """
        self.i_count += 1
        tlist = self.transitions.get(self.state, [])
        for (test, dst, action, tag) in tlist + self.transitions[None]:
            t_info = TransitionInfo(self.state, dst, self.i_count, None)
            result = test(i, t_info) if callable(test) else test == i
            t_info = t_info._replace(result=result)
            if result:
                if dst is not None:
                    self.state = dst
                # Run the action after the state change so it could override the end state (e.g. pop state from a stack)
                out = action(i, t_info) if callable(action) else action
                # Be sure to trace the actual end state after `action` is done
                self.tracer(i, TraceInfo(t_info, test, action, tag, out, self.state))
                return out
            self.tracer(i, TraceInfo(t_info, test, action, tag, None, self.state))

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
    def c(i, _):
        return i in l
    return c


def anyTest(l):
    "Creates a test closure that returns the first truish result of the tests in `l`"
    def c(i, t):
        for test in l:
            r = test(i, t)
            if r:
                return r
        return False
    return c


def matchTest(pattern):
    "Creates a test closure that returns true if an input matches `pattern` using `re.match`"
    r = re.compile(pattern)
    def c(i, _):
        return r.match(i)
    return c
#####


###  Actions  ###
def inputAction(i, _):
    """Returns the input that matched the transition"""
    return i
#####


###  Utilities  ###
def format_transition_table(sm):
    """TODO: impliment this"""
    pass
#####


###  Tracing  ###
class Tracer():
    """Collects a trace of state machine transitions (or not) by input."""
    def __init__(self, printer=print):
        """Creates a Tracer instance with a `printer` callback for lines of trace output.

        The instance is callable and can be used directly as the `tracer` callback of a `StateMachine`.  The `printer` is expected to add newlines or otherwise separate each line output; a prefix can be added to each line like this: `printer=lambda s: print(f"T: {s}")`"""
        self.input_count = 0
        self.printer = printer


    def __call__(self, i, t):
        """Processes a tracer callback from a `StateMachine` instance, pushing each line of output to the `printer` callback."""
        (t_info, test, action, tag, out, end) = t
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
            self.printer(f"\t    {t_info.state} --> {end}")
            self.printer(f"\t    ==> '{out}'")


class RecentTracer(object):
    """Keeps a limited trace of significant state machine transitions to provide a recent "traceback" particularly for understanding unrecognized input.

    Only "successful" transitions are recorded, and if a transition stays in the same state, those are counted but only the last is retained."""
    def __init__(self, depth=10):
        """Creates a RecentTracer instance with trace depth.

        The instance is callable and can be used directly as the `tracer` callback of a `StateMachine`, likewise the `throw` method can be used as the `unrecognized` callback (and both are used default)."""
        self.buffer = deque(maxlen=depth)  # [(t_info, (loop_count, t_count, i_count)), ...]
        self.t_count = 0  # Count of tested transitions since the last one that was followed


    def __call__(self, i, t):
        """Processes a tracer callback from a `StateMachine` instance."""
        (t_info, *_) = t
        self.t_count += 1
        if not t_info.result:
            return

        loop_count = 1
        if len(self.buffer):
            (_, ((s, *_), *_), (lc, *_)) = self.buffer[-1]  # FIXME: this kind of unpacking is out of control
            if t_info.state == s and (t_info.state == t.end):
                # if the state isn't changing, bump the loop count and replace the last entry
                loop_count = lc + 1
                self.buffer.pop()

        self.buffer.append((i, t, (loop_count, self.t_count)))
        self.t_count = 0


    def throw(self, i, s, c):
        """Raises a `ValueError` for an unrecognized input to a `StateMachine` with a trace of that machine's recent significant transitions."""
        traceLines = "\n".join(self.formatTrace())
        msg = f"Unrecognized input\nStateMachine Traceback (most recent transition last):\n{traceLines}\nValueError: '{s}' did not recognize {c}: '{i}'"
        raise ValueError(msg)


    def formatTrace(self):
        """Formats the recent significant transitions into a list of lines for output."""
        trace = []
        for (ti, (t_info, test, action, tag, out, end), (lc, tc)) in self.buffer:  # FIXME: this kind of unpacking is out of control
            if lc > 1:
                trace.append(f"  ...(Looped {lc} times)")
            trace.append(f"  {t_info.count}: {ti}")
            t_string = f"      ({tc} tested) "
            if tag:
                t_string += f"[{tag}] "
            t_string += f"{t_info.result} <-- ({t_info.state}, {test}, {action}, {t_info.dst})"
            trace.append(t_string)
            trace.append(f"          {t_info.state} --> {end}\n          ==> '{out}'")
        return trace
#####


###  Main  ###
if __name__ == "__main__":
    import random

    def adlib(x):
        "Dynamically assemble messages from nested collections of parts.  Tuples are pieces to be strung together, lists are variants to choose among; anything else is used as a string"
        if type(x) is tuple:
            return "".join([ adlib(i) for i in x ])  # Joining with "|" can be helpful to see how messages get put together
        if type(x) is list:
            return adlib(random.choice(x))
        return str(x)

    (above, below) = ("above", "below")
    messages = {
        above: ("You are on the deck of a small sailboat on a ", ["calm", "serene", "blue", "clear", "glistening",], " sea; a hatch leads below."),
        below: ("You are in the ", ["cozy", "homey", "snug",], " cabin of a small boat, just enough room for a bunk and a tiny desk with a logbook; a hatch leads up."),
        "sail": ("You ", ["set", "adjust", "tack",], " your sail ", ["to", "toward", "for"], " {}."),
        "sleep": ("The bunk is ", ["soft", "comfortable", "warm", "cozy",], " and you ", ["rest", "sleep", "snooze", "nap", "doze",], " ", ["well", "deeply", "blissfully", "nicely"], "."),
        "log": [("Weather was ", ["fair", "good", "lovely",], "."),
            (["Good", "Quick", "Slow",], " sailing ", ["today", ("this ", ["morning", "afternoon", "evening",])], "."),
        ],
    }

    def lookAction(i, t):
        s = t.dst if t.dst is not None else t.state
        return adlib(messages[s])

    def sailAction(i, t):
        s = input("Where to? > ")
        return adlib(messages["sail"]).format(s)

    log_entries = [(["Fair", "Nice", "Brisk",], " weather."),]  # Put one bogus entry in 'cos choose can't take an empty array
    def writeAction(*_):
        s = input("What do you want to say? > ")
        log_entries.append(s)
        return "Written"

    world = StateMachine("start")
    # world = StateMachine("start", tracer=20)  # Keep a much deeper trace
    # world = StateMachine("start", tracer=Tracer(printer=lambda s: print(f"T: {s}")))  # Complete tracer with prefix
    world.add("start", trueTest, above, lookAction, tag="Start")
    world.add(above, inTest(["d", "down", "below",]), below, lookAction, tag="Go below")
    world.add(above, inTest(["s", "sail",]), None, sailAction, tag="Sail")

    world.add(below, inTest(["u", "up", "above",]), above, lookAction, tag="Go above")
    world.add(below, inTest(["r", "read", "read logbook",]), None, lambda *_: adlib([messages["log"], log_entries]), tag="Read")
    world.add(below, inTest(["w", "write", "log",]), None, writeAction, tag="Write")
    world.add(below, inTest(["s", "sleep", "bunk", "lie down", "lay down", "nap",]), None, lambda *_: adlib(messages["sleep"]), tag="Sleep")

    world.add(None, inTest(["l", "look",]), None, lookAction, tag="Look")
    world.add(None, lambda i,_: i != "crash", None, "Sorry, you can't do that.", tag="Not crash")  # You can type "crash" to dump the state machine's trace

    print("Smooth Sailing")
    print("Press enter to start.")
    while True:
        out = world.input(input("> "))
        if out:
            print(out)

#####
