from sheets import read_cb_database, persist_new_product, get_products_from_db_by_cbs
from products import return_found_and_missing_cb_products
from sheets import get_counted_products, generate_result_sheet
from ui import take_input_for_product, show_message, st

if __name__ == "__main__":


    st.header("Operação Natal - Campinas")
    st.write("By Lofi, Ygor e Mikio")

    # Handling first state of inital page
    if 'ste' not in st.session_state:
        st.session_state.ste = 0

    # Loads the databases
    if st.session_state.ste == 0:

        #counted_products = get_counted_products()
        st.session_state.counted_products = get_counted_products()

        products_from_db = read_cb_database()

        counted_products_found_in_db, missing_cb_products = return_found_and_missing_cb_products(st.session_state.counted_products, products_from_db)


        if(len(missing_cb_products) > 0):
            show_message("\nOs produtos cujos códigos de barras não foram encontrados no banco de dados serão mostrados abaixo. Por favor os cadastre.   \nOs produtos permanecerão cadastrados mesmo que você feche a aplicação no meio do processo.\n\n")

            st.session_state.missing_cb_products = missing_cb_products

            if st.button("Okay"):
                st.session_state.ste += 1
                st.rerun()
        else:
            st.session_state.ste = 0

    # There are products that need to be registered or checked
    elif st.session_state.ste == 1:

        st.session_state.missing_cbs = list({product.cb for product in st.session_state.missing_cb_products})

        for cb in st.session_state.missing_cbs:

            products_with_cb = [product for product in st.session_state.missing_cb_products if product.cb == cb]

            product_db = take_input_for_product(products_with_cb)

            if(product_db != None):
                persist_new_product(product_db)

        st.session_state.ste += 1

    elif st.session_state.ste == 2:
        
    # for product in counted_products_found_in_db:

    #     confirm_product(product)


        cb_name_list = get_products_from_db_by_cbs(list({product.cb for product in st.session_state.counted_products}))


        generate_result_sheet(st.session_state.counted_products, cb_name_list)

        st.session_state.ste = 0
