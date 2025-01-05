from math import ceil, log, floor

number_system = 2
word = 8 #units
memory_size = 1000 #words

instruction_stack_size = 250 #units


type_addressing_quantity = 4
commands_quantity = 16


word_capacity = number_system ** word
memory_unit_qauntity = memory_size * word
instruction_word = ceil(log(type_addressing_quantity, number_system)) + ceil(log(commands_quantity, number_system)) + word #units
instruction_capacity = min(word_capacity, floor(instruction_stack_size / instruction_word))

print('word_capacity: ', word_capacity)
print('memory_unit_qauntity: ', memory_unit_qauntity)
print('instruction_word: ', instruction_word)
print('instruction_capacity: ', instruction_capacity)


