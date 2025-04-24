# Generated Syntax Analyzer
# This code is automatically generated based on CFG rules

# Global variables
TS = []  # Token Stream
# append $ to the end of the token stream to indicate end of input

index = 0  # Current token index

class Token:
    def __init__(self, cp, vp=""):
        self.CP = cp  # Class Part
        self.VP = vp  # Value Part

def init_parser(tokens):
    global TS, index
    TS = tokens
    index = 0

def Program():
  if TS[index].CP == "DT" or TS[index].CP == "interface":
    if TS[index].CP == "<Decl>*":
      index += 1
      return True
  return False

def Decl():
  if TS[index].CP == "DT":
    if Var_Decl():
      if Decl_Prime():
        return True
  elif TS[index].CP == "Public" or TS[index].CP == "Private":
    if Modifier():
      if Decl_Type():
        if Decl_Prime():
          return True
  elif TS[index].CP == "interface":
    if TS[index].CP == "interface":
      index += 1
      if TS[index].CP == "ID":
        index += 1
        if Interface_Body():
          if Decl_Prime():
            return True
  elif TS[index].CP == "while" or TS[index].CP == "for" or TS[index].CP == "if" or TS[index].CP == "return" or TS[index].CP == "ID" or TS[index].CP == "++" or TS[index].CP == "--":
    if Stmt():
      if Decl_Prime():
        return True
  return False

def Decl_Prime():
  if TS[index].CP == "DT" or TS[index].CP == "interface":
    if Decl():
      return True
  elif index >= len(TS):
    return True
  return False

def Decl_Type():
  if TS[index].CP == "class":
    if TS[index].CP == "class":
      index += 1
      if cont():
        if Inheritance():
          if Body():
            return True
  elif TS[index].CP == "(":
    if cont():
      if TS[index].CP == "(":
        index += 1
        if Params():
          if TS[index].CP == ")":
            index += 1
            if Body():
              return True
  return False

def Var_Decl():
  if TS[index].CP == "DT":
    if TS[index].CP == "DT":
      index += 1
      if TS[index].CP == "ID":
        index += 1
        if Var_Init():
          if TS[index].CP == ";":
            index += 1
            return True
  return False

def Var_Init():
  if TS[index].CP == "=":
    if TS[index].CP == "=":
      index += 1
      if Expr():
        return True
  elif TS[index].CP == ";":
    return True
  return False

def Func_Decl():
  if TS[index].CP == "Public" or TS[index].CP == "Private":
    if Modifier():
      if cont():
        if TS[index].CP == "(":
          index += 1
          if Params():
            if TS[index].CP == ")":
              index += 1
              if Body():
                return True
  return False

def Params():
  if TS[index].CP == "DT":
    if TS[index].CP == "DT":
      index += 1
      if TS[index].CP == "ID":
        index += 1
        if Default_Value():
          if Param_Rest():
            return True
  elif TS[index].CP == ")":
    return True
  return False

def Param_Rest():
  if TS[index].CP == ",":
    if TS[index].CP == ",":
      index += 1
      if TS[index].CP == "DT":
        index += 1
        if TS[index].CP == "ID":
          index += 1
          if Default_Value():
            if Param_Rest():
              return True
  elif TS[index].CP == ")":
    return True
  return False

def Default_Value():
  if TS[index].CP == "=":
    if TS[index].CP == "=":
      index += 1
      if Expr():
        return True
  elif TS[index].CP == ")":
    return True
  return False

def Class_Decl():
  if TS[index].CP == "Public" or TS[index].CP == "Private":
    if Modifier():
      if TS[index].CP == "class":
        index += 1
        if cont():
          if Inheritance():
            if Body():
              return True
  return False

def Inheritance():
  if TS[index].CP == "extends":
    if TS[index].CP == "extends":
      index += 1
      if TS[index].CP == "ID":
        index += 1
        return True
  elif True  # Epsilon production:
    return True
  return False

