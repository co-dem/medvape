import openpyxl


book = openpyxl.open('list.xlsx')
sheet = book.active

def get_products(xl = sheet):
    tastes = []

    for i in range(1, 300):
        if xl.cell(row = i, column = 1).value != None:
            tastes.append(xl.cell(row = i, column = 1).value)
        else:
            break
    print(f'list updated\n{tastes}')
    
    return tastes

def update_database():
    global book, sheet

    book.close()

    book = openpyxl.open('list.xlsx')
    sheet = book.active

    return sheet
def check_product(name):
    global sheet

    if name in get_products(xl = sheet):
        return True

    else:
        return False