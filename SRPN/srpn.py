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
    # Initialize object as branch node
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    # Add children to binary tree
    def insert(self, data):
        # Always fill from the left
        if self.left is None:
            self.left = Node(data)
        else:
            self.right = Node(data)

    # Return list of elements in order of binary tree
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

    # Edge cases observed
    if num_str == "08":
        return 8
    elif num_str == "09":
        return 9

    for character in num_str:
        if not is_number(character):
            return None

        # Return negative saturation when invalid octal is passed
        if int(character) > 7:
            return (2 ** 31) * -1
        
        # Increment through base-8 each character
        total *= 8
        total += int(character)

    return total

# Performs arithmetic on two operands given an opcode
def perform_arithmetic(operand1, operand2, operator, stack_scope = stack):
    # Make sure it's not a float <0 when assessing whether it's an octal or not
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
            return None

        stack_scope.append(saturate(float(operand2 / operand1)))

    elif operator == "%":
        operand1 = abs(operand1)
        operand2 = abs(operand2)

        if operand1 == 0:
            print("Divide by 0.")
            return None

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
    # Alternatively, ASCII analysis would be a better implementation here
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
    # Build up a new number as we analyse original number
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
        # When printing, we only print integers despite the numbers being stored as
        # float values
        print(int(math.floor(float(print_statement))))
        process_command(str(print_statement), stack_scope, True)
            
    number = number[location + 1:]
    result = assess_non_number(number, stack_scope = stack_scope)
    return result

# If we are printing something, we need to determine what to print
# and adjust the stack accordingly
def assess_print_command(head_node, stack_scope = stack):
  if "=" in str(head_node.data):
      location = str(head_node.data).find("=")
      originalLocation = location

      if location == 0:
          print("Stack empty.")
      else:
          if location != len(head_node.data) - 1:
              head_node.data = str(head_node.data[:location]) + str(head_node.data[location + 1:])
          else:
              head_node.data = str(head_node.data[:location])

          location -= 1

          printing = ""
          order10 = 0

          while not is_number(str(head_node.data)[location]) and location >= 0:
          
              location -= 1

          if location < 0:
              print("Stack empty.")

          else:
              while location >= 0 and is_number(str(head_node.data)[location]):
                  printing = str(head_node.data)[location] + printing
                  location -= 1
                  order10 += 1

              if printing[0:1] == "0":
                  printing = octalToDecimal(int(printing))

              result = saturate(int(printing))
              print(result)
              stack_scope.append(result)
                    
              length = originalLocation - location
              head_node.data = head_node.data[:location + 1] + head_node.data[location + length:]

              if head_node.data == "":
                  return None

# Use binary tree to determine when to complete an operation in accordance
# to BIDMAS rules
def assess_operator_on_non_number(head_node, stack_scope = stack):
  for i in range (0, len(operators)):
      operator = operators[len(operators) - i - 1]

      if operator in str(head_node.data):
          location = head_node.data.find(operator)

          # Functionality currently doesn't work for odd numbers
          # of "-" above 1
          if location == 0 and operator == "-":
              if len(str(head_node.data)) == 1:
                  print("Stack underflow.")
                  return None
              elif not is_number(str(head_node.data)[1]):
                  print("Stack underflow.")
                  head_node.data = str(head_node.data[1:])

              continue

          # Determine operands
          left_hand_side = head_node.data[:location]
          right_hand_side = head_node.data[location + len(operator):]

          head_node.left = Node(left_hand_side)
          head_node.right = Node(right_hand_side)
              
          if head_node.left.data == "":
              # If we're assessing no operands within the same command, check
              # whether there is a command already on the stack
              if len(stack_scope) > 0:
                  head_node.left.data = stack_scope.pop()
              else:
                  print("Stack underflow.")
                  # Remove redundant nodes and take up the filled node's data
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

          # Recursively create binary tree
          if not is_number(head_node.left.data):
              assess_non_number(head_node.left.data, head_node.left, stack_scope = stack_scope)

          if not is_number(head_node.right.data):
              assess_non_number(head_node.right.data, head_node.right, stack_scope = stack_scope)

          # When we're ready to perform the operation on 2 numbers
          if is_number(head_node.left.data) and is_number(head_node.right.data):
              if head_node.data == "^":
                  head_node.data = "**"
                    
              if str(head_node.left.data)[0:1] == "0" and str(head_node.left.data)[1:2] != ".":
                  head_node.left.data = octalToDecimal(head_node.left.data)

              if str(head_node.right.data)[0:1] == "0" and str(head_node.right.data)[1:2] != ".":
                  head_node.right.data = octalToDecimal(head_node.right.data)

              # Numbers can be stored in the stack as floats
              left_data = saturate(float(head_node.left.data))
              right_data = saturate(float(head_node.right.data))

              # Traverse up the tree having completed the operation
              head_node.data = eval(str(left_data) + head_node.data + str(right_data))
              head_node.left = None
              head_node.right = None

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
        assess_print_command(head_node, stack_scope)
        assess_operator_on_non_number(head_node, stack_scope)

    return head_node.in_order_traversal(head_node)[0]

# Takes in a command from the input alphabet and acts accordingly
def process_command(command, stack_scope = stack, is_decimal = False):
    global commenting
    
    if command == "#":
        commenting = not commenting
        return None

    # If multiple commands have been issued on the same input
    elif len(command.split()) > 1:

        local_stack = []

        for element in command.split():
            # Recursively call this function using a local stack
            pc = process_command(str(element), local_stack)

            if pc != None:
                print(str(pc))

        # When commands have been dealt with locally, append them to the global
        # stack
        for element in local_stack:
            if len(stack_scope) > 22:
                return None

            stack_scope.append(element)
    
    # Ignore all inputs when unclosed comment
    elif commenting:
        return None    

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

        # We only print out integer numbers
        # Elements of the stack are sometimes stored as strings for ease of analysis
        return int(math.floor(float(stack_scope[len(stack_scope) - 1])))

    elif command == "d":
        if len(stack_scope) == 0:
            print(-1 * 2 ** 31)

        for element in stack_scope:
            print(int(math.floor(float(element))))

        return None

    elif command == "r":
        # Cycle through the random numbers array
        r_number = r_numbers.pop(0)
        r_numbers.append(r_number)

        process_command(str(saturate(r_number)), stack_scope)

    elif command == " ":
        return None

    # Assess whether or not the dot is an input or the function has been
    # recursively called with a float-type command
    elif command.__contains__(".") and not is_decimal:
        position = command.find(".")

        print("Unrecognised operator or operand \".\".")

        # Floating point notation, doesn't make sense in the context of floating
        # points but imagine they are the values either side of the floating point
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

    # Stack has a maximum length of 22
    elif len(stack_scope) > 22:
        print("Stack overflow.")
        return None

    # Append number to the stack normally
    else:
        if command[0:1] == "0" and command[1:2] != ".":
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
        except:
            exit()