def Modifier():
  if TS[index].CP == "Public":
    if TS[index].CP == "Public":
      index += 1
      return True
  elif TS[index].CP == "Private":
    if TS[index].CP == "Private":
      index += 1
      return True
  elif TS[index].CP == "cont" or TS[index].CP == "class":
    return True
  return False

def Interface_Decl():
  if TS[index].CP == "interface":
    if TS[index].CP == "interface":
      index += 1
      if TS[index].CP == "ID":
        index += 1
        if Interface_Body():
          return True
  return False

def Interface_Body():
  if TS[index].CP == "func":
    if Method_Sig():
      if Interface_Body():
        return True
  elif True  # Epsilon production:
    return True
  return False

def Method_Sig():
  if TS[index].CP == "func":
    if TS[index].CP == "func":
      index += 1
      if TS[index].CP == "ID":
        index += 1
        if TS[index].CP == "(":
          index += 1
          if Params():
            if TS[index].CP == ")":
              index += 1
              if Type():
                if Semi():
                  return True
  return False

def Semi():
  if TS[index].CP == ";":
    if TS[index].CP == ";":
      index += 1
      return True
  elif True  # Epsilon production:
    return True
  return False

def Type():
  if TS[index].CP == "num" or TS[index].CP == "str" or TS[index].CP == "bool" or TS[index].CP == "float":
    if Primitive_Type():
      return True
  elif TS[index].CP == "num" or TS[index].CP == "str" or TS[index].CP == "bool" or TS[index].CP == "float" or TS[index].CP == "ID":
    if Base_Type():
      if Array_Suffix():
        return True
  elif TS[index].CP == "List" or TS[index].CP == "Dict":
    if Container_Type():
      return True
  elif TS[index].CP == "ID":
    if TS[index].CP == "ID":
      index += 1
      return True
  elif TS[index].CP == "void":
    if TS[index].CP == "void":
      index += 1
      return True
  return False

def Container_Type():
  if TS[index].CP == "List" or TS[index].CP == "Dict":
    if Container_Name():
      if TS[index].CP == "<":
        index += 1
        if Container_Params():
          if TS[index].CP == ">":
            index += 1
            return True
  return False

def Container_Params():
  if TS[index].CP == "num" or TS[index].CP == "str" or TS[index].CP == "bool" or TS[index].CP == "float" or TS[index].CP == "ID" or TS[index].CP == "void":
    if Type():
      if Second_Type():
        return True
  return False

def Second_Type():
  if TS[index].CP == ",":
    if TS[index].CP == ",":
      index += 1
      if Type():
        return True
  elif TS[index].CP == ">":
    return True
  return False

def Stmt():
  if TS[index].CP == "while" or TS[index].CP == "for" or TS[index].CP == "if" or TS[index].CP == "return":
    if SST():
      return True
  elif TS[index].CP == "while" or TS[index].CP == "for" or TS[index].CP == "if" or TS[index].CP == "return":
    if SST():
      if SST():
        if MST_Rest():
          return True
  return False

def MST_Rest():
  if TS[index].CP == "while" or TS[index].CP == "for" or TS[index].CP == "if" or TS[index].CP == "return":
    if SST():
      if MST_Rest():
        return True
  elif True  # Epsilon production:
    return True
  return False

def SST():
  if TS[index].CP == "while":
    if TS[index].CP == "while":
      index += 1
      if TS[index].CP == "(":
        index += 1
        if cond():
          if TS[index].CP == ")":
            index += 1
            if Body():
              return True
  elif True  # Check for Dec-st:
    if Dec_st():
      return True
  elif TS[index].CP == "for":
    if TS[index].CP == "for":
      index += 1
      if TS[index].CP == "(":
        index += 1
        if For_Init():
          if TS[index].CP == ";":
            index += 1
            if For_Cond():
              if TS[index].CP == ";":
                index += 1
                if For_Update():
                  if TS[index].CP == ")":
                    index += 1
                    if Body():
                      return True
  elif TS[index].CP == "if":
    if TS[index].CP == "if":
      index += 1
      if TS[index].CP == "(":
        index += 1
        if cond():
          if TS[index].CP == ")":
            index += 1
            if Body():
              if Elif_Part():
                if Else_Part():
                  return True
  elif TS[index].CP == "return":
    if TS[index].CP == "return":
      index += 1
      if Return_Expr():
        if TS[index].CP == ";":
          index += 1
          return True
  elif TS[index].CP == "ID" or TS[index].CP == "NUM" or TS[index].CP == "STR" or TS[index].CP == "BOOL" or TS[index].CP == "(" or TS[index].CP == "++" or TS[index].CP == "--":
    if Expr():
      if TS[index].CP == ";":
        index += 1
        return True
  return False

