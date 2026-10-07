from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Token:
    type: str
    value: str
    position: int

    def __repr__(self):
        return f"Token(type={self.type!r}, value={self.value!r})"


KEYWORDS = {
    "let": "LET",
    "set": "SET",
    "is": "IS",
    "to": "TO",
    "say": "SAY",
    "ask": "ASK",
    "and": "AND",
    "store": "STORE",
    "in": "IN",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "while": "WHILE",
    "do": "DO",
    "end": "END",
    "true": "TRUE",
    "false": "FALSE",
}

OPERATORS = {"+", "-", "*", "/", "(", ")"}


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.index = 0
        self.length = len(source)

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

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

            if ch in OPERATORS:
                tokens.append(Token(ch, ch, self.index))
                self.index += 1
                continue

            if ch == '?':
                tokens.append(Token("QUESTION", "?", self.index))
                self.index += 1
                continue

            raise SyntaxError(f"Unexpected character {ch!r} at position {self.index}")

        tokens.append(Token("EOF", "", self.index))
        return tokens

    def _peek(self, offset: int = 1) -> str:
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
                mapping = {'n': '\n', 't': '\t', '"': '"', '\\': '\\'}
                buffer.append(mapping.get(esc, esc))
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
        token_type = KEYWORDS.get(text, "IDENT")
        return Token(token_type, text, start)
