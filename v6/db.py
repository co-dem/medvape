import openpyxl


book = openpyxl.open('list.xlsx')
sheet = book.active
stats = {}

def get_products(xl = sheet) -> list:
    tastes = []

    for i in range(1, 300):
        if xl.cell(row = i, column = 1).value != None:
            tastes.append(xl.cell(row = i, column = 1).value)
        else:
            break
    print(f'list updated\n{tastes}')
    
    return tastes

def update_database() -> any:
    global book, sheet

    book.close()

    book = openpyxl.open('list.xlsx')
    sheet = book.active

    return sheet

def check_product(name) -> bool:
    global sheet

    if name in get_products(xl = sheet):
        return True

    else:
        return False


def upload_products() -> dict:
    global stats

    for i in get_products():
        prod_exists = stats.get(i)
        if prod_exists == None:
            stats[i] = 0
    
    return stats

def changestats(product_name: str):
    global stats

    prod_check = stats.get(product_name)
    if prod_check >= 0:
        stats[product_name] += 1
        return stats
    else:
        return ValueError

def clear_stats() -> dict:
    global stats

    for i in stats:
        stats[i] = 0
    return stats

def showstats() -> dict:
    global stats
    return stats
#| coded by codem