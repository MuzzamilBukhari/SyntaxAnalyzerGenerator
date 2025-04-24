import pandas as pd

# Create a sample dataframe that matches your Excel structure
data = [
    ['<Program> → <Decl>*', '<Program>', '{DT, <Modifier>, interface, <SST>, ε}', '{$}'],
    ['<Decl> → <Var-Decl> <Decl-Prime>', '<Decl>', '{DT}', '{<Decl>, $}'],
    ['<Decl> → <Modifier> <Decl-Type> <Decl-Prime>', '<Decl>', '{Public, Private, ε}', '{<Decl>, $}'],
    ['<Decl> → interface ID { <Interface-Body> } <Decl-Prime>', '<Decl>', '{interface}', '{<Decl>, $}'],
    ['<Decl-Prime> → <Decl> <Decl-Prime>', '<Decl-Prime>', '{DT, <Modifier>, interface}', '{$}'],
    ['<Decl-Prime> → ε', '<Decl-Prime>', '{$}', '{$}'],
]

# Create DataFrame
df = pd.DataFrame(data, columns=['Production Rules', 'Non-terminal Symbol', 'Selection Set (FIRST)', 'Follow Set'])

# Save to Excel
df.to_excel('c:/Users/Hasan/Desktop/implementation cfg/cfg_grammar.xlsx', index=False)

print("Sample Excel file created at: c:/Users/Hasan/Desktop/implementation cfg/cfg_grammar.xlsx")
print("Run the parser generator with: python parser_generator.py cfg_grammar.xlsx generated_parser.py")