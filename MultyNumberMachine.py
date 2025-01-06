from math import ceil, log, floor

class Constants:

    def __init__(self, NS:int, word:int, memory_size:int, instruction_stack_size:int):
        self.NS = NS
        self.word = word
        self.memory_size = memory_size
        self.instruction_stack_size = instruction_stack_size

        self.type_addressing_quantity = 4
        self.commands_quantity = 16

        self.word_capacity = self.NS ** self.word
        self.memory_unit_qauntity = self.memory_size * self.word
        self.instruction_word = ceil(log(self.type_addressing_quantity, self.NS)) + ceil(log(self.commands_quantity, self.NS)) + self.word  # units
        self.instruction_capacity = min(self.word_capacity, floor(self.instruction_stack_size / self.instruction_word))

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