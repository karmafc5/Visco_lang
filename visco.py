from __future__ import annotations

from src.bytecode import BytecodeProgram


class VirtualMachine:
    def __init__(self):
        self.env = {}
        self.stack = []

    def run(self, program: BytecodeProgram):
        for instruction in program.instructions:
            opcode = instruction.opcode
            arg = instruction.arg

            if opcode == "LOAD_CONST":
                self.stack.append(arg)
            elif opcode == "LOAD_NAME":
                self.stack.append(self.env[arg])
            elif opcode == "STORE_NAME":
                self.env[arg] = self.stack.pop()
            elif opcode == "ADD":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left + right)
            elif opcode == "SUB":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left - right)
            elif opcode == "MUL":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left * right)
            elif opcode == "DIV":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left / right)
            elif opcode == "INPUT":
                prompt = self.stack.pop()
                self.stack.append(input(prompt))
            elif opcode == "PRINT":
                value = self.stack.pop()
                print(value)
            elif opcode == "JUMP_IF_FALSE":
                condition = self.stack.pop()
                if not condition:
                    # placeholder: real branching requires labels; kept as no-op for now
                    pass
            elif opcode == "JUMP":
                pass
            elif opcode == "LABEL":
                pass
            else:
                raise RuntimeError(f"Unknown opcode: {opcode}")

        return self.env
