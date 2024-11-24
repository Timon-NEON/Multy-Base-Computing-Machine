from time import *

class NumberProcessing:
    def __init__(self, numb2=-1, numb10=-1):
        if numb2 != -1:
            self.keep_numb2_numb(numb2)
        elif numb10 != -1:
            self.keep_numb10_numb(numb10)
        else:
            self.val = 0

    def keep_numb2_numb(self, numb2):
        if numb2 < 0: numb2 = 0
        self.val = numb2

    def keep_numb10_numb(self, numb10):
        if numb10 < 0: numb10 = 0
        number_list = []
        while numb10 >= 1:
            number_list.append(numb10 % 2)
            numb10 //= 2
        numb2 = 0
        for i in range(len(number_list) - 1, -1, -1):  # reverse
            numb2 = numb2 * 10 + number_list[i]
        self.val = numb2

    def append(self, numb2):
        self.val = self.val * 10 + numb2

    def incr(self):
        self.keep_numb10_numb(self.numb10() + 1)

    def decr(self):
        self.keep_numb10_numb(self.numb10() - 1)

    def numb10(self):
        numb10 = 0
        val_copy = self.val
        power = 0
        while val_copy > 0:
            numb10 += (val_copy % 10) * 2 ** power
            power += 1
            val_copy //= 10
        return numb10

    def list(self, size):
        lst = [0] * size
        val_copy = self.val
        power = 0
        counter = size - 1
        while val_copy > 0 and counter >= 0:
            lst[counter] = val_copy % 10
            power += 1
            val_copy //= 10
            counter -= 1
        return lst

class It(NumberProcessing):

    def get_number(self):
        return Number(numb2=self.val)

class Number(NumberProcessing):

    def get_iterator(self):
        return It(numb2=self.val)

class MainMachine:
    def __init__(self, NumberSystem = 2):
        self.ns = NumberSystem
        self.unit_size = 8
        self.unit_amount = 1024
        self.const = {'main': {
            'unit': {
                'size': self.unit_size,
                'amount': self.unit_amount,
            },
        },}

        self.memoryBlock = MemoryBlock(2, self.const)
        self.mem = self.memoryBlock.mem
        self.const['mem'] = self.memoryBlock.constant

        self.instructionsBlock = InstructionRegisterBlock_2(64, self.const)
        self.instruction_stack = self.instructionsBlock.stack
        self.const['instr'] = self.instructionsBlock.const

        self.aluBlock = ALUBlock_2(self.ns, self.mem, self.const)
        self.const['alu'] = self.aluBlock.const

    def get_bites(self, bit_address: Number, source, size: int) -> Number:
        number = Number()
        for it in range(size):  # from byte back to front
            number.append(source[bit_address.numb10() + it])
        return number

    def get_byte(self, address: It, source) -> Number:
        if source == self.mem:
            local_unit_size = self.unit_size
        else:
            local_unit_size = self.const['instr']['size']
        return self.get_bites(Number(numb10=address.numb10() * local_unit_size), source, local_unit_size)

    def add_instruction(self, type_addressing: int, code_operation: int, address: int):
        type_addressing = Number(numb10=type_addressing)
        code_operation = Number(numb10=code_operation)
        address = It(numb10=address)

        bit_it_counter = Number(numb10=self.get_byte(self.const['mem']['instr'], self.mem).numb10() * self.const['instr']['size']) #value counter from `mem` expresses iterator in stack of instructions

        bit_counter = 0
        for el in type_addressing.list(self.const['instr']['type']['size']):
            self.instruction_stack[bit_it_counter.numb10() + bit_counter] = el
            bit_counter += 1
        for el in code_operation.list(self.const['instr']['code']['size']):
            self.instruction_stack[bit_it_counter.numb10() + bit_counter] = el
            bit_counter += 1
        for el in address.list(self.const['instr']['address']['size']):
            self.instruction_stack[bit_it_counter.numb10() + bit_counter] = el
            bit_counter += 1
        self.aluBlock.action(Number(0), self.const['alu']['incr'], self.const['mem']['instr'])

    def execute(self):
        while self.get_byte(self.const['mem']['counter'], self.mem).val < self.get_byte(self.const['mem']['instr'], self.mem).val:
            bit_it_counter = Number(numb10=self.get_byte(self.const['mem']['counter'], self.mem).numb10() * self.const['instr']['size'])
            print(bit_it_counter.numb10())
            print(self.get_byte(self.const['mem']['counter'], self.mem).numb10(), self.get_byte(self.const['mem']['instr'], self.mem).numb10())
            type_addressing = self.get_bites(Number(numb10=bit_it_counter.numb10() + self.const['instr']['type']['start']), self.instruction_stack, self.const['instr']['type']['size'])
            code_operation = self.get_bites(Number(numb10=bit_it_counter.numb10() + self.const['instr']['code']['start']), self.instruction_stack, self.const['instr']['code']['size'])
            address = It(numb2=self.get_bites(Number(numb10=bit_it_counter.numb10() + self.const['instr']['address']['start']), self.instruction_stack, self.const['instr']['address']['size']).val)

            self.aluBlock.action(type_addressing, code_operation, address)
            self.aluBlock.action(Number(0), self.const['alu']['incr'], self.const['mem']['counter'])


