# Visco Language

Visco is a small, original programming language designed to feel natural and readable.

The goal is to let you write programs in plain English-like syntax, while the compiler translates them into executable bytecode or Python behind the scenes.

## Syntax examples

```visco
let name is "victor"
say "  " + name

ask "What is your name?" and store in name
say "My name is " + name

set total to 10 + 5
say "The total is " + total
```

## Roadmap

### Phase 1: Core language foundation
- Design the syntax
- Build the lexer
- Build the parser
- Build the AST

### Phase 2: Compiler and runtime
- Build the compiler
- Create bytecode
- Build the VM
- Add variables
- Add arithmetic

### Phase 3: Control flow and usability
- Add IF
- Add WHILE
- Add error handling
- Add browser playground

## Project structure

```text
Visco_lang/
  README.md
  visco.py
  src/
    __init__.py
    ast.py
    bytecode.py
    compiler.py
    lexer.py
    parser.py
    vm.py
  examples/
    hello.visco
    add.visco
    greet.visco
  browser/
    index.html
  docs/
    roadmap.md
```

## How to run

```bash
python3 visco.py run examples/greet.visco
python3 visco.py run "let name is \"victor\"\nsay \"Hello \" + name"
```

## Current status

This repository currently includes:
- a natural-language lexer
- parser support for `let`, `set`, `say`, and `ask`
- an AST model
- a bytecode compiler and VM
- sample Visco programs

This is the foundation for building a richer language in later stages.
