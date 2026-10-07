from __future__ import annotations

from src.ast import AskStatement, BinaryOp, IfStatement, LetStatement, Literal, Program, SayStatement, SetStatement, Variable, WhileStatement
from src.bytecode import BytecodeProgram


class Compiler:
    def compile(self, program: Program) -> BytecodeProgram:
        bytecode = BytecodeProgram()
        for stmt in program.statements:
            self._compile_statement(stmt, bytecode)
        return bytecode

    def _compile_statement(self, stmt, bytecode: BytecodeProgram):
        if isinstance(stmt, LetStatement):
            self._compile_expr(stmt.value, bytecode)
            bytecode.append("STORE_NAME", stmt.name)
            return

        if isinstance(stmt, SetStatement):
            self._compile_expr(stmt.value, bytecode)
            bytecode.append("STORE_NAME", stmt.name)
            return

        if isinstance(stmt, SayStatement):
            self._compile_expr(stmt.value, bytecode)
            bytecode.append("PRINT")
            return

        if isinstance(stmt, AskStatement):
            bytecode.append("LOAD_CONST", stmt.prompt)
            bytecode.append("INPUT")
            bytecode.append("STORE_NAME", stmt.name)
            return

        if isinstance(stmt, IfStatement):
            self._compile_expr(stmt.condition, bytecode)
            bytecode.append("JUMP_IF_FALSE", "else")
            for child in stmt.then_block:
                self._compile_statement(child, bytecode)
            if stmt.else_block is not None:
                bytecode.append("JUMP", "end")
                bytecode.append("LABEL", "else")
                for child in stmt.else_block:
                    self._compile_statement(child, bytecode)
                bytecode.append("LABEL", "end")
            else:
                bytecode.append("LABEL", "else")
            return

        if isinstance(stmt, WhileStatement):
            bytecode.append("LABEL", "while_start")
            self._compile_expr(stmt.condition, bytecode)
            bytecode.append("JUMP_IF_FALSE", "while_end")
            for child in stmt.body:
                self._compile_statement(child, bytecode)
            bytecode.append("JUMP", "while_start")
            bytecode.append("LABEL", "while_end")
            return

        raise TypeError(f"Unsupported statement type: {type(stmt)!r}")

    def _compile_expr(self, expr, bytecode: BytecodeProgram):
        if isinstance(expr, Literal):
            bytecode.append("LOAD_CONST", expr.value)
            return

        if isinstance(expr, Variable):
            bytecode.append("LOAD_NAME", expr.name)
            return

        if isinstance(expr, BinaryOp):
            self._compile_expr(expr.left, bytecode)
            self._compile_expr(expr.right, bytecode)
            mapping = {
                "+": "ADD",
                "-": "SUB",
                "*": "MUL",
                "/": "DIV",
            }
            opcode = mapping.get(expr.op, "ADD")
            bytecode.append(opcode)
            return

        raise TypeError(f"Unsupported expression type: {type(expr)!r}")

    def to_python(self, program: Program) -> str:
        lines = []
        for stmt in program.statements:
            lines.extend(self._python_lines(stmt))
        return "\n".join(lines)

    def _python_lines(self, stmt):
        if isinstance(stmt, LetStatement):
            return [f"{stmt.name} = {self._python_expr(stmt.value)}"]
        if isinstance(stmt, SetStatement):
            return [f"{stmt.name} = {self._python_expr(stmt.value)}"]
        if isinstance(stmt, SayStatement):
            return [f"print({self._python_expr(stmt.value)})"]
        if isinstance(stmt, AskStatement):
            return [f"{stmt.name} = input({stmt.prompt!r})"]
        raise TypeError(f"Unsupported node: {type(stmt)!r}")

    def _python_expr(self, expr):
        if isinstance(expr, Literal):
            return repr(expr.value)
        if isinstance(expr, Variable):
            return expr.name
        if isinstance(expr, BinaryOp):
            return f"({self._python_expr(expr.left)} {expr.op} {self._python_expr(expr.right)})"
        raise TypeError(f"Unsupported expression: {type(expr)!r}")
