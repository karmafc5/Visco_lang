# Visco Roadmap

This document records the planned phases for building Visco into a full language.

## Phase 1: Design the language syntax
- Define the language grammar
- Create readable natural-language statements
- Align keywords and syntax for a beginner-friendly language

### Proposed syntax

```visco
let name is "victor"
set total to 10 + 5
say "Hello " + name
ask "What is your name?" and store in name
```

## Phase 2: Lexer
- Convert source text to tokens
- Recognize keywords, strings, numbers, identifiers, operators
- Ignore whitespace and comments

## Phase 3: Parser
- Build a parser for statements and expressions
- Support assignment, output, input, arithmetic
- Produce an AST

## Phase 4: AST
- Represent program structure in nodes
- Support `Let`, `Set`, `Say`, `Ask`, `BinaryOp`, `Literal`, and `Variable`

## Phase 5: Compiler
- Translate AST to bytecode or intermediate representation
- Add variable handling and arithmetic
- Keep the compiler simple and easy to extend

## Phase 6: Bytecode
- Define instruction set
- Support `LOAD_CONST`, `LOAD_NAME`, `STORE_NAME`, `ADD`, `SUB`, etc.
- Build a compiler from AST to instruction list

## Phase 7: VM
- Execute the bytecode in a runtime
- Manage stack and environment
- Add clean runtime error handling

## Phase 8: Control flow
- Add `if`
- Add `while`
- Support nested blocks

## Phase 9: Error handling
- Lexing errors
- Parsing errors
- Runtime errors
- Helpful developer messages

## Phase 10: Browser playground
- Lightweight editor
- Run code in the browser
- Show output and bytecode preview

## Phase 11: Expansion
- Function definitions
- Arrays and lists
- Strings and formatting
- Modules and imports
- Standard library

