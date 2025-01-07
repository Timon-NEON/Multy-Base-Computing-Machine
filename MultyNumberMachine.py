from math import ceil, log, floor

class NumberProcessing:
    def __init__(self, NS:int, numb=None, numb10=-1):
        self.NS = NS
        if numb != None:
            self.keep_orig_numb(numb)
        elif numb10 != -1:
            self.keep_numb10_numb(numb10)
        else:
            self.val = 0

    def __str__(self):
        return str(type(self)) + '  ' + str(self.val) + '  ' + str(self.list())

    def __add__(self, other):
        if isinstance(other, NumberProcessing):
            return type(self)(self.NS, numb10=self.val + other.val)
        elif isinstance(other, int):
            return type(self)(self.NS, numb10=self.val + other)
        return self

    def __and__(self, other):
        if isinstance(other, NumberProcessing):
            if self.val < other.val:
                return self
            else:
                return other
        elif isinstance(other, int):
            if self.val < other:
                return self
            else:
                return type(self)(self.NS, numb10=other)
        else:
            return self

    def __or__(self, other):
        if isinstance(other, NumberProcessing):
            if self.val > other.val:
                return self
            else:
                return other
        elif isinstance(other, int):
            if self.val > other:
                return self
            else:
                return type(self)(self.NS, numb10=other)
        else:
            return self

    def __xor__(self, other):
        if isinstance(other, NumberProcessing):
            return type(self)(self.NS, numb10=(self.val + other.val) % self.NS)
        elif isinstance(other, int):
            return type(self)(self.NS, numb10=(self.val + other) % self.NS)
        else:
            return self

    def __eq__(self, other):
        if isinstance(other, NumberProcessing):
            return type(self)(self.NS, self.val == other.val)
        elif isinstance(other, int):
            return type(self)(self.NS, self.val == other)
        else:
            return self


    def keep_orig_numb(self, numb:list):
        self.val = 0
        for i in range(len(numb)):
            self.val += numb[-i - 1] * self.NS ** i

    def keep_numb10_numb(self, numb10):
        self.val = numb10

    def append(self, numb):
        self.val = self.val * self.NS + numb

    def incr(self):
        self.val += 1

    def decr(self):
        self.val -= 1

    def list(self, size=-1):
        lst = [0] * size
        val_copy = self.val
        power = 0
        counter = size - 1
        while val_copy > 0 and (counter >= 0 or size == -1):
            lst.append(val_copy % self.NS)
            power += 1
            val_copy //= self.NS
            counter -= 1
        lst.reverse()
        return [0] * (size - len(lst)) + lst


class Unit(NumberProcessing):

    def get_number(self):
        return Number(self.NS, numb10=self.val)

    def get_word(self):
        return Word(self.NS, numb10=self.val)


class Word(NumberProcessing):

    def get_number(self):
        return Number(self.NS, numb10=self.val)

    def get_unit(self):
        return Unit(self.NS, numb10=self.val)


class Number(NumberProcessing):

    def get_word(self):
        return Word(self.NS, numb10=self.val)

    def get_unit(self):
        return Unit(self.NS, numb10=self.val)


class InformationBasis:
    def __init__(self, NS:int, mainConst:dict, memory_size=0, lst=None):
        self.NS = NS
        self.mainConst = mainConst
        if memory_size != 0:
            self.__mem = [0] * memory_size
        elif lst != None:
            self.__mem = lst
        else:
            self.__mem = []

    def read(self, unit: Unit) -> Number:
        return Number(self.NS, self.__mem[unit.val])

    def update(self, unit: Unit, number: Number):
        self.__mem[unit.val] = number.val



