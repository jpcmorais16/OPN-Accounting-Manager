from models import Product_db
from models import Product


 # keeping everything about input/output here so its easier to create a GUI later (there shouldn't be prints/inputs in many different places of the code)
def show_message(message):
    print(message)

def take_product_type():

    while(True):

        type_n = input("Qual é o tipo deste produto? Digite o número\n\n\
    1) Alimento medido por peso (Ex: g, kg)\n\
    2) Alimento medido por volume (Ex: L, mL)\n\
    3) Item de limpeza medido por peso (Ex: g, kg)\n\
    4) Item de limpeza medido por volume (Ex: L, mL)\n\
    5) Item de limpeza medido por outra coisa (Ex: un)\n\
    6) Nenhum dos anteriores\n\n")

        try:
            int(type_n)
        except:
            print("Digite um número de 1 a 6")
            continue

        
        if(int(type_n) < 1 or int(type_n) > 6):
            print("Digite um número de 1 a 6")
            continue

        type = ''

        match(int(type_n)):

            case 1: 
                type = 'Alimentos (peso)'
                break

            case 2: 
                type = 'Alimentos (volume)'
                break
            
            case 3:
                type = 'Limpeza (peso)'
                break

            case 4:
                type = 'Limpeza (volume)'
                break

            case 5:
                type = 'Limpeza (outros)'
                break
        
        break

    return type



def is_volume_product(type):

    return type == 'Alimentos (volume)' or type == 'Limpeza (volume)'

def is_weight_product(type):

    return  type == 'Alimentos (peso)' or type == 'Limpeza (peso)'


def take_unit(type):
    unit = ''

    while True :

        if is_weight_product(type):
            unit = input("\nInsira a unidade na qual é medida este produto:\n\
        1) kg\n\
        2) g\n\
        3) mg\n")
            

        if is_volume_product(type):
            unit = input("\nInsira a unidade na qual é medida este produto:\n\
        1) L\n\
        2) mL\n")
            
        try:
            int(unit)
        except:
            print("Digite um dos números ou apenas aperte enter")
            continue

        if is_weight_product(type) and (int(unit) < 1 or int(unit) > 3):
            print("Digite um dos números ou apenas aperte enter")
            continue

        if is_volume_product(type) and (int(unit) < 1 or int(unit) > 2):
            print("Digite um dos números ou apenas aperte enter")
            continue

        break
    return int(unit)

def take_measurement():
    while True:

        measurement = input("Insira a medida (quantos kg, L, g, mL, mg).\n")
        
        try:
            measurement = float(measurement)
        except:
            print("Digite um valor numérico")
            continue

        break

    return measurement


def take_input_for_product(products: list[Product]):

    while True:

        names = [product.name for product in products]

        product = Product_db(products[0].cb, products[0].name)

        if(len(names) > 1):

            print(f"\n O cb {products[0].cb} foi contabilizado com mais de um nome:")

            for name in names:
                
                print(name)
            
            actual_name = input("\nPor favor digite aqui o nome correto\n")

            product = Product_db(products[0].cb, actual_name)


        print(f"CB: {product.cb}, Item: {product.name}")

        cancel = input("\nSe por algum motivo não quiser cadastrar este item (cb errado por exemplo), digite 'n' e aperte enter. Apenas aperte enter se quiser prosseguir com o cadastro.\n")

        if cancel == 'N' or cancel == 'n':
            return None
        


        name = input("\nO nome está correto? Se sim, só aperte enter. Se não, digite o nome correto.\n")

        if name == '':
            name = product.name
            

        
        type = take_product_type()

        
        if type == 'Limpeza (outros)' or type == '':

            return Product_db(product.cb, name, type)
        

        skip = input("\nAgora vem a parte de inserir as informações sobre a medida deste produto. Se você não souber (talvez quem cadastrou o cb não tenha colocado o peso/volume), digite 'p' e aperte enter. Se tiver tudo certo, apenas aperte enter.\n")

        if skip == 'p' or skip == 'P':

            restart = input(f"\nTudo certo com o produto: cb: {product.cb}, item: {name}, tipo: {type}? Você pode recomeçar o cadastro dele digitando 'n' e apertando enter\n")

            if restart == 'n' or restart == 'N':
                continue

            return Product_db(product.cb, name, type)


        unit = take_unit(type)

        measurement = take_measurement()

        restart = input(f"\nTudo certo com o produto: cb: {product.cb}, item: {name}, tipo: {type}, valor da medida: {measurement}? Você pode recomeçar o cadastro dele digitando 'n' e apertando enter\n")

        if restart == 'n' or restart == 'N':
            continue


        if is_weight_product(type):
            if unit == 2:
                measurement = measurement/1000

            if unit == 3:
                measurement = measurement/1000000

        if is_volume_product(type):

            if unit == 2:
                measurement = measurement/1000


        return Product_db(product.cb, name, type, measurement)