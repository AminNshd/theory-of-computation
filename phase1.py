import random
from collections import deque

class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def reachable(self):
        """Return a list of all reachable states from the start state."""
        visited_states = set()
        stack = [self.start_state]

        while stack:
            state = stack.pop()
            visited_states.add(state)

            for symbol in self.alphabet:
                next_state = self._get_next_state(state, symbol)
                if next_state not in visited_states:
                    stack.append(next_state)

        return list(visited_states)

    def is_language_empty(self):
        """Check if the language accepted by the DFA is empty."""
        reachable_states = self.reachable()
        return len(set(reachable_states).intersection(set(self.accept_states))) == 0

    def is_language_infinite(self):
        visited = set()  # Set to store visited states
        # Stack to keep track of states and corresponding input
        stack = [(self.start_state, '')]

        while stack:
            current_state, input_string = stack.pop()

            # If the current state and input string combination has been visited before,
            # then the DFA is infinite
            if (current_state, input_string) in visited:
                return True

            visited.add((current_state, input_string))

            if len(input_string) >= 1000:
                # We assume that if the length of the input string exceeds a threshold (e.g., 1000),
                # then we consider the DFA as infinite to avoid potentially infinite loops.
                return True

            if current_state in self.accept_states:
                # If we reach an accepting state, we continue to the next input string
                stack.append((self.start_state, input_string))

            for symbol in self.alphabet:
                next_state = self.transitions.get((current_state, symbol))
                if next_state is not None:
                    stack.append((next_state, input_string + symbol))

        return False

    def get_language_size(self):
        language_size = 0
        visited_states = set()
        stack = [(self.start_state, '')]

        while stack:
            state, word = stack.pop()
            visited_states.add(state)

            if state in self.accept_states:
                language_size += 1

            for symbol in self.alphabet:
                next_state = self._get_next_state(state, symbol)
                if next_state not in visited_states:
                    stack.append((next_state, word + symbol))

        return language_size

    def get_language_members(self):
        language_members = []
        visited_states = set()
        stack = [(self.start_state, '')]

        while stack:
            state, word = stack.pop()
            visited_states.add(state)

            if state in self.accept_states:
                language_members.append(word)

            for symbol in self.alphabet:
                next_state = self._get_next_state(state, symbol)
                if next_state not in visited_states:
                    stack.append((next_state, word + symbol))

        return language_members

    def get_longest_string_length(self):
        visited_states = set()
        queue = deque([(self.start_state, '')])
        longest_length = 0

        while queue:
            state, word = queue.popleft()
            visited_states.add(state)

            if state in self.accept_states:
                longest_length = max(longest_length, len(word))

            for symbol in self.alphabet:
                next_state = self._get_next_state(state, symbol)
                if next_state is not None and next_state not in visited_states:
                    queue.append((next_state, word + symbol))

        if longest_length == 0:
            # If no accepting state is reached, return -1 to indicate no string is accepted
            return -1
        else:
            return longest_length

    def get_shortest_string_length(self):
        visited_states = set()
        queue = [(self.start_state, 0)]

        while queue:
            state, length = queue.pop(0)
            visited_states.add(state)

            if state in self.accept_states:
                return length

            for symbol in self.alphabet:
                next_state = self._get_next_state(state, symbol)
                if next_state is not None and next_state not in visited_states:
                    queue.append((next_state, length + 1))

        return -1

    def accepts_string(self, input_string):
        current_state = self.start_state

        for symbol in input_string:
            current_state = self._get_next_state(current_state, symbol)
            if current_state is None:
                return False

        return current_state in self.accept_states

    def get_accepting_and_rejecting_strings(self):
        accepting_strings = []
        rejecting_strings = []
        max_attempts = 1000
        attempts = 0
        longest_string_length = self.get_longest_string_length()

        while len(accepting_strings) < 2 or len(rejecting_strings) < 2:
            word = ''.join(random.choices(
                list(self.alphabet), k=longest_string_length + 1))
            if self.accepts_string(word):
                if len(accepting_strings) < 2 and word not in accepting_strings:
                    accepting_strings.append(word)
            else:
                if len(rejecting_strings) < 2 and word not in rejecting_strings:
                    rejecting_strings.append(word)

            attempts += 1
            if attempts >= max_attempts:
                break

        return accepting_strings, rejecting_strings

    def get_k_length_strings(self, k):
        k_length_strings = []
        stack = [(self.start_state, '')]

        while stack:
            state, word = stack.pop()

            if len(word) == k and state in self.accept_states:
                k_length_strings.append(word)

            if len(word) < k:
                for symbol in self.alphabet:
                    next_state = self._get_next_state(state, symbol)
                    if next_state is not None:
                        stack.append((next_state, word + symbol))

        return k_length_strings

    def count_m_length_strings(self, m):
        count = 0
        stack = [(self.start_state, '')]

        while stack:
            state, word = stack.pop()

            if len(word) == m and state in self.accept_states:
                count += 1

            if len(word) < m:
                for symbol in self.alphabet:
                    next_state = self._get_next_state(state, symbol)
                    if next_state is not None:
                        stack.append((next_state, word + symbol))

        return count

    def get_complement(self):
        complement_accept_states = [
            state for state in self.states if state not in self.accept_states]
        return DFA(self.states, self.alphabet, self.transitions, self.start_state, complement_accept_states)

    def _get_next_state(self, current_state, symbol):
        if (current_state, symbol) in self.transitions:
            return self.transitions[(current_state, symbol)]
        else:
            return None

    def __and__(self, other):
        """Compute the intersection of two DFAs."""
        intersect_states = set()
        intersect_alphabet = set(self.alphabet) & set(other.alphabet)
        intersect_transitions = {}
        intersect_accept_states = set()

        for state1 in self.states:
            for state2 in other.states:
                intersect_state = (state1, state2)
                intersect_states.add(intersect_state)

                if state1 in self.accept_states and state2 in other.accept_states:
                    intersect_accept_states.add(intersect_state)

                for symbol in intersect_alphabet:
                    next_state1 = self._get_next_state(state1, symbol)
                    next_state2 = other._get_next_state(state2, symbol)

                    if next_state1 is not None and next_state2 is not None:
                        intersect_transitions[(intersect_state, symbol)] = (
                            next_state1, next_state2)

        intersect_start_state = (self.start_state, other.start_state)
        intersect_dfa = DFA(intersect_states, intersect_alphabet,
                            intersect_transitions, intersect_start_state, intersect_accept_states)
        return intersect_dfa

    def __or__(self, other):
        """Compute the union of two DFAs."""
        union_states = set()
        union_alphabet = set(self.alphabet) | set(other.alphabet)
        union_transitions = {}
        union_accept_states = set()

        for state1 in self.states:
            for state2 in other.states:
                union_state = (state1, state2)
                union_states.add(union_state)

                if state1 in self.accept_states or state2 in other.accept_states:
                    union_accept_states.add(union_state)

                for symbol in union_alphabet:
                    next_state1 = self._get_next_state(state1, symbol)
                    next_state2 = other._get_next_state(state2, symbol)

                    if next_state1 is not None and next_state2 is not None:
                        union_transitions[(union_state, symbol)] = (
                            next_state1, next_state2)

        union_start_state = (self.start_state, other.start_state)
        union_dfa = DFA(union_states, union_alphabet,
                        union_transitions, union_start_state, union_accept_states)
        return union_dfa

    def __sub__(self, other):
        """Compute the difference of two DFAs."""
        other_complement = other.get_complement()
        difference_dfa = self & other_complement
        return difference_dfa

    def __eq__(self, other):
        """Check if two DFAs are equivalent."""
        return self.get_complement() - other == DFA(set(), self.alphabet, {}, None, set())

    def is_separated(self, other):
        """Check if two DFAs are separated."""
        return (self & other).is_language_empty()

    def print_dfa(self):
        print("States:", self.states)
        print("Alphabet:", self.alphabet)
        print("Transitions:")
        for transition, next_state in self.transitions.items():
            print(transition, "->", next_state)
        print("Start state:", self.start_state)
        print("Accept states:", self.accept_states)


