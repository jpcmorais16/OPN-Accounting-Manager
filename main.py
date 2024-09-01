from sheets import read_cb_database, persist_new_product, get_products_from_db_by_cbs
from products import return_found_and_missing_cb_products
from sheets import get_counted_products, generate_result_sheet
from ui import take_input_for_product, show_message

if __name__ == "__main__":

    counted_products = get_counted_products() 

    products_from_db = read_cb_database() 

    counted_products_found_in_db, missing_cb_products = return_found_and_missing_cb_products(counted_products, products_from_db) 


    if(len(missing_cb_products) > 0):
        show_message("\nOs produtos cujos códigos de barras não foram encontrados no banco de dados serão mostrados abaixo. Por favor os cadastre.Os produtos permanecerão cadastrados mesmo que você feche a aplicação no meio do processo.\n\n")

    missing_cbs = list({product.cb for product in missing_cb_products})

    for cb in missing_cbs:

        products_with_cb = [product for product in missing_cb_products if product.cb == cb]

        product_db = take_input_for_product(products_with_cb)

        if(product_db != None):
            persist_new_product(product_db)


        
    # for product in counted_products_found_in_db:

    #     confirm_product(product)


    cb_name_list = get_products_from_db_by_cbs(list({product.cb for product in counted_products}))


    generate_result_sheet(counted_products, cb_name_list)
