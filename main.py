from enum import Enum
from pyparsing import Word, Literal, Keyword, Regex, MatchFirst, OneOrMore, ZeroOrMore 
from pyparsing import alphas, alphanums, lineno, Optional, Suppress


def parse():
  class error_types(Enum):
      ILEGAL_SYMBOL = "simbolo ilegal"
      INVALID_ID = "identificador invalido"
      OPEN_STRING = "string no cerrado"
      BADLY_FORMED_NUMBER = "numero mal formado"

  class types(Enum):
      STRING_TIPO = "STRING_TIPO"
      BOOL_TIPO = "BOOL_TIPO"
      FLOAT_TIPO = "FLOAT_TIPO"
      INT_TIPO = "INT_TIPO"


  # VARIABLES
  ID = Word(alphas, alphanums).set_results_name("ID", list_all_matches=True)

  # LITERALS
  INT_LITERAL = Regex(r"\d+").set_results_name("INT_LITERAL", list_all_matches=True)
  FLOAT_LITERAL = Regex(r"(\d+\.\d+(E[+-]?\d+)?|\d+E[+-]?\d+)").set_results_name("FLOAT_LITERAL", list_all_matches=True)
  STRING_LITERAL = Regex(r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\'').set_results_name("STRING_LITERAL", list_all_matches=True)
  BOOL_LITERAL = MatchFirst(Keyword("true"), Keyword("false")).set_results_name("BOOL_LITERAL", list_all_matches=True)

  # KEYWORDS
  IF = Keyword("if").set_results_name("IF", list_all_matches=True)
  ELSE = Keyword("else").set_results_name("ELSE", list_all_matches=True)
  WHILE = Keyword("while").set_results_name("WHILE", list_all_matches=True)
  FOR = Keyword("for").set_results_name("FOR", list_all_matches=True)
  PRINT = Keyword("print").set_results_name("PRINT", list_all_matches=True)
  BREAK = Keyword("break").set_results_name("BREAK", list_all_matches=True)
  CONTINUE = Keyword("continue").set_results_name("CONTINUE", list_all_matches=True)

  # ARITHMETIC OPERATORS
  MAS = Literal("+").set_results_name("MAS", list_all_matches=True)
  MENOS = Literal("-").set_results_name("MENOS", list_all_matches=True)
  MULT = Literal("*").set_results_name("MULT", list_all_matches=True)
  DIV = Literal("/").set_results_name("DIV", list_all_matches=True)
  MOD = Literal("%").set_results_name("MOD", list_all_matches=True)

  # INCREMENT/DECREMENT OPERATORS
  INCREMENT = Literal("++").set_results_name("INCREMENT", list_all_matches=True)
  DECREMENT = Literal("--").set_results_name("DECREMENT", list_all_matches=True)

  # ASIGN OPERATOR
  ASIGN = Literal("=").set_results_name("ASIGN", list_all_matches=True)

  # RELATIONAL OPERATORS
  EQ = Literal("==").set_results_name("EQ", list_all_matches=True)
  NE = Literal("!=").set_results_name("NE", list_all_matches=True)
  LT = Literal("<").set_results_name("LT", list_all_matches=True)
  GT = Literal(">").set_results_name("GT", list_all_matches=True)
  LE = Literal("<=").set_results_name("LE", list_all_matches=True)
  GE = Literal(">=").set_results_name("GE", list_all_matches=True)

  # BOOLEAN OPERATORS
  AND = Literal("&&").set_results_name("AND", list_all_matches=True)
  OR = Literal("||").set_results_name("OR", list_all_matches=True)
  NOT = Literal("!").set_results_name("NOT", list_all_matches=True)

  # DELIMITERS
  PARENI = Literal("(").set_results_name("PARENI", list_all_matches=True)
  PAREND = Literal(")").set_results_name("PAREND", list_all_matches=True)
  LLAVEI = Literal("{").set_results_name("LLAVEI", list_all_matches=True)
  LLAVED = Literal("}").set_results_name("LLAVED", list_all_matches=True)
  PUNTOYCOMA = Literal(";").set_results_name("PUNTOYCOMA", list_all_matches=True)
  COMA = Literal(",").set_results_name("COMA", list_all_matches=True)

  # TYPES
  INT = Keyword("int").set_results_name("INT_TIPO", list_all_matches=True)
  FLOAT = Keyword("float").set_results_name("FLOAT_TIPO", list_all_matches=True)
  BOOL = Keyword("bool").set_results_name("BOOL_TIPO", list_all_matches=True)
  STRING = Keyword("string").set_results_name("STRING_TIPO", list_all_matches=True)

  # COMMENTS
  SINGLELINE_COMMENT = (Literal("//").suppress() + Regex(r".*").suppress())
  MULTILINE_COMMENT = (Literal("/*").suppress() + Regex(r"[\s\S]*\*/").suppress())

  # HANDLE ERRORS
  OPEN_STRING = Regex(r'"[^"\n]*(?=\n|$)|\'[^\'\n]*(?=\n|$)').set_results_name("OPEN_STRING", list_all_matches=True)
  ILEGAL_SYMBOL = Regex(r".").set_results_name("ILEGAL_SYMBOL", list_all_matches=True)
  INVALID_ID = (Regex(r"[^a-zA-Z][a-zA-Z][a-zA-Z0-9]*")).set_results_name("INVALID_ID", list_all_matches=True)
  BADLY_FORMED_NUMBER = Regex(r"(\d+(\.\d+)?[eE][+-]?|\d+\.(?!\d)|\d*\.\d+\.\d*)").set_results_name("BADLY_FORMED_NUMBER", list_all_matches=True)

  # GROUPING
  tipo = MatchFirst([INT, FLOAT, BOOL, STRING])
  literal = MatchFirst([FLOAT_LITERAL, STRING_LITERAL, BOOL_LITERAL])
  keyword = MatchFirst([IF, ELSE, WHILE, FOR, PRINT, BREAK, CONTINUE])
  comment = MatchFirst([SINGLELINE_COMMENT, MULTILINE_COMMENT])
  increment_decrement = MatchFirst([INCREMENT, DECREMENT])
  relational_operator = MatchFirst([EQ, NE, LE, GE, LT, GT])
  boolean_operator = MatchFirst([AND, OR, NOT])
  arithmetic_operator = MatchFirst([MAS, MENOS, MULT, DIV, MOD])
  delimeters = MatchFirst([PARENI, PAREND, LLAVEI, LLAVED, PUNTOYCOMA, COMA])
  errors = MatchFirst([OPEN_STRING, INVALID_ID])

  lexer = MatchFirst([
      comment,
      keyword,
      tipo,
      BADLY_FORMED_NUMBER,
      literal,
      ID,
      increment_decrement,
      relational_operator,
      boolean_operator,
      arithmetic_operator,
      ASIGN,
      delimeters,
      errors,
      INT_LITERAL,
      ILEGAL_SYMBOL
  ])

  with open("program.txt") as f:
    text = f.read()

  prev_line = 1
  prev_name = ""
  symbol_table = []
  errored = False

  for tokens, start, end in lexer.scan_string(text):
    line = lineno(start, text)

    for name, values in tokens.items():
      for v in values:
        if prev_name in types.__members__ and name == "ID":
          symbol_table.append((v, line))

        prev_name = name

        if name in error_types.__members__:
          error = error_types[name]
          print("\n")
          print(f"ERROR LEXICO (linea {line}): {error.value}: '{v}'")
          print("\n")
          errored = True
          break


        if line != prev_line and not errored:
          print("\n")

        errored = False

        print(f"({line}, {name}, {v})")
        prev_line = line

  print("\n")
  print("TABLE DE SIMBOLOS:")
  for value in symbol_table:
    print(f"{value[0]} -> linea {value[1]}")


try:
  parse()
except Exception as e:
  print("No se ha cargado el archivo program.txt")
