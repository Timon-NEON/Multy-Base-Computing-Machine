from math import ceil, log, floor

class NumberProcessing:
    def __init__(self, param:list, numb10=-1, numb=None):
        self.param = param
        self.NS = param[0]
        self.word_size = param[1]
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
            return type(self)(self.param, numb10=self.val + other.val)
        elif isinstance(other, int):
            return type(self)(self.param, numb10=self.val + other)
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
                return type(self)(self.param, numb10=other)
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
                return type(self)(self.param, numb10=other)
        else:
            return self

    def __xor__(self, other):
        word_capacity = self.NS ** self.word_size
        if isinstance(other, NumberProcessing):
            return type(self)(self.param, numb10=(self.val + other.val) % word_capacity)
        elif isinstance(other, int):
            return type(self)(self.param, numb10=(self.val + other) % word_capacity)
        else:
            return self

    def __eq__(self, other):
        if isinstance(other, NumberProcessing):
            return type(self)(self.param, int(self.val == other.val))
        elif isinstance(other, int):
            return type(self)(self.param, int(self.val == other))
        else:
            return self


    def keep_orig_numb(self, numb:list):
        self.val = 0
        for i in range(len(numb)):
            self.val += numb[-i - 1] * self.NS ** i

    def keep_numb10_numb(self, numb10):
        self.val = numb10

    def append(self, numb: int):
        self.val = self.val * self.NS + numb

    def incr(self):
        self.val += 1

    def decr(self):
        self.val -= 1

    def list(self, size=-1):
        lst = []
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
        return Number(self.param, numb10=self.val)

    def get_word(self):
        return Word(self.param, numb10=self.val)


class Word(NumberProcessing):

    def get_number(self):
        return Number(self.param, numb10=self.val)

    def get_unit(self):
        return Unit(self.param, numb10=self.val)


class Number(NumberProcessing):

    def get_word(self):
        return Word(self.param, numb10=self.val)

    def get_unit(self):
        return Unit(self.param, numb10=self.val)


class InformationBasis:
    def __init__(self, mainConst:dict, memory_size=0, lst=None):
        self.NS = mainConst['NS']
        self.mainConst = mainConst
        self.param = [self.NS, self.mainConst['main']['word']['size']]
        if memory_size != 0:
            self.memory_size = memory_size
            self.__mem = [0] * memory_size
        elif lst != None:
            self.memory_size = len(lst)
            self.__mem = lst
        else:
            self.memory_size = 0
            self.__mem = []

    def read(self, unit: Unit) -> Number:
        return Number(self.param, self.__mem[unit.val])

    def update(self, unit: Unit, number: Number):
        self.__mem[unit.val] = number.val

    def print(self):
        print(*self.__mem)



