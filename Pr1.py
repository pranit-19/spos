# Simple Pass-I of a Two-Pass Assembler (Python)
# Works with the sample program provided by the user.
# Produces: intermediate code, symbol table, literal table, pool table.

import re

# --- Assembler Tables (simple) ---
IS = {               # Imperative Statements (opcode -> code)
    "STOP": "00",
    "ADD":  "01",
    "SUB":  "02",
    "MULT": "03",
    "MOVER":"04",
    "MOVEM":"05",
    "BC":   "06",
    "DIV":  "07",
    "COMP": "08",
    "READ": "09",
    "PRINT":"10",
}
AD = {               # Assembler Directives
    "START":"01",
    "END":"02",
    "ORIGIN":"03",
    "EQU":"04",
    "LTORG":"05",
}
DL = {               # Declarative Statements
    "DC":"01",
    "DS":"02",
}
REG = {              # Registers
    "AREG": "1",
    "BREG": "2",
    "CREG": "3",
    "DREG": "4",
}

# --- Helper functions ---
def normalize_quotes(s):
    # Convert unicode quotes to normal ascii single quote
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return s

def tokenize(line):
    # remove commas, normalize quotes, split by whitespace
    line = normalize_quotes(line).strip()
    # preserve ='<num>' as single token
    parts = re.split(r'\s+|,', line)
    parts = [p for p in parts if p != '' ]
    return parts

def is_literal(tok):
    # Matches ='<number>' or ="<number>"
    return bool(re.match(r"^=\'.+\'$|^=\".+\"$|^=\d+$", tok))

def literal_value(tok):
    # returns inner value of literal
    if tok.startswith("="):
        v = tok[1:]
        if v.startswith("'") and v.endswith("'"):
            return v[1:-1]
        if v.startswith('"') and v.endswith('"'):
            return v[1:-1]
        return v
    return tok

def eval_expr(expr, symtab):
    # Very simple expression evaluator: handles forms like SYMBOL, SYMBOL+num, num
    expr = normalize_quotes(expr)
    expr = expr.replace(" ", "")
    # if purely numeric
    if re.fullmatch(r"\d+", expr):
        return int(expr)
    # SYMBOL+NUM or SYMBOL-NUM
    m = re.match(r"([A-Za-z_]\w*)([+\-]\d+)$", expr)
    if m:
        sym = m.group(1)
        op = expr[len(sym)]
        num = int(expr[len(sym)+1:])
        if sym not in symtab or symtab[sym] is None:
            raise ValueError(f"Symbol '{sym}' not defined yet for expression '{expr}'")
        base = symtab[sym]
        return base + num if op == "+" else base - num
    # single symbol
    if expr in symtab:
        if symtab[expr] is None:
            raise ValueError(f"Symbol '{expr}' not defined yet for expression '{expr}'")
        return symtab[expr]
    raise ValueError(f"Unable to evaluate expression '{expr}'")

