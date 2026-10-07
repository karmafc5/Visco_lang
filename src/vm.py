from __future__ import annotations

import argparse
from pathlib import Path

from src.compiler import Compiler
from src.lexer import Lexer
from src.parser import Parser


def run_source(source: str):
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()
    python_code = Compiler().to_python(program)
    namespace = {"__builtins__": __builtins__, "input": input}
    exec(python_code, namespace, namespace)
    return namespace


def run_file(path: str):
    source = Path(path).read_text(encoding="utf-8")
    return run_source(source)


def compile_to_python(source: str):
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()
    return Compiler().to_python(program)


def main():
    parser = argparse.ArgumentParser(description="Visco compiler")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a Visco source file or inline source")
    run_parser.add_argument("source", help="Path to a .visco file or inline source text")

    compile_parser = subparsers.add_parser("compile", help="Compile a Visco source file to Python")
    compile_parser.add_argument("source", help="Path to a .visco file or inline source text")

    args = parser.parse_args()

    if args.command == "run":
        if Path(args.source).exists():
            run_file(args.source)
        else:
            run_source(args.source)
    elif args.command == "compile":
        if Path(args.source).exists():
            source = Path(args.source).read_text(encoding="utf-8")
        else:
            source = args.source
        print(compile_to_python(source))


if __name__ == "__main__":
    main()
