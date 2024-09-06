import streamlit as st
from models import Product_db, Product

def show_message(message):
    st.write(message)

def take_product_type():
    type_options = {
        "1) Alimento medido por peso (Ex: g, kg)": "Alimentos (peso)",
        "2) Alimento medido por volume (Ex: L, mL)": "Alimentos (volume)",
        "3) Item de limpeza medido por peso (Ex: g, kg)": "Limpeza (peso)",
        "4) Item de limpeza medido por volume (Ex: L, mL)": "Limpeza (volume)",
        "5) Item de limpeza medido por outra coisa (Ex: un)": "Limpeza (outros)"
    }

    type_n = st.selectbox(
        "Qual é o tipo deste produto? Escolha uma opção:",
        list(type_options.keys())
    )

    return type_options[type_n]

def is_volume_product(type):
    return type == 'Alimentos (volume)' or type == 'Limpeza (volume)'

def is_weight_product(type):
    return type == 'Alimentos (peso)' or type == 'Limpeza (peso)'

def take_unit(type):
    unit_options = {
        "Alimentos (peso)": ["kg", "g", "mg"],
        "Limpeza (peso)": ["kg", "g", "mg"],
        "Alimentos (volume)": ["L", "mL"],
        "Limpeza (volume)": ["L", "mL"]
    }

    unit = st.selectbox(
        "Insira a unidade na qual é medido este produto:",
        unit_options.get(type, [])
    )

    return unit

def take_measurement():
    measurement = st.number_input(
        "Insira a medida (quantos kg, L, g, mL, mg).",
        min_value=0.0, format="%.6f"
    )
    return measurement

def take_input_for_product(products: list[Product]):
    # Initialize session state variables
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'product' not in st.session_state:
        st.session_state.product = Product_db(products[0].cb, products[0].name)
    if 'name' not in st.session_state:
        st.session_state.name = ''
    if 'type' not in st.session_state:
        st.session_state.type = ''
    if 'unit' not in st.session_state:
        st.session_state.unit = ''
    if 'measurement' not in st.session_state:
        st.session_state.measurement = 0.0

    if st.session_state.step == 1:
        names = [product.name for product in products]
        st.session_state.product = Product_db(products[0].cb, products[0].name)

        if len(names) > 1:
            st.write(f"O cb {products[0].cb} foi contabilizado com mais de um nome:")
            actual_name = st.selectbox("Por favor escolha o nome correto", names)
            st.session_state.product = Product_db(products[0].cb, actual_name)

        st.write(f"CB: {st.session_state.product.cb}, Item: {st.session_state.product.name}")
        st.table({"Item: ": st.session_state.product.name, "Código de Barras: ": st.session_state.product.cb, })
        cancel = st.text_input(
            "Se por algum motivo não quiser cadastrar este item (cb errado por exemplo), digite 'n'.",
            placeholder="Digite 'n' para cancelar"
        )

        if cancel.lower() == 'n':
            return None

        name = st.text_input("O nome está correto? Se sim, deixe em branco.")
        st.session_state.name = name if name else st.session_state.product.name

        if st.button("Próximo"):
            st.session_state.step += 1
            st.rerun()

    elif st.session_state.step == 2:
        st.session_state.type = take_product_type()

        if st.button("Próximo"):
            st.session_state.step += 1

    elif st.session_state.step == 3:
        if st.session_state.type == 'Limpeza (outros)' or st.session_state.type == '':
            st.write("Produto registrado com sucesso!")
            st.stop()

        skip = st.text_input(
            "Se não souber a medida do produto, digite 'p'.",
            placeholder="Digite 'p' para pular"
        )

        if skip.lower() == 'p':
            st.write("Produto registrado com sucesso!")
            st.stop()

        if st.button("Próximo"):
            st.session_state.step += 1

    elif st.session_state.step == 4:
        st.session_state.unit = take_unit(st.session_state.type)

        if st.button("Próximo"):
            st.session_state.step += 1

    elif st.session_state.step == 5:
        st.session_state.measurement = take_measurement()

        confirm = st.text_input(
            f"Tudo certo com o produto: cb: {st.session_state.product.cb}, item: {st.session_state.name}, tipo: {st.session_state.type}, valor da medida: {st.session_state.measurement}? Se não, digite 'n'.",
            placeholder="Digite 'n' para recomeçar"
        )

        if confirm.lower() == 'n':
            st.session_state.step = 1

        if st.button("Registrar Produto"):
            if is_weight_product(st.session_state.type):
                if st.session_state.unit == "g":
                    st.session_state.measurement /= 1000
                elif st.session_state.unit == "mg":
                    st.session_state.measurement /= 1000000

            if is_volume_product(st.session_state.type) and st.session_state.unit == "mL":
                st.session_state.measurement /= 1000

            product = Product_db(
                st.session_state.product.cb,
                st.session_state.name,
                st.session_state.type,
                st.session_state.measurement
            )
            st.write("Produto registrado com sucesso!")
            #st.stop()
            return product
