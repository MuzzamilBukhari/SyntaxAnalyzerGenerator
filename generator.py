import pandas as pd
import re

def generate_syntax_analyzer(excel_path, output_file_path="syntax_analyzer.py"):
    """
    Generate a syntax analyzer class from grammar rules in an Excel file
    
    Args:
        excel_path (str): Path to the Excel file containing grammar rules
        output_file_path (str): Path to save the generated Python file
    """
    # Read grammar from Excel file
    print(f"Reading grammar from {excel_path}...")
    df = pd.read_excel(excel_path)
    
    # Dictionary to store non-terminals and their production rules
    grammar = {}
    
    # Process each row in the Excel file
    for _, row in df.iterrows():
        # Convert values to string to prevent strip() errors on non-string types
        try:
            production_rule = str(row['Production Rules']).strip()
            selection_set = str(row['Selection Set']).strip()
            
            # Skip rows where production rule is empty or NaN
            if production_rule == 'nan' or not production_rule:
                continue
            
            # Extract non-terminal from production rule
            non_terminal_match = re.match(r'<([^>]+)>', production_rule)
            if non_terminal_match:
                non_terminal = non_terminal_match.group(0)
                non_terminal_name = non_terminal_match.group(1)
                
                # Extract the right-hand side of the production rule
                rule_parts = production_rule.split('→', 1)
                if len(rule_parts) > 1:
                    production_body = rule_parts[1].strip()
                else:
                    production_body = ""
                
                # Process selection set - remove curly braces around equals sign
                selection_set = selection_set.replace('{=}', '=')
                
                # Skip if selection set is 'nan' or empty
                if selection_set == 'nan':
                    selection_set = ""
                    
                # Split the selection set by comma and remove leading/trailing whitespace
                terminals = [term.strip() for term in selection_set.split(',') if term.strip() and term.strip() != 'nan']
                
                # Add to grammar dictionary
                if non_terminal not in grammar:
                    grammar[non_terminal] = []
                
                grammar[non_terminal].append({
                    'body': production_body,
                    'selection': terminals
                })
        except Exception as e:
            print(f"Error processing row: {row}, Error: {e}")
            continue
    
    print(f"Found {len(grammar)} non-terminals in grammar.")
    
    # Generate Python code
    with open(output_file_path, 'w', encoding='utf-8') as f:
        # Write class definition
        f.write("class SA:\n")
        f.write("    def __init__(self, token_stream):\n")
        f.write("        self.TS = token_stream\n")
        f.write("        self.index = 0\n")
        f.write("        \n")
        f.write("        if self.S():\n")
        f.write("            if self.index < len(self.TS) and self.TS[self.index] == \"$\":\n")
        f.write("                print(\"Syntax is valid\")\n")
        f.write("                return\n")
        f.write("            else:\n")
        f.write("                print(\"Syntax is invalid\")\n")
        f.write("        else:\n")
        f.write("            print(\"Syntax is invalid\")\n")
        f.write("\n")
        
        # Generate methods for each non-terminal
        for non_terminal, productions in grammar.items():
            # Extract name without angle brackets
            func_name = non_terminal.strip('<>')
            
            # Replace apostrophes with _prime to make valid function names
            func_name = func_name.replace("'", "_prime")
            
            f.write(f"    def {func_name}(self):\n")
            
            # If there's only one production rule
            if len(productions) == 1:
                production = productions[0]
                body = production['body']
                
                # Handle epsilon production
                if body == "∈" or body == "":
                    f.write("        # Epsilon production\n")
                    f.write("        return True\n\n")
                    continue
                
                # Generate code for the production body
                generate_production_body(f, body, 8)
                f.write("\n")
            else:
                # Multiple production rules - use if-elif structure based on selection sets
                for i, production in enumerate(productions):
                    selection_set = production['selection']
                    body = production['body']
                    
                    # Format the selection set for condition
                    condition = ", ".join([f"'{term}'" for term in selection_set if term.strip()])
                    
                    if i == 0:
                        f.write(f"        if self.index < len(self.TS) and self.TS[self.index].CP in {{{condition}}}:\n")
                    else:
                        f.write(f"        elif self.index < len(self.TS) and self.TS[self.index].CP in {{{condition}}}:\n")
                    
                    # Handle epsilon production
                    if body == "∈" or body == "":
                        f.write("            # Epsilon production\n")
                        f.write("            return True\n")
                        continue
                    
                    # For non-epsilon rules
                    if body.strip():
                        symbols = re.findall(r'<[^>]+>|[^\s<>]+', body)
                        process_symbols(f, symbols, 12)
                
                # End with a return False
                f.write("        return False\n\n")
    
    print(f"Syntax analyzer class generated and saved to {output_file_path}")

def process_symbols(f, symbols, indent_level):
    """
    Process symbols in production body with proper nesting according to the example
    
    Args:
        f: File handle to write to
        symbols: List of symbols (terminals and non-terminals)
        indent_level: Current indentation level
    """
    if not symbols:
        return
    
    indent = " " * indent_level
    symbol = symbols[0]
    remaining = symbols[1:]
    
    if symbol.startswith('<') and symbol.endswith('>'):
        # Non-terminal
        func_name = symbol.strip('<>')
        f.write(f"{indent}if self.{func_name}():\n")
        
        if remaining:
            # Process remaining symbols with increased indentation
            process_symbols(f, remaining, indent_level + 4)
        else:
            # Last symbol
            f.write(f"{indent}    return True\n")
    else:
        # Terminal
        f.write(f"{indent}if self.TS[self.index].CP == '{symbol}':\n")
        f.write(f"{indent}    self.index += 1\n")
        
        if remaining:
            # Process remaining symbols with increased indentation
            process_symbols(f, remaining, indent_level + 4)
        else:
            # Last symbol
            f.write(f"{indent}    return True\n")

def generate_production_body(f, body, indent_level):
    """
    Generate code for a production body - for single production rules
    
    Args:
        f: File handle to write to
        body (str): The production body (right side of the rule)
        indent_level (int): Indentation level for the generated code
    """
    symbols = re.findall(r'<[^>]+>|[^\s<>]+', body)
    process_symbols(f, symbols, indent_level)

if __name__ == "__main__":
    import sys
    import os
    
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Use relative path to the Excel file in the same directory
    excel_path = os.path.join(current_dir, "grammer.xlsx")
    output_path = "syntax_analyzer.py"
    generate_syntax_analyzer(excel_path, output_path)
