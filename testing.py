import unittest

import binMachine as bM

class Test(unittest.TestCase):
    UI = bM.UI()
    machine = UI.machine
    comm = machine.const['alu']
    reserved = machine.const['mem']['reserved']
    unit_size = machine.const['main']['unit']['size']

    def get_byte(self, byte: int) -> bM.Number:
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
        for i in range(10):
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


    def test_load_n_storage(self):
        n1, n2, n3, n4 = 156, 27 + 1, 89, 203
        res1 = (((n1 & n2) | n3) ^ n4)
        print(res1)
        self.UI.add_instruction(1, self.comm['load'], n1)
        self.UI.add_instruction(0, self.comm['store'], 0)
        self.UI.add_instruction(1, self.comm['load'], n2)
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


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
