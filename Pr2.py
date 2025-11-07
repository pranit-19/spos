# ------------------------------
# PASS-II of Two-Pass Assembler (Fixed Version)
# ------------------------------

import re

# Symbol table (from Pass-I)
symbol_table = {
    "X": 214,
    "L1": 202,
    "NEXT": 207,
    "BACK": 202
}

# Literal table (from Pass-I)
literal_table = {
    1: 205,
    2: 206,
    3: 210,
    4: 211,
    5: 215
}

# Intermediate Code
intermediate_code = [
    "(AD,01) (C,200)",
    "(IS,04) 1 (L,1)",
    "(IS,05) 1 (S,1)",
    "(IS,04) 2 (L,2)",
    "(AD,03) (S,2)+3",
    "(AD,05)",
    "(L,1)",
    "(L,2)",
    "(IS,01) 1 (L,3)",
    "(IS,02) 2 (L,4)",
    "(IS,07) 1 (S,4)",
    "(AD,05)",
    "(L,3)",
    "(L,4)",
    "(AD,04) (S,2)",
    "(IS,03) 3 (L,5)",
    "(IS,00)",
    "(DL,02) (C,1)",
    "(AD,02)"
]

# Opcode to mnemonic mapping
opcode_table = {
    "04": "MOVER",
    "05": "MOVEM",
    "01": "ADD",
    "02": "SUB",
    "03": "MULT",
    "07": "DIV",
    "00": "STOP"
}

register_map = {"1": "AREG", "2": "BREG", "3": "CREG"}

# ------------------------------
# PASS II Logic
# ------------------------------

lc = 200
machine_code = []

for line in intermediate_code:
    line = line.strip()

    # Ignore Assembler Directives
    if not line or "(AD" in line:
        continue

    # Handle Declarative (DS)
    if "(DL,02)" in line:
        machine_code.append(f"{lc}  --- (Data Space Reserved)")
        lc += 1
        continue

    # Handle Declarative (DC)
    if "(DL,01)" in line:
        value = re.search(r"\(C,(\d+)\)", line)
        const = value.group(1) if value else "0"
        machine_code.append(f"{lc}  00  0  {const}")
        lc += 1
        continue

    # Handle Imperative Statements
    if "(IS" in line:
        parts = re.findall(r"\(IS,(\d+)\)|(\d)|\(L,(\d+)\)|\(S,(\d+)\)", line)
        # parts gives tuples like [('04','','',''), ('','1','',''), ('','','1','')]
        opcode, reg, mem = "00", "0", "000"

        for p in parts:
            if p[0]:  # IS opcode
                opcode = p[0]
            elif p[1]:  # Register
                reg = p[1]
            elif p[2]:  # Literal
                lit_index = int(p[2])
                mem = literal_table.get(lit_index, 0)
            elif p[3]:  # Symbol
                sym_index = int(p[3])
                # In this example, symbols are indexed by appearance order (X=1, L1=2, NEXT=3, BACK=4)
                sym_list = list(symbol_table.values())
                if sym_index <= len(sym_list):
                    mem = sym_list[sym_index - 1]

        machine_code.append(f"{lc}  {opcode}  {reg}  {mem}")
        lc += 1

# ------------------------------
# OUTPUT
# ------------------------------
print("---- MACHINE CODE (PASS II OUTPUT) ----")
for code in machine_code:
    print(code)
