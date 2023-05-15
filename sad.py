import pandas as pd
#Здесь реализован алгоритм замены значений из столбца разделенными символами "|" на значения из словаря, который был получен из excel.
# загрузить первый xlsx файл
df1 = pd.read_excel('куда.xlsx')
filename = 'Откуда.xlsx'
# загрузить второй xlsx файл
df2 = pd.read_excel(filename)
# выбрать столбец ключей и значений из первого xlsx файла
key_col = 'NOTE'
value_col = 'Название'

# создать словарь из столбцов выбранных выше
my_dict = dict(zip(df1[key_col], df1[value_col]))
# выбрать столбец со значениями для преобразования
values_col = 'Кадастровый номер земельного участка'
print(df2.iloc[242][values_col])


# разбить каждое значение в столбце по символу '|'
split_values = df2[values_col].astype(str).str.split('|')

# применить функцию map() для каждого элемента в split_values, чтобы преобразовать его с помощью словаря my_dict
transformed_values = split_values.apply(lambda x: '|'.join(filter(lambda y: y != '', [my_dict.get(y, '') for y in x])))


# сохранить преобразованные значения в новый столбец 'New Column'
df2['New Column'] = transformed_values
# сохранить DataFrame в новый xlsx файл
df2.to_excel(filename, index = False)
