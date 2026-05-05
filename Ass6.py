# Ass 6 code optimization

import re   # (Not used here, but generally used for pattern matching)

# Function to check if a value is a number
def is_number(x):
    try:
        float(x)     # Try converting to float
        return True  # If success → it is a number
    except:
        return False # If error → not a number


# -------- Read input --------
with open("tac.txt") as f:   # Open file tac.txt in read mode
    lines = []               # List to store cleaned lines

    for line in f:           # Read file line by line
        line = line.strip()  # Remove spaces and newline characters

        if not line:         # If line is empty
            continue         # Skip it

        line = line.replace(";", "")  # Remove semicolons (;)
        lines.append(line)            # Store cleaned line


# Dictionary to store variable values (for propagation)
values = {}

# List to store final optimized code
optimized = []

# Dictionary for Common Subexpression Elimination (CSE)
expr_table = {}   # Stores expressions already computed


# -------- Optimization --------
for line in lines:           # Process each line
    parts = line.split()     # Split line into tokens

    # Case: a = 5   (simple assignment)
    if len(parts) == 3:
        var = parts[0]   # variable name (a)
        val = parts[2]   # value (5)

        # Constant Propagation
        # If val already has a known value, replace it
        if val in values:
            val = values[val]

        values[var] = val                    # Store value of variable
        optimized.append(f"{var} = {val}")   # Add optimized line


    # Case: a = b op c   (expression)
    elif len(parts) == 5:
        var = parts[0]   # result variable (a)
        op1 = parts[2]   # first operand (b)
        op = parts[3]    # operator (+, -, *, /)
        op2 = parts[4]   # second operand (c)

        # -------- Constant Propagation --------
        # Replace operands with known values if available
        if op1 in values:
            op1 = values[op1]
        if op2 in values:
            op2 = values[op2]

        expr = f"{op1} {op} {op2}"  # Form expression string

        # 🔥 Common Subexpression Elimination (CSE)
        # If this expression was already computed before
        if expr in expr_table:
            prev = expr_table[expr]                 # Get previous variable
            optimized.append(f"{var} = {prev}")     # Reuse old result
            values[var] = prev                      # Update value table
            continue                               # Skip further processing
        else:
            expr_table[expr] = var  # Store new expression

        # -------- Constant Folding --------
        # If both operands are numbers → evaluate directly
        if is_number(op1) and is_number(op2):

            if op == '+': 
                res = float(op1) + float(op2)
            elif op == '-': 
                res = float(op1) - float(op2)
            elif op == '*': 
                res = float(op1) * float(op2)
            elif op == '/': 
                res = float(op1) / float(op2)

            # Convert result to int if possible (like 5.0 → 5)
            res = str(int(res) if res.is_integer() else res)

            values[var] = res                    # Store result
            optimized.append(f"{var} = {res}")   # Add optimized line

        # -------- Algebraic Simplification --------
        # Example: a = b + 0 → a = b
        elif op == '+' and op2 == '0':
            values[var] = op1
            optimized.append(f"{var} = {op1}")

        # Example: a = b * 1 → a = b
        elif op == '*' and op2 == '1':
            values[var] = op1
            optimized.append(f"{var} = {op1}")

        # -------- Default Case --------
        else:
            values[var] = var   # No optimization possible
            optimized.append(f"{var} = {op1} {op} {op2}")


# -------- Output --------
print("\nOptimized Code:\n")

for line in optimized:   # Print each optimized line
    print(line)
