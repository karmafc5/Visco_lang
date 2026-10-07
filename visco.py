from src.visco_compiler import Compiler
import argparse
from pathlib import Path


def run_file(path: str):
    source = Path(path).read_text(encoding="utf-8")
    result = Compiler().run(source)
    return result


def compile_file(input_path: str, output_path: str):
    source = Path(input_path).read_text(encoding="utf-8")
    compiled = Compiler().compile(source)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(compiled, encoding="utf-8")
    print(f"Compiled {input_path} -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Visco language compiler")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a Visco source file or inline code")
    run_parser.add_argument("source", help="Path to a .vs file or inline source text")

    compile_parser = subparsers.add_parser("compile", help="Compile a Visco source file to Python")
    compile_parser.add_argument("input", help="Path to the Visco .vs file")
    compile_parser.add_argument("output", help="Path to the generated Python file")

    args = parser.parse_args()

    if args.command == "run":
        if Path(args.source).exists():
            run_file(args.source)
        else:
            Compiler().run(args.source)
    elif args.command == "compile":
        compile_file(args.input, args.output)


if __name__ == "__main__":
    main()
