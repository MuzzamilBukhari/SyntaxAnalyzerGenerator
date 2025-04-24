import pandas as pd
import re
from collections import defaultdict

def extract_terminals_and_nonterminals(production):
    """Extract terminal and non-terminal symbols from a production rule."""
    terminals = []
    nonterminals = []
    
    # Find all non-terminals (enclosed in < >)
    non_term_pattern = r'<([^>]+)>'
    nonterminals = re.findall(non_term_pattern, production)
    
    # Remove non-terminals and extract terminals
    # This is a simplified approach - might need refinement based on your grammar format
    cleaned = re.sub(non_term_pattern, '', production).strip()
    tokens = [t.strip() for t in cleaned.split() if t.strip() and t.strip() not in ['→', '->', '*', '{', '}', '|']]
    terminals = tokens
    
    return terminals, nonterminals

def generate_parser_code(excel_path, output_path):
    """Generate parser code from Excel file containing CFG rules."""
    try:
        # Read the Excel file
        df = pd.read_excel(excel_path)
        
        # Check if columns match expected format
        expected_cols = ['Production Rules', 'Non-terminal Symbol', 'Selection Set (FIRST)', 'Follow Set']
        if not all(col in df.columns for col in expected_cols):
            print(f"Error: Excel file must contain columns: {expected_cols}")
            print(f"Found columns: {list(df.columns)}")
            return
        
        # Start with header code
        code = """# Generated Syntax Analyzer
# This code is automatically generated based on CFG rules

# Global variables
TS = []  # Token Stream
index = 0  # Current token index

class Token:
    def __init__(self, cp, vp=""):
        self.CP = cp  # Class Part
        self.VP = vp  # Value Part

def init_parser(tokens):
    global TS, index
    TS = tokens
    index = 0

"""
        
        # Group productions by non-terminal
        grammar = defaultdict(list)
        for _, row in df.iterrows():
            if pd.notna(row['Production Rules']):
                rule = row['Production Rules']
                first_set = row['Selection Set (FIRST)'] if pd.notna(row['Selection Set (FIRST)']) else ""
                follow_set = row['Follow Set'] if pd.notna(row['Follow Set']) else ""
                
                # Extract non-terminal and its production
                lhs, rhs = rule.split('→', 1) if '→' in rule else rule.split('->', 1)
                lhs = lhs.strip()
                rhs = rhs.strip()
                
                grammar[lhs].append((rhs, first_set, follow_set))
        
        # Generate code for each grouped non-terminal
        for non_terminal, productions in grammar.items():
            function_name = non_terminal.replace('<', '').replace('>', '').replace('-', '_')
            code += f"def {function_name}():\n"
            
            # Generate if-elif statements for each production
            for i, (prod, first_set, follow_set) in enumerate(productions):
                # Determine condition based on FIRST set
                conditions = []
                
                # If production is empty (epsilon), use FOLLOW set instead
                if prod.strip() == 'ε' or prod.strip() == 'epsilon':
                    # Use FOLLOW set for epsilon productions
                    if follow_set:
                        follow_items = follow_set.replace('{', '').replace('}', '').split(',')
                        for item in follow_items:
                            item = item.strip()
                            if item and item != 'ε' and item != 'epsilon':
                                if item.startswith('<') and item.endswith('>'):
                                    # Skip non-terminals in follow set
                                    continue
                                if item == '$':
                                    conditions.append("index >= len(TS)")
                                else:
                                    conditions.append(f'TS[index].CP == "{item}"')
                    
                    if not conditions:
                        conditions.append("True  # Epsilon production")
                else:
                    # Use FIRST set for non-epsilon productions
                    if first_set:
                        first_items = first_set.replace('{', '').replace('}', '').split(',')
                        for item in first_items:
                            item = item.strip()
                            if item and item != 'ε' and item != 'epsilon':
                                if item.startswith('<') and item.endswith('>'):
                                    # Skip non-terminals in first set for now
                                    continue
                                if item == '$':
                                    conditions.append("index >= len(TS)")
                                else:
                                    conditions.append(f'TS[index].CP == "{item}"')
                    
                    # If no valid FIRST conditions were created, we'll use the first terminal from the production
                    if not conditions:
                        terminals, nonterminals = extract_terminals_and_nonterminals(prod)
                        if terminals:
                            conditions.append(f'TS[index].CP == "{terminals[0]}"')
                        elif nonterminals:
                            conditions.append(f"True  # Check for {nonterminals[0]}")
                        else:
                            conditions.append("True")
                
                # Write the condition
                if i == 0:
                    code += "  if "
                else:
                    code += "  elif "
                
                code += " or ".join(conditions) if conditions else "True"
                code += ":\n"
                
                # Process production body
                if prod.strip() == 'ε' or prod.strip() == 'epsilon':
                    # For epsilon production, just return true
                    code += "    return True\n"
                else:
                    # Process each symbol in the production
                    indent = "    "
                    
                    # Split production into symbols
                    symbols = [s.strip() for s in prod.split() if s.strip() and s.strip() not in ['→', '->', '*']]
                    
                    # Special handling for { } in grammar rules
                    in_braces = False
                    for symbol in symbols:
                        if symbol == '{':
                            in_braces = True
                            continue
                        elif symbol == '}':
                            in_braces = False
                            continue
                        
                        if symbol.startswith('<') and symbol.endswith('>'):
                            # Non-terminal - call its function
                            nt_name = symbol.replace('<', '').replace('>', '').replace('-', '_')
                            code += f"{indent}if {nt_name}():\n"
                            indent += "  "
                        elif symbol:
                            # Terminal - match token and increment index
                            code += f"{indent}if TS[index].CP == \"{symbol}\":\n"
                            code += f"{indent}  index += 1\n"
                            indent += "  "
                    
                    # Return true if all matches succeeded
                    code += f"{indent}return True\n"
            
            # Add final return false
            code += "  return False\n\n"
        
        # Add main parser function
        code += """def parse(tokens):
    """
        
        # Get the start symbol (usually the first production rule)
        start_symbol = None
        for _, row in df.iterrows():
            rule = row['Production Rules']
            if pd.notna(rule):
                start_symbol = rule.split('→')[0].strip() if '→' in rule else rule.split('->')[0].strip()
                break
        
        if start_symbol:
            start_function = start_symbol.replace('<', '').replace('>', '').replace('-', '_')
            code += f"""    # Initialize parser
    init_parser(tokens)
    
    # Start parsing from the start symbol
    if {start_function}() and index >= len(TS):
        print("Parsing successful!")
        return True
    else:
        print(f"Syntax error at token: {{index if index < len(TS) else 'end of input'}}")
        return False
"""
        
        # Write the generated code to the output file with UTF-8 encoding
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code)
            
        print(f"Parser code successfully generated and saved to {output_path}")
        
    except Exception as e:
        print(f"Error generating parser code: {e}")

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python parser_generator.py <excel_file_path> <output_code_path>")
        sys.exit(1)
        
    excel_path = sys.argv[1]
    output_path = sys.argv[2]
    
    generate_parser_code(excel_path, output_path)