class MainMachine:
    def __init__(self, NS:int, word:int, memory_size:int, instruction_stack_size:int):
        self.NS = NS
        self.word = word
        self.memory_size = memory_size
        self.instr_stack_size = instruction_stack_size

        self.type_addressing_quantity = 4
        self.commands_quantity = 16

        self.word_capacity = self.NS ** self.word
        self.memory_units_quantity = self.memory_size * self.word

        self.instr_type_size = ceil(log(self.type_addressing_quantity, self.NS))
        self.instr_command_size = ceil(log(self.commands_quantity, self.NS))
        self.instr_word = self.instr_type_size + self.instr_command_size + self.word  # units
        self.instr_capacity = min(self.word_capacity, floor(self.instr_stack_size / self.instr_word))
        self.instr_units_quantity = self.instr_capacity * self.instr_word

        self.first_block_reservation = 5

        self.const ={
            'main': {
                'word': {
                    'size': self.word,
                    'amount': self.memory_size,
                    'capacity': self.word_capacity,
                },
            },
            'instr' : {
                'word': {
                    'type': {
                        'start': 0,
                        'size': self.instr_type_size,
                    },
                    'code': {
                        'start': self.instr_type_size,
                        'size': self.instr_command_size,
                    },
                    'address': {
                        'start': self.instr_type_size + self.instr_command_size,
                        'size': self.word,
                    },
                    'size': self.instr_word,
                },
                'capacity': self.instr_capacity,
            },
            'alu': {
                'load': Number(self.NS, numb10=0),
                'and': Number(self.NS, numb10=1),
                'or': Number(self.NS, numb10=2),
                'xor': Number(self.NS, numb10=3),
                'add': Number(self.NS, numb10=4),
                'subtr': Number(self.NS, numb10=5),
                'store': Number(self.NS, numb10=7),
                'incr': Number(self.NS, numb10=8),
                'decr': Number(self.NS, numb10=9),
                'cmpb': Number(self.NS, numb10=10),
                'cmps': Number(self.NS, numb10=11),
                'cmpe': Number(self.NS, numb10=12),
                'next': Number(self.NS, numb10=13),
                'goto': Number(self.NS, numb10=14),

                'end': Number(self.NS, numb10=0),
                'clr': Number(self.NS, numb10=1),
                'cin': Number(self.NS, numb10=3),
            },
            'mem': {
                'reserved': self.first_block_reservation,
                'batt': Word(self.NS, numb10=0),
                'counter': Word(self.NS, numb10=1),
                'instr': Word(self.NS, numb10=2),
                'instr_continue': Word(self.NS, numb10=3),
                'cache': Word(self.NS, numb10=4),
            },
        }

        self.MB = MemoryBlock(2, self.const, memory_size=self.memory_units_quantity)

        self.IB = InstructionRegisterBlock_2(self.NS, self.const, memory_size=self.instr_units_quantity)

        self.AB = ALUBlock_2(self.NS, self.MB, self.const)

    def get_unit(self, value: NumberProcessing, word_capacity: int):
        return Unit(value.NS, numb10=value.val * word_capacity)

    def read_units(self, unit_address: Unit, source: InformationBasis, size: int) -> Number:
        number = Number(self.NS)
        for it in range(size):
            unit = Unit(self.NS, numb10=unit_address.val + it)
            number.append(source.read(unit))
        return number

    def read_word(self, address: Word, source: InformationBasis) -> Number:
        if type(source) == MemoryBlock:
            local_unit_size = self.word
        else:
            local_unit_size = self.const['instr']['word']['size']
        return self.read_units(self.get_unit(address, local_unit_size), source, local_unit_size)

    def add_instruction(self, type_addressing: int, code_operation: int, address: int):
        type_addressing = Number(self.NS, numb10=type_addressing)
        code_operation = Number(self.NS, numb10=code_operation)
        address = Word(self.NS, numb10=address)

        unit_counter = self.get_unit(self.read_word(self.const['mem']['instr'], self.MB), self.const['instr']['word']['size']) #value counter from `mem` expresses iterator in stack of instructions

        bit_counter = 0
        instruction = type_addressing.list(self.const['instr']['word']['type']['size']) + code_operation.list(self.const['instr']['word']['code']['size']) + address.list(self.const['instr']['address']['word']['size'])
        for el in instruction:
            unit = Unit(self.NS, unit_counter.val + bit_counter)
            self.IB.update(unit, el)
            bit_counter += 1
        self.AB.action(Number(self.NS, 0), self.const['alu']['incr'], self.const['mem']['instr'])

    def execute(self):
        self.__preparing()
        while self.read_word(self.const['mem']['instr_continue'], self.MB).val == 1:
            unit_counter = self.get_unit(self.read_word(self.const['mem']['counter'], self.MB), self.const['instr']['word']['size'])
            type_addressing = self.read_units(Unit(self.NS, numb10=unit_counter.val + self.const['instr']['word']['type']['start']), self.IB, self.const['instr']['word']['type']['size'])
            code_operation = self.read_units(Unit(self.NS, numb10=unit_counter.val + self.const['instr']['word']['code']['start']), self.IB, self.const['instr']['word']['code']['size'])
            address = Word(self.NS, numb10=self.read_units(Unit(self.NS, numb10=unit_counter.val + self.const['instr']['word']['address']['start']), self.IB, self.const['instr']['word']['address']['size']).val)
            self.AB.action(Number(self.NS, 0), self.const['alu']['incr'], self.const['mem']['counter'])
            self.AB.action(type_addressing, code_operation, address)
            self.AB.compare_smaller_sp(self.const['mem']['counter'], self.const['mem']['instr'], self.const['mem']['instr_continue'])


    def __preparing(self):
        self.AB.action(Number(self.NS, 0), self.const['alu']['incr'], self.const['mem']['instr_continue'])
       


