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


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse(self):
        statements = []
        while not self._check("EOF"):
            statements.append(self._parse_statement())
        return Program(statements)

    def _parse_statement(self):
        if self._match("LET"):
            name = self._expect("IDENT").value
            self._expect("IS")
            value = self._parse_expression()
            return LetStatement(name, value)

        if self._match("SET"):
            name = self._expect("IDENT").value
            self._expect("TO")
            value = self._parse_expression()
            return SetStatement(name, value)

        if self._match("SAY"):
            value = self._parse_expression()
            return SayStatement(value)

        if self._match("ASK"):
            prompt = self._expect("STRING").value
            self._expect("AND")
            self._expect("STORE")
            self._expect("IN")
            name = self._expect("IDENT").value
            return AskStatement(prompt, name)

        if self._match("IF"):
            condition = self._parse_expression()
            self._expect("THEN")
            then_block = []
            while not self._check("ELSE") and not self._check("END"):
                then_block.append(self._parse_statement())
            else_block = None
            if self._match("ELSE"):
                else_block = []
                while not self._check("END"):
                    else_block.append(self._parse_statement())
            self._expect("END")
            return IfStatement(condition, then_block, else_block)

        if self._match("WHILE"):
            condition = self._parse_expression()
            self._expect("DO")
            body = []
            while not self._check("END"):
                body.append(self._parse_statement())
            self._expect("END")
            return WhileStatement(condition, body)

        raise SyntaxError(f"Unexpected token {self._peek()!r}")

    def _parse_expression(self):
        return self._parse_additive()

    def _parse_additive(self):
        left = self._parse_multiplicative()
        while self._match("+", "-"):
            op = self._previous().value
            right = self._parse_multiplicative()
            left = BinaryOp(left, op, right)
        return left

    def _parse_multiplicative(self):
        left = self._parse_unary()
        while self._match("*", "/"):
            op = self._previous().value
            right = self._parse_unary()
            left = BinaryOp(left, op, right)
        return left

    def _parse_unary(self):
        if self._match("+", "-"):
            op = self._previous().value
            right = self._parse_unary()
            return BinaryOp(Literal(0), op, right)
        return self._parse_primary()

    def _parse_primary(self):
        if self._match("NUMBER"):
            return Literal(float(self._previous().value) if "." in self._previous().value else int(self._previous().value))

        if self._match("STRING"):
            return Literal(self._previous().value)

        if self._match("TRUE"):
            return Literal(True)

        if self._match("FALSE"):
            return Literal(False)

        if self._match("IDENT"):
            return Variable(self._previous().value)

        if self._match("("):
            expr = self._parse_expression()
            self._expect(")")
            return expr

        raise SyntaxError(f"Unexpected token {self._peek()!r} while parsing expression")

    def _peek(self):
        return self.tokens[self.index]

    def _previous(self):
        return self.tokens[self.index - 1]

    def _check(self, *types):
        token = self.tokens[self.index]
        return token.type in types or token.value in types

    def _match(self, *types):
        if self._check(*types):
            self.index += 1
            return True
        return False

    def _expect(self, token_type):
        token = self.tokens[self.index]
        if token.type == token_type or token.value == token_type:
            self.index += 1
            return token
        raise SyntaxError(f"Expected {token_type!r}, got {token!r}")
