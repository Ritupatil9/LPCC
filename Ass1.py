# Two Pass Assembler
import re
machine_instructions = {
    "STOP",
    "ADD",
    "SUB",
    "MULT",
    "MOVER",
    "MOVEM",
    "COMP",
    "BC",
    "DIV",
    "READ",
    "PRINT"
}
assembler_directives = {"START", "ORIGIN", "EQU", "LTORG", "END", "DS", "DC"}


symtab = {}
littab = []
pooltab = [1]
IC = []

lc = 0
lc_add = []
symbol= []
littab = []

with open("input.txt", "r") as file:
    lines = file.readlines()

all_tokens = []

for line in lines:
    # remove newline + strip spaces
    line = line.strip()
    
    # extract words (removes punctuation automatically)
    tokens = re.findall(r'\b\w+\b|[=+\-*]', line)
    
    all_tokens.append(tokens)

# print result
for t in all_tokens:
    print(t)

for i in all_tokens:
    if not i:
        continue
        
    
    if 'START' in i:
        lc = int(i[i.index('START') + 1])
        continue

    # Ensure label is added to symbol table before processing rest of line
    if i[0] not in assembler_directives and i[0] not in machine_instructions:
        symtab[i[0]] = lc

    if '=' in i:
       literal = i[-1]
       littab.append([literal, -1])
        
    if 'LTORG' in i:
        if littab:
            start_idx = pooltab[-1] - 1
            for lit_idx in range(start_idx, len(littab)):
                if littab[lit_idx][1] == -1:
                    littab[lit_idx][1] = lc
                    lc_add.append(lc)
                    lc += 1
            pooltab.append(len(littab) + 1)
        continue

    if 'END' in i:
        if littab:
            start_idx = pooltab[-1] - 1
            for lit_idx in range(start_idx, len(littab)):
                if littab[lit_idx][1] == -1:
                    littab[lit_idx][1] = lc
                    lc_add.append(lc)
                    lc += 1
        break
        
    # Increment LC appropriately
    if 'DS' in i:
        # Increment by the integer value following 'DS'
        lc += int(i[i.index('DS') + 1]) - 1

    if 'ORIGIN' in i :
        idx = i.index('ORIGIN') + 1
        if i[idx] in symtab :
            if len(i) > idx + 1:
                if i[idx+1] == "+":
                    lc = symtab[i[idx]] + int(i[idx+2])
                elif i[idx+1] == "-":
                    lc = symtab[i[idx]] - int(i[idx+2])
                elif i[idx+1] == "*":
                    lc = symtab[i[idx]] * int(i[idx+2])
                elif i[idx+1] == "/":
                    lc = symtab[i[idx]] / int(i[idx+2])
                else:
                    lc = symtab[i[idx]]
            else:
                lc = symtab[i[idx]]
        else :
            lc = int(i[idx])
        continue

    lc_add.append(lc)
    lc += 1
    
 
    

    

print("Location Counters:")
print(lc_add)
print("Symbol Table:")
print(symtab)
print("Literal Table:")
print(littab)
print("Pool Table:")
print(pooltab)