def Return_Expr():
  if TS[index].CP == "ID" or TS[index].CP == "NUM" or TS[index].CP == "STR" or TS[index].CP == "BOOL" or TS[index].CP == "(" or TS[index].CP == "++" or TS[index].CP == "--":
    if Expr():
      return True
  elif TS[index].CP == ";":
    return True
  return False

def if_else():
  if TS[index].CP == "if":
    if TS[index].CP == "if":
      index += 1
      if TS[index].CP == "(":
        index += 1
        if cond():
          if TS[index].CP == ")":
            index += 1
            if Body():
              if Elif_Part():
                if Else_Part():
                  return True
  return False

def Elif_Part():
  if TS[index].CP == "elif":
    if TS[index].CP == "elif":
      index += 1
      if TS[index].CP == "(":
        index += 1
        if cond():
          if TS[index].CP == ")":
            index += 1
            if Body():
              if Elif_Part():
                return True
  elif True  # Epsilon production:
    return True
  return False

def Else_Part():
  if TS[index].CP == "else":
    if TS[index].CP == "else":
      index += 1
      if Body():
        return True
  elif True  # Epsilon production:
    return True
  return False

def For_Init():
  if TS[index].CP == "DT":
    if Var_Decl():
      return True
  elif TS[index].CP == "ID":
    if Asgn_st():
      return True
  elif TS[index].CP == ";":
    return True
  return False

def For_Cond():
  if TS[index].CP == "ID" or TS[index].CP == "NUM" or TS[index].CP == "STR" or TS[index].CP == "BOOL" or TS[index].CP == "(" or TS[index].CP == "++" or TS[index].CP == "--":
    if Expr():
      return True
  elif TS[index].CP == ";":
    return True
  return False

def For_Update():
  if TS[index].CP == "ID" or TS[index].CP == "NUM" or TS[index].CP == "STR" or TS[index].CP == "BOOL" or TS[index].CP == "(" or TS[index].CP == "++" or TS[index].CP == "--":
    if Expr():
      return True
  elif TS[index].CP == ")":
    return True
  return False

def Asgn_st():
  if TS[index].CP == "ID":
    if LValue():
      if Asgn_OP():
        if Expr():
          if TS[index].CP == ";":
            index += 1
            return True
  return False

def LValue():
  if TS[index].CP == "ID":
    if TS[index].CP == "ID":
      index += 1
      if LValue_Suffix():
        return True
  return False

def LValue_Suffix():
  if TS[index].CP == "[":
    if TS[index].CP == "[":
      index += 1
      if Expr():
        if TS[index].CP == "]":
          index += 1
          return True
  elif True  # Epsilon production:
    return True
  return False

def Asgn_OP():
  if TS[index].CP == "=":
    if TS[index].CP == "=":
      index += 1
      return True
  elif TS[index].CP == "+=":
    if TS[index].CP == "+=":
      index += 1
      return True
  elif TS[index].CP == "-=":
    if TS[index].CP == "-=":
      index += 1
      return True
  elif TS[index].CP == "*=":
    if TS[index].CP == "*=":
      index += 1
      return True
  elif TS[index].CP == "/=":
    if TS[index].CP == "/=":
      index += 1
      return True
  elif TS[index].CP == "%=":
    if TS[index].CP == "%=":
      index += 1
      return True
  return False

def Expr():
  if True  # Check for Logic-Or-Expr:
    if Logic_Or_Expr():
      return True
  return False

