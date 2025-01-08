import unittest

import binMachine as bM

class Test(unittest.TestCase):
    UI = bM.UI()
    machine = UI.machine
    comm = machine.const['alu']
    reserved = machine.const['mem']['reserved']
    unit_size = machine.const['main']['unit']['size']

    def get_byte(self, byte: int, public_memory: bool = False) -> bM.Number:
        if public_memory: byte += self.machine.const['mem']['reserved']
        numb = bM.Number()
        for it in range(self.unit_size):
            numb.append(self.machine.mem[byte * self.unit_size + it])
        return (numb.numb10())

    def process_input(self, address: int, type_addressing: int = 0) -> int:
        if (type_addressing == 1):
            return address
        result = self.get_byte(address + self.reserved)
        return result.numb10()

    def show_memory(self):
        for i in range(self.UI.machine.const['mem']['reserved'] + 10):
            if i == self.UI.machine.const['mem']['reserved']:
                print()
            print(i, '|', end=' ', sep='')
            for j in range(self.unit_size):
                print(self.machine.mem[i * self.unit_size + j], end=' ')
            print()

    def clear_machine(self):
        for i in range(len(self.machine.mem)):
            self.machine.mem[i] = 0

    # test laod code fucntion
    def execute(self):
        self.UI.execute()


    def test_load_n_storage_n_logic_n_incr(self):
        self.clear_machine()
        print('test_load_n_storage_n_logic_n_incr')
        n1, n2, n3, n4 = 156, 27, 89, 203
        res1 = (((n1 & n2) | n3) ^ n4)
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
        self.UI.add_instruction(0, self.comm['and'], 1)
        self.UI.add_instruction(0, self.comm['or'], 2)
        self.UI.add_instruction(0, self.comm['xor'], 3)
        self.UI.execute()
        self.show_memory()
        res2 = self.get_byte(0)
        self.assertEqual(res1, res2)

    def test_addition(self):
        self.clear_machine()
        print('test_addition')
        n1, n2, n3 = 13, 300, 200
        res1 = (n1 + n2 + n3) % self.machine.const['main']['unit']['capacity']
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
        res2 = self.get_byte(0)
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
        res2 = self.get_byte(0, True)
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
            res2 = self.get_byte(4 + i, public_memory=True)
            print(res1)
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
            res2 = self.get_byte(i, public_memory=True)
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
        res2 = self.get_byte(0, True)
        print(res2)
        print(self.get_byte(0))
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
        res2 = self.get_byte(1, True)
        print(res2)
        print(self.get_byte(0))
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
        res2 = self.get_byte(n2, True)
        print(res2)
        print(self.get_byte(0))
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
    #    res2 = self.get_byte(10)
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
        res2 = self.get_byte(0, True)
        print(res2)
        self.assertEqual(n1, res2)


if __name__ == '__main__':
    unittest.main()
