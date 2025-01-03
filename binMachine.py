from time import *

class NumberProcessing:
    def __init__(self, numb2=-1, numb10=-1):
        if numb2 != -1:
            self.keep_numb2_numb(numb2)
        elif numb10 != -1:
            self.keep_numb10_numb(numb10)
        else:
            self.val = 0

    def __str__(self):
        return str(type(self)) + '  ' + str(self.val) + '  ' + str(self.val)

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

class Bit(NumberProcessing):

    def get_number(self):
        return Number(numb2=self.val)


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
        self.return_stack_size = 16
        self.const = {'main': {
            'unit': {
                'size': self.unit_size,
                'amount': self.unit_amount,
                'capacity': self.ns ** self.unit_size,
            },
            'st': {
                'size': self.return_stack_size,
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
        self.__preparing()
        while self.get_byte(self.const['mem']['instr_continue'], self.mem).val == 1:
            bit_it_counter = Number(numb10=self.get_byte(self.const['mem']['counter'], self.mem).numb10() * self.const['instr']['size'])
            self.aluBlock.action(Number(0), self.const['alu']['incr'], self.const['mem']['counter'])
            #print(bit_it_counter.numb10())
            #print(self.get_byte(self.const['mem']['counter'], self.mem).numb10(), self.get_byte(self.const['mem']['instr'], self.mem).numb10())
            type_addressing = self.get_bites(Number(numb10=bit_it_counter.numb10() + self.const['instr']['type']['start']), self.instruction_stack, self.const['instr']['type']['size'])
            code_operation = self.get_bites(Number(numb10=bit_it_counter.numb10() + self.const['instr']['code']['start']), self.instruction_stack, self.const['instr']['code']['size'])
            address = It(numb2=self.get_bites(Number(numb10=bit_it_counter.numb10() + self.const['instr']['address']['start']), self.instruction_stack, self.const['instr']['address']['size']).val)

            self.aluBlock.action(type_addressing, code_operation, address)
            self.aluBlock.compare_smaller_sp(self.const['mem']['counter'], self.const['mem']['instr'], self.const['mem']['instr_continue'])


    def __preparing(self):
        self.aluBlock.action(Number(0), self.const['alu']['incr'], self.const['mem']['instr_continue'])
        self.aluBlock.update_val(Bit(0), self.const['mem']['f_block'], Bit(numb10=self.memoryBlock.first_block_reservation).list(self.const['main']['unit']['size']))


class MemoryBlock:
    """
    Memory constant:
    byte: 8 bit

    Memory structer:
    0-3 bytes: reserved
        0: battery
        1: instruction counter
        2: instruction quantity
        3: storage value 0/1, if 1 -- program continues executing
        4: cache (using for inputting the value)
        5: counter of used values in return stack
        6: size of return stack
        7: constant value that storage quantity of used bytes in memory for variables and constants
    """
    def __init__(self, NumberSystem, mainConst):
        self.NS = NumberSystem
        self.mainConst = mainConst

        self.mem = [0] * self.mainConst['main']['unit']['size'] * self.mainConst['main']['unit']['amount']
        self.first_block_reservation = 8

        self.constant = {
            'reserved': self.first_block_reservation + self.mainConst['main']['st']['size'],
            'batt': It(numb10=0),
            'counter': It(numb10=1),
            'instr': It(numb10=2),
            'instr_continue': It(numb10=3),
            'cache': It(numb10=4),
            'st_counter': It(numb10=5),
            'st_size': It(numb10=6),
            'f_block': It(numb10=7),
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
            'subtr': Number(numb10=5),
            'store': Number(numb10=7),
            'incr': Number(numb10=8),
            'decr': Number(numb10=9),
            'cmpb': Number(numb10=10),
            'cmps': Number(numb10=11),
            'cmpe': Number(numb10=12),
            'next': Number(numb10=13),
            'goto': Number(numb10=14),
        }

        self.unit_size = self.mainConst['main']['unit']['size']  # used big number times

    def action(self, type_addressing: Number, code_operation: Number, address: It):
        """
        A - input value
        B - battery
        """
        it_source = It()
        if type_addressing.numb10() == 1:
            source_A = address.list(self.unit_size)
        elif type_addressing.numb10() == 2:
            bit_address = self.__get_bit(address)
            new_address = self.__get_value(bit_address, self.mem)
            new_address = self.__get_it(new_address)
            self.action(Number(numb10=0), code_operation, new_address)
            return
        else:
            it_source.keep_numb10_numb(address.numb10())
            source_A = self.mem
        bit_it_A = self.__get_bit(it_source)
        bit_it_B = self.__get_bit(self.mainConst['mem']['batt'])
        if type_addressing.numb10() == 3:
            match code_operation.val:
                case _ as code if self.const['load'].val == code:  # load
                    self.load_f(bit_it_A, bit_it_B, source_A)
        else:
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
                case _ as code if self.const['subtr'].val == code:  # add
                    self.subtraction_f(bit_it_A, bit_it_B, source_A)
                case _ as code if self.const['incr'].val == code: #increment
                    self.increment_f(bit_it_A, source_A)
                case _ as code if self.const['decr'].val == code: #decrement
                    self.decrement_f(bit_it_A, source_A)
                case _ as code if self.const['store'].val == code: #store
                    self.store_f(bit_it_A, bit_it_B, source_A)
                case _ as code if self.const['cmpb'].val == code: #compare A > Battery
                    self.compare_bigger_f(bit_it_A, bit_it_B, source_A)
                case _ as code if self.const['cmps'].val == code: #compare A < Battery
                    self.compare_smaller_f(bit_it_A, bit_it_B, source_A)
                case _ as code if self.const['cmpe'].val == code: #compare A == Battery
                    self.compare_equal_f(bit_it_A, bit_it_B, source_A)
                case _ as code if self.const['next'].val == code: #if A % 2 == 0: skip next instruction
                    self.next_f(bit_it_A, bit_it_B, source_A)
                case _ as code if self.const['goto'].val == code: #go to A instruction
                    self.goto_f(bit_it_A, bit_it_B, source_A)


    def load_f(self, bit_it_A: Bit, bit_it_B: Bit, source_A):
        for it in range(self.unit_size): #simple copying of byte
            self.mem[bit_it_B.numb10() + it] = source_A[bit_it_A.numb10() + it]

    def store_f(self, bit_it_A: Bit, bit_it_B: Bit, source_A):
        for it in range(self.unit_size):
            source_A[bit_it_A.numb10() + it] = self.mem[bit_it_B.numb10() + it]

    def and_f(self, bit_it_A: Bit, bit_it_B: Bit, source_A):
        for it in range(self.unit_size):
            self.mem[bit_it_B.numb10() + it] = self.mem[bit_it_B.numb10() + it] & source_A[bit_it_A.numb10() + it]

    def or_f(self, bit_it_A: Bit, bit_it_B: Bit, source_A):
        for it in range(self.unit_size):
            self.mem[bit_it_B.numb10() + it] = self.mem[bit_it_B.numb10() + it] | source_A[bit_it_A.numb10() + it]

    def xor_f(self, bit_it_A: Bit, bit_it_B: Bit, source_A):
        for it in range(self.unit_size):
            self.mem[bit_it_B.numb10() + it] = self.mem[bit_it_B.numb10() + it] ^ source_A[bit_it_A.numb10() + it]

    def add_f(self, bit_it_A: Bit, bit_it_B: Bit, source_A):
        self.action(Number(0), self.const['store'], self.mainConst['mem']['cache'])
        bit_it_C = self.__get_bit(self.mainConst['mem']['cache'])
        self.mem[bit_it_B.numb10() + self.unit_size - 1] = source_A[bit_it_A.numb10() + self.unit_size - 1] ^ self.mem[bit_it_B.numb10() + self.unit_size - 1]
        for it in range(self.unit_size -2, -1, -1):
            self.mem[bit_it_B.numb10() + it] = source_A[bit_it_A.numb10() + it] ^ self.mem[bit_it_C.numb10() + it] ^ (((self.mem[bit_it_C.numb10() + it + 1] | source_A[bit_it_A.numb10() + it + 1]) & (self.mem[bit_it_B.numb10() + it + 1] == 0)) | (self.mem[bit_it_C.numb10() + it + 1] & source_A[bit_it_A.numb10() + it + 1]))

    def subtraction_f(self, bit_it_A: Bit, bit_it_B: Bit, source_A):
        print('Maybe later')

    def increment_f(self, bit_it_A: Bit, source_A):
        for it in range(self.unit_size -1, -1, -1):  # from byte back to front
            if source_A[bit_it_A.numb10() + it] == self.NS - 1:
                source_A[bit_it_A.numb10() + it] = 0
            else:
                source_A[bit_it_A.numb10() + it] += 1
                return

    def decrement_f(self, bit_it_A: Bit, source_A):
        for it in range(self.unit_size -1, -1, -1):  # from byte back to front
            if source_A[bit_it_A.numb10() + it] == 0:
                source_A[bit_it_A.numb10() + it] = self.NS - 1
            else:
                source_A[bit_it_A.numb10() + it] -= 1
                return

    def compare_bigger_f(self, bit_it_A: Bit, bit_it_B: Bit, source_A):
        self.mem[bit_it_B.numb10() + self.unit_size - 1] = int(source_A[bit_it_A.numb10() + self.unit_size - 1] == (source_A[bit_it_A.numb10() + self.unit_size - 1] or self.mem[bit_it_B.numb10() + self.unit_size - 1]) and source_A[bit_it_A.numb10() + self.unit_size - 1] != self.mem[bit_it_B.numb10() + self.unit_size - 1])
        for it in range(self.unit_size - 2, -1, -1):
            A = source_A[bit_it_A.numb10() + it]
            B = self.mem[bit_it_B.numb10() + it]
            if (A != B):
                self.mem[bit_it_B.numb10() + self.unit_size - 1] = int(A == (A or B))
            self.mem[bit_it_B.numb10() + it] = 0

    def compare_smaller_f(self, bit_it_A: Bit, bit_it_B: Bit, source_A):
        self.mem[bit_it_B.numb10() + self.unit_size - 1] = int(self.mem[bit_it_B.numb10() + self.unit_size - 1] == (source_A[bit_it_A.numb10() + self.unit_size - 1] or self.mem[bit_it_B.numb10() + self.unit_size - 1]) and source_A[bit_it_A.numb10() + self.unit_size - 1] !=self.mem[bit_it_B.numb10() + self.unit_size - 1])
        for it in range(self.unit_size - 2, -1, -1):
            A = source_A[bit_it_A.numb10() + it]
            B = self.mem[bit_it_B.numb10() + it]
            if (A != B):
                self.mem[bit_it_B.numb10() + self.unit_size - 1] = int(B == (A or B))
            self.mem[bit_it_B.numb10() + it] = 0

    def compare_equal_f(self, bit_it_A: Bit, bit_it_B: Bit, source_A):
        self.mem[bit_it_B.numb10() + self.unit_size - 1] = int(source_A[bit_it_A.numb10() + self.unit_size - 1] == self.mem[bit_it_B.numb10() + self.unit_size - 1])
        for it in range(self.unit_size - 2, -1, -1):
            A = source_A[bit_it_A.numb10() + it]
            B = self.mem[bit_it_B.numb10() + it]
            if (A != B):
                self.mem[bit_it_B.numb10() + self.unit_size - 1] = 0
            self.mem[bit_it_B.numb10() + it] = 0

    def next_f(self, bit_it_A: Bit, bit_it_B: Bit, source_A):
        if source_A[bit_it_A.numb10() + self.unit_size - 1] == 0:
            self.action(Number(0), self.const['incr'], self.mainConst['mem']['counter'])

    def goto_f(self, bit_it_A: Bit, bit_it_B: Bit, source_A):
        self.update_val(bit_it_A, self.mainConst['mem']['counter'], source_A)


    def compare_smaller_sp(self, it_A: It, it_B: It, storage: It):
        # safe 1 if A < B, values in memory
        bit_it_A = self.__get_bit(it_A)
        bit_it_B = self.__get_bit(it_B)
        bit_it_S = self.__get_bit(storage)
        self.mem[bit_it_S.numb10() + self.unit_size - 1] = int(self.mem[bit_it_B.numb10() + self.unit_size - 1] == (self.mem[bit_it_A.numb10() + self.unit_size - 1] or self.mem[bit_it_B.numb10() + self.unit_size - 1]) and self.mem[bit_it_A.numb10() + self.unit_size - 1] != self.mem[bit_it_B.numb10() + self.unit_size - 1])
        for it in range(self.unit_size - 2, -1, -1):
            A = self.mem[bit_it_A.numb10() + it]
            B = self.mem[bit_it_B.numb10() + it]
            if (A != B):
                self.mem[bit_it_S.numb10() + self.unit_size - 1] = int(B == (A or B))

    def __get_value(self, bit_it_A: Bit, source_A):
        value = Number(numb10=0)
        for it in range(self.unit_size): #simple copying of byte
            value.append(source_A[bit_it_A.numb10() + it])
        return value

    def __get_bit(self, it_A: It):
        return Bit(numb10= it_A.numb10() * self.unit_size)

    def __get_it(self, numb_A: Number, public=True):
        if public:
            return It(numb10=numb_A.numb10() + self.mainConst['mem']['reserved'])
        else:
            return It(numb10=numb_A.numb10())

    def update_val(self, bit_it_A, bit_it_B, source_A):
        """
        :param bit_it_A: new_value
        :param bit_it_B: updated_value in memory
        :param source_A: source of new_value
        :return:
        """
        if type(bit_it_A) != Bit: bit_it_A = self.__get_bit(bit_it_A)
        if type(bit_it_B) != Bit: bit_it_B = self.__get_bit(bit_it_B)
        for it in range(self.unit_size): #simple copying of byte
            self.mem[bit_it_B.numb10() + it] = source_A[bit_it_A.numb10() + it]

    def __material_conditional_op(self, A: int, B: int):
        return A <= B

    def __equality_op(self, A: int, B: int):
        return A == B

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
        self.machine.execute()


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
