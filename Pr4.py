# ------------------------------
# Pass-II of Two-Pass Macroprocessor (Simple & Readable)
# ------------------------------

def pass2_expand(mdt, mnt, ala, source_lines):
    """
    mdt: list of strings (MDT lines, in order)
    mnt: dict mapping macro_name -> mdt_start_index (0-based)
    ala: dict mapping macro_name -> list of formal args (e.g. ["&ARG1","&ARG2"])
    source_lines: list of program lines (strings) containing macro calls
    returns: list of expanded output lines
    """
    output = []

    for line in source_lines:
        line_stripped = line.strip()
        if line_stripped == "" or line_stripped.upper() == "START" or line_stripped.upper() == "END":
            # copy non-macro lines (START/END etc.) as-is
            output.append(line_stripped)
            continue

        # split first token to detect macro invocation
        parts = [p.strip() for p in line_stripped.split(None, 1)]
        name = parts[0]
        rest = parts[1] if len(parts) > 1 else ""

        # if name is a macro (in MNT) -> expand
        if name in mnt:
            mdt_index = mnt[name]
            # parse actual args (comma separated)
            actuals = []
            if rest:
                actuals = [a.strip() for a in rest.split(",") if a.strip() != ""]

            formals = ala.get(name, [])
            # build mapping formal -> actual (by position)
            mapping = {}
            for i, formal in enumerate(formals):
                if i < len(actuals):
                    mapping[formal] = actuals[i]
                else:
                    mapping[formal] = ""  # missing actual -> empty

            # Walk MDT from mdt_index until MEND and output with replacements
            idx = mdt_index
            while idx < len(mdt):
                mline = mdt[idx].strip()
                if mline.upper() == "MEND":
                    break
                # replace all formal occurrences with actuals safely (exact substring replacement)
                expanded = mline
                # replace longer formals first (defensive) but here formals don't overlap
                for formal in formals:
                    if formal:
                        expanded = expanded.replace(formal, mapping.get(formal, ""))
                output.append(expanded)
                idx += 1
            # done expanding this macro
        else:
            # not a macro -> copy as-is
            output.append(line_stripped)

    return output


# ------------------------------
# Example input (from your problem)
# ------------------------------
MDT = [
    "INCR &ARG1, &ARG2",
    "MOVER AREG, &ARG1",
    "ADD AREG, &ARG2",
    "MEND",
    "DECR &ARG3, &ARG4",
    "MOVER AREG, &ARG3",
    "SUB AREG, &ARG4",
    "MEND"
]

# MNT gives index into MDT (0-based)
MNT = {
    "INCR": 0,
    "DECR": 4
}

ALA = {
    "INCR": ["&ARG1", "&ARG2"],
    "DECR": ["&ARG3", "&ARG4"]
}

# Source program containing macro calls
SOURCE = [
    "START",
    "INCR N1, N2",
    "DECR N3, N4",
    "END"
]

# ------------------------------
# Run pass-2 expansion
# ------------------------------
expanded = pass2_expand(MDT, MNT, ALA, SOURCE)

# Print output
print("---- EXPANDED OUTPUT ----")
for line in expanded:
    print(line)
