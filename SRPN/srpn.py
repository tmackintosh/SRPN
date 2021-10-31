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
        int(number)
        return True
    except:
        return False


def assess_non_number(number, local_stack = []):
    if len(number) == 1:
        print("Unrecognised operator or operand \"" + number + "\".")
        return None

    for operator in operators:
        while operator in number:
            location = number.find(operator)

            remaining = number[location + 1:]
            
            while operator in remaining:
                location = remaining.find(operator)
                
                if location == 0:
                    location = remaining[1:].find(operator)

                remaining = remaining[location + 1:]

            operand1 = None
            operand2 = None

            operand1Finished = False
            operand2Finished = False

            operand1Length = 0
            operand2Length = 0

            operand1Negative = False
            operand2Negative = False

            operand1Octal = False
            operand2Octal = False

            count = 0

            while not operand1Finished or not operand2Finished:
                count += 1

                if not operand1Finished:

                    cursor = location - count
                    character = number[cursor:cursor + 1]

                    if is_number(character):
                        if character == "0":
                            operand1Octal = True
                        else:
                            operand1Octal = False

                        operand1Length += 1

                        if operand1 is None:
                            operand1 = int(character)
                        else:
                            operand1 += int(character) * (10 ** (count - 1))
                    elif character == "n":
                        operand1Negative = True
                        operand1Finished = True
                    else:
                        operand1Finished = True

                if not operand2Finished:
                    cursor = location + count
                    character = number[cursor:cursor + 1]

                    if is_number(character):
                        operand2Length += 1

                        if count == 1 and character == "0":
                            operand2Octal = True
                            continue

                        if operand2 is None:
                            operand2 = int(character)
                        else:
                            operand2 *= 10
                            operand2 += int(character)
                    elif count == 1 and character == "n":
                            operand2Negative = True
                    else:
                        operand2Finished = True

            if operand1Length == 0 and operand2Length == 0:
                print("Stack underflow.")
                number.replace(operator, "", 1)

            if operator == "-" and operand1Length == 0:
                  number = number.replace("-", "n", 1)
                  continue

            if operand1Negative:
                operand1 *= -1

            if operand2Negative:
                operand2 *= -1

            if operand1Octal:
                operand1 = octalToDecimal(operand1)

            if operand2Octal:
                operand2 = octalToDecimal(operand2)

            perform_arithmetic(operand2, operand1, operator, local_stack)
            value = local_stack.pop()
            
            arithmetic_substring = number[location - operand1Length: location + operand2Length + 1]
            number = number.replace(arithmetic_substring, str(value))


    #
    # Submit this if unsuccessful
    #
    
    currentOperand = None
    currentOperandNegative = False

    for element in number:
        # Below is added in

        if is_number(element):
            if currentOperand is None:
                currentOperand = 0
            
            currentOperand *= 10
            currentOperand += int(element)
            continue
        elif element == "n":
            if currentOperand is None:
                currentOperandNegative = True
                continue
            else:
                if currentOperandNegative:
                    currentOperand *= 1

                local_stack.append(currentOperand)
                currentOperand = None
                currentOperandNegative = False
                continue

        elif element == ")" and currentOperand is not None:
            if currentOperandNegative:
                currentOperand *= -1

            local_stack.append(currentOperand)
            currentOperand = None
            currentOperandNegative = False
            continue
        elif element == "(":
            continue

        if currentOperand is not None:
            if currentOperandNegative:
                currentOperand *= -1

            local_stack.append(currentOperand)
            currentOperand = None
            currentOperandNegative = False

        # Above is added in
        pc = process_command(element, local_stack)

        if pc is not None:
            print(str(pc))

    if currentOperand is not None:
        if currentOperandNegative:
            currentOperand *= -1

        local_stack.append(currentOperand)
        currentOperand = None
        currentOperandNegative = False

    for element in local_stack:
        stack.append(element)

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
            assess_non_number(mantissa)

        if is_number(exponent):
            exponent = saturate(int(exponent))
            stack_scope.append(exponent)
        else:
            assess_non_number(exponent)

    elif not is_number(command):
        assess_non_number(command)

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