class MainMachine:
    def __init__(self, NS:int, word:int, memory_size:int, instruction_stack_size:int):
        self.NS = NS
        self.word = word
        self.memory_size = memory_size
        self.instr_stack_size = instruction_stack_size

        self.type_addressing_quantity = 4
        self.commands_quantity = 16

        self.word_capacity = self.NS ** self.word
        self.memory_units_quantity = min(self.word_capacity, self.memory_size * word)

        self.instr_type_size = ceil(log(self.type_addressing_quantity, self.NS))
        self.instr_command_size = ceil(log(self.commands_quantity, self.NS))
        self.instr_word = self.instr_type_size + self.instr_command_size + self.word  # units
        self.instr_capacity = min(self.word_capacity, self.instr_stack_size)
        self.instr_units_quantity = self.instr_capacity * self.instr_word

        self.first_block_reservation = 5

        self.param = [self.NS, self.word]

        self.const ={
            'NS': self.NS,
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
                'load': Number(self.param, numb10=0),
                'min': Number(self.param, numb10=1),
                'max': Number(self.param, numb10=2),
                'add': Number(self.param, numb10=4),
                'subtr': Number(self.param, numb10=5),
                'store': Number(self.param, numb10=7),
                'incr': Number(self.param, numb10=8),
                'decr': Number(self.param, numb10=9),
                'cmpb': Number(self.param, numb10=10),
                'cmps': Number(self.param, numb10=11),
                'cmpe': Number(self.param, numb10=12),
                'next': Number(self.param, numb10=13),
                'goto': Number(self.param, numb10=14),

                'end': Number(self.param, numb10=0),
                'clr': Number(self.param, numb10=1),
                'cin': Number(self.param, numb10=3),
            },
            'mem': {
                'reserved': self.first_block_reservation,
                'batt': Word(self.param, numb10=0),
                'counter': Word(self.param, numb10=1),
                'instr': Word(self.param, numb10=2),
                'instr_continue': Word(self.param, numb10=3),
                'cache': Word(self.param, numb10=4),
            },
        }



        self.MB = MemoryBlock(self.const, memory_size=self.memory_units_quantity)

        self.IB = InstructionRegisterBlock_2(self.const, memory_size=self.instr_units_quantity)

        self.AB = ALUBlock_2(self.MB, self.const)

    def get_unit(self, value: NumberProcessing, word_capacity: int):
        return Unit(value.param, numb10=value.val * word_capacity)

    def read_units(self, unit_address: Unit, source: InformationBasis, size: int) -> Number:
        number = Number(self.param)
        for it in range(size):
            unit = Unit(self.param, numb10=unit_address.val + it)
            number.append(source.read(unit).val)
        return number

    def read_word(self, address: Word, source: InformationBasis) -> Number:
        if type(source) == MemoryBlock:
            local_unit_size = self.word
        else:
            local_unit_size = self.const['instr']['word']['size']
        return self.read_units(self.get_unit(address, local_unit_size), source, local_unit_size)

    def add_instruction(self, type_addressing: int, code_operation: int, address: int):
        type_addressing = Number(self.param, numb10=type_addressing)
        code_operation = Number(self.param, numb10=code_operation)
        address = Word(self.param, numb10=address)

        unit_counter = self.get_unit(self.read_word(self.const['mem']['instr'], self.MB), self.const['instr']['word']['size']) #value counter from `mem` expresses iterator in stack of instructions

        bit_counter = 0
        instruction = type_addressing.list(self.const['instr']['word']['type']['size']) + code_operation.list(self.const['instr']['word']['code']['size']) + address.list(self.const['instr']['word']['address']['size'])
        for el in instruction:
            unit = Unit(self.param, unit_counter.val + bit_counter)
            self.IB.update(unit, Number(self.param, el))
            bit_counter += 1
        self.AB.action(Number(self.param, 0), self.const['alu']['incr'], self.const['mem']['instr'])

    def execute(self):
        self.__preparing()
        while self.read_word(self.const['mem']['instr_continue'], self.MB).val == 1:
            unit_counter = self.get_unit(self.read_word(self.const['mem']['counter'], self.MB), self.const['instr']['word']['size'])
            type_addressing = self.read_units(Unit(self.param, numb10=unit_counter.val + self.const['instr']['word']['type']['start']), self.IB, self.const['instr']['word']['type']['size'])
            code_operation = self.read_units(Unit(self.param, numb10=unit_counter.val + self.const['instr']['word']['code']['start']), self.IB, self.const['instr']['word']['code']['size'])
            address = Word(self.param, numb10=self.read_units(Unit(self.param, numb10=unit_counter.val + self.const['instr']['word']['address']['start']), self.IB, self.const['instr']['word']['address']['size']).val)
            self.AB.action(Number(self.param, 0), self.const['alu']['incr'], self.const['mem']['counter'])
            self.AB.action(type_addressing, code_operation, address)
            self.AB.compare_smaller_sp(self.const['mem']['counter'], self.const['mem']['instr'], self.const['mem']['instr_continue'])


    def __preparing(self):
        self.AB.action(Number(self.param, 0), self.const['alu']['incr'], self.const['mem']['instr_continue'])
       


class MemoryBlock(InformationBasis):
    pass



