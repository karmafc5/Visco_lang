from __future__ import annotations

from dataclasses import dataclass
from typing import List


class Token:
    def __init__(self, type_name: str, value: str, position: int = 0):
        self.type = type_name
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type!r}, {self.value!r})"


@dataclass
class NumberNode:
    value: float


@dataclass
class StringNode:
    value: str


@dataclass
class VariableNode:
    name: str


@dataclass
class BinaryOpNode:
    left: object
    op: str
    right: object


@dataclass
class CallNode:
    name: str
    args: List[object]


@dataclass
class LetStatement:
    name: str
    value: object


@dataclass
class PrintStatement:
    value: object


@dataclass
class Program:
    statements: List[object]


class Lexer:
    KEYWORDS = {"let", "print", "input", "ask", "fn", "return", "if", "else", "while"}

    def __init__(self, source: str):
        self.source = source
        self.index = 0
        self.length = len(source)

    def tokenize(self):
        tokens = []
        while self.index < self.length:
            ch = self.source[self.index]

            if ch.isspace():
                self.index += 1
                continue

            if ch == '"':
                tokens.append(self._read_string())
                continue

            if ch.isdigit() or (ch == '.' and self._peek().isdigit()):
                tokens.append(self._read_number())
                continue

            if ch.isalpha() or ch == '_':
                tokens.append(self._read_identifier())
                continue

            if ch in "();=+-*/,()":
                tokens.append(Token(ch, ch, self.index))
                self.index += 1
                continue

            raise SyntaxError(f"Unexpected character: {ch!r} at position {self.index}")

        tokens.append(Token("EOF", "", self.index))
        return tokens

    def _peek(self, offset: int = 1):
        pos = self.index + offset
        return self.source[pos] if pos < self.length else ""

    def _read_string(self):
        start = self.index
        self.index += 1
        buffer = []
        while self.index < self.length:
            ch = self.source[self.index]
            if ch == '"':
                self.index += 1
                return Token("STRING", ''.join(buffer), start)
            if ch == '\\':
                self.index += 1
                if self.index >= self.length:
                    raise SyntaxError("Unterminated string literal")
                esc = self.source[self.index]
                escape_map = {'n': '\n', 't': '\t', '"': '"', '\\': '\\'}
                buffer.append(escape_map.get(esc, esc))
                self.index += 1
                continue
            buffer.append(ch)
            self.index += 1
        raise SyntaxError("Unterminated string literal")

    def _read_number(self):
        start = self.index
        seen_dot = False
        while self.index < self.length:
            ch = self.source[self.index]
            if ch.isdigit():
                self.index += 1
            elif ch == '.' and not seen_dot:
                seen_dot = True
                self.index += 1
            else:
                break
        return Token("NUMBER", self.source[start:self.index], start)

    def _read_identifier(self):
        start = self.index
        while self.index < self.length:
            ch = self.source[self.index]
            if ch.isalnum() or ch == '_':
                self.index += 1
            else:
                break
        text = self.source[start:self.index]
        token_type = "KEYWORD" if text in self.KEYWORDS else "IDENT"
        return Token(token_type, text, start)


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
        if self._match("KEYWORD", "let"):
            name = self._expect("IDENT").value
            self._expect("=")
            value = self._parse_expression()
            self._consume_optional_semicolon()
            return LetStatement(name, value)

        if self._match("KEYWORD", "print"):
            if self._match("("):
                value = self._parse_expression()
                self._expect(")")
            else:
                value = self._parse_expression()
            self._consume_optional_semicolon()
            return PrintStatement(value)

        expr = self._parse_expression()
        self._consume_optional_semicolon()
        return expr

    def _consume_optional_semicolon(self):
        self._match(";")

    def _parse_expression(self):
        return self._parse_additive()

    def _parse_additive(self):
        left = self._parse_multiplicative()
        while self._match("+", "-"):
            op = self._previous().value
            right = self._parse_multiplicative()
            left = BinaryOpNode(left, op, right)
        return left

    def _parse_multiplicative(self):
        left = self._parse_unary()
        while self._match("*", "/"):
            op = self._previous().value
            right = self._parse_unary()
            left = BinaryOpNode(left, op, right)
        return left

    def _parse_unary(self):
        if self._match("+", "-"):
            op = self._previous().value
            right = self._parse_unary()
            return BinaryOpNode(NumberNode(0), op, right)
        return self._parse_primary()

    def _parse_primary(self):
        if self._match("NUMBER"):
            return NumberNode(float(self._previous().value))

        if self._match("STRING"):
            return StringNode(self._previous().value)

        if self._match("IDENT"):
            name = self._previous().value
            if self._match("("):
                args = []
                if not self._check(")"):
                    while True:
                        args.append(self._parse_expression())
                        if not self._match(","):
                            break
                self._expect(")")
                return CallNode(name, args)
            return VariableNode(name)

        if self._match("("):
            expr = self._parse_expression()
            self._expect(")")
            return expr

        raise SyntaxError(f"Unexpected token {self._peek()!r} while parsing expression")

    def _peek(self):
        return self.tokens[self.index]

    def _previous(self):
        return self.tokens[self.index - 1]

    def _check(self, *token_types):
        token = self.tokens[self.index]
        return token.type in token_types or token.value in token_types

    def _match(self, *token_types):
        if self._check(*token_types):
            self.index += 1
            return True
        return False

    def _expect(self, token_type):
        token = self.tokens[self.index]
        if token.type == token_type or token.value == token_type:
            self.index += 1
            return token
        raise SyntaxError(f"Expected {token_type!r}, got {token!r}")


class CodeGenerator:
    def generate(self, node):
        if isinstance(node, Program):
            return "\n".join(self.generate(stmt) for stmt in node.statements)

        if isinstance(node, LetStatement):
            return f"{node.name} = {self.generate(node.value)}"

        if isinstance(node, PrintStatement):
            return f"print({self.generate(node.value)})"

        if isinstance(node, NumberNode):
            if node.value.is_integer():
                return str(int(node.value))
            return str(node.value)

        if isinstance(node, StringNode):
            return repr(node.value)

        if isinstance(node, VariableNode):
            return node.name

        if isinstance(node, BinaryOpNode):
            left = self.generate(node.left)
            right = self.generate(node.right)
            return f"({left} {node.op} {right})"

        if isinstance(node, CallNode):
            args = ", ".join(self.generate(arg) for arg in node.args)
            return f"{node.name}({args})"

        raise TypeError(f"Unsupported node type: {type(node)!r}")


class Compiler:
    def compile(self, source: str):
        tokens = Lexer(source).tokenize()
        program = Parser(tokens).parse()
        generated = CodeGenerator().generate(program)
        return "# Generated by Visco compiler\n" + generated + "\n"

    def run(self, source: str):
        generated = self.compile(source)
        namespace = {
            "__builtins__": __builtins__,
            "input": input,
            "ask": input,
            "add": lambda a, b: a + b,
            "sub": lambda a, b: a - b,
            "mul": lambda a, b: a * b,
            "div": lambda a, b: a / b,
            "to_text": lambda value: str(value),
        }
        exec(generated, namespace, namespace)
        return namespace


__all__ = ["Compiler", "Lexer", "Parser", "CodeGenerator"]
