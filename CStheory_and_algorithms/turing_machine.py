class Turing():
    def __init__(self, states, tape_alphabet, input_alphabet, delta, starting_state, accepting_states, rejecting_states):
        """
        Initialize the Turing machine.

        :param states: A list of states in the Turing machine
        :param tape_alphabet: A list of valid symbols for the tape alphabet
        :param input_alphabet: A list of valid symbols for the input alphabet
        :param delta: A dictionary representing the transition function, where the key is
                      the current state and symbol, and the value is a tuple (next_state,
                      write_symbol, move_direction)
        :param starting_state: The initial state of the Turing machine
        :param accepting_states: A tuple of states that are considered accepting states
        :param rejecting_states: A tuple of states that are considered rejecting states
        """

        self.states = states
        self.tape_alphabet = tape_alphabet
        self.input_alphabet = input_alphabet
        self.delta = delta
        self.starting_state = starting_state
        self.accepting_states = accepting_states
        self.rejecting_states = rejecting_states

    def print_state(self):
        """
        Print the current state of the Turing machine.
        """

        print(f'Current state - {self.current_state}\n'
              f'Current symbol - {self.current_symbol}\n'
              f'Transition - {self.transition}')
        print(self.head)
        print(self.tape, '\n')

    def check_input(self, input):
        """
        Process the input string through the Turing machine and determine whether
        the input is accepted or rejected.

        :param input: The input string to process
        """

        input = str(input)
        self.current_state = self.starting_state
        self.tape = ['_' for i in range(1000)]  # Initialize the tape with blanks ('_')
        self.head = ['_' for i in range(1000)]  # Initialize the head position indicator
        self.head[0] = '^'  # Set the initial head position to the first cell
        self.head_ind = 0  # Set the initial head index to the start of the tape

        # Load the input onto the tape
        for symbol in input:
            self.tape[self.head_ind] = symbol
            self.head_ind += 1
        self.head_ind = 0

        # Main loop to process the input until an accepting or rejecting state is reached
        while self.current_state not in (self.accepting_states or self.rejecting_states):
            self.current_symbol = self.tape[self.head_ind]  # Read the current symbol under the head

            # Check if the symbol is valid in the tape alphabet
            if self.current_symbol not in self.tape_alphabet:
                print(f'\nInput is NOT accepted due to an invalid symbol - {self.current_symbol}')
                return

            # Try to fetch the transition for the current state and symbol
            try:
                self.transition = self.delta[self.current_state][self.current_symbol]
            except KeyError:
                print(f'\nInput is NOT accepted because no transition is defined from state - '
                      f'{self.current_state}, for symbol - {self.current_symbol}')
                return

            # If no transition is found, reject the input
            if self.transition is None:
                print(f'\nInput is NOT accepted because no transition is defined from state - '
                      f'{self.current_state}, for symbol - {self.current_symbol}')
                return

            self.print_state()

            # Update the head position and write the symbol on the tape
            self.head[self.head_ind] = '_'
            self.tape[self.head_ind] = self.transition[1]
            # Move the head left or right based on the transition direction ('R' or 'L')
            self.head_ind += 1 if self.transition[2] == 'R' else -1
            # if self.head_ind < 0:
            #     self.head_ind = 0
            self.head[self.head_ind] = '^'
            # Update the current state to the next state from the transition
            self.current_state = self.transition[0]

        result = f'Input \'{input}\' is accepted by the Turing machine.\n' if self.current_state in self.accepting_states \
            else f'Input \'{input}\' is NOT accepted by the Turing machine.\n'
        print(result)


# Example usage of the Turing machine:
states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
input_alphabet = ['0', '1', '_']
tape_alphabet = ['0', '1', '_']
delta = {
    'qs': {'_': ('q0', '_', 'R')},

    'q0': {'0': ('q0', '0', 'R'), '1': ('q0', '1', 'R'), '_': ('q1', '_', 'R')},

    'q1': {'0': ('q1', '0', 'R'), '1': ('q1', '1', 'R'), '_': ('q2', '_', 'L')},

    'q2': {'0': ('q2', '1', 'L'), '1': ('q3', '0', 'L'), '_': ('q5', '_', 'R')},

    'q3': {'0': ('q3', '0', 'L'), '1': ('q3', '1', 'L'), '_': ('q4', '_', 'L')},

    'q4': {'0': ('q0', '1', 'R'), '1': ('q4', '0', 'L'), '_': ('q0', '1', 'R')},

    'q5': {'1': ('q5', '_', 'R'), '_': ('q6', '_', 'R')},

    'q6': {'_': ('q6', '_', 'R')}
}
starting_state = ('qs')
accepting_states = ('q6')
rejecting_states = ()

# The Turing machine performs binary summation. The input format is:
# _(first binary number)_(second binary number), for example:
# _101_10 is correct
# 101_10 is not correct
# source for this tm - https://stackoverflow.com/questions/59045832/turing-machine-for-addition-and-comparison-of-binary-numbers

tm = Turing(states, tape_alphabet, input_alphabet, delta, starting_state, accepting_states, rejecting_states)
tm.check_input('_10101_1101')  # 21 + 13 = 34
tm.check_input('_10_1')  # 2 + 1 = 3
tm.check_input('10_1')  # invalid input
tm.check_input('abc')  # invalid symbols
