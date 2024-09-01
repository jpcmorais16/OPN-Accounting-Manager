import pandas as pd
import re
from models import Product, Product_db
from functools import reduce


def get_counted_products() -> list[Product]:
    excel_file = pd.ExcelFile("coleta_cb.xlsx")
    sheet_names = excel_file.sheet_names
    result = []

    for supermarket in sheet_names:
        df = pd.read_excel("coleta_cb.xlsx", sheet_name=supermarket, skiprows=1)
        shift = df.loc[0, 'Código de barras']  # the shift is the first row

        for _, row in df.iterrows():
            if (pd.notna(row['Código de barras']) and
                pd.isna(row['Item']) and
                pd.isna(row['Quantidade']) and
                pd.isna(row['Check']) and
                re.fullmatch(r"^(?:\d{8}|\d{12}|\d{13})$", str(row['Código de barras'])) is None):
                shift = str(row['Código de barras'])
                continue

            if pd.isna(row['Quantidade']):
                continue

            result.append(Product((row['Código de barras']), supermarket, row['Item'], int(row['Quantidade']), shift))
    return result


def read_cb_database() -> list[Product_db]:
    try:
        df = pd.read_excel("Banco de dados.xlsx", sheet_name='CB')
        df['CB'] = pd.to_numeric(df['CB'], errors='coerce')
        df = df.sort_values('CB')
        df = df[df['CB'].notna()]
        df = df[df['Item'].notna()]
        
        result = [Product_db(row['CB'], row['Item'], row['Tipo']) for _, row in df.iterrows()]
        return result
    
    except FileNotFoundError:
        print("O arquivo de banco de dados da aplicação não foi encontrado")
        exit()
    
    except Exception as e:
        print("Erro no banco de dados, chama um computeiro para analisar!")
        print("Erro: ", e)
        exit()


def persist_new_product(product: Product_db):
    cb = pd.read_excel("Banco de dados.xlsx", sheet_name='CB')
    cb.loc[len(cb)] = [product.cb, product.name, product.type]

    df = pd.DataFrame()

    if product.type != '':
        df = pd.read_excel("Banco de dados.xlsx", sheet_name=product.type)
        df.loc[len(df)] = [product.name, product.measurement]

    with pd.ExcelWriter('Banco de dados.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        cb.to_excel(writer, sheet_name='CB', index=False)
        if product.type != '':
            df.to_excel(writer, sheet_name=product.type, index=False)


def get_products_from_db_by_cbs(cbs: list[str]):
    try:
        df = pd.read_excel("Banco de dados.xlsx", sheet_name='CB')
        products = df[df['CB'].isin(cbs)]
        return [(row['CB'], row['Item'], row['Tipo']) for _, row in products.iterrows()]
    
    except FileNotFoundError:
        print("O arquivo de banco de dados da aplicação não foi encontrado")
        exit()
    
    except Exception as e:
        print("Erro no banco de dados, chama um computeiro para analisar!")
        print("Erro: ", e)
        exit()


def generate_result_sheet(counted_products: list[Product], cb_name_list: list[tuple[str, str, str]]):
    
    # cada produto contabilizado possui um turno e um supermercado
    # queremos padronizar os nomes baseado no que for encontrado no banco pelo cb

    # hash por cb! cb:(nome, product)

    
    # criar hash
    cb_hash = {}

    for cb, _, _ in cb_name_list:
        cb_hash[cb] = None


    for cb, name, type in cb_name_list:
        
        products_with_cb = [product for product in counted_products if product.cb == cb]

        cb_hash[cb] = (name, type, products_with_cb)

    

    # Página geral (todos os produtos)
    main_page = pd.DataFrame({'CB': [], 'Item': [], 'Tipo': [], 'Supermercado': [], 'Turno': [], 'Quantidade': []})

    for cb in cb_hash:

        name, type, products = cb_hash[cb]

        for product in products:
            main_page.loc[len(main_page)] = [cb, name, type, product.supermarket, product.shift, product.amount]

        main_page = main_page.sort_values('Tipo')
       

    # Páginas de tipo

    weight_food_page = pd.DataFrame({'Item': [], 'Supermercado': [], 'Quantidade': []})
    volume_food_page = pd.DataFrame({'Item': [], 'Supermercado': [], 'Quantidade': []})
    weight_cleaning_page = pd.DataFrame({'Item': [], 'Supermercado': [], 'Quantidade': []})
    volume_cleaning_page = pd.DataFrame({'Item': [], 'Supermercado': [], 'Quantidade': []})
    other_cleaning_page = pd.DataFrame({'Item': [], 'Supermercado': [], 'Quantidade': []})
    other_page = pd.DataFrame({'Item': [], 'Supermercado': [], 'Quantidade': []})

    for cb in cb_hash:

        name, type, products = cb_hash[cb]

        if(type == 'Alimentos (peso)'):
            for product in products:
                weight_food_page.loc[len(weight_food_page)] = [name, product.supermarket, product.amount]

        elif(type == 'Alimentos (volume)'):
            for product in products:
                volume_food_page.loc[len(volume_food_page)] = [name, product.supermarket, product.amount]

        elif(type == 'Limpeza (peso)'):
            for product in products:
                weight_cleaning_page.loc[len(weight_cleaning_page)] = [name, product.supermarket, product.amount]

        elif(type == 'Limpeza (volume)'):
            for product in products:
                volume_cleaning_page.loc[len(volume_cleaning_page)] = [name, product.supermarket, product.amount]

        elif(type == 'Limpeza (outros)'):
            for product in products:
                other_cleaning_page.loc[len(volume_cleaning_page)] = [name, product.supermarket, product.amount]

        else:
            for product in products:
                other_page.loc[len(other_page)] = [name, product.supermarket, product.amount]



    # Páginas por supermercado (ordenar por turno)

    supermarkets = list({product.supermarket for product in counted_products})
    
    supermarket_dfs = {}

    for supermarket in supermarkets:

        supermarket_dfs[supermarket] = pd.DataFrame({'Item':[], 'Turno': [], 'Quantidade': []})

        for cb in cb_hash:

            name, type, products = cb_hash[cb]

            for product in products:

                if product.supermarket == supermarket:

                    supermarket_dfs[supermarket].loc[len(supermarket_dfs[supermarket])] = [name, product.shift, product.amount]



    # Página de resultados

    #products_from_db = read_cb_database()

    total_amount = reduce(lambda x, p: x + p.amount, counted_products, 0)
    different_products = len(cb_hash)




    # Persistencia
    with pd.ExcelWriter('Resultado.xlsx') as writer:

        main_page.to_excel(writer, sheet_name='Resultado Geral', index=False)

        weight_food_page.to_excel(writer, sheet_name='Alimentos (peso)', index=False)
        volume_food_page.to_excel(writer, sheet_name='Alimentos (volume)', index=False)
        weight_cleaning_page.to_excel(writer, sheet_name='Limpeza (peso)', index=False)
        volume_cleaning_page.to_excel(writer, sheet_name='Limpeza (volume)', index=False)
        other_cleaning_page.to_excel(writer, sheet_name='Limpeza (outros)', index=False)
        other_page.to_excel(writer, sheet_name='Outros', index=False)

        for supermarket in supermarkets:

            df = supermarket_dfs[supermarket]

            df.to_excel(writer, sheet_name=supermarket, index=False)

        


    results = pd.DataFrame()