class MemoryBlock(InformationBasis):
    pass



class ALUBlock_2:
    def __init__(self, NumberSystem, MB, mainConst):
        self.NS = NumberSystem
        self.MB = MB
        self.mainConst = mainConst
        self.const = mainConst['alu']



        self.word_size = self.mainConst['main']['word']['size']

    def action(self, type_addressing: Number, code_operation: Number, address: Word):
        """
        A - input value
        B - battery
        """
        word_source = Word(self.NS)
        if type_addressing.val == 1 or type_addressing.val == 3:
            source_A = InformationBasis(self.NS, self.mainConst, self.word_size, lst=address.list(self.word_size))
        elif type_addressing.val == 2:
            unit_address = self.__read_unit(address)
            new_address = self.__read_value(unit_address, self.MB)
            new_address = self.__read_word(new_address)
            self.action(Number(self.NS), code_operation, new_address)
            return
        else:
            word_source.keep_numb10_numb(address.val)
            source_A = self.MB
        unit_A = self.__read_unit(word_source)
        unit_B = self.__read_unit(self.mainConst['mem']['batt'])
        if type_addressing.val == 3:
            match code_operation.val:
                case _ as code if self.const['end'].val == code:  # end
                    self.end_c()
        else:
            match code_operation.val:
                case _ as code if self.const['load'].val == code: #load
                    self.load_f(unit_A, unit_B, source_A)
                case _ as code if self.const['and'].val == code: #and
                    self.and_f(unit_A, unit_B, source_A)
                case _ as code if self.const['or'].val == code:  # or
                    self.or_f(unit_A, unit_B, source_A)
                case _ as code if self.const['xor'].val == code:  # xor
                    self.xor_f(unit_A, unit_B, source_A)
                case _ as code if self.const['add'].val == code:  # add
                    self.add_f(unit_A, unit_B, source_A)
                case _ as code if self.const['subtr'].val == code:  # add
                    self.subtraction_f(unit_A, unit_B, source_A)
                case _ as code if self.const['incr'].val == code: #increment
                    self.increment_f(unit_A, source_A)
                case _ as code if self.const['decr'].val == code: #decrement
                    self.decrement_f(unit_A, source_A)
                case _ as code if self.const['store'].val == code: #store
                    self.store_f(unit_A, unit_B, source_A)
                case _ as code if self.const['cmpb'].val == code: #compare A > Battery
                    self.compare_bigger_f(unit_A, unit_B, source_A)
                case _ as code if self.const['cmps'].val == code: #compare A < Battery
                    self.compare_smaller_f(unit_A, unit_B, source_A)
                case _ as code if self.const['cmpe'].val == code: #compare A == Battery
                    self.compare_equal_f(unit_A, unit_B, source_A)
                case _ as code if self.const['next'].val == code: #if A % 2 == 0: skip next instruction
                    self.next_f(unit_A, unit_B, source_A)
                case _ as code if self.const['goto'].val == code: #go to A instruction
                    self.goto_f(unit_A, unit_B, source_A)


    def load_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        for it in range(self.word_size): #simple copying of byte
            self.MB.update(unit_B + it, source_A.read(unit_A + it).val)

    def store_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        for it in range(self.word_size):
            self.MB.update(unit_A + it, source_A.read(unit_B + it).val)

    def and_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        for it in range(self.word_size):
            self.MB.update(unit_B + it, (source_A.read(unit_A + it) & source_A.read(unit_B + it)).val)

    def or_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        for it in range(self.word_size):
            self.MB.update(unit_B + it, (source_A.read(unit_A + it) | source_A.read(unit_B + it)).val)

    def xor_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        for it in range(self.word_size):
            self.MB.update(unit_B + it, (source_A.read(unit_A + it) ^ source_A.read(unit_B + it)).val)

    def add_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        pass
        #self.action(Number(self.NS), self.const['store'], self.mainConst['mem']['cache'])
        #unit_C = self.__get_bit(self.mainConst['mem']['cache'])
        #self.mem[unit_B.val + self.word_size - 1] = source_A[unit_A.val + self.word_size - 1] ^ self.mem[unit_B.val + self.word_size - 1]
        #for it in range(self.word_size -2, -1, -1):
        #    self.mem[unit_B.val + it] = source_A[unit_A.val + it] ^ self.mem[bit_it_C.val + it] ^ (((self.mem[bit_it_C.val + it + 1] | source_A[unit_A.val + it + 1]) & (self.mem[unit_B.val + it + 1] == 0)) | (self.mem[bit_it_C.val + it + 1] & source_A[unit_A.val + it + 1]))

    def subtraction_f(self, unit_A: Unit, unit_B: Unit, source_A):
        pass

    def increment_f(self, unit_A: Unit, source_A: InformationBasis):
        for it in range(self.word_size -1, -1, -1):  # from byte back to front
            current_val = source_A.read(unit_A + it)
            if current_val.val == self.NS - 1:
                source_A.update(unit_A + it, 0)
            else:
                source_A.update(unit_A + it, current_val.val + 1)
                return

    def decrement_f(self, unit_A: Unit, source_A: InformationBasis):
        for it in range(self.word_size -1, -1, -1):  # from byte back to front
            current_val = source_A.read(unit_A + it)
            if current_val.val == 0:
                source_A.update(unit_A + it,  self.NS - 1)
            else:
                source_A.update(unit_A + it, current_val.val - 1)
                return

    def compare_bigger_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        last_it = self.word_size - 1
        self.MB.update(unit_B.val + last_it, ((source_A.read(unit_A + last_it) == source_A.read(unit_A + last_it) | self.MB.read(unit_B + last_it)) and ((source_A.read(unit_A + last_it) == self.MB.read(unit_B + last_it)) == Unit(self.NS))).val)
        for it in range(self.word_size - 2, -1, -1):
            A = source_A.read(unit_A + it)
            B = self.MB.read(unit_B + it)
            if ((A == B).val == 0):
                self.MB.update(unit_B + last_it, (A == (A | B)).val)
            self.MB.update(unit_B + it, 0)

    def compare_smaller_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        last_it = self.word_size - 1
        self.MB.update(unit_B.val + last_it, ((self.MB.read(unit_B + last_it) == source_A.read(unit_A + last_it) | self.MB.read(unit_B + last_it)) and ((source_A.read(unit_A + last_it) == self.MB.read(unit_B + last_it)) == Unit(self.NS))).val)
        for it in range(self.word_size - 2, -1, -1):
            A = source_A.read(unit_A + it)
            B = self.MB.read(unit_B + it)
            if ((A == B).val == 0):
                self.MB.update(unit_B + last_it, (B == (A | B)).val)
            self.MB.update(unit_B + it, 0)

    def compare_equal_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        last_it = self.word_size - 1
        self.MB.update(unit_B + last_it, (source_A.read(unit_A + last_it) == self.MB.read(unit_B + last_it)).val)
        for it in range(self.word_size - 2, -1, -1):
            A = source_A.read(unit_A + it)
            B = self.MB.read(unit_B + it)
            if ((A == B).val == 0):
                self.MB.update(unit_B + last_it, 0)
            self.MB.update(unit_B + it, 0)

    def next_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        if source_A.read(unit_A + self.word_size - 1).val == 0:
            self.action(Number(self.NS), self.const['incr'], self.mainConst['mem']['counter'])

    def goto_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        self.update_val(unit_A, self.mainConst['mem']['counter'], source_A)

    #def save_return_f(self, unit_A: Unit, unit_B: Unit, source_A):
    #    stack_counter_it = self.mainConst['mem']['st_counter']
    #    stack_counter_bit = self.__get_bit(stack_counter_it)
    #    stack_counter_value = self.__get_value(stack_counter_bit, self.mem) + self.mainConst['mem']['f_block'] + 1
    #    stack_counter_value_it = self.__get_it(stack_counter_value, False)
    #    stack_counter_value_bit = self.__get_bit(stack_counter_value_it)
    #    self.update_val(unit_A, stack_counter_value_bit, source_A)
    #    self.increment_f(stack_counter_bit, self.mem)

    def end_c(self):
        self.update_val(self.mainConst['mem']['instr'], self.mainConst['mem']['counter'], self.MB)

    #def return_c(self):
    #    stack_counter_it = self.mainConst['mem']['st_counter']
    #    stack_counter_bit = self.__get_bit(stack_counter_it)
    #    stack_counter_value = self.__get_value(stack_counter_bit, self.mem) + self.mainConst['mem']['f_block'] + 1
    #    stack_counter_value_it = self.__get_it(stack_counter_value, False)
    #    stack_counter_value_bit = self.__get_bit(stack_counter_value_it)
    #    self.update_val(self.mainConst['mem']['instr'], stack_counter_value_bit, self.mem)
    #    self.decrement_f(stack_counter_bit, self.mem)


    def compare_smaller_sp(self, word_A: Word, word_B: Word, storage: Word):
        # safe 1 if A < B, values in memory
        unit_A = self.__read_unit(word_A)
        unit_B = self.__read_unit(word_B)
        unit_S = self.__read_unit(storage)
        last_it = self.word_size - 1  ##>|< ?
        self.MB.update(unit_S + last_it, ((self.MB.read(unit_B + last_it) == self.MB.read(unit_A + last_it) | self.MB.read(unit_B + last_it)) and ((self.MB.read(unit_A + last_it) == self.MB.read(unit_B + last_it)) == Unit(self.NS))).val)
        for it in range(self.word_size - 2, -1, -1):
            A = self.MB.read(unit_A + it)
            B = self.MB.read(unit_B + it)
            if ((A == B).val == 0):
                self.MB.update(unit_S + last_it, 0)
            self.MB.update(unit_S + it, 0)


    def __read_value(self, unit_A: Unit, source_A: InformationBasis):
        value = Number(self.NS)
        for it in range(self.word_size):
            unit = Unit(self.NS, unit_A.val + it)
            value.append(source_A.read(unit))
        return value

    def __read_word(self, numb_A: Number, public=True):
        if public:
            return Word(self.NS, numb10=numb_A.val + self.mainConst['mem']['reserved'])
        else:
            return Word(self.NS, numb10=numb_A.val)

    def __read_unit(self, word_A: Word) -> Unit:
        return Unit(self.NS, numb10=word_A.val * self.word_size)

    def update_val(self, unit_A, unit_B, source_A: InformationBasis):
        """
        :param unit_A: new_value
        :param unit_B: updated_value in memory
        :param source_A: source of new_value
        :return:
        """
        if type(unit_A) != Unit: unit_A = self.__read_unit(unit_A)
        if type(unit_B) != Unit: unit_B = self.__read_unit(unit_B)
        for it in range(self.word_size):
            self.MB.update(unit_B + it, source_A.read(unit_A + it))


class InstructionRegisterBlock_2(InformationBasis):
    pass




class UI:
    machine: MainMachine
    def __init__(self, NS:int=2, word:int=8, memory_size:int=1024, instruction_stack_size:int=256):
        self.NS = NS
        self.machine = MainMachine(NS, word, memory_size, instruction_stack_size)

    def execute(self):
        self.machine.execute()


    def add_instruction(self, type_addressing: int, code_operation, address: int):
        if type_addressing != 1: address += self.machine.const['mem']['reserved']
        if type(code_operation) == Number: code_operation = code_operation.val
        self.machine.add_instruction(type_addressing, code_operation, address)
