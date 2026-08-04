#!/usr/bin/env python3

import sys
from collections import Counter

def signed8(x):
    return x - 256 if x & 0x80 else x


def decode(data, pos, base):

    op = data[pos]
    pc = base + pos

    # -----------------------------------------------------
    # 1 byte instructions
    # -----------------------------------------------------

    one = {
        0x00: "NOP",
        0x04: "INC A",
        0x14: "DEC A",
        0x22: "RET",
        0x32: "RETI",
        0x40: "JC",
        0x50: "JNC",
        0x60: "JZ",
        0x70: "JNZ",
        0x80: "SJMP",
        0x90: None,
        0xA3: "INC DPTR",
        0xE0: "MOVX A,@DPTR",
        0xE4: "CLR A",
        0xF0: "MOVX @DPTR,A",
    }

    # -----------------------------------------------------
    # MOV A,R0-R7
    # 0xE8 - 0xEF
    # -----------------------------------------------------

    if 0xE8 <= op <= 0xEF:
        r = op - 0xE8
        return 1, f"MOV A,R{r}", "normal", None

    # -----------------------------------------------------
    # MOV R0-R7,A
    # 0xF8 - 0xFF
    # -----------------------------------------------------

    if 0xF8 <= op <= 0xFF:
        r = op - 0xF8
        return 1, f"MOV R{r},A", "normal", None

    # -----------------------------------------------------
    # MOV R0-R7,#imm
    # 78-7F
    # -----------------------------------------------------

    if 0x78 <= op <= 0x7F and pos + 1 < len(data):
        r = op - 0x78
        v = data[pos + 1]

        return (
            2,
            f"MOV R{r},#0x{v:02X}",
            "normal",
            None
        )

    # -----------------------------------------------------
    # MOV A,#imm
    # -----------------------------------------------------

    if op == 0x74 and pos + 1 < len(data):

        v = data[pos + 1]

        return (
            2,
            f"MOV A,#0x{v:02X}",
            "normal",
            None
        )

    # -----------------------------------------------------
    # MOV DPTR,#imm16
    # -----------------------------------------------------

    if op == 0x90 and pos + 2 < len(data):

        hi = data[pos + 1]
        lo = data[pos + 2]

        addr = (hi << 8) | lo

        return (
            3,
            f"MOV DPTR,#0x{addr:04X}",
            "dptr",
            addr
        )

    # -----------------------------------------------------
    # LJMP
    # -----------------------------------------------------

    if op == 0x02 and pos + 2 < len(data):

        hi = data[pos + 1]
        lo = data[pos + 2]

        target = (hi << 8) | lo

        return (
            3,
            f"LJMP 0x{target:04X}",
            "jump",
            target
        )

    # -----------------------------------------------------
    # LCALL
    # -----------------------------------------------------

    if op == 0x12 and pos + 2 < len(data):

        hi = data[pos + 1]
        lo = data[pos + 2]

        target = (hi << 8) | lo

        return (
            3,
            f"LCALL 0x{target:04X}",
            "call",
            target
        )

    # -----------------------------------------------------
    # ACALL
    # -----------------------------------------------------

    if op & 0x1F in (
        0x01,
        0x11,
        0x21,
        0x31,
        0x41,
        0x51,
        0x61,
        0x71
    ):

        if pos + 1 < len(data):

            # 8051 ACALL address calculation
            low = data[pos + 1]

            target = (
                ((pc + 2) & 0xF800)
                | ((op & 0xE0) << 3)
                | low
            )

            return (
                2,
                f"ACALL 0x{target:04X}",
                "call",
                target
            )

    # -----------------------------------------------------
    # SJMP
    # -----------------------------------------------------

    if op == 0x80 and pos + 1 < len(data):

        rel = signed8(data[pos + 1])

        target = (pc + 2 + rel) & 0xFFFF

        return (
            2,
            f"SJMP 0x{target:04X}",
            "jump",
            target
        )

    # -----------------------------------------------------
    # Conditional relative jumps
    # -----------------------------------------------------

    conditional = {
        0x40: "JC",
        0x50: "JNC",
        0x60: "JZ",
        0x70: "JNZ",
    }

    if op in conditional and pos + 1 < len(data):

        rel = signed8(data[pos + 1])

        target = (pc + 2 + rel) & 0xFFFF

        return (
            2,
            f"{conditional[op]} 0x{target:04X}",
            "conditional",
            target
        )

    # -----------------------------------------------------
    # MOV direct,#imm
    # -----------------------------------------------------

    if op == 0x75 and pos + 2 < len(data):

        direct = data[pos + 1]
        value = data[pos + 2]

        return (
            3,
            f"MOV 0x{direct:02X},#0x{value:02X}",
            "normal",
            None
        )

    # -----------------------------------------------------
    # MOVX @Ri,A
    # -----------------------------------------------------

    if op == 0xF2:
        return 1, "MOVX @R0,A", "xdata", None

    if op == 0xF3:
        return 1, "MOVX @R1,A", "xdata", None

    # -----------------------------------------------------
    # MOVX A,@Ri
    # -----------------------------------------------------

    if op == 0xE2:
        return 1, "MOVX A,@R0", "xdata", None

    if op == 0xE3:
        return 1, "MOVX A,@R1", "xdata", None

    # -----------------------------------------------------
    # ADD A,#imm
    # -----------------------------------------------------

    if op == 0x24 and pos + 1 < len(data):

        return (
            2,
            f"ADD A,#0x{data[pos+1]:02X}",
            "normal",
            None
        )

    # -----------------------------------------------------
    # SUBB A,#imm
    # -----------------------------------------------------

    if op == 0x94 and pos + 1 < len(data):

        return (
            2,
            f"SUBB A,#0x{data[pos+1]:02X}",
            "normal",
            None
        )

    # -----------------------------------------------------
    # ANL A,#imm
    # -----------------------------------------------------

    if op == 0x54 and pos + 1 < len(data):

        return (
            2,
            f"ANL A,#0x{data[pos+1]:02X}",
            "normal",
            None
        )

    # -----------------------------------------------------
    # ORL A,#imm
    # -----------------------------------------------------

    if op == 0x44 and pos + 1 < len(data):

        return (
            2,
            f"ORL A,#0x{data[pos+1]:02X}",
            "normal",
            None
        )

    # -----------------------------------------------------
    # XRL A,#imm
    # -----------------------------------------------------

    if op == 0x64 and pos + 1 < len(data):

        return (
            2,
            f"XRL A,#0x{data[pos+1]:02X}",
            "normal",
            None
        )

    # -----------------------------------------------------
    # PUSH direct
    # -----------------------------------------------------

    if op == 0xC0 and pos + 1 < len(data):

        return (
            2,
            f"PUSH 0x{data[pos+1]:02X}",
            "stack",
            None
        )

    # -----------------------------------------------------
    # POP direct
    # -----------------------------------------------------

    if op == 0xD0 and pos + 1 < len(data):

        return (
            2,
            f"POP 0x{data[pos+1]:02X}",
            "stack",
            None
        )

    # -----------------------------------------------------
    # Unknown / data
    # -----------------------------------------------------

    return (
        1,
        f"DB 0x{op:02X}",
        "unknown",
        None
    )


