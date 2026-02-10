from automata import run_dfa, run_nfa, nfa_to_dfa

ALPHABET = {'a', 'b'}

# --------------------
# DFA definition
# --------------------
DFA_TRANS = {
    'q0': {'a': 'q1', 'b': 'q0'},
    'q1': {'a': 'q1', 'b': 'q2'},
    'q2': {'a': 'q1', 'b': 'q3'},
    'q3': {'a': 'q1', 'b': 'q0'},
}
DFA_START = 'q0'
DFA_ACCEPT = {'q3'}

# --------------------
# NFA definition
# --------------------
NFA_TRANS = {
    'n0': {'a': {'n0', 'n1'}, 'b': {'n0'}},
    'n1': {'b': {'n2'}},
    'n2': {'b': {'n3'}},
}
EPS = {}  # epsilon transitions empty here
NFA_START = {'n0'}
NFA_ACCEPT = {'n3'}

TESTS = ["", "abb", "aabb", "ab", "babb", "abba", "bbbbabb", "aaabbb", "bab", "bb", "a", "baabb"]

def header(t):
    print("\n" + "=" * len(t))
    print(t)
    print("=" * len(t))

def main():
    # 1) DFA tests
    header("Part 1: DFA tests")
    for s in TESTS:
        ok = run_dfa(DFA_TRANS, DFA_START, DFA_ACCEPT, s, ALPHABET)
        print(f"DFA input={s!r:10s} accepted={ok}")

    # 2) NFA tests with trace for selected strings
    header("Part 2: NFA tests (with trace)")
    for s in ["abb", "abba", "babb"]:
        ok, trace = run_nfa(NFA_TRANS, EPS, NFA_START, NFA_ACCEPT, s, ALPHABET)
        print(f"\nNFA input={s!r} accepted={ok}")
        for label, states in trace:
            print(f"  {label:20s} -> {sorted(states)}")

    # 3) Build DFA from NFA
    header("Part 3: Build DFA from NFA (subset construction)")
    dfa2_trans, dfa2_start, dfa2_accept = nfa_to_dfa(NFA_TRANS, EPS, NFA_START, NFA_ACCEPT, ALPHABET)
    print(f"Constructed DFA start: {sorted(dfa2_start)}")
    print(f"Constructed DFA #states: {len(dfa2_trans)}")

    # 4) Equivalence check
    header("Part 4: Equivalence check (DFA vs DFA-from-NFA vs NFA)")
    all_match = True
    for s in TESTS:
        d1 = run_dfa(DFA_TRANS, DFA_START, DFA_ACCEPT, s, ALPHABET)
        d2 = run_dfa(dfa2_trans, dfa2_start, dfa2_accept, s, ALPHABET)
        n_ok, _ = run_nfa(NFA_TRANS, EPS, NFA_START, NFA_ACCEPT, s, ALPHABET)
        match = (d1 == d2 == n_ok)
        if not match:
            all_match = False
        print(f"input={s!r:10s} DFA={d1} DFA_from_NFA={d2} NFA={n_ok} match={match}")

    print("\nALL TESTS MATCHED" if all_match else "\nMISMATCH FOUND - debug your code")

if __name__ == "__main__":
    main()