class MemoryBlock:
    """
    Memory constant:
    byte: 8 bit

    Memory structer:
    0-3 bytes: reserved
        0: battery
        1: instruction counter
        2: instruction quantity
        3: cache (using for inputting the value)
    """
    def __init__(self, NumberSystem, mainConst):
        self.NS = NumberSystem
        self.mainConst = mainConst

        self.mem = [0] * self.mainConst['main']['unit']['size'] * self.mainConst['main']['unit']['amount']

        self.constant = {
            'reserved': 4,
            'batt': It(numb10=0),
            'counter': It(numb10=1),
            'instr': It(numb10=2),
            'cache': It(numb10=3),
        }


class ALUBlock_2:
    def __init__(self, NumberSystem, mem, mainConst):
        self.NS = NumberSystem
        self.mem = mem
        self.mainConst = mainConst

        self.const = {
            'load': Number(numb10=0),
            'and': Number(numb10=1),
            'or': Number(numb10=2),
            'xor': Number(numb10=3),
            'add': Number(numb10=4),
            'store': Number(numb10=7),
            'incr': Number(numb10=9),
        }

    def action(self, type_addressing: Number, code_operation: Number, address: It):
        """
        A - input value
        B - battery
        """
        it_source = It()
        if type_addressing.numb10() == 1:
            source_A = address.list(self.mainConst['main']['unit']['size'])
        else:
            it_source.keep_numb10_numb(address.numb10())
            source_A = self.mem
        bit_it_A = Number(numb10=it_source.numb10() * self.mainConst['main']['unit']['size'])
        bit_it_B = Number(numb10=self.mainConst['mem']['batt'].numb10() * self.mainConst['main']['unit']['size'])
        match code_operation.val:
            case _ as code if self.const['load'].val == code: #load
                self.load_f(bit_it_A, bit_it_B, source_A)
            case _ as code if self.const['and'].val == code: #and
                self.and_f(bit_it_A, bit_it_B, source_A)
            case _ as code if self.const['or'].val == code:  # or
                self.or_f(bit_it_A, bit_it_B, source_A)
            case _ as code if self.const['xor'].val == code:  # xor
                self.xor_f(bit_it_A, bit_it_B, source_A)
            case _ as code if self.const['add'].val == code:  # add
                self.add_f(bit_it_A, bit_it_B, source_A)
            case _ as code if self.const['incr'].val == code: #increment
                self.increment_f(bit_it_A, source_A)
            case _ as code if self.const['store'].val == code: #store
                self.store_f(bit_it_A, bit_it_B, source_A)


    def load_f(self, bit_it_A: Number, bit_it_B: Number, source_A):
        for it in range(self.mainConst['main']['unit']['size']): #simple copying of byte
            self.mem[bit_it_B.numb10() + it] = source_A[bit_it_A.numb10() + it]

    def store_f(self, bit_it_A: Number, bit_it_B: Number, source_A):
        for it in range(self.mainConst['main']['unit']['size']):
            source_A[bit_it_A.numb10() + it] = self.mem[bit_it_B.numb10() + it]

    def and_f(self, bit_it_A: Number, bit_it_B: Number, source_A):
        for it in range(self.mainConst['main']['unit']['size']):
            self.mem[bit_it_B.numb10() + it] = self.mem[bit_it_B.numb10() + it] & source_A[bit_it_A.numb10() + it]

    def or_f(self, bit_it_A: Number, bit_it_B: Number, source_A):
        for it in range(self.mainConst['main']['unit']['size']):
            self.mem[bit_it_B.numb10() + it] = self.mem[bit_it_B.numb10() + it] | source_A[bit_it_A.numb10() + it]

    def xor_f(self, bit_it_A: Number, bit_it_B: Number, source_A):
        for it in range(self.mainConst['main']['unit']['size']):
            self.mem[bit_it_B.numb10() + it] = self.mem[bit_it_B.numb10() + it] ^ source_A[bit_it_A.numb10() + it]

    def add_f(self, bit_it_A: Number, bit_it_B: Number, source_A):
        unit_size = self.mainConst['main']['unit']['size'] # used big number times
        self.action(Number(0), self.const['store'], self.mainConst['mem']['cache'])
        bit_it_C = Number(numb10=self.mainConst['mem']['cache'].numb10() * unit_size)
        self.mem[bit_it_B.numb10() + unit_size - 1] = source_A[bit_it_A.numb10() + unit_size - 1] ^ self.mem[bit_it_B.numb10() + unit_size - 1]
        for it in range(unit_size -2, -1, -1):
            self.mem[bit_it_B.numb10() + it] = source_A[bit_it_A.numb10() + it] ^ self.mem[bit_it_C.numb10() + it] ^ (((self.mem[bit_it_C.numb10() + it + 1] | source_A[bit_it_A.numb10() + it + 1]) & (self.mem[bit_it_B.numb10() + it + 1] == 0)) | (self.mem[bit_it_C.numb10() + it + 1] & source_A[bit_it_A.numb10() + it + 1]))

    def increment_f(self, bit_it_A: Number, source_A):
        for it in range(self.mainConst['main']['unit']['size'] -1, -1, -1):  # from byte back to front
            if source_A[bit_it_A.numb10() + it] == self.NS - 1:
                source_A[bit_it_A.numb10() + it] = 0
            else:
                source_A[bit_it_A.numb10() + it] += 1
                return

