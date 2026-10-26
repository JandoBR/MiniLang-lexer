# MiniLang lexer

A lexical analyser for a small C-like language, written in Python with `pyparsing`. It
reads `program.txt` from its own directory, prints the token stream with line numbers, and
then the symbol table. Lexical errors are reported with the line they occur on.

## Requirements

Python 3.8+ and `pyparsing`:

```bash
pip install pyparsing
```

## Run it

1. Put the program you want to analyse in `program.txt`, next to `main.py`.
2. Run `python main.py`.
3. Two examples are included: copy `valid_minilang_example.txt` or
   `invalid_minilang_example.txt` over `program.txt` and run again.

## Grammar

### Base definitions

> Auxiliary abstractions from `pyparsing`.

```text
alphas     -> [a-zA-Z]
d          -> [0-9]
alphanums  -> alphas | d
```

### Identifiers

```text
ID -> alphas · (alphanums)*
```

> **Valid:** `x`, `contador`, `var14ble`
> **Invalid:** `1x`, `@var`, `_total`

### Literals

> `\.` is a literal dot; `.` is any character. `[^" \ ]` is any character except a quote
> or a backslash.

```text
INT_LITERAL    -> (d)+
FLOAT_LITERAL  -> (d)+ · \. · (d)+ · (E · (+|-)? · (d)+)? | (d)+ · E · (+|-)? · (d)+
STRING_LITERAL -> " · ([^" \] | \ · . )* · " | ' · ([^' \] | \ · .)* · '
BOOL_LITERAL   -> true | false
```

### Keywords

| Token | Lexeme | Token | Lexeme |
|-------|--------|-------|--------|
| `IF` | `if` | `PRINT` | `print` |
| `ELSE` | `else` | `BREAK` | `break` |
| `WHILE` | `while` | `CONTINUE` | `continue` |
| `FOR` | `for` | | |

### Operators and delimiters

| Category | Tokens | Lexemes |
|----------|--------|---------|
| **Arithmetic** | `MAS`, `MENOS`, `MULT`, `DIV`, `MOD` | `+`, `-`, `*`, `/`, `%` |
| **Inc/dec** | `INCREMENT`, `DECREMENT` | `++`, `--` |
| **Relational** | `EQ`, `NE`, `LT`, `GT`, `LE`, `GE` | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| **Boolean** | `AND`, `OR`, `NOT` | `&&`, `\|\|`, `!` |
| **Assignment** | `ASIGN` | `=` |
| **Types** | `INT`, `FLOAT`, `BOOL`, `STRING` | `int`, `float`, `bool`, `string` |

**Delimiters:** `( ) { } ; ,` (`PARENI`, `PAREND`, `LLAVEI`, `LLAVED`, `PUNTOYCOMA`, `COMA`).

### Comments

```text
SINGLELINE_COMMENT -> // · .*
MULTILINE_COMMENT  -> /* · [any_char]* · */
```

### Error handling

> `[^"\n]` is any character except a quote or a newline. `(?=\n|$)` is a lookahead for the
> end of the line.

```text
OPEN_STRING         -> " · ([^"\n])* · (?=\n|$) | ' · ([^'\n])* · (?=\n|$)
ILEGAL_SYMBOL       -> .
INVALID_ID          -> [^alphas] · (alphanums)+
BADLY_FORMED_NUMBER -> (d)+ (\. (d)+)? [eE][+-]? | (d)+ \. (?!d) | (d)* \. (d)+ \. (d)*
```

## Output

For every token: `(line, token, lexeme)`. Then the symbol table maps each identifier to the
line where it first appears.
