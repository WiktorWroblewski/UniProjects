from pyvis.network import Network


# finite-state automaton
class Fsa:
    def __init__(self, states, alphabet, delta, starting_state, final_states):
        """
        Initialize the finite-state automaton.

        :param states: A tuple of states in the automaton
        :param alphabet: A tuple of valid symbols (alphabet) for the automaton
        :param delta: A dictionary representing the transition function, where
                      the key is a (current_state, symbol) tuple, and the value
                      is the next state
        :param starting_state: The initial state of the automaton
        :param final_states: A tuple of states that are considered accepting states
        """

        self.states = states
        self.alphabet = alphabet
        self.delta = delta
        self.starting_state = starting_state
        self.final_states = final_states

    def check_input(self, inp):
        """
        Process an input string through the automaton and determine whether it is accepted.

        :param inp: The input string to check
        """

        self.current_state = self.starting_state
        inp = str(inp)
        i = 0  # Step counter for tracing

        # Process each symbol in the input string
        for symbol in inp:
            print(f'\n-----------------------------------------------\n'
                  f'Step {i}:\n'
                  f'Current state - {self.current_state}\n'
                  f'Read symbol - {symbol}')

            # Check if the symbol is in the automaton's alphabet
            if symbol not in self.alphabet:
                print(f'Invalid symbol {symbol}\n'
                      f'-----------------------------------------------\n'
                      f'Input is NOT accepted due to an invalid symbol')
                return

            # Get the next state based on the current state and input symbol
            next_state = self.delta.get((self.current_state, symbol))
            if next_state is None:
                print(f'No transition from state {self.current_state} for symbol {symbol}\n'
                      f'-----------------------------------------------\n'
                      f'Input is NOT accepted due to a missing transition.')
                return


            print(f'transition to - {next_state}\n'
                  f'-----------------------------------------------')

            i += 1
            self.current_state = next_state

        result = f'Input \'{inp}\' is accepted by the automaton.\n' if self.current_state in self.final_states\
            else f'Input \'{inp}\' is NOT accepted by the automaton.\n'
        print(result)

    def draw(self):
        """
        Visualize the automaton as a directed graph using PyVis and save the graph to an HTML file.
        """

        G = Network(directed=True)

        for state in self.states:
            color = 'blue'
            if state in self.final_states:
                color = 'green'
            G.add_node(state, shape='circle', color=color)

        # Construct labels for transitions between states
        labels = {}
        for (source, symbol), dest in self.delta.items():
            if (source, dest) not in labels:
                labels[(source, dest)] = []
            labels[(source, dest)].append(symbol)

        # Add edges to the graph with corresponding labels
        for (source, dest), symbols in labels.items():
            temp = ''.join(symbols)  # Combine symbols for the same transition
            G.add_edge(source, dest, label=temp)

        G.write_html("graph.html")


# Example usage of the finite-state automaton:
states = ('q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6')
alphabet = ('a', 'b', 'c')
delta = {
        ('q0', 'a'): 'q2',
        ('q0', 'b'): 'q2',
        ('q0', 'c'): 'q2',
        ('q2', 'a'): 'q1',
        ('q2', 'b'): 'q1',
        ('q2', 'c'): 'q6',
        ('q1', 'a'): 'q4',
        ('q1', 'b'): 'q0',
        ('q1', 'c'): 'q3',
        ('q3', 'a'): 'q3',
        ('q3', 'b'): 'q3',
        ('q3', 'c'): 'q3',
        ('q4', 'a'): 'q0',
        ('q4', 'b'): 'q5',
        ('q4', 'c'): 'q5',
        ('q5', 'a'): 'q4',
        ('q5', 'b'): 'q4',
        ('q5', 'c'): 'q4',
        ('q6', 'a'): 'q3',
        ('q6', 'b'): 'q3',
        ('q6', 'c'): 'q3'
}
starting_state = 'q0'
final_states = ('q0', 'q4', 'q5')

automaton = Fsa(states, alphabet, delta, starting_state, final_states)
automaton.check_input('abc')
automaton.check_input('123')
automaton.check_input('cba')
automaton.draw()
