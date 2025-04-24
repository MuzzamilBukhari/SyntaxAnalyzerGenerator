"""
This demo shows how the generated parser will work using the example you provided:

<F> -> <TS> ID <opts>
    -> <cast>
    -> ! <F>
    -> (<E>)

And following your logic of index++ for terminals.
"""

# Example of how the generated parser will look for your CFG rules
class Token:
    def __init__(self, cp, vp=""):
        self.CP = cp  # Class Part (Type of token)
        self.VP = vp  # Value Part (Actual value)

# Sample token stream for testing
TS = []  # Token Stream
index = 0  # Current token index

def init_parser(tokens):
    global TS, index
    TS = tokens
    index = 0

# Example function generated for the <F> non-terminal
def F():
    global index
    
    # First production: <F> -> <TS> ID <opts>
    if TS[index].CP == "this" or TS[index].CP == "Super" or TS[index].CP == "ID":
        if TS():  # Call function for <TS> non-terminal
            if TS[index].CP == "ID":
                index += 1  # Match terminal ID and increment index
                if opts():  # Call function for <opts> non-terminal
                    return True
    
    # Second production: <F> -> <cast>
    elif TS[index].CP == "string" or TS[index].CP == "int" or TS[index].CP == "float":  # Assuming these are in FIRST(<cast>)
        if cast():  # Call function for <cast> non-terminal
            return True
    
    # Third production: <F> -> ! <F>
    elif TS[index].CP == "!":
        index += 1  # Match terminal ! and increment index
        if F():  # Recursive call to F()
            return True
    
    # Fourth production: <F> -> (<E>)
    elif TS[index].CP == "(":
        index += 1  # Match terminal ( and increment index
        if E():  # Call function for <E> non-terminal
            if TS[index].CP == ")":
                index += 1  # Match terminal ) and increment index
                return True
    
    return False

# Stub functions for the other non-terminals used in the example
def TS():
    global index
    # Simplified implementation for demo
    if TS[index].CP in ["this", "Super", "ID"]:
        index += 1
        return True
    return False

def opts():
    # Simplified implementation for demo
    return True

def cast():
    # Simplified implementation for demo
    return True

def E():
    # Simplified implementation for demo
    return True

# Test with a sample token stream
def test_parser():
    # Creating a sample token stream for the input "this ID"
    tokens = [
        Token("this"),
        Token("ID", "myVariable")
    ]
    
    init_parser(tokens)
    result = F()
    
    if result and index >= len(TS):
        print("Parsing successful!")
        return True
    else:
        print(f"Syntax error at token: {index if index < len(TS) else 'end of input'}")
        return False

if __name__ == "__main__":
    test_parser()

print("""
How the parser works:
1. For each non-terminal in your CFG, a function is generated (like F() above)
2. Each alternative production becomes an if/elif branch
3. Terminals are matched directly against the token stream (with index++)
4. Non-terminals are handled by calling their respective functions
5. The parsing succeeds if all the required tokens match and we reach the end of input

The parser_generator.py script automates the creation of these functions from your Excel file.
""")