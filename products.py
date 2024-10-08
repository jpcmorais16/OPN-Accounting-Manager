import pandas as pd
from models import Product, Product_db
from ui import show_message
import streamlit as st


def binary_search(products_from_db: list[Product_db], product: Product) -> bool:
    lo, hi = 0, len(products_from_db) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if int(product.cb) == products_from_db[mid].cb:
            return True
        if int(product.cb) > products_from_db[mid].cb:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


def return_found_and_missing_cb_products(counted_products: list[Product], products_from_db: list[Product_db]) -> tuple[list[Product], list[Product]]:
    found, not_found = [], []
    
    for counted_product in counted_products:
        try:
            int(counted_product.cb)
        except:
            show_message(f"Há um código de barras errado que será desconsiderado.  \n")
            data = {"Código de Barras": counted_product.cb, "Nome do Produto": counted_product.name, "Supermercado": counted_product.supermarket, "Turno": counted_product.shift}
            st.table(data)
            continue

        if binary_search(products_from_db, counted_product):
            found.append(counted_product)
        else:
            not_found.append(counted_product)


    if len({product.cb for product in not_found}) > 0:
        show_message(f"\nDos {len({product.cb for product in counted_products})} códigos de barras contabilizados, {len({product.cb for product in not_found})} não estão no banco de dados.\n\n")
        if "msg_not_found" not in st.session_state:
            st.session_state["msg_not_found"] = f"\nDos {len({product.cb for product in counted_products})} códigos de barras contabilizados, {len({product.cb for product in not_found})} não estão no banco de dados.\n\n"

    
    else:
        show_message("Todos os cbs contabilizados estão no banco de dados!")

    return found, not_found