def print_DFA(_dfa: DFA, input_string: str):
    # Test the DFA operations
    print("Is the language empty? ", _dfa.is_language_empty())
    is_infinite = _dfa.is_language_infinite()
    print("Is the language infinite? ", is_infinite)
    if not is_infinite:
        print("Language size: ", _dfa.get_language_size())
        print("Language members: ", _dfa.get_language_members())
    print("Longest string length: ", _dfa.get_longest_string_length()
          if not is_infinite else "inf")
    print("Shortest string length: ", _dfa.get_shortest_string_length())
    print("Does the DFA accept the input string '{}'? ".format(
        input_string), _dfa.accepts_string(input_string))
    accepting_strings, rejecting_strings = _dfa.get_accepting_and_rejecting_strings()
    print("Accepting strings: ", accepting_strings)
    print("Rejecting strings: ", rejecting_strings)
    k = 3
    print("All the {}-length strings that the DFA accepts: ".format(k),
          _dfa.get_k_length_strings(k))
    m = 2
    print("The count of all the {}-length strings that the DFA accepts: ".format(m),
          _dfa.count_m_length_strings(m))
    complement_dfa = _dfa.get_complement()
    print("\nComplement DFA:")
    print("States:", complement_dfa.states)
    print("Alphabet:", complement_dfa.alphabet)
    print("Transitions:", complement_dfa.transitions)
    print("Start State:", complement_dfa.start_state)
    print("Accept States:", complement_dfa.accept_states)
    print("--------------------------\n")


