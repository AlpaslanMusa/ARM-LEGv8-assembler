#
# AMR-LEGv8 assembler
# A python script is based on the work of Warren Seto and Ralph Quinto (https://github.com/nextseto/ARM-LEGv8/blob/master/legv8_asm.py)
# Version 4.0
# Developers: Aydogan Musa
#

# Set our program ending flag to False
program_running = True
# Greet the user
print()
print("###########################################################")
print("Welcome !")
print("Just pass your assembly code par line and press enter")
print("example for R-type: ADD r1,r2,r3")
print("example for D-type: LDUR r3, [r10, #1]")
print("example for B-type: B #2")
print("example for CB-type: CBZ r1, #2 or CBNZ r1, #2")
print("to exit the program just type: quit")
print("###########################################################")
print()

while program_running:
    # Get Instruction from keyboard
    raw_instruction = input('\nEnter an ARM LEGv8 Assembly Instruction: ')

    # Does the user want to quit ?
    if raw_instruction == "quit":
        program_running = False
        break

    # Otherwise, nope, user wants to keep going
    else:
        # Formatting the inputted string for parsing
        formatted_instruction = raw_instruction.replace(' ', ',').replace(']', '').replace('[', '').replace('#', '')

        # Split input into list for parsing
        instruction_list = list(filter(None, formatted_instruction.split(',')))
        print(instruction_list)
        # One-to-one relationship between opcodes and their binary representation
        OPCODES = {
            'LDUR' : ['11111000010'],
            'STUR' : ['11111000000'],
            'ADD'  : ['10001011000', '+'],
            'SUB'  : ['11001011000', '-'],
            'ORR'  : ['10101010000', '|'],
            'EOR'  : ['11101010000', '~'],
            'AND'  : ['10001010000', '&'],
            'LSL'  : ['11010011011', '<<'],
            'LSR'  : ['11010011010', '>>'],
            'CBZ'  : ['10110100'],
            'CBNZ' : ['10110101'],
            'B'    : ['000101']
        }

        # [31:0] == [MSB:LSB]
        machine_code = OPCODES[instruction_list[0]][0]
        print('\n------- C Interpretation -------')
        if (instruction_list[0] == 'LDUR' or instruction_list[0] == 'STUR'): # D-Type

            dt_address = 0 if len(instruction_list) < 4 else int(''.join(filter(str.isdigit, instruction_list[3])))
            op = '00'
            rn = int(''.join(filter(str.isdigit, instruction_list[2])))
            rt = int(''.join(filter(str.isdigit, instruction_list[1])))

            if (instruction_list[0] == 'LDUR'): # LDUR

                print('Register[' + str(rt) + '] = RAM[ Register[' + str(rn) + ']' + ('' if len(instruction_list) < 4 else (' + ' + str(dt_address))) + ' ]')
                machine_code += str(bin(dt_address)[2:].zfill(9))+ op + str(bin(rn)[2:].zfill(5)) + str(bin(rt)[2:].zfill(5))
            else: # STUR

                print('RAM[ Register[' + str(rn) + ']' + ('' if len(instruction_list) < 4 else (' + ' + str(dt_address))) + ' ] = Register[' + str(rt) + ']')
                machine_code += str(bin(dt_address)[2:].zfill(9))+ op + str(bin(rn)[2:].zfill(5)) + str(bin(rt)[2:].zfill(5))

        elif (instruction_list[0] == 'ADD' or instruction_list[0] == 'SUB' or
            instruction_list[0] == 'ORR' or instruction_list[0] == 'AND' or
            instruction_list[0] == 'EOR'): # R-Type

            rm = int(''.join(filter(str.isdigit, instruction_list[3])))
            shamt = '000000'
            rn = int(''.join(filter(str.isdigit, instruction_list[2])))
            rd = int(''.join(filter(str.isdigit, instruction_list[1])))
            print('Register[' + str(rd) + '] = Register[' + str(rn) + '] ' + OPCODES[instruction_list[0]][1] + ' Register[' + str(rm) + ']')
            machine_code += str(bin(rm)[2:].zfill(5)) + shamt + str(bin(rn)[2:].zfill(5)) + str(bin(rd)[2:].zfill(5))

        elif (instruction_list[0] == 'LSL' or instruction_list[0] == 'LSR'):

            rm = '00000'
            shamt = int(''.join(filter(str.isdigit, instruction_list[3])))
            rn = int(''.join(filter(str.isdigit, instruction_list[2])))
            rd = int(''.join(filter(str.isdigit, instruction_list[1])))
            print('Register[' + str(rd) + '] = Register[' + str(rn) + '] ' + OPCODES[instruction_list[0]][1] + ' '+  str(shamt) )
            machine_code += rm + str(bin(shamt)[2:].zfill(6)) + str(bin(rn)[2:].zfill(5)) + str(bin(rd)[2:].zfill(5))

        elif (instruction_list[0] == 'B'): # B-Type
            if(int(instruction_list[1]) < 0):
                br_address = int(''.join(instruction_list[1]))
                print('PC = PC + ' + '(' + str(br_address) + ')')
                machine_code += str(bin(br_address & int("1"*26, 2))[2:])
            else:
                br_address = int(''.join(filter(str.isdigit, instruction_list[1])))
                print('PC = + ' + '(' + str(br_address) + ')')
                machine_code += str(bin(br_address)[2:].zfill(26))

        elif (instruction_list[0] == 'CBZ'): # CB-Type

            if(int(instruction_list[2]) < 0):
                cond_br_address = int(''.join(instruction_list[2]))
                rt = int(''.join(filter(str.isdigit, instruction_list[1])))
                print('if ( Register[' + str(rt) + '] == 0 ) { PC = PC + ' + '(' + str(cond_br_address) + ')' + ' }')
                print('else { PC++ }')
                machine_code += str(bin(cond_br_address & int("1"*19, 2))[2:]) + str(bin(rt)[2:].zfill(5))
            else:
                cond_br_address = int(''.join(filter(str.isdigit, instruction_list[2])))
                rt = int(''.join(filter(str.isdigit, instruction_list[1])))
                print('if ( Register[' + str(rt) + '] == 0 ) { PC = PC + ' + '(' + str(cond_br_address) + ')' + ' }')
                print('else { PC++ }')
                machine_code += str(bin(cond_br_address)[2:].zfill(19)) + str(bin(rt)[2:].zfill(5))

        elif (instruction_list[0] == 'CBNZ'):
            if(int(instruction_list[2]) < 0):
                cond_br_address = int(''.join(instruction_list[2]))
                rt = int(''.join(filter(str.isdigit, instruction_list[1])))
                print('if ( Register[' + str(rt) + '] =! 0 ) { PC = PC + ' + '(' + str(cond_br_address) + ')' + ' }')
                print('else { PC++ }')
                machine_code += str(bin(cond_br_address & int("1"*19, 2))[2:]) + str(bin(rt)[2:].zfill(5))
            else:
                cond_br_address = int(''.join(filter(str.isdigit, instruction_list[2])))
                rt = int(''.join(filter(str.isdigit, instruction_list[1])))
                print('if ( Register[' + str(rt) + '] =! 0 ) { PC = PC + ' + '(' + str(cond_br_address) + ')' + ' }')
                print('else { PC++ }')
                machine_code += str(bin(cond_br_address)[2:].zfill(19)) + str(bin(rt)[2:].zfill(5))

        else:
            raise RuntimeError('OPCODE (' + instruction_list[0] + ') not supported')

        # Output the machine code representation of the input
        print('\n------- Machine Code (' + str(len(machine_code)) + '-bits) -------')
        print('BINARY : ' + machine_code)
        print('HEX    : ' + str(hex(int(machine_code, 2)))[2:])
        print('')

# Say goodbye to the user
print()
print("Thanks! Bye")