def Logic_Or_Expr():
  if True  # Check for Logic-And-Expr:
    if Logic_And_Expr():
      if Logic_Or_Tail():
        return True
  return False

def Logic_Or_Tail():
  if TS[index].CP == "or":
    if TS[index].CP == "or":
      index += 1
      if Logic_And_Expr():
        if Logic_Or_Tail():
          return True
  elif TS[index].CP == ";" or TS[index].CP == "]" or TS[index].CP == ")" or TS[index].CP == "in":
    return True
  return False

def Logic_And_Expr():
  if True  # Check for Equality-Expr:
    if Equality_Expr():
      if Logic_And_Tail():
        return True
  return False

def Logic_And_Tail():
  if TS[index].CP == "and":
    if TS[index].CP == "and":
      index += 1
      if Equality_Expr():
        if Logic_And_Tail():
          return True
  elif TS[index].CP == "or" or TS[index].CP == ";" or TS[index].CP == "]" or TS[index].CP == ")" or TS[index].CP == "in":
    return True
  return False

def Equality_Expr():
  if True  # Check for Rel-Expr:
    if Rel_Expr():
      if Equality_Tail():
        return True
  return False

def Equality_Tail():
  if TS[index].CP == "==":
    if TS[index].CP == "==":
      index += 1
      if Rel_Expr():
        if Equality_Tail():
          return True
  elif TS[index].CP == "!=":
    if TS[index].CP == "!=":
      index += 1
      if Rel_Expr():
        if Equality_Tail():
          return True
  elif TS[index].CP == "and" or TS[index].CP == "or" or TS[index].CP == ";" or TS[index].CP == "]" or TS[index].CP == ")" or TS[index].CP == "in":
    return True
  return False

def Rel_Expr():
  if True  # Check for Add-Expr:
    if Add_Expr():
      if Rel_Tail():
        return True
  return False

def Rel_Tail():
  if TS[index].CP == "<":
    if TS[index].CP == "<":
      index += 1
      if Add_Expr():
        if Rel_Tail():
          return True
  elif TS[index].CP == ">":
    if TS[index].CP == ">":
      index += 1
      if Add_Expr():
        if Rel_Tail():
          return True
  elif TS[index].CP == "<=":
    if TS[index].CP == "<=":
      index += 1
      if Add_Expr():
        if Rel_Tail():
          return True
  elif TS[index].CP == ">=":
    if TS[index].CP == ">=":
      index += 1
      if Add_Expr():
        if Rel_Tail():
          return True
  elif TS[index].CP == "==" or TS[index].CP == "!=" or TS[index].CP == "and" or TS[index].CP == "or" or TS[index].CP == ";" or TS[index].CP == "]" or TS[index].CP == ")" or TS[index].CP == "in":
    return True
  return False

def Add_Expr():
  if True  # Check for Mult-Expr:
    if Mult_Expr():
      if Add_Tail():
        return True
  return False

def Add_Tail():
  if TS[index].CP == "+":
    if TS[index].CP == "+":
      index += 1
      if Mult_Expr():
        if Add_Tail():
          return True
  elif TS[index].CP == "-":
    if TS[index].CP == "-":
      index += 1
      if Mult_Expr():
        if Add_Tail():
          return True
  elif TS[index].CP == "<" or TS[index].CP == ">" or TS[index].CP == "<=" or TS[index].CP == ">=" or TS[index].CP == "==" or TS[index].CP == "!=" or TS[index].CP == "and" or TS[index].CP == "or" or TS[index].CP == ";" or TS[index].CP == "]" or TS[index].CP == ")" or TS[index].CP == "in":
    return True
  return False

def Mult_Expr():
  if True  # Check for Unary-Expr:
    if Unary_Expr():
      if Mult_Tail():
        return True
  return False