class ALUBlock_2:
    def __init__(self, MB, mainConst):
        self.NS = mainConst['NS']
        self.MB = MB
        self.mainConst = mainConst
        self.const = mainConst['alu']
        self.param = [self.NS, self.mainConst['main']['word']['size']]



        self.word_size = self.mainConst['main']['word']['size']

    def action(self, type_addressing: Number, code_operation: Number, address: Word):
        """
        A - input value
        B - battery
        """
        word_source = Word(self.param)
        if type_addressing.val == 1 or type_addressing.val == 3:
            source_A = InformationBasis(self.mainConst, lst=address.list(self.word_size))
        elif type_addressing.val == 2:
            unit_address = self.__get_unit(address)
            new_address = self.__read_value(unit_address, self.MB)
            new_address = self.__get_word(new_address)
            self.action(Number(self.param), code_operation, new_address)
            return
        else:
            word_source.keep_numb10_numb(address.val)
            source_A = self.MB
        unit_A = self.__get_unit(word_source)
        unit_B = self.__get_unit(self.mainConst['mem']['batt'])
        if type_addressing.val == 3:
            match code_operation.val:
                case _ as code if self.const['end'].val == code:  # end
                    self.end_c()
        else:
            match code_operation.val:
                case _ as code if self.const['load'].val == code: #load
                    self.load_f(unit_A, unit_B, source_A)
                case _ as code if self.const['min'].val == code: #and
                    self.min_f(unit_A, unit_B, source_A)
                case _ as code if self.const['max'].val == code:  # or
                    self.max_f(unit_A, unit_B, source_A)
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
            self.MB.update(unit_B + it, source_A.read(unit_A + it))

    def store_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        for it in range(self.word_size):
            self.MB.update(unit_A + it, source_A.read(unit_B + it))

    def min_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        A = self.__read_value(unit_A, source_A)
        B = self.__read_value(unit_B, self.MB)
        C = A & B
        self.update_val(C, unit_B)

    def max_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        A = self.__read_value(unit_A, source_A)
        B = self.__read_value(unit_B, self.MB)
        C = A | B
        self.update_val(C, unit_B)

    def add_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        A = self.__read_value(unit_A, source_A)
        B = self.__read_value(unit_B, self.MB)
        C = A ^ B
        self.update_val(C, unit_B)

    def subtraction_f(self, unit_A: Unit, unit_B: Unit, source_A):
        pass

    def increment_f(self, unit_A: Unit, source_A: InformationBasis):
        for it in range(self.word_size -1, -1, -1):  # from byte back to front
            current_val = source_A.read(unit_A + it)
            if current_val.val == self.NS - 1:
                source_A.update(unit_A + it, Number(self.param))
            else:
                source_A.update(unit_A + it, Number(self.param, current_val.val + 1))
                return

    def decrement_f(self, unit_A: Unit, source_A: InformationBasis):
        for it in range(self.word_size -1, -1, -1):  # from byte back to front
            current_val = source_A.read(unit_A + it)
            if current_val.val == 0:
                source_A.update(unit_A + it,  Number(self.param, self.NS - 1))
            else:
                source_A.update(unit_A + it, Number(self.param, current_val.val - 1))
                return

    def compare_bigger_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        last_it = self.word_size - 1
        self.MB.update(unit_B + last_it, ((source_A.read(unit_A + last_it) == source_A.read(unit_A + last_it) | self.MB.read(unit_B + last_it)) & ((source_A.read(unit_A + last_it) == self.MB.read(unit_B + last_it)) == Unit(self.param))))
        for it in range(self.word_size - 2, -1, -1):
            A = source_A.read(unit_A + it)
            B = self.MB.read(unit_B + it)
            if ((A == B).val == 0):
                self.MB.update(unit_B + last_it, (A == (A | B)))
            self.MB.update(unit_B + it, Number(self.param))

    def compare_smaller_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        last_it = self.word_size - 1
        self.MB.update(unit_B + last_it, ((self.MB.read(unit_B + last_it) == source_A.read(unit_A + last_it) | self.MB.read(unit_B + last_it)) & ((source_A.read(unit_A + last_it) == self.MB.read(unit_B + last_it)) == Unit(self.param))))
        for it in range(self.word_size - 2, -1, -1):
            A = source_A.read(unit_A + it)
            B = self.MB.read(unit_B + it)
            if ((A == B).val == 0):
                self.MB.update(unit_B + last_it, (B == (A | B)))
            self.MB.update(unit_B + it, Number(self.param))

    def compare_equal_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        last_it = self.word_size - 1
        self.MB.update(unit_B + last_it, (source_A.read(unit_A + last_it) == self.MB.read(unit_B + last_it)))
        for it in range(self.word_size - 2, -1, -1):
            A = source_A.read(unit_A + it)
            B = self.MB.read(unit_B + it)
            if ((A == B).val == 0):
                self.MB.update(unit_B + last_it, Number(self.param))
            self.MB.update(unit_B + it, Number(self.param))

    def next_f(self, unit_A: Unit, unit_B: Unit, source_A: InformationBasis):
        if source_A.read(unit_A + (self.word_size - 1)).val == 0:
            self.action(Number(self.param), self.const['incr'], self.mainConst['mem']['counter'])

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
        unit_A = self.__get_unit(word_A)
        unit_B = self.__get_unit(word_B)
        unit_S = self.__get_unit(storage)
        last_it = self.word_size - 1  ##>|< ?
        self.MB.update(unit_S + last_it, ((self.MB.read(unit_B + last_it) == self.MB.read(unit_A + last_it) | self.MB.read(unit_B + last_it)) & (self.MB.read(unit_A + last_it) == self.MB.read(unit_B + last_it)) == Unit(self.param)))
        for it in range(self.word_size - 2, -1, -1):
            A:Number = self.MB.read(unit_A + it)
            B:Number = self.MB.read(unit_B + it)
            if ((A == B).val == 0):
                self.MB.update(unit_S + last_it, (B == (A | B)))
            self.MB.update(unit_S + it, Number(self.param))


    def __read_value(self, unit_A: Unit, source_A: InformationBasis):
        value = Number(self.param)
        for it in range(self.word_size):
            value.append(source_A.read(unit_A + it).val)
        return value

    def __get_word(self, numb_A: Number, public=True):
        if public:
            return Word(self.param, numb10=numb_A.val + self.mainConst['mem']['reserved'])
        else:
            return Word(self.param, numb10=numb_A.val)

    def __get_unit(self, word_A: Word) -> Unit:
        return Unit(self.param, numb10=word_A.val * self.word_size)

    def update_val(self, unit_A, unit_B, source_A: InformationBasis=None):
        """
        :param unit_A: new_value
        :param unit_B: updated_value in memory
        :param source_A: source of new_value
        :return:
        """
        if type(unit_A) == Number:
            source_A = InformationBasis(self.mainConst, lst=unit_A.list(self.word_size))
            unit_A = Unit(self.param)
        if type(unit_A) != Unit: unit_A = self.__get_unit(unit_A)
        if type(unit_B) != Unit: unit_B = self.__get_unit(unit_B)
        for it in range(self.word_size):
            self.MB.update(unit_B + it, source_A.read(unit_A + it))


class InstructionRegisterBlock_2(InformationBasis):
    pass




class UI:
    machine: MainMachine
    def __init__(self, NS:int=2, word:int=8, memory_size:int=1024, instruction_stack_size:int=256):
        self.param = NS
        self.machine = MainMachine(NS, word, memory_size, instruction_stack_size)

    def execute(self):
        self.machine.execute()


    def add_instruction(self, type_addressing: int, code_operation, address: int):
        if type_addressing == 0 or type_addressing == 2: address += self.machine.const['mem']['reserved']
        if type(code_operation) == Number: code_operation = code_operation.val
        self.machine.add_instruction(type_addressing, code_operation, address)
