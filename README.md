# Visco_lang

Visco_lang is a small programming language built from scratch as a teaching project. It is designed to take input, process it, and produce output in a simple, readable way.

Examples:

- Add numbers
- Read a name from input
- Print a custom greeting

The compiler is currently bootstrapped in Python and compiles Visco source into Python. This gives us a working compiler pipeline quickly while keeping the project easy to understand and extend.

## Language features

The language supports:

- variable declarations with `let`
- arithmetic expressions (`+`, `-`, `*`, `/`)
- function calls such as `add(2, 3)`
- string concatenation using `+`
- `print(...)` statements
- `input(...)` for reading text input

## Example program

```visco
let name = input("What is your name? ");
print("My name is " + name);

let total = add(10, 5);
print("The total is " + to_string(total));
```

## Running the compiler

```bash
python3 visco.py run examples/greet.vs
python3 visco.py compile examples/greet.vs build/greet.py
```

## Project structure

- `visco.py` - command-line entry point
- `src/visco_compiler.py` - lexer, parser, compiler, runtime
- `examples/` - sample Visco programs

## Next steps

The next milestone is to add:

- `if` statements
- `while` loops
- function declarations
- a real bytecode or native code backend
- eventually a more self-hosted compiler architecture