def Mult_Tail():
  if TS[index].CP == "*":
    if Unary_Expr():
      if Mult_Tail():
        return True
  elif TS[index].CP == "/":
    if TS[index].CP == "/":
      index += 1
      if Unary_Expr():
        if Mult_Tail():
          return True
  elif TS[index].CP == "%":
    if TS[index].CP == "%":
      index += 1
      if Unary_Expr():
        if Mult_Tail():
          return True
  elif TS[index].CP == "+" or TS[index].CP == "-" or TS[index].CP == "<" or TS[index].CP == ">" or TS[index].CP == "<=" or TS[index].CP == ">=" or TS[index].CP == "==" or TS[index].CP == "!=" or TS[index].CP == "and" or TS[index].CP == "or" or TS[index].CP == ";" or TS[index].CP == "]" or TS[index].CP == ")" or TS[index].CP == "in":
    return True
  return False

def Unary_Expr():
  if TS[index].CP == "!":
    if TS[index].CP == "!":
      index += 1
      if Unary_Expr():
        return True
  elif TS[index].CP == "-":
    if TS[index].CP == "-":
      index += 1
      if Unary_Expr():
        return True
  elif TS[index].CP == "ID" or TS[index].CP == "NUM" or TS[index].CP == "STR" or TS[index].CP == "BOOL" or TS[index].CP == "(":
    if Primary_Expr():
      return True
  return False

def Primary_Expr():
  if TS[index].CP == "ID":
    if TS[index].CP == "ID":
      index += 1
      if Primary_Suffix():
        return True
  elif TS[index].CP == "NUM":
    if TS[index].CP == "NUM":
      index += 1
      return True
  elif TS[index].CP == "STR":
    if TS[index].CP == "STR":
      index += 1
      return True
  elif TS[index].CP == "BOOL":
    if TS[index].CP == "BOOL":
      index += 1
      return True
  elif TS[index].CP == "(":
    if TS[index].CP == "(":
      index += 1
      if Expr():
        if TS[index].CP == ")":
          index += 1
          return True
  return False

def Primary_Suffix():
  if TS[index].CP == "[":
    if TS[index].CP == "[":
      index += 1
      if Expr():
        if TS[index].CP == "]":
          index += 1
          return True
  elif TS[index].CP == "(":
    if TS[index].CP == "(":
      index += 1
      if Args():
        if TS[index].CP == ")":
          index += 1
          return True
  elif TS[index].CP == ".":
    if TS[index].CP == ".":
      index += 1
      if TS[index].CP == "ID":
        index += 1
        return True
  elif TS[index].CP == "++":
    if TS[index].CP == "++":
      index += 1
      return True
  elif TS[index].CP == "--":
    if TS[index].CP == "--":
      index += 1
      return True
  elif TS[index].CP == "*" or TS[index].CP == "/" or TS[index].CP == "%" or TS[index].CP == "+" or TS[index].CP == "-" or TS[index].CP == "<" or TS[index].CP == ">" or TS[index].CP == "<=" or TS[index].CP == ">=" or TS[index].CP == "==" or TS[index].CP == "!=" or TS[index].CP == "and" or TS[index].CP == "or" or TS[index].CP == ";" or TS[index].CP == "]" or TS[index].CP == ")" or TS[index].CP == "in":
    return True
  return False

def Args():
  if TS[index].CP == "ID" or TS[index].CP == "NUM" or TS[index].CP == "STR" or TS[index].CP == "BOOL" or TS[index].CP == "(" or TS[index].CP == "++" or TS[index].CP == "--":
    if Expr():
      if Args_Rest():
        return True
  elif TS[index].CP == ")":
    return True
  return False

def Args_Rest():
  if TS[index].CP == ",":
    if TS[index].CP == ",":
      index += 1
      if Expr():
        if Args_Rest():
          return True
  elif TS[index].CP == ")":
    return True
  return False

def Body():
  if True  # Check for MST:
    if MST():
      return True
  elif TS[index].CP == "while" or TS[index].CP == "for" or TS[index].CP == "if" or TS[index].CP == "return":
    if SST():
      return True
  return False

def parse(tokens):
        # Initialize parser
    init_parser(tokens)
    
    # Start parsing from the start symbol
    if Program() and index >= len(TS):
        print("Parsing successful!")
        return True
    else:
        print(f"Syntax error at token: {index if index < len(TS) else 'end of input'}")
        return False