# --- Main Pass-I implementation ---
def pass_one(lines):
    lc = 0
    intermediate = []          # list of tuples: (lc, list_of_code_tokens)
    symtab = {}                # symbol -> address (None if undefined)
    littab = []                # list of dicts: {'literal': "= '5'", 'value': '5', 'addr': None}
    lit_index_map = {}         # literal string -> index in littab (1-based)
    pool_table = [1]           # stores starting literal index of each pool (1-based)
    current_pool_start = 1

    # helper to add literal
    def add_literal(lit):
        lit = normalize_quotes(lit)
        if lit not in lit_index_map:
            idx = len(littab) + 1
            littab.append({'literal': lit, 'value': literal_value(lit), 'addr': None})
            lit_index_map[lit] = idx
        return lit_index_map[lit]

    # helper to flush literal pool at current lc
    def flush_literal_pool():
        nonlocal lc, pool_table
        start_idx = pool_table[-1]
        idx = start_idx
        while idx <= len(littab):
            if littab[idx-1]['addr'] is None:
                littab[idx-1]['addr'] = lc
                # each literal occupies one word; assign and increment LC
                intermediate.append((lc, [("DL", DL["DC"]), ("C", littab[idx-1]['value'])]))
                lc += 1
            idx += 1
        # if any literal was assigned, and there remain more literals, start a new pool
        if start_idx <= len(littab):
            # next pool will start at next literal (if new literals appear later)
            pool_table.append(len(littab) + 1)

    # Preprocess lines to remove empty lines and comments (none in sample)
    prog = [l.strip() for l in lines if l.strip() != ""]

    i = 0
    while i < len(prog):
        line = prog[i]
        parts = tokenize(line)
        label = None
        opcode = None
        operands = []

        # Determine whether first token is a label or opcode
        if len(parts) == 0:
            i += 1
            continue
        first = parts[0].upper()
        # If first token is an opcode or directive, no label
        if first in IS or first in AD or first in DL:
            opcode = first
            operands = parts[1:]
        else:
            # token is label
            label = parts[0]
            if len(parts) > 1:
                opcode = parts[1].upper()
                operands = parts[2:]
            else:
                # label alone line (rare)
                opcode = None
                operands = []

        # If label present, put/define in symbol table with current LC
        if label:
            if label in symtab and symtab[label] is not None:
                # duplicate label definition (could warn)
                pass
            symtab[label] = lc

        # Handle directives and instructions
        if opcode is None:
            i += 1
            continue

        # Assembler directives
        if opcode in AD:
            code = [("AD", AD[opcode])]
            if opcode == "START":
                # operand gives starting address
                if len(operands) >= 1:
                    addr = int(operands[0])
                    code.append(("C", addr))
                    lc = addr
                else:
                    lc = 0
                intermediate.append((None, code))  # START not assigned an LC usually
            elif opcode == "END":
                # assign remaining literals (end of program)
                intermediate.append((None, code))
                flush_literal_pool()
            elif opcode == "LTORG":
                intermediate.append((None, code))
                flush_literal_pool()
            elif opcode == "ORIGIN":
                # operand is expression
                if len(operands) >= 1:
                    new_lc = eval_expr(operands[0], symtab)
                    code.append(("C", new_lc))
                    lc = new_lc
                intermediate.append((None, code))
            elif opcode == "EQU":
                # Usually: LABEL EQU expr   --> set label to expr
                if label is None:
                    # sometimes EQU used without label; handle operand expression target
                    pass
                else:
                    if len(operands) >= 1:
                        val = eval_expr(operands[0], symtab)
                        symtab[label] = val
                    intermediate.append((None, code + [("C", operands[0] if operands else "")]))
            else:
                intermediate.append((None, code))
        # Declarative statements
        elif opcode in DL:
            if opcode == "DS":
                # allocate operands[0] words
                size = int(operands[0]) if operands else 1
                intermediate.append((lc, [("DL", DL[opcode]), ("C", size)]))
                lc += size
            elif opcode == "DC":
                val = operands[0] if operands else "0"
                val = normalize_quotes(val)
                # if quoted constant, remove quotes
                if val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]
                intermediate.append((lc, [("DL", DL[opcode]), ("C", val)]))
                lc += 1
        # Imperative statements (instructions)
        elif opcode in IS:
            code = [("IS", IS[opcode])]
            # operands may be like: AREG, = '5' or AREG, X etc.
            op_syms = []
            for op in operands:
                if op == "":
                    continue
                # split comma-inside-case already handled by tokenize
                # check register
                if op.upper() in REG:
                    code.append(("RG", REG[op.upper()]))
                elif is_literal(op):
                    # add to literal table and reference it
                    idx = add_literal(op)
                    code.append(("L", idx))
                else:
                    # symbol or numeric constant or conditional code like LT,GT
                    # For BC instruction, operand might be condition and label: BC LT, BACK
                    if opcode == "BC":
                        # BC has two operands: condition and label
                        # For our sample, operands list would be ['LT', 'BACK']
                        # treat LT as condition code and BACK as symbol
                        cond = op.upper()
                        if cond in ["LT","LE","GT","GE","EQ","NE","ANY"]:
                            code.append(("CC", cond))
                        else:
                            # symbol
                            if op not in symtab:
                                symtab[op] = None
                            code.append(("S", op))
                    else:
                        # symbol or number
                        if re.fullmatch(r"\d+", op):
                            code.append(("C", op))
                        else:
                            if op not in symtab:
                                symtab[op] = None
                            code.append(("S", op))
            intermediate.append((lc, code))
            lc += 1
        else:
            # unknown opcode - treat as comment or skip
            intermediate.append((None, [("??", opcode)]))
        i += 1

    # Clean up pool table: last entry may be beyond last literal; remove if past end
    # Make pool_table entries unique and valid
    pool_table = [p for p in pool_table if p <= len(littab)]

    return intermediate, symtab, littab, pool_table

# --- Example usage with the user's sample program ---
sample_program = [
"START 200",
"MOVER AREG, ='5'",
"MOVEM AREG, X",
"L1 MOVER BREG, ='2'",
"ORIGIN L1+3",
"LTORG",
"NEXT ADD AREG, ='1'",
"SUB BREG, ='2'",
"BC LT, BACK",
"LTORG",
"BACK EQU L1",
"ORIGIN NEXT+5",
"MULT CREG, ='4'",
"STOP",
"X DS 1",
"END"
]

# Run pass one
intermediate, symtab, littab, pool_table = pass_one(sample_program)

# Pretty print results
print("---- Intermediate Code (Pass-I) ----")
for item in intermediate:
    lc, tokens = item
    lc_str = f"{lc}" if lc is not None else "    "
    tok_str = " ".join([f"({t[0]},{t[1]})" for t in tokens])
    print(f"{lc_str:4} : {tok_str}")

print("\n---- Symbol Table ----")
print("Index  Symbol   Address")
idx = 1
for s,a in sorted(symtab.items(), key=lambda x: x[0]):
    addr = a if a is not None else "-"
    print(f"{idx:5}  {s:7}  {addr}")
    idx += 1

print("\n---- Literal Table ----")
print("Index  Literal   Value   Address")
for i,ent in enumerate(littab, start=1):
    print(f"{i:5}  {ent['literal']:8}  {ent['value']:6}  {ent['addr'] if ent['addr'] is not None else '-'}")

print("\n---- Pool Table ----")
print(pool_table)
