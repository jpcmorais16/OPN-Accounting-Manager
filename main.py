from sheets import read_cb_database, persist_new_product, get_products_from_db_by_cbs
from products import return_found_and_missing_cb_products
from sheets import get_counted_products, generate_result_sheet
from ui import take_input_for_product, show_message
import streamlit as st


if __name__ == "__main__":

    st.title("Operação Natal CPS - OPN Hackers")
    st.write("By lofi, ygor and (no) mikio")

    # Prevents from reading the base every time a widget is updated
    # It makes it so by saving those variables into session memory, like a cache
    if "counted_products" not in st.session_state:
        st.session_state["counted_products"] = get_counted_products() 

    if "products_from_db" not in st.session_state:
        st.session_state["products_from_db"] = read_cb_database() 

    condition1 = "counted_products_found_in_db" not in st.session_state
    condition2 = "missing_cb_products" not in st.session_state

    if condition1 and condition2:
        st.session_state["counted_products_found_in_db"], st.session_state["missing_cb_products"] = return_found_and_missing_cb_products(st.session_state["counted_products"], st.session_state["products_from_db"]) 


    if(len(st.session_state["missing_cb_products"]) > 0):
        show_message("\nOs produtos cujos códigos de barras não foram encontrados no banco de dados serão mostrados abaixo.  \nPor favor, cadastre-os.  \nOs produtos permanecerão cadastrados mesmo que você feche a aplicação no meio do processo.\n\n")

    if "missing_cbs" not in st.session_state:
        st.session_state["missing_cbs"] = list({product.cb for product in st.session_state["missing_cb_products"]})

    # This will allows to do a loop with our missing cb products
    if "current_index_missing_cbs" not in st.session_state:
        st.session_state["current_index_missing_cbs"] = 0
    
    if st.session_state["current_index_missing_cbs"] < len(st.session_state["missing_cbs"]):
        cb = st.session_state["missing_cbs"][st.session_state["current_index_missing_cbs"]]
        st.write("Lembrando novamente: " + st.session_state["msg_not_found"])

        products_with_cb = [product for product in st.session_state["missing_cb_products"] if product.cb == cb]

        product_db = take_input_for_product(products_with_cb)

        
    else:
        cb_name_list = get_products_from_db_by_cbs(list({product.cb for product in st.session_state["counted_products"]}))
        st.write("Result sheet generated!")
        generate_result_sheet(st.session_state["counted_products"], cb_name_list)
