from __future__ import annotations

from src.ast import (
    AskStatement,
    BinaryOp,
    IfStatement,
    LetStatement,
    Literal,
    Program,
    SayStatement,
    SetStatement,
    Variable,
    WhileStatement,
)


class Compiler:
    def compile(self, program: Program):
        return self.to_python(program)

    def to_python(self, program: Program) -> str:
        lines = []
        for stmt in program.statements:
            lines.extend(self._emit_statement(stmt, 0))
        return "\n".join(lines)

    def _emit_statement(self, stmt, indent: int):
        pad = " " * indent

        if isinstance(stmt, LetStatement):
            return [f"{pad}{stmt.name} = {self._emit_expr(stmt.value)}"]

        if isinstance(stmt, SetStatement):
            return [f"{pad}{stmt.name} = {self._emit_expr(stmt.value)}"]

        if isinstance(stmt, SayStatement):
            return [f"{pad}print({self._emit_expr(stmt.value)})"]

        if isinstance(stmt, AskStatement):
            return [f"{pad}{stmt.name} = input({stmt.prompt!r})"]

        if isinstance(stmt, IfStatement):
            lines = [f"{pad}if {self._emit_expr(stmt.condition)}:"]
            for child in stmt.then_block:
                lines.extend(self._emit_statement(child, indent + 4))
            if stmt.else_block is not None:
                lines.append(f"{pad}else:")
                for child in stmt.else_block:
                    lines.extend(self._emit_statement(child, indent + 4))
            return lines

        if isinstance(stmt, WhileStatement):
            lines = [f"{pad}while {self._emit_expr(stmt.condition)}:"]
            for child in stmt.body:
                lines.extend(self._emit_statement(child, indent + 4))
            return lines

        raise TypeError(f"Unsupported statement type: {type(stmt)!r}")

    def _emit_expr(self, expr):
        if isinstance(expr, Literal):
            if expr.value is None:
                return "None"
            if isinstance(expr.value, str):
                return repr(expr.value)
            return repr(expr.value)

        if isinstance(expr, Variable):
            return expr.name

        if isinstance(expr, BinaryOp):
            left = self._emit_expr(expr.left)
            right = self._emit_expr(expr.right)
            return f"({left} {expr.op} {right})"

        raise TypeError(f"Unsupported expression type: {type(expr)!r}")
