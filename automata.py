Executable Automata: DFA, NFA, epsilon-closure, and subset construction (NFA -> DFA).

Implements the exact functions required by the Week 3 Group Coding Exercise.
"""

from collections import deque


def run_dfa(transitions, start_state, accepting_states, s, alphabet):
    """Execute a DFA.

    transitions[state][symbol] = next_state

    Returns True if accepted, else False.
    """

    # 1) Reject invalid symbols
    for ch in s:
        if ch not in alphabet:
            return False

    # 2) Start at start_state
    state = start_state

    # 3) Walk through the string
    for ch in s:
        state = transitions[state][ch]

    # 4) Accept if final state is accepting
    return state in accepting_states


def epsilon_closure(states, eps):
    """Return epsilon-closure of a set of states.

    states: a set of states
    eps: dict mapping state -> set of epsilon-next-states

    Return all states reachable from 'states' using ONLY epsilon moves.
    """
    stack = list(states)
    closure = set(states)

    while stack:
        s = stack.pop()
        for t in eps.get(s, set()):
            if t not in closure:
                closure.add(t)
                stack.append(t)

    return closure


def run_nfa(nfa, eps, start_states, accepting_states, s, alphabet):
    """Execute an NFA (with trace).

    nfa[state][symbol] = set(next_states)
    eps[state] = set(epsilon_next_states)

    Returns (accepted, trace)
    trace is a list of (label, active_states_set)
    """

    # 1) Reject invalid symbols
    for ch in s:
        if ch not in alphabet:
            return (False, [])

    # 2) Start from epsilon-closure of start states
    active = epsilon_closure(set(start_states), eps)
    trace = [("start", set(active))]

    # 3) Process each symbol
    for i, ch in enumerate(s):
        next_states = set()

        # Move from each active state on symbol ch
        for st in active:
            for t in nfa.get(st, {}).get(ch, set()):
                next_states.add(t)

        # Apply epsilon closure after consuming symbol
        active = epsilon_closure(next_states, eps)
        trace.append((f"after '{ch}' at pos {i}", set(active)))

    # 4) Accept if ANY active state is accepting
    accepted = any(st in accepting_states for st in active)
    return (accepted, trace)


def nfa_to_dfa(nfa, eps, start_states, accepting_states, alphabet):
    """Convert NFA to DFA using subset construction.

    Returns (dfa_transitions, dfa_start, dfa_accepting)

    dfa_state is a frozenset of NFA states.
    dfa_transitions[dfa_state][symbol] = next_dfa_state
    """

    start = frozenset(epsilon_closure(set(start_states), eps))

    queue = deque([start])
    seen = {start}

    dfa_transitions = {}
    dfa_accepting = set()

    while queue:
        dfa_state = queue.popleft()
        dfa_transitions[dfa_state] = {}

        # Accepting if it contains at least one NFA accepting state
        if any(st in accepting_states for st in dfa_state):
            dfa_accepting.add(dfa_state)

        for ch in alphabet:
            next_states = set()

            # union transitions from each NFA state in this subset
            for nfa_state in dfa_state:
                next_states |= nfa.get(nfa_state, {}).get(ch, set())

            next_closure = frozenset(epsilon_closure(next_states, eps))
            dfa_transitions[dfa_state][ch] = next_closure

            if next_closure not in seen:
                seen.add(next_closure)
                queue.append(next_closure)

    return (dfa_transitions, start, dfa_accepting)
