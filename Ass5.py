import re

def precedence(op):
    if op in ('+', '-'):
        return 1
    elif op in ('*', '/'):
        return 2
    return 0

def infix_to_postfix(expr):
    stack = []
    output = []

    tokens = re.findall(r'\w+|[-+*/()]', expr)
    print(tokens)
    for token in tokens:
        if token.isalnum(): # If token is variable or number , Directy push it to output
            output.append(token)

        elif token == '(': # If token is '(', push it to stack
            stack.append(token)

        elif token == ')': # If token is ')', pop all the operators from stack until '(' is found
            while stack and stack[-1] != '(': # Pop until '(' is found
                output.append(stack.pop()) # Pop the operator from stack and add it to output
            stack.pop() # Pop the '(' from stack

        else: # If token is an operator
            while stack and precedence(stack[-1]) >= precedence(token): # Pop all the operators from stack until '(' is found or precedence is less than
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return output


expr = input("Enter Expression (Example A=B+C*D): ")

left, right = expr.split('=')

postfix = infix_to_postfix(right)

stack = []
temp = 1

print("\nThree Address Code:")

for token in postfix:
    if token.isalnum():
        stack.append(token)
    else:
        op2 = stack.pop()
        op1 = stack.pop()

        t = f"T{temp}"
        temp += 1

        print(f"{t} = {op1} {token} {op2}")
        stack.append(t)

print(f"{left} = {stack.pop()}")
