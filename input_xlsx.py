import openpyxl

book = openpyxl.open('input.xlsx', read_only=True)
sheet = book.active

sheet_data = []

for row in range(2, sheet.max_row + 1):
    city: str = sheet[row][0].value
    bau_link: str = sheet[row][1].value
    leroy_link: str = sheet[row][2].value
    conv_factor: bool = sheet[row][3].value
    retail_price: bool = sheet[row][4].value
    tuple_row = (city, bau_link, leroy_link, conv_factor, retail_price) #кортеж значений листа
    sheet_data.append(tuple_row)

print(sheet_data)