class InstructionRegisterBlock_2:
    """
    Instruction: 16 bites
        0-1: type of addressing (0: straight, 1: immediate, 2: indirect)
        2-5: code of operation (p.151)
        6-13: address
        14-15: unused

    """
    def __init__(self, instruction_amount, mainConst):
        self.stack = [0] * (16 * instruction_amount)
        self.mainConst = mainConst
        self.const = {
            'type': {
                'start': 0,
                'size': 2,
            },
            'code': {
                'start': 2,
                'size': 4,
            },
            'address': {
                'start': 6,
                'size': self.mainConst['main']['unit']['size'],
            },
            'size': 16,
        }




class UI_console:
    def __init__(self, NumberSystem = 2):
        self.NS = NumberSystem
        self.machine = MainMachine(NumberSystem)

        self.const = {
            'input': {
                'type': {
                    '0': Number(0),
                    '1': Number(1),
                    'straight': Number(0),
                    'immediate': Number(1),
                },
                'code': self.machine.const['alu'],
            }
        }

    def insert_instructions(self):
        quantity_instructions = int(input("Print quantity of instructions: "))
        print('Print: type_addressing, code_operation, and address')
        counter = 0
        while counter < quantity_instructions:
            lst = input(str(counter + 1) + '. ').split()
            counter -= self.__add_instruction(lst)
            counter += 1

    def execute(self):
        self.machine.launch()


    def __add_instruction(self, lst):
        if (len(lst) != 3):
            print("You have to write 3 different values. Try again.")
            return 1
        s_type, s_code, s_address = lst

        if s_type.lower() in self.const['input']['type']:
            type = self.const['input']['type'][s_type.lower()]
        else:
            print("Type parameter is not correct. Try again.")
            return 1

        if s_code.lower() in self.const['input']['code']:
            code = self.const['input']['code'][s_code.lower()]
        else:
            print("Code parameter is not correct. Try again.")
            return 1

        try:
            address = It(numb10=int(s_address))
        except:
            print("Address parameter is not correct. Try again.")
            return 1

        if type.val == 0:
            address = It(numb10=address.numb10() + self.machine.const['mem']['reserved'])

        self.machine.add_instruction(type.numb10(), code.numb10(), address.numb10())
        return 0

class UI:
    machine: MainMachine
    def __init__(self, NumberSystem = 2):
        self.NS = NumberSystem
        self.machine = MainMachine(NumberSystem)

    def execute(self):
        self.machine.execute()


    def add_instruction(self, type_addressing: int, code_operation, address: int):
        if type_addressing != 1: address += self.machine.const['mem']['reserved']
        if type(code_operation) == Number: code_operation = code_operation.numb10()
        self.machine.add_instruction(type_addressing, code_operation, address)
