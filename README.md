
# Manual de uso del programa

### Requisitos previos
El analizador requiere **Python 3.8+** y la librería `pyparsing`. Puedes instalarla con:
```bash
pip install pyparsing
```

---

### ¿Cómo ejecutar?
1. Suba o cree el archivo `program.txt` en el mismo directorio donde se encuentra `main.py`.
2. Ejecute el código. El analizador leerá y procesará el archivo automáticamente.
3. Se incluyen ejemplos predefinidos en el repositorio.

---

## **Expresiones y definiciones regulares**

### Definiciones Base
> **Nota:** Estas definiciones son abstracciones auxiliares propias de la librería `pyparsing`.

```text
alphas     -> [a-zA-Z]
d          -> [0-9]
alphanums  -> alphas | d
```

---

### Identificadores
```text
ID -> alphas · (alphanums)*
```
> **Válidos:** `x`, `contador`, `var14ble`  
> **Inválidos:** `1x`, `@var`, `_total`

---

### Literales
> **Nota:** `\.` se refiere al punto literal, mientras que `.` representa cualquier carácter. `[^" \ ]` significa cualquier carácter excepto comillas o barra invertida.

```text
INT_LITERAL    -> (d)+
FLOAT_LITERAL  -> (d)+ · \. · (d)+ · (E · (+|-)? · (d)+)? | (d)+ · E · (+|-)? · (d)+
STRING_LITERAL -> " · ([^" \] | \ · . )* · " | ' · ([^' \] | \ · .)* · '
BOOL_LITERAL   -> true | false
```

---

### Palabras Reservadas
| Token | Lexema | Token | Lexema |
|-------|--------|-------|--------|
| `IF` | `if` | `PRINT` | `print` |
| `ELSE` | `else` | `BREAK` | `break` |
| `WHILE` | `while` | `CONTINUE` | `continue` |
| `FOR` | `for` | | |

---

### Operadores y Delimitadores

| Categoría | Tokens | Lexemas |
|-----------|--------|---------|
| **Aritméticos** | `MAS`, `MENOS`, `MULT`, `DIV`, `MOD` | `+`, `-`, `*`, `/`, `%` |
| **Inc/Dec** | `INCREMENT`, `DECREMENT` | `++`, `--` |
| **Relación** | `EQ`, `NE`, `LT`, `GT`, `LE`, `GE` | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| **Booleanos** | `AND`, `OR`, `NOT` | `&&`, `||`, `!` |
| **Asignación** | `ASIGN` | `=` |
| **Tipos** | `INT`, `FLOAT`, `BOOL`, `STRING` | `int`, `float`, `bool`, `string` |

**Delimitadores:** `( ) { } ; ,` (`PARENI`, `PAREND`, `LLAVEI`, `LLAVED`, `PUNTOYCOMA`, `COMA`)

---

### Comentarios
```text
SINGLELINE_COMMENT -> // · .*
MULTILINE_COMMENT  -> /* · [any_char]* · */
```

---

### Manejo de errores
> **Nota:** `[^"\n]` es cualquier carácter excepto comillas o salto de línea. `(?=\n|$)` es un lookahead para el fin de línea.

```text
OPEN_STRING         -> " · ([^"\n])* · (?=\n|$) | ' · ([^'\n])* · (?=\n|$)
ILEGAL_SYMBOL       -> .
INVALID_ID          -> [^alphas] · (alphanums)+
BADLY_FORMED_NUMBER -> (d)+ (\. (d)+)? [eE][+-]? | (d)+ \. (?!d) | (d)* \. (d)+ \. (d)*
```

---

### Agrupaciones
Categorías utilizadas para construir la lógica del lexer:

* **comment:** `SINGLELINE_COMMENT | MULTILINE_COMMENT`
* **keyword:** `IF | ELSE | WHILE | FOR | PRINT | BREAK | CONTINUE`
* **tipo:** `INT_TIPO | FLOAT_TIPO | BOOL_TIPO | STRING_TIPO`
* **literal:** `FLOAT_LITERAL | INT_LITERAL | STRING_LITERAL | BOOL_LITERAL`
* **increment_decrement:** `INCREMENT | DECREMENT`
* **relational_operator:** `EQ | NE | LE | GE | LT | GT`
* **boolean_operator:** `AND | OR | NOT`
* **arithmetic_operator:** `MAS | MENOS | MULT | DIV | MOD`
* **delimiters:** `PARENI | PAREND | LLAVEI | LLAVED | PUNTOYCOMA | COMA`
* **errors:** `OPEN_STRING | INVALID_ID | ILEGAL_SYMBOL`

---

### Orden de Precedencia del Lexer
El lexer evalúa las reglas en este orden de prioridad:

1. `comment`
2. `keyword`
3. `tipo`
4. `BADLY_FORMED_NUMBER`
5. `literal`
6. `ID`
7. `increment_decrement`
8. `relational_operator`
9. `boolean_operator`
10. `arithmetic_operator`
11. `ASIGN`
12. `delimiters`
13. `errors`