# Define the DFA parameters
states = {'A', 'B', 'C', 'E', 'F', 'G'}
alphabet = {'a', 'b'}
transitions = {
    ('A', 'a'): 'B',
    ('A', 'b'): 'C',
    ('B', 'a'): 'C',
    ('B', 'b'): 'C',
    ('C', 'a'): 'E',
    ('C', 'b'): 'G',
    ('G', 'a'): 'G',
    ('G', 'b'): 'G',
    ('E', 'a'): 'G',
    ('E', 'b'): 'F',
    ('F', 'a'): 'G',
    ('F', 'b'): 'G',
}
start_state = 'A'
accept_states = {'A' , 'B' , 'C' , 'F'}

# Create an instance of the DFA
dfa = DFA(states, alphabet, transitions, start_state, accept_states)

print_DFA(dfa, "abab")











# states = {'q0', 'q1', 'q2'}
# alphabet = {'a', 'b'}
# transitions = {('q0', 'a'): 'q1', ('q0', 'b'): 'q2',
#                ('q1', 'a'): 'q1', ('q1', 'b'): 'q2',
#                ('q2', 'a'): 'q2', ('q2', 'b'): 'q2',
#                }
# start_state = 'q0'
# accept_states = {'q1'}


# dfa2 = DFA(states, alphabet, transitions, start_state, accept_states)


# states = {'q0', 'q1', 'q2'}
# alphabet = {'a', 'b'}
# transitions = {('q0', 'a'): 'q2', ('q0', 'b'): 'q1',
#                ('q1', 'a'): 'q2', ('q1', 'b'): 'q1',
#                ('q2', 'a'): 'q2', ('q2', 'b'): 'q2',
#                }
# start_state = 'q0'
# accept_states = {'q1'}
# dfa3 = DFA(states, alphabet, transitions, start_state, accept_states)

# states = {'q0', 'q1', 'q2'}
# alphabet = {'a', 'b'}
# transitions = {('q0', 'a'): 'q2', ('q0', 'b'): 'q1',
#                ('q1', 'a'): 'q2', ('q1', 'b'): 'q1',
#                ('q2', 'a'): 'q2', ('q2', 'b'): 'q2',
#                }
# start_state = 'q0'
# accept_states = {'q1'}
# dfa4 = DFA(states, alphabet, transitions, start_state, accept_states)

#states = {'q0', 'q1'}
#alphabet = {'a', 'b'}
# transitions = {('q0', 'a'): 'q1', ('q0', 'b'): 'q0',
               #('q1', 'a'): 'q1', ('q1', 'b'): 'q0',
              # }
#start_state = 'q0'
#accept_states = {'q1'}

#dfa5 = DFA(states, alphabet, transitions, start_state, accept_states)
#print_DFA(dfa5, "aaaaaaba")

# states = {'q0', 'q1', 'q2'}
# alphabet = {'a', 'b'}
# transitions = {('q0', 'a'): 'q2', ('q0', 'b'): 'q1',
#                ('q1', 'a'): 'q1', ('q1', 'b'): 'q1',
#                ('q2', 'a'): 'q2', ('q2', 'b'): 'q2',
#                }
# start_state = 'q0'
# accept_states = {'q1'}

# dfa6 = DFA(states, alphabet, transitions, start_state, accept_states)
