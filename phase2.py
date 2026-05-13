from collections import deque


class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accepting_states = accepting_states

    def isNull(self):
        for reachable in self.reachableStates():
            # print(reachable)
            if reachable in self.accepting_states:
                return False
        return True

    def reachableStates(self):
        visited = set(self.start_state)
        states = deque([self.start_state])
        while states:
            state = states.popleft()
            for next_state in self.transitions[state].values():
                if next_state not in visited:
                    visited.add(next_state)
                    states.append(next_state)
        return visited

    def __or__(self, other_dfa):
        return self.union(other_dfa)

    def __and__(self, other_dfa):
        return self.intersection(other_dfa)

    def __eq__(self, other_dfa):
        return self.are_equivalent(other_dfa)
    
    def __sub__(self, other_dfa):
        return self.difference(other_dfa)

    def difference(self, other_dfa):
        complement_other_dfa = other_dfa.complement()
        return self.intersection(complement_other_dfa)

    def union(self, other_dfa):
        new_states = set(self.states).union(other_dfa.states)
        new_alphabet = set(self.alphabet).union(other_dfa.alphabet)
        new_transitions = {}
        new_start_state = self.start_state
        new_accepting_states = set(self.accepting_states).union(
            other_dfa.accepting_states)

        for state in new_states:
            if state in self.states and state in other_dfa.states:
                new_transitions[state] = {
                    symbol: self.transitions[state].get(symbol, state) for symbol in new_alphabet
                }
            elif state in self.states:
                new_transitions[state] = self.transitions[state]
            else:
                new_transitions[state] = other_dfa.transitions[state]

        return DFA(new_states, new_alphabet, new_transitions, new_start_state, new_accepting_states)

    def intersection(self, other_dfa):
        new_states = set()
        new_alphabet = set(self.alphabet).intersection(other_dfa.alphabet)
        new_transitions = {}
        new_start_state = (self.start_state, other_dfa.start_state)
        new_accepting_states = set()

        stack = [(self.start_state, other_dfa.start_state)]
        while stack:
            state1, state2 = stack.pop()
            new_state = (state1, state2)
            new_states.add(new_state)

            if state1 in self.accepting_states and state2 in other_dfa.accepting_states:
                new_accepting_states.add(new_state)

            new_transitions[new_state] = {}
            for symbol in new_alphabet:
                next_state1 = self.transitions[state1].get(symbol)
                next_state2 = other_dfa.transitions[state2].get(symbol)
                if next_state1 is not None and next_state2 is not None:
                    new_transitions[new_state][symbol] = (
                        next_state1, next_state2)
                    if (next_state1, next_state2) not in new_states:
                        stack.append((next_state1, next_state2))

        return DFA(new_states, new_alphabet, new_transitions, new_start_state, new_accepting_states)

    def complement(self):
        new_states = self.states
        new_alphabet = self.alphabet
        new_transitions = self.transitions
        new_start_state = self.start_state
        new_accepting_states = new_states.difference(self.accepting_states)

        return DFA(new_states, new_alphabet, new_transitions, new_start_state, new_accepting_states)

    def are_equivalent(self, other_dfa):
        return ((self & other_dfa.complement()) | (self.complement() & other_dfa)).isNull()

    def are_disjoint(self, other_dfa):
        # Check if the intersection is empty
        intersection = self.intersection(other_dfa)
        return len([state for state in intersection.accepting_states if state in intersection.reachableStates()]) == 0
        # return not intersection.accepting_states in intersection.reachableStates()

    def run(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Invalid symbol: {symbol}")
            current_state = self.transitions[current_state][symbol]
        return current_state in self.accepting_states


    def printDFA(self):
        print("states are:        ", self.states)
        print("alphabets are:     ", self.alphabet)
        print("initial_state is:  ", self.start_state)
        print("accept_states are: ", self.accepting_states)
        print("transitions are:   ", self.transitions, "\n")



dfa1 = DFA({'0', '1'},  # states
           {'a', 'b'},  # alphabet
           {'0', '1'},  # transitions
           '0',  # initial state
           {'1'})  # accept states
dfa1_transitions = {
    '0': {'a': '0', 'b': '1'},
    '1': {'a': '0', 'b': '1'}
}
dfa1.transitions = dfa1_transitions

dfa2 = DFA({'A', 'B', 'C'},  # states
           {'a', 'b'},  # alphabet
           {'a'},  # transitions
           'A',  # initial state
           {'A' , 'B'})  # accept states
dfa2_transitions = {
    'A': {'a': 'B', 'b': 'A'},
    'B': {'a': 'C', 'b': 'A'},
    'C': {'a': 'C', 'b': 'C'}
}
dfa2.transitions = dfa2_transitions

dfa5 = DFA({'P', 'Q', 'R'},  # states
           {'a', 'b'},  # alphabet
           {'a'},  # transitions
           'P',  # initial state
           {'R'})  # accept states
dfa5_transitions = {
    'P': {'a': 'Q', 'b': 'P'},
    'Q': {'a': 'Q', 'b': 'R'},
    'R': {'a': 'Q', 'b': 'P'}
}
dfa5.transitions = dfa5_transitions

dfa3 = DFA({'0', '1', '2'},  # states
           {'a', 'b'},  # alphabet
           {'0', '1', '2'},  # transitions
           '0',  # initial state
           {'2'})  # accept states
dfa3_transitions = {
    '0': {'a': '1', 'b': '2'},
    '1': {'a': '1', 'b': '0'},
    '2': {'a': '2', 'b': '2'}
}
dfa3.transitions = dfa3_transitions


dfa4 = DFA({'0', '1'},  # states
           {'a', 'b'},  # alphabet
           {'0'},  # transitions
           '0',  # initial state
           {'1'})  # accept states
dfa4_transitions = {
    '0': {'a': '1', 'b': '0'},
    '1': {'a': '1', 'b': '1'}
}
dfa4.transitions = dfa4_transitions






# Perform union, intersection, and equivalence operations
print("Intersection of DFA2 and DFA5 is:")
(dfa2 & dfa5).printDFA()


print("Union of DFA2 and DFA5 is:")
(dfa2 | dfa5).printDFA()


print("Difference of DFA2 and DFA5 is:")
(dfa2 - dfa5).printDFA()


print("Are DFA2 and DFA5 disjoint? ", dfa2.are_disjoint(dfa5))


print("Is DFA2 equivalent to DFA5? ", dfa2 == dfa5)



