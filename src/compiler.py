from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class Instruction:
    opcode: str
    arg: Any = None


@dataclass
class BytecodeProgram:
    instructions: List[Instruction] = field(default_factory=list)

    def append(self, opcode: str, arg: Any = None):
        self.instructions.append(Instruction(opcode, arg))

    def __repr__(self):
        return "\n".join(f"{i.opcode} {i.arg}" if i.arg is not None else i.opcode for i in self.instructions)
