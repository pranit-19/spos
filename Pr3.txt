# ----------------------------------------------
# PASS-I of Two-Pass Macro Processor (Clean Windows-safe version)
# Builds: MNT, MDT, ALA
# ----------------------------------------------

def pass1_macro(lines):
    mnt = []           # Macro Name Table
    mdt = []           # Macro Definition Table
    ala_table = {}     # Macro Name -> Argument List Array

    in_macro = False
    current_macro = None

    for line in lines:
        line = line.strip()

        # Skip blank lines
        if not line:
            continue

        # Start of macro definition
        if line.upper() == "MACRO":
            in_macro = True
            continue

        # End of macro definition
        if line.upper() == "MEND":
            mdt.append("MEND")
            in_macro = False
            current_macro = None
            continue

        if in_macro:
            parts = line.replace(",", " ").split()

            # First line after MACRO (macro name and parameters)
            if current_macro is None:
                current_macro = parts[0]
                args = [a.strip() for a in parts[1:] if a.strip().startswith("&")]

                # Save in MNT and ALA
                mnt.append({"Name": current_macro, "MDT_Index": len(mdt) + 1})
                ala_table[current_macro] = args

            else:
                # Replace formal arguments (&ARG1, &ARG2, etc.) with #1, #2
                args = ala_table[current_macro]
                new_line = line
                for i, arg in enumerate(args):
                    # Replace exact argument only, not partial text
                    new_line = new_line.replace(arg, f"#{i+1}")
                mdt.append(new_line)

        # Lines outside MACRO/MEND are ignored in Pass-I
        else:
            continue

    return mnt, mdt, ala_table


# ----------------------------------------------
# INPUT PROGRAM
# ----------------------------------------------
program = [
    "START",
    "MACRO",
    "INCR &ARG1, &ARG2",
    "ADD AREG, &ARG2",
    "MEND",
    "MACRO",
    "DECR &ARG3, &ARG4",
    "SUB AREG, &ARG3",
    "MOVER CREG, &ARG4",
    "MEND",
    "INCR N1, N2",
    "DECR N3, N4",
    "END"
]

# Run Pass-I
mnt, mdt, ala = pass1_macro(program)

# ----------------------------------------------
# OUTPUT RESULTS
# ----------------------------------------------
print("---- MNT (Macro Name Table) ----")
print("No.  MacroName   MDT Index")
for i, entry in enumerate(mnt, start=1):
    print(f"{i:<4} {entry['Name']:<10} {entry['MDT_Index']}")

print("\n---- MDT (Macro Definition Table) ----")
for i, line in enumerate(mdt, start=1):
    print(f"{i:<4} {line}")

print("\n---- ALA (Argument List Array) ----")
for macro, args in ala.items():
    print(f"{macro:<8}: ", end="")
    for i, a in enumerate(args, start=1):
        print(f"{i}->{a}", end="  ")
    print()
