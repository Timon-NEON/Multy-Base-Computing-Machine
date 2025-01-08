import unittest

from MultyNumberMachine import *

NS = 25
word = 65
memory_size= 200
instruction_stack_size= 300

class Test(unittest.TestCase):
    NS = NS
    word = word
    memory_size = memory_size
    instruction_stack_size = instruction_stack_size
    UI = UI(NS=NS, word=word, memory_size=memory_size, instruction_stack_size=instruction_stack_size)
    machine = UI.machine
    comm = machine.const['alu']
    reserved = machine.const['mem']['reserved']
    word_size = machine.const['main']['word']['size']
    param = [NS, UI.machine.const['main']['word']['size']]

    def get_word(self, word: int, public_memory: bool = False) -> Number:
        if public_memory: word += self.machine.const['mem']['reserved']
        numb = Number(self.param)
        for it in range(self.word_size):
            numb.append(self.machine.MB.read(Unit(self.param, word * self.word_size + it)).val)
        return (numb.val)

    def show_memory(self, instr=False):
        if instr:
            word_size = self.machine.const['instr']['word']['size']
            Block = self.machine.IB
        else:
            word_size = self.word_size
            Block = self.machine.MB

        for i in range(self.UI.machine.const['mem']['reserved'] + 10):
            if i == self.UI.machine.const['mem']['reserved']:
                print()
            print(i, '|', end=' ', sep='')
            for j in range(word_size):
                print(Block.read(Unit(self.param, i * word_size + j)).val, end=' ')
            print()
        print()
        print()

    def clear_machine(self):
        for i in range(self.machine.MB.memory_size):
            self.machine.MB.update(Unit(self.param, i), Number(self.param))


    def execute(self):
        self.UI.execute()

    def test_load_n_storage_n_logic_n_incr(self):
        self.clear_machine()
        print('test_load_n_storage_n_logic_n_incr')
        n1, n2, n3, n4 = 1, 27, 88, 203
        print(self.NS ** self.machine.const['main']['word']['size'])
        res1 = (max(min(n1, n2), n3) + n4) % (self.NS ** self.machine.const['main']['word']['size'])
        print(res1)
        self.UI.add_instruction(1, self.comm['load'], n1)
        self.UI.add_instruction(0, self.comm['store'], 0)
        self.UI.add_instruction(1, self.comm['load'], n2 - 1)
        self.UI.add_instruction(0, self.comm['store'], 1)
        self.UI.add_instruction(0, self.comm['incr'], 1)
        self.UI.add_instruction(1, self.comm['load'], n3)
        self.UI.add_instruction(0, self.comm['store'], 2)
        self.UI.add_instruction(1, self.comm['load'], n4)
        self.UI.add_instruction(0, self.comm['store'], 3)
        self.UI.add_instruction(0, self.comm['load'], 0)
        self.UI.add_instruction(0, self.comm['min'], 1)
        self.UI.add_instruction(0, self.comm['max'], 2)
        self.UI.add_instruction(0, self.comm['add'], 3)
        self.UI.execute()
        self.show_memory()
        self.show_memory(True)
        res2 = self.get_word(0)
        self.assertEqual(res1, res2)



    def test_addition(self):
        self.clear_machine()
        print('test_addition')
        n1, n2, n3 = 13, 300, 200
        res1 = (n1 + n2 + n3) % self.machine.const['main']['word']['capacity']
        print(res1)
        self.UI.add_instruction(1, self.comm['load'], n1)
        self.UI.add_instruction(0, self.comm['store'], 0)
        self.UI.add_instruction(1, self.comm['load'], n2)
        self.UI.add_instruction(0, self.comm['store'], 1)
        self.UI.add_instruction(1, self.comm['load'], n3)
        self.UI.add_instruction(0, self.comm['store'], 2)
        self.UI.add_instruction(0, self.comm['load'], 0)
        self.UI.add_instruction(0, self.comm['add'], 1)
        self.UI.add_instruction(0, self.comm['add'], 2)
        self.UI.execute()
        self.show_memory()
        res2 = self.get_word(0)
        self.assertEqual(res1, res2)

    def test_decrement(self):
        self.clear_machine()
        print('test_decrement')
        n1 = 5
        res1 = n1 - 1
        self.UI.add_instruction(1, self.comm['load'], n1)
        self.UI.add_instruction(0, self.comm['store'], 0)
        self.UI.add_instruction(0, self.comm['decr'], 0)
        self.UI.execute()
        self.show_memory()
        res2 = self.get_word(0, True)
        print(res2)
        self.assertEqual(res1, res2)

    def test_comparing(self):
        self.clear_machine()
        print('test_comparing')
        n1, n2, n3, n4 = 45, 78, 2, 45
        self.UI.add_instruction(1, self.comm['load'], n1)
        self.UI.add_instruction(0, self.comm['store'], 0)
        self.UI.add_instruction(1, self.comm['load'], n2)
        self.UI.add_instruction(0, self.comm['store'], 1)
        self.UI.add_instruction(1, self.comm['load'], n3)
        self.UI.add_instruction(0, self.comm['store'], 2)
        self.UI.add_instruction(1, self.comm['load'], n4)
        self.UI.add_instruction(0, self.comm['store'], 3)
        self.UI.add_instruction(0, self.comm['load'], 0)
        self.UI.add_instruction(0, self.comm['cmpb'], 1)
        self.UI.add_instruction(0, self.comm['store'], 4)
        self.UI.add_instruction(0, self.comm['load'], 0)
        self.UI.add_instruction(0, self.comm['cmpb'], 2)
        self.UI.add_instruction(0, self.comm['store'], 5)
        self.UI.add_instruction(0, self.comm['load'], 0)
        self.UI.add_instruction(0, self.comm['cmpb'], 3)
        self.UI.add_instruction(0, self.comm['store'], 6)
        self.UI.add_instruction(0, self.comm['load'], 0)
        self.UI.add_instruction(0, self.comm['cmps'], 1)
        self.UI.add_instruction(0, self.comm['store'], 7)
        self.UI.add_instruction(0, self.comm['load'], 0)
        self.UI.add_instruction(0, self.comm['cmps'], 2)
        self.UI.add_instruction(0, self.comm['store'], 8)
        self.UI.add_instruction(0, self.comm['load'], 0)
        self.UI.add_instruction(0, self.comm['cmps'], 3)
        self.UI.add_instruction(0, self.comm['store'], 9)
        self.UI.add_instruction(0, self.comm['load'], 0)
        self.UI.add_instruction(0, self.comm['cmpe'], 1)
        self.UI.add_instruction(0, self.comm['store'], 10)
        self.UI.add_instruction(0, self.comm['load'], 0)
        self.UI.add_instruction(0, self.comm['cmpe'], 2)
        self.UI.add_instruction(0, self.comm['store'], 11)
        self.UI.add_instruction(0, self.comm['load'], 0)
        self.UI.add_instruction(0, self.comm['cmpe'], 3)
        self.UI.add_instruction(0, self.comm['store'], 12)

        self.UI.execute()
        self.show_memory()
        res1 = [
            n2 > n1, n3 > n1, n4 > n1,
            n2 < n1, n3 < n1, n4 < n1,
            n2 == n1, n3 == n1, n4 == n1,
        ]
        for i in range(len(res1)):
            res2 = self.get_word(4 + i, public_memory=True)
            print(res1[i])
            self.assertEqual(res1[i], res2)


    def test_next(self):
        self.clear_machine()
        print('test_next')
        n1, n2 = 1, 3
        self.UI.add_instruction(1, self.comm['load'], n1)
        self.UI.add_instruction(0, self.comm['store'], 0)
        self.UI.add_instruction(1, self.comm['load'], n2)
        self.UI.add_instruction(0, self.comm['store'], 1)
        self.UI.add_instruction(0, self.comm['next'], 0)
        self.UI.add_instruction(0, self.comm['decr'], 0)
        self.UI.add_instruction(0, self.comm['next'], 1)
        self.UI.add_instruction(0, self.comm['decr'], 1)

        self.UI.execute()
        self.show_memory()
        res1 = [
            (n1 // 2) * 2,
            (n2 // 2) * 2,
        ]
        print(res1)
        for i in range(len(res1)):
            res2 = self.get_word(i, public_memory=True)
            self.assertEqual(res1[i], res2)

    def test_goto(self):
        self.clear_machine()
        print('test_goto')
        n1 = 255
        self.UI.add_instruction(0, self.comm['incr'], 0)
        self.UI.add_instruction(1, self.comm['load'], n1)
        self.UI.add_instruction(0, self.comm['cmps'], 0)
        self.UI.add_instruction(0, self.comm['store'], 1)
        self.UI.add_instruction(0, self.comm['next'], 1)
        self.UI.add_instruction(1, self.comm['goto'], 0)

        self.UI.execute()
        self.show_memory()
        res2 = self.get_word(0, True)
        print(res2)
        print(self.get_word(0))
        self.assertEqual(n1, res2)

    def test_double_loop(self):
        self.clear_machine()
        print('test_goto')
        n1, n2 = 255, 2
        self.UI.add_instruction(0, self.comm['incr'], 0)
        self.UI.add_instruction(1, self.comm['load'], n1)
        self.UI.add_instruction(0, self.comm['cmps'], 0)
        self.UI.add_instruction(0, self.comm['store'], 2)
        self.UI.add_instruction(0, self.comm['next'], 2)
        self.UI.add_instruction(1, self.comm['goto'], 0)
        self.UI.add_instruction(0, self.comm['incr'], 1)
        self.UI.add_instruction(1, self.comm['load'], 0)
        self.UI.add_instruction(0, self.comm['store'], 0)
        self.UI.add_instruction(1, self.comm['load'], n2)
        self.UI.add_instruction(0, self.comm['cmps'], 1)
        self.UI.add_instruction(0, self.comm['store'], 2)
        self.UI.add_instruction(0, self.comm['next'], 2)
        self.UI.add_instruction(1, self.comm['goto'], 0)

        self.UI.execute()
        self.show_memory()
        res2 = self.get_word(1, True)
        print(res2)
        print(self.get_word(0))
        self.assertEqual(n2, res2)

    def test_second_type_addressing(self):
        self.clear_machine()
        print('test_second_type_addressing')
        n1, n2 = 1, 8
        self.UI.add_instruction(0, self.comm['incr'], 0)
        self.UI.add_instruction(2, self.comm['incr'], 0)
        self.UI.add_instruction(1, self.comm['load'], n2)
        self.UI.add_instruction(0, self.comm['cmps'], 0)
        self.UI.add_instruction(0, self.comm['store'], n2 + 1)
        self.UI.add_instruction(0, self.comm['next'], n2 + 1)
        self.UI.add_instruction(1, self.comm['goto'], 0)

        self.UI.execute()
        self.show_memory()
        res2 = self.get_word(n2, True)
        print(res2)
        print(self.get_word(0))
        self.assertEqual(n1, res2)

    #def test_svrt(self):
    #    self.clear_machine()
    #    print('test_svrt')
    #    n1, n2, n3 = 12, 8, 7
    #    self.UI.add_instruction(1, self.comm['load'], n1)
    #    self.UI.add_instruction(0, self.comm['store'], 0)
    #    self.UI.add_instruction(0, self.comm['svrt'], 0)
    #    self.UI.add_instruction(1, self.comm['load'], n2)
    #    self.UI.add_instruction(0, self.comm['store'], 0)
    #    self.UI.add_instruction(0, self.comm['svrt'], 0)
    #    self.UI.add_instruction(1, self.comm['svrt'], n3)
#
#
    #    self.UI.execute()
    #    self.show_memory()
    #    res2 = self.get_word(10)
    #    print(res2)
    #    self.assertEqual(n3, res2)

    def test_end(self):
        self.clear_machine()
        print('test_end')
        n1 = 1
        self.UI.add_instruction(0, self.comm['incr'], 0)
        self.UI.add_instruction(3, self.comm['end'], 0)
        self.UI.add_instruction(0, self.comm['incr'], 0)


        self.UI.execute()
        self.show_memory()
        res2 = self.get_word(0, True)
        print(res2)
        self.assertEqual(n1, res2)

if __name__ == '__main__':
    unittest.main()
