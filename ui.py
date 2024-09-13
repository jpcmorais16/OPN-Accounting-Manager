from models import Product_db
from models import Product
import streamlit as st
import pandas as pd
from sheets import persist_new_product

 # keeping everything about input/output here so its easier to create a GUI later (there shouldn't be prints/inputs in many different places of the code)
def show_message(message):
    st.write(message)

def take_product_type():
    options = ['Alimentos (peso)', 'Alimentos (volume)', 'Limpeza (peso)', 'Limpeza (volume)', 'Limpeza (outros)', 'Nenhuma das anteriores']
    
    number_type = {
        "Alimentos (peso)": 1,
        "Alimentos (volume)": 2,
        "Limpeza (peso)": 3,
        "Limpeza (volume)": 4,
        "Limpeza (outros)": 5,
    }

    type = st.selectbox("Selecione o tipo do produto", options, key='type_return')
    return type


def is_volume_product(type):

    return type == 'Alimentos (volume)' or type == 'Limpeza (volume)'

def is_weight_product(type):

    return  type == 'Alimentos (peso)' or type == 'Limpeza (peso)'


def take_unit():
    unit = st.selectbox("Selecione a unidade", ['kg', 'g', 'mg', 'L', 'mL'], key='unit_return')
    return unit

def take_measurement():
    measurement = st.number_input("Insira a medida (quantos kg, L, g, mL, mg).", min_value=0.0, step=0.1, key='measurement_return')
    return measurement

def persist_product():
    if st.session_state['confirm_return'] == 'Sim':
        product_db = Product_db(st.session_state['cb_return'], st.session_state['name_return'], st.session_state['type_return'], st.session_state['measurement_return'])
        if(product_db is not None):
            persist_new_product(product_db)
    
    st.session_state["current_index_missing_cbs"] += 1

def take_input_for_product(products: list[Product]):

    names = [product.name for product in products]
    product = Product_db(products[0].cb, products[0].name)

    if len(names) > 1:
        st.warning(f"O cb {products[0].cb} foi contabilizado com mais de um nome.")
        actual_name = st.text_input("Por favor, digite o nome correto:")
        product = Product_db(products[0].cb, actual_name)

    data = {'CB': product.cb, 'Nome do produto': product.name, "Type": product.type, "Measurement": product.measurement}
    data = pd.DataFrame(data, index=['Info'])
    st.write(f"CB: {product.cb}, Item: {product.name}, Type: {product.type}, Measurement: {product.measurement}")
    st.table(data)

    name_return = ''
    type_return = ''
    measurement_return = 0.0

    with st.form('product_form'):
        st.session_state['cb_return'] = product.cb

        name = st.text_input("Nome do produto:", key='name_return', value=product.name)
        type = take_product_type()

        name_return = name
        type_return = type

        if type == "Limpeza (outros)" or type == "":
            measurement_return = 0.0
 
        unit = take_unit()
        measurement = take_measurement()
        
        if is_weight_product(type):
            if unit == 'g':
                measurement = measurement / 1000
            elif unit == 'mg':
                measurement = measurement / 1000000

        if is_volume_product(type):
            if unit == 'mL':
                measurement = measurement / 1000

        measurement_return = measurement

        st.write("Se você marcar essa opção Não, todos os campos anteriores serão desconsiderados e o produto não será registrado no banco de dados.")
        st.radio(f"Deseja cadastrar o produto?", ("Sim", "Não"), key='confirm_return')

        submitted = st.form_submit_button("Concluir", on_click=persist_product)