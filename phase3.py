def lambda_closure(states, transitions):
    lambda_states = set(states)
    stack = list(states)

    while stack:
        state = stack.pop()
        if state in transitions and '$' in transitions[state]:
            for lambda_state in transitions[state]['$']:
                if lambda_state not in lambda_states:
                    lambda_states.add(lambda_state)
                    stack.append(lambda_state)

    return lambda_states

def move(states, transitions, symbol):
    move_states = set()

    for state in states:
        if state in transitions and symbol in transitions[state]:
            move_states.update(transitions[state][symbol])

    return move_states

def nfa_to_dfa(nfa_states, alphabet, transitions, start_state, final_states):
    dfa_states = []
    dfa_transitions = {}
    dfa_start_state = frozenset(lambda_closure({start_state}, transitions))
    dfa_final_states = []

    stack = [dfa_start_state]
    processed_states = set()

    while stack:
        current_state = stack.pop()
        processed_states.add(frozenset(current_state))

        dfa_states.append(frozenset(current_state))

        if any(state in final_states for state in current_state):
            dfa_final_states.append(frozenset(current_state))

        for symbol in alphabet:
            move_states = move(current_state, transitions, symbol)
            lambda_states = lambda_closure(move_states, transitions)

            dfa_transitions.setdefault(frozenset(current_state), {})[symbol] = frozenset(lambda_states)

            if frozenset(lambda_states) not in processed_states:
                stack.append(frozenset(lambda_states))

    return dfa_states, alphabet, dfa_transitions, dfa_start_state, dfa_final_states




nfa_states = ['A', 'B', 'C', 'D' , 'E']
alphabet = ['a', 'b']
transitions = {
    'A': {
        'a': {'A', 'B', 'C', 'D', 'E'},
        'b': {'E', 'D'}
    },
    'B': {
        'a': {'C'},
        'b': {'E'}
    },
    'C': {
        'b': {'B'}
    },
    'D': {
        'a': {'E'},
        'b': {'D'}
    }

}
start_state = 'A'
final_states = ['E']


dfa_states, alphabet, dfa_transitions, dfa_start_state, dfa_final_states = nfa_to_dfa(nfa_states, alphabet, transitions, start_state, final_states)

# Print the resulting DFA data
print("DFA States:", dfa_states)
print("Alphabet:", alphabet)
print("DFA Transitions:", dfa_transitions)
print("DFA Start State:", dfa_start_state)
print("DFA Final States:", dfa_final_states)

def generate_strings(length, alphabet):
    # Generate all possible strings of length "length" using the characters in "alphabet"
    if length == 0:
        yield ''
    else:
        for char in alphabet:
            for string in generate_strings(length-1, alphabet):
                yield char + string

class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accepting_states = accepting_states
        self.members = []
        self.reachable_states = []

    def accept(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            if not current_state in self.reachable_states: 
                self.reachable_states.append(current_state)
            current_state = self.transitions[current_state][symbol]

        return current_state in self.accepting_states

    def Finite_Language_Members(self):
        max_length = len(self.states)
        for length in range(max_length+1):
            for string in generate_strings(length, self.alphabet):
                if self.accept(string):
                    if len(string) == 0:
                        self.members.append("lambda")
                    else:
                        self.members.append(string)
        return self.members

    def Minimizing(self):
        new_states = self.reachable_states
        new_transitions = {}
        for state in new_states:
            new_transitions[state] = {}
            for symbol in self.alphabet:
                new_transitions[state][symbol] = self.transitions[state][symbol]

        pairs = []
        for i in new_states:
            for j in new_states:
                if ((i != j) and not (j + i in pairs)):
                    pairs.append(i + j)
        marked_pairs = []
        step = 1
        while (True):
            end = 0
            
            if (step == 1):
                for pair in pairs:
                    current_state_1 = pair[0]
                    current_state_2 = pair[1]
                    if ((current_state_1 in self.accepting_states and current_state_2 not in self.accepting_states)
                            or (current_state_1 not in self.accepting_states and current_state_2 in self.accepting_states)):
                        marked_pairs.append(pair)
                        
                        end += 1
                step += 1
                
            else:
                
                for pair in pairs:
                    if (pair not in marked_pairs):
                        current_state_1 = pair[0]
                        current_state_2 = pair[1]
                        for symbol in self.alphabet:
                            next_state_1 = new_transitions[current_state_1][symbol]
                            next_state_2 = new_transitions[current_state_2][symbol]
                            next_state = next_state_1 + next_state_2
                            next_state_reverse = next_state_2 + next_state_1
                            if (next_state in marked_pairs or next_state_reverse in marked_pairs):
                                marked_pairs.append(pair)
                                end += 1
                                break
                                
            if (end == 0):
                break
            step += 1
        unmarked_pairs = list(set(pairs) - set(marked_pairs))
        if (len(unmarked_pairs) != 0):
            minimized_states = []
            for i in new_states:
                for n in range(len(unmarked_pairs)):
                    if (i in unmarked_pairs[n]):
                        break
                    if (n == (len(unmarked_pairs) - 1)):
                        minimized_states.append(i)
            unmarked_pairs.sort()
            equal_states = {}
            for pair in unmarked_pairs:
                if (equal_states != {}):
                    key = list(equal_states.keys())
                    for n in range(len(key)):
                        if (pair[0] in equal_states[key[n]]):
                            equal_states[key[n]].add(pair[1])
                            break
                        if (n == (len(key) - 1)):
                            equal_states.update({pair[0]: {pair[0], pair[1]}})
                else:
                    equal_states.update({pair[0]: {pair[0], pair[1]}})
            for keys in equal_states.keys():
                minimized_states.append(list(equal_states[keys]))
            new_accepting_states = []
            for minimized_state in minimized_states:
                if (self.start_state in minimized_state):
                    new_start_state = minimized_state
                for final in self.accepting_states:
                    if (final in minimized_state):
                        new_accepting_states.append(minimized_state)
                        break
            new_transitions_func = {}
            for state in minimized_states:
                new_value_dict = {}
                for symbol in self.alphabet:
                    simple_value = new_transitions[state[0]][symbol]
                    for destination in minimized_states:
                        if (simple_value in destination):
                            value_in_form = destination
                    new_value_dict[symbol] = value_in_form
                new_transitions_func.update({str(state): new_value_dict})
            print('---------------------------------------------')
            print('The Minimized DFA : ')
            print('States=',minimized_states)
            print('Alphabet: ',self.alphabet)
            print('Transitions: ',new_transitions)
            print('Start state: ',new_start_state)
            print('Final state: ',new_accepting_states)
        else:
            print('Your DFA is Also Minimized')

dfa = DFA(
    [
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
    ],
    ['1', '0'],
    {
        'A': {
            '0': 'D',
            '1': 'B'
        },
        'B': {
            '0': 'C',
            '1': 'F'
        },
        'C': {
            '0': 'C',
            '1': 'F'
        },
        'D': {
            '0': 'A',
            '1': 'E'
        },
        'E': {
            '0': 'C',
            '1': 'F'
        },
        'F': {
            '0': 'F',
            '1': 'F'
        },
        'G': {
            '0': 'D',
            '1': 'E'
        }
    },
    'A',
    ['C','E','B']
)

dfa.Finite_Language_Members()
dfa.Minimizing()
