# Saturated Reverse Polish Calculator #

import math

stack = []
commenting = False
operators = ["^", "/", "*", "+", "-", "%"]
r_numbers = [1804289383,
              846930886,
              1681692777,
              1714636915,
              1957747793,
              424238335,
              719885386,
              1649760492,
              596516649,
              1189641421,
              1025202362,
              1350490027,
              783368690,
              1102520059,
              2044897763,
              1967513926,
              1365180540,
              1540383426,
              304089172,
              1303455736,
              35005211,
              521595368,
              1804289383 ]

# Set up template for binary tree used for single line observations
class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        if self.left is None:
            self.left = Node(data)
        else:
            self.right = Node(data)

    def in_order_traversal(self, root):
        res = []

        if root:
            res = self.in_order_traversal(root.left)
            res.append(root.data)
            res = res + self.in_order_traversal(root.right)

        return res

# Takes any input and returns the saturated value
def saturate(result):
    newresult = result

    if result > (2 ** 31) - 1:
        newresult = (2 ** 31) - 1
    elif result < (2 ** 31) * -1:
        newresult = (2 ** 31) * -1

    return newresult

# Converts any octal input into decimal
def octalToDecimal(number):
    num_str = str(number)
    total = 0

    if num_str == "08":
        return 8
    elif num_str == "09":
        return 9

    for character in num_str:
        if not is_number(character):
            return None

        if int(character) > 7:
            return (2 ** 31) * -1
        
        total *= 8
        total += int(character)

    return total

# Performs arithmetic on two operands given an opcode
def perform_arithmetic(operand1, operand2, operator, stack_scope = stack):
    if str(operand1)[0:1] == "0" and str(operand1)[1:2] != ".":
        operand1 = octalToDecimal(operand1)

    if str(operand2)[0:1] == "0" and str(operand2)[1:2] != ".":
        operand2 = octalToDecimal(operand2)

    if operator == "+":
        stack_scope.append(saturate(operand1 + operand2))
    elif operator == "-":
        stack_scope.append(saturate(operand2 - operand1))
    elif operator == "/":
        if operand1 == 0:
            print("Divide by 0.")
            return

        # Division can return values of type float.
        # In the SRPN calculator we are reproducing, values
        # must be of type int.
        stack_scope.append(saturate(int(operand2 / operand1)))
    elif operator == "%":
        operand1 = abs(operand1)
        operand2 = abs(operand2)

        result = saturate(operand2 % operand1)

        stack_scope.append(result)
    elif operator == "*":
        stack_scope.append(saturate(operand1 * operand2))
    elif operator == "^":
        if operand1 < 0:
            print("Negative power.")
            stack_scope.append(operand2)
            stack_scope.append(operand1)
        else:
            stack_scope.append(saturate(operand2 ** operand1))

# Returns whether or not the input can be converted into integer format
def is_number(number):
    try:
        if "+" in str(number):
            return False

        if "." in str(number):
            location = str(number).find(".")
            number = str(number)[:location] + str(number)[location + 1:]

        int(number)
        return True
    except:
        return False

# Takes an input and removes unnecessary operators
def remove_characters(number):
    new_number = ""

    for character in number:
        if character in operators:
            new_number = new_number + character
            continue
            
        if is_number(character):
            new_number = new_number + character
            continue

        if character == "d" or character == "=":
            new_number = new_number + character
            continue

        if character == "r":
            r_number = r_numbers.pop(0)
            r_numbers.append(r_number)

            new_number = new_number + str(r_number)
            continue

        if character == " " or character == ".":
            new_number = new_number + character
            continue

        print("Unknown operator or operand \"" + character + "\"")

    return new_number

# Prints out a section of a single line input defined by the position of
# the print identifier 
def print_section(number, stack_scope = stack):
    location = str(number).find("d")

    print_statement = assess_non_number(number[:location], stack_scope = stack_scope)
    if print_statement is not None:
        print(int(math.floor(float(print_statement))))
        process_command(str(print_statement), stack_scope, True)
            
    number = number[location + 1:]
    result = assess_non_number(number, stack_scope = stack_scope)
    return result

# If a command is concatenated, create a binary tree to deal with the different parts of the command
def assess_non_number(number, head_node = None, stack_scope = stack):
    number = remove_characters(number)

    if head_node is None:
        if number == "":
            return None

        head_node = Node(number)

    if "d" in str(number):
        return print_section(number)

    if not is_number(head_node.data):
        # if "=" in str(head_node.data):
        #     location = str(head_node.data).find("=")

        #     if location == 0:
        #         print("Stack empty.")
        #     else:
        #         if location != len(head_node.data) - 1:
        #             head_node.data = str(head_node.data[:location]) + str(head_node.data[location + 1:])
        #         else:
        #             head_node.data = str(head_node.data[:location])

        #         location -= 1

        #         printing = ""
        #         order10 = 0

        #         while not is_number(str(head_node.data)[location]) and location >= 0:
        #             location -= 1

        #         if location < 0:
        #             print("Stack empty.")

        #         else:
        #             while location >= 0 and is_number(str(head_node.data)[location]):
        #                 printing = str(head_node.data)[location] + printing
        #                 location -= 1
        #                 order10 += 1

        #             result = saturate(int(printing))
        #             print(result)

        for i in range (0, len(operators)):
            operator = operators[len(operators) - i - 1]
            if operator in str(head_node.data):
                location = head_node.data.find(operator)

                if location == 0 and operator == "-":
                    if len(str(head_node.data)) == 1:
                        print("Stack underflow.")
                        return None
                    elif not is_number(str(head_node.data)[1]):
                        print("Stack underflow.")
                        head_node.data = str(head_node.data[1:])

                    continue

                left_hand_side = head_node.data[:location]
                right_hand_side = head_node.data[location + len(operator):]

                head_node.left = Node(left_hand_side)
                head_node.right = Node(right_hand_side)
              
                if head_node.left.data == "":
                    if len(stack_scope) > 0:
                        head_node.left.data = stack_scope.pop()
                    else:
                        print("Stack underflow.")
                        head_node.data = head_node.right.data
                        head_node.left = None
                        head_node.right = None
                        continue
                
                if head_node.right.data == "":
                    if len(stack_scope) > 0:
                        head_node.right.data = stack_scope.pop()
                    else:
                        print("Stack underflow.")
                        head_node.data = head_node.left.data
                        head_node.left = None
                        head_node.right = None
                        continue

                head_node.data = operator

                if not is_number(head_node.left.data):
                    assess_non_number(head_node.left.data, head_node.left, stack_scope = stack_scope)

                if not is_number(head_node.right.data):
                    assess_non_number(head_node.right.data, head_node.right, stack_scope = stack_scope)

                if is_number(head_node.left.data) and is_number(head_node.right.data):
                    if head_node.data == "^":
                        head_node.data = "**"
                    
                    if str(head_node.left.data)[0:1] == "0":
                        head_node.left.data = octalToDecimal(head_node.left.data)

                    if str(head_node.right.data)[0:1] == "0":
                        head_node.right.data = octalToDecimal(head_node.right.data)

                    left_data = saturate(float(head_node.left.data))
                    right_data = saturate(float(head_node.right.data))

                    head_node.data = eval(str(left_data) + head_node.data + str(right_data))
                    head_node.left = None
                    head_node.right = None

    return head_node.in_order_traversal(head_node)[0]

# Takes in a command from the input alphabet and acts accordingly
def process_command(command, stack_scope = stack, is_decimal = False):
    global commenting
    
    if command == "#":
        commenting = not commenting
        return None

    if commenting:
        return None

    elif len(command.split()) > 1:

        local_stack = []

        for element in command.split():
            pc = process_command(str(element), local_stack)

            if pc != None:
                print(str(pc))

        for element in local_stack:
            process_command(str(element), stack_scope, True)
            

    elif command in operators:
        if len(stack_scope) < 2:
            print("Stack underflow.")
            return None

        operand1 = stack_scope.pop()
        operand2 = stack_scope.pop()

        perform_arithmetic(float(operand1), float(operand2), command, stack_scope)

    elif command == "=":
        if len(stack_scope) == 0:
          return "Stack empty."

        return int(math.floor(stack_scope[len(stack_scope) - 1]))

    elif command == "d":
        if len(stack_scope) == 0:
            print(-1 * 2 ** 31)

        for element in stack_scope:
            print(int(math.floor(float(element))))

        return None

    elif command == "r":
        r_number = r_numbers.pop(0)
        r_numbers.append(r_number)

        process_command(str(saturate(r_number)), stack_scope)

    elif command == " ":
        return None

    elif command.__contains__(".") and not is_decimal:
        position = command.find(".")

        print("Unrecognised operator or operand \".\".")

        mantissa = command[0:position]
        exponent = command[position + 1:]

        if is_number(mantissa):
            mantissa = saturate(int(mantissa))
            process_command(str(mantissa), stack_scope)
        else:
            result = assess_non_number(mantissa, stack_scope = stack_scope)

            if len(stack_scope) > 22:
                print("Stack overflow.")
                return None
                    
            if result == "":
                return None

            stack_scope.append(str(result))

        if is_number(exponent):
            exponent = saturate(int(exponent))
            process_command(str(exponent), stack_scope)
        else:
            result = assess_non_number(exponent, stack_scope = stack_scope)
            
            if result is not None:
                if len(stack_scope) > 22:
                    print("Stack overflow.")
                    return None

                if result == "":
                    return None

                stack_scope.append(str(result))

    elif not is_number(command):
        location = 0
        adjusted = False
        while command[location] == "-":
            adjusted = True
            print("Stack underflow.")
            location += 1

        command = command[location:]

        if not is_number(command) and adjusted:
            return process_command(str(command), stack_scope)

        result = assess_non_number(command, stack_scope = stack_scope)
        if result is not None:
            if len(stack_scope) > 22:
                print("Stack overflow.")
                return None
                    
            if result == "":
                return None

            stack_scope.append(str(result))

    elif len(stack_scope) > 22:
        print("Stack overflow.")
        return None

    else:
        if command[0:1] == "0":
            octal = saturate(float(octalToDecimal(command)))
            stack_scope.append(saturate(octal))
        else:
            stack_scope.append(saturate(float(command)))


#This is the entry point for the program.
#Do not edit the below
if __name__ == "__main__":
    while True:
        try:
            cmd = input()
            pc = process_command(cmd)
            if pc != None:
                print(str(pc))
        except Exception as e:
            # print(e)
            exit()
