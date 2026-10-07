from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class LetStatement:
    name: str
    value: Any


@dataclass
class SetStatement:
    name: str
    value: Any


@dataclass
class SayStatement:
    value: Any


@dataclass
class AskStatement:
    prompt: str
    name: str


@dataclass
class BinaryOp:
    left: Any
    op: str
    right: Any


@dataclass
class Literal:
    value: Any


@dataclass
class Variable:
    name: str


@dataclass
class IfStatement:
    condition: Any
    then_block: List[Any]
    else_block: Optional[List[Any]] = None


@dataclass
class WhileStatement:
    condition: Any
    body: List[Any]


@dataclass
class Program:
    statements: List[Any]
