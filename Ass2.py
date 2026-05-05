# Macro Processor (Final Version with Nested Macro Support)

mdt = []
mnt = {}
p = []

# Read input file
with open("macro.txt") as f:
    for line in f:
        p.append(line.strip())

# -------- PASS 1: Build MNT & MDT --------
i = 0
while i < len(p):
    if p[i] == "MACRO":
        i += 1
        name, *params = p[i].split()
        start = len(mdt)

        i += 1
        while p[i] != "MEND":
            mdt.append(p[i])
            i += 1

        mdt.append("MEND")
        mnt[name] = (params, start)

    i += 1


# -------- Recursive Function (for Nested Macros) --------
def expand(line):
    parts = line.split()

    if parts and parts[0] in mnt:
        params, start = mnt[parts[0]]
        mp = dict(zip(params, parts[1:]))

        j = start
        while mdt[j] != "MEND":
            temp = mdt[j]

            # Replace parameters
            for k in mp:
                temp = temp.replace(k, mp[k])

            expand(temp)   # 🔥 recursive call
            j += 1
    else:
        print(line)


# -------- PASS 2: Expand Macros --------
print("\nExpanded Code:\n")

i = 0
while i < len(p):
    if p[i] == "MACRO":
        while p[i] != "MEND":
            i += 1
    else:
        expand(p[i])

    i += 1


# -------- Print MNT --------
print("\nMNT:")
for k, v in mnt.items():
    print(k, v)

# -------- Print MDT --------
print("\nMDT:")
for idx, line in enumerate(mdt):
    print(idx, line)
