import argparse

from MultyBaseComputingMachine import *

class Environment:

    def __init__(self, program_name=None, program=''):
        self.machine = None
        self.program_name = program_name
        self.read()

    def read(self):
        with open(self.program_name, "r") as program:
            setup = program.readline()
            self.create_machine(setup)
            for line in program:
                self.add_command(line)
            program.close()
        self.UI.execute()
        #self.show_memory()

    def create_machine(self, setup):
        setup_lst = list(map(int, setup.split()))
        self.UI = UI(setup_lst)
        self.machine = self.UI.machine
        self.word_size = self.machine.const['main']['word']['size']
        self.param = [self.machine.NS, self.UI.machine.const['main']['word']['size']]

    def add_command(self, line):
        command = line.split()
        if len(command) <= 0: return
        command_lst = command + ['0'] * (3 - len(command))
        self.UI.add_instruction_list([command_lst[2], command_lst[0], command_lst[1]])

    def show_memory(self, instr=False):
        if instr:
            memory_size = self.machine.instr_stack_size
            word_size = self.machine.const['instr']['word']['size']
            Block = self.machine.IB
        else:
            memory_size = self.machine.memory_size
            word_size = self.word_size
            Block = self.machine.MB

        for i in range(min(self.UI.machine.const['mem']['reserved'] + 5, memory_size)):
            if i == self.UI.machine.const['mem']['reserved']:
                print()
            print(i, '|', end=' ', sep='')
            for j in range(word_size):
                print(Block.read(Unit(self.param, i * word_size + j)).val, end=' ')
            print()
        print()
        print()






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Program name reader")
    parser.add_argument("program_name", type=str, help="Program name")
    args = parser.parse_args()
    Environment(args.program_name)