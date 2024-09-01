import pandas as pd
import re



#print(pd.ExcelFile("Banco de dados.xlsx").sheet_names)

cb = pd.read_excel("Banco de dados.xlsx", sheet_name='CB')

alimentos_peso = pd.read_excel("Banco de dados.xlsx", sheet_name='Alimentos (peso)')

alimentos_volume = pd.read_excel("Banco de dados.xlsx", sheet_name='Alimentos (volume)')

limpeza_peso = pd.read_excel("Banco de dados.xlsx", sheet_name='Limpeza (peso)')

limpeza_volume = pd.read_excel("Banco de dados.xlsx", sheet_name='Limpeza (volume)')

limpeza_outros = pd.read_excel("Banco de dados.xlsx", sheet_name='Limpeza (outros)')

output = pd.DataFrame({'CB': [], 'Name': [], 'Tipo': []})



for _, row in cb.iterrows():

    tipo = ''

    if(alimentos_peso['Item'].str.contains(row['Item'], regex=False).any()):
        tipo = 'Alimentos (peso)'

    if(alimentos_volume['Item'].str.contains(row['Item'], regex=False).any()):
        tipo = 'Alimentos (volume)'

    if(limpeza_peso['Item'].str.contains(row['Item'], regex=False).any()):
        tipo = 'Limpeza (peso)'

    if(limpeza_volume['Item'].str.contains(row['Item'], regex=False).any()):
        tipo = 'Limpeza (volume)'

    if(limpeza_outros['Item'].str.contains(row['Item'], regex=False).any()):
        tipo = 'Limpeza (outros)'

    output.loc[len(output)] = [row['CB'], row['Item'], tipo]


with pd.ExcelWriter('output.xlsx') as writer:
    output.to_excel(writer, sheet_name='cbs', index=False)

#     por_peso.to_excel(writer, sheet_name='Peso', index=False)
#     por_volume.to_excel(writer, sheet_name='Volume', index=False)
#     outros.to_excel(writer, sheet_name='Outros', index=False)