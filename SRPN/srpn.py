# Saturated Reverse Polish Calculator #

stack = []
commenting = False
operators = ["/", "*", "+", "-", "%", "^"]
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

    for character in num_str:
        if not is_number(character):
            return None

        if int(character) > 7:
            return None
        
        total *= 8
        total += int(character)

    return total

# Performs arithmetic on two operands given an opcode
def perform_arithmetic(operand1, operand2, operator, stack_scope = stack):
    if str(operand1)[0:1] == "0":
        operand1 = octalToDecimal(operand1)

    if str(operand2)[0:1] == "0":
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
        stack_scope.append(saturate(operand2 % operand1))
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

        int(number)
        return True
    except:
        return False

# If a command is concatenated, create a binary tree to deal with the different parts of the command
def assess_non_number(number, head_node = None):
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

        if character == " ":
            new_number = new_number + " "
            continue

        print("Unknown operator or operand \"" + character + "\"")

    number = new_number

    if head_node is None:
        if number == "":
            return None

        head_node = Node(number)

    if "d" in str(number):
        location = str(number).find("d")

        print_statement = assess_non_number(number[:location])
        if print_statement is not None:
            print(print_statement)
        
        number = str(print_statement) + number[location + 1:]
        return assess_non_number(number)

    if not is_number(head_node.data):
        if "=" in str(head_node.data):
            # location = str(head_node.data).find("=")

            # if location == len(str(head_node.data)) - 1:
            #     if is_number(str(head_node.data)[:location]):
            #         print(str(head_node.data)[:location])
            #         head_node.data = str(head_node.data)[:location]
            #     else:
            #         number_to_print = str(head_node.data[:location])

            #         result = assess_non_number(number_to_print)

            #         print(result)

            #         return result

            location = str(head_node.data).find("=")

            if location == 0:
                print("Stack empty.")
            else:
                head_node.data = str(head_node.data[:location]) + str(head_node.data[location + 1:])
                location -= 1

                printing = 0
                order10 = 0

                while not is_number(str(head_node.data)[location]):
                    location -= 1

                while is_number(str(head_node.data)[location]):
                    printing += int(str(head_node.data[location])) * (10 ** order10)
                    head_node.data = str(head_node.data[:location]) + str(head_node.data[location + 1:])
                    location -= 1
                    order10 += 1

                print(printing)

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
                    print("Stack underflow.")
                    head_node.data = head_node.right.data
                    head_node.left = None
                    head_node.right = None
                    continue
                
                if head_node.right.data == "":
                    print("Stack underflow.")
                    head_node.data = head_node.left.data
                    head_node.left = None
                    head_node.right = None
                    continue

                head_node.data = operator

                if not is_number(head_node.left.data):
                    assess_non_number(head_node.left.data, head_node.left)

                if not is_number(head_node.right.data):
                    assess_non_number(head_node.right.data, head_node.right)

                if is_number(head_node.left.data) and is_number(head_node.right.data):
                    if head_node.data == "^":
                        head_node.data = "**"
                    
                    if str(head_node.left.data)[0:1] == "0":
                        head_node.left.data = octalToDecimal(head_node.left.data)

                    if str(head_node.right.data)[0:1] == "0":
                        head_node.right.data = octalToDecimal(head_node.right.data)

                    left_data = saturate(int(head_node.left.data))
                    right_data = saturate(int(head_node.right.data))

                    head_node.data = eval(str(left_data) + head_node.data + str(right_data))
                    head_node.left = None
                    head_node.right = None

    return head_node.in_order_traversal(head_node)[0]

# Takes in a command from the input alphabet and acts accordingly
def process_command(command, stack_scope = stack):
    global commenting
    
    if command == "#":
        commenting = not commenting
        return None

    if commenting:
        return None

    elif len(command.split()) > 1:

        local_stack = []

        for element in command.split():
            pc = process_command(element, local_stack)

            if pc != None:
                print(str(pc))

        for element in local_stack:
            stack_scope.append(element)
            

    elif command in operators:
        if len(stack_scope) < 2:
            print("Stack underflow.")
            return None

        operand1 = stack_scope.pop()
        operand2 = stack_scope.pop()

        perform_arithmetic(operand1, operand2, command, stack_scope)

    elif command == "=":
        if len(stack_scope) == 0:
          return "Stack empty."

        return stack_scope[len(stack_scope) - 1]

    elif command == "d":
        if len(stack_scope) == 0:
            print(-1 * 2 ** 31)

        for element in stack_scope:
            print(element)

        return None

    elif command == "r":
        r_number = r_numbers.pop(0)
        r_numbers.append(r_number)

        stack_scope.append(saturate(r_number))

    elif command == " ":
        return None

    elif command.__contains__("."):
        position = command.find(".")

        mantissa = command[0:position]
        exponent = command[position + 1:]

        if is_number(mantissa):
            mantissa = saturate(int(mantissa))
            stack_scope.append(mantissa)
        else:
            result = assess_non_number(mantissa)

            if result is not None:
                stack_scope.append(result)

        if is_number(exponent):
            exponent = saturate(int(exponent))
            stack_scope.append(exponent)
        else:
            result = assess_non_number(exponent)
            
            if result is not None:
                stack_scope.append(assess_non_number(exponent))

    elif not is_number(command):
        location = 0
        adjusted = False
        while command[location] == "-":
            adjusted = True
            print("Stack underflow.")
            location += 1

        command = command[location:]

        if not is_number(command) and adjusted:
            return process_command(command, stack_scope)

        result = assess_non_number(command)
        if result is not None:
            stack_scope.append(result)

    elif len(stack_scope) > 22:
        print("Stack overflow.")
        return None

    else:
        if command[0:1] == "0":
            octal = octalToDecimal(saturate(int(command)))
            stack_scope.append(saturate(octal))
        else:
            stack_scope.append(saturate(int(command)))


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