# ---------------------------------------------------------
# Main analysis
# ---------------------------------------------------------

def analyze(filename):

    with open(filename, "rb") as f:
        data = f.read()

    print("=" * 70)
    print("8051 FIRMWARE ANALYZER")
    print("=" * 70)

    print(f"File       : {filename}")
    print(f"Size       : {len(data)} bytes")
    print(f"Size hex   : 0x{len(data):X}")
    print()

    # -----------------------------------------------------
    # FF regions
    # -----------------------------------------------------

    print("[1] FF REGIONS")
    print("-" * 70)

    ff_start = None
    ff_regions = []

    for i, b in enumerate(data):

        if b == 0xFF:

            if ff_start is None:
                ff_start = i

        else:

            if ff_start is not None:

                if i - ff_start >= 16:
                    ff_regions.append(
                        (ff_start, i - 1, i - ff_start)
                    )

                ff_start = None

    if ff_start is not None:

        if len(data) - ff_start >= 16:
            ff_regions.append(
                (
                    ff_start,
                    len(data) - 1,
                    len(data) - ff_start
                )
            )

    for start, end, size in ff_regions:

        print(
            f"0x{start:05X}-0x{end:05X}"
            f"  ({size} bytes)"
        )

    print()

    # -----------------------------------------------------
    # 8051 linear disassembly
    # -----------------------------------------------------

    print("[2] DISASSEMBLY")
    print("-" * 70)

    instructions = []

    pos = 0

    while pos < len(data):

        size, asm, typ, target = decode(
            data,
            pos,
            0
        )

        if pos + size > len(data):
            size = len(data) - pos

        raw = data[pos:pos + size]

        instructions.append(
            (
                pos,
                raw,
                asm,
                typ,
                target
            )
        )

        pos += size

    # -----------------------------------------------------
    # Output file
    # -----------------------------------------------------

    asm_file = filename + ".asm"

    with open(asm_file, "w") as out:

        out.write("; 8051 firmware analysis\n")
        out.write(f"; file: {filename}\n")
        out.write(f"; size: {len(data)} bytes\n\n")

        for addr, raw, asm, typ, target in instructions:

            hx = " ".join(
                f"{x:02X}" for x in raw
            )

            out.write(
                f"{addr:04X}:  "
                f"{hx:<15} "
                f"{asm}\n"
            )

    print(f"Assembly saved: {asm_file}")
    print()

    # -----------------------------------------------------
    # Calls
    # -----------------------------------------------------

    print("[3] CALL TARGETS")
    print("-" * 70)

    calls = Counter()

    for addr, raw, asm, typ, target in instructions:

        if typ == "call" and target is not None:

            calls[target] += 1

    for target, count in sorted(calls.items()):

        print(
            f"0x{target:04X}"
            f"    {count} call(s)"
        )

    print()

    # -----------------------------------------------------
    # Jumps
    # -----------------------------------------------------

    print("[4] JUMP TARGETS")
    print("-" * 70)

    jumps = Counter()

    for addr, raw, asm, typ, target in instructions:

        if typ in ("jump", "conditional"):

            if target is not None:
                jumps[target] += 1

    for target, count in sorted(jumps.items()):

        print(
            f"0x{target:04X}"
            f"    {count} jump(s)"
        )

    print()

    # -----------------------------------------------------
    # DPTR constants
    # -----------------------------------------------------

    print("[5] DPTR VALUES")
    print("-" * 70)

    dptrs = Counter()

    for addr, raw, asm, typ, target in instructions:

        if typ == "dptr":

            dptrs[target] += 1

    for value, count in sorted(dptrs.items()):

        print(
            f"0x{value:04X}"
            f"    {count} time(s)"
        )

    print()

    # -----------------------------------------------------
    # XDATA related addresses
    # -----------------------------------------------------

    print("[6] POSSIBLE XDATA ADDRESSES")
    print("-" * 70)

    for value, count in sorted(dptrs.items()):

        if value >= 0x0100:

            print(
                f"0x{value:04X}"
                f"    {count} time(s)"
            )

    print()

    # -----------------------------------------------------
    # RET statistics
    # -----------------------------------------------------

    print("[7] RETURN INSTRUCTIONS")
    print("-" * 70)

    ret = 0
    reti = 0

    for addr, raw, asm, typ, target in instructions:

        if asm == "RET":
            ret += 1

        elif asm == "RETI":
            reti += 1

    print(f"RET  : {ret}")
    print(f"RETI : {reti}")
    print()

    # -----------------------------------------------------
    # Opcode statistics
    # -----------------------------------------------------

    print("[8] OPCODE STATISTICS")
    print("-" * 70)

    opcodes = Counter(data)

    for opcode, count in opcodes.most_common():

        print(
            f"{opcode:02X} : {count:6d}"
        )

    print()

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(f"Bytes             : {len(data)}")
    print(f"Instructions      : {len(instructions)}")
    print(f"CALL targets      : {len(calls)}")
    print(f"JUMP targets      : {len(jumps)}")
    print(f"DPTR constants    : {len(dptrs)}")
    print(f"RET               : {ret}")
    print(f"RETI              : {reti}")
    print(f"FF regions        : {len(ff_regions)}")

    print()
    print(f"Assembly file: {asm_file}")


def main():

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "  ./analyze8051.py flash.bin"
        )

        sys.exit(1)

    analyze(sys.argv[1])


if __name__ == "__main__":
    main()
