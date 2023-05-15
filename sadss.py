import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Открытие диалогового окна для выбора файлов
root = tk.Tk()
root.withdraw()

from_file_path = filedialog.askopenfilename(title="Выберите файл Откуда")
to_file_path = filedialog.askopenfilename(title="Выберите файл Куда")

# Загрузка данных из файлов
from_df = pd.read_excel(from_file_path)
to_df = pd.read_excel(to_file_path)

# Выбор столбцов для обработки
from_col = input("Введите букву столбца с кадастровыми номерами в файле Откуда (например, Кадастровый номер): ")
to_col = input("Введите букву столбца, в который нужно записать результат в файле Куда (например, NOTE): ")
lookup_col = input("Введите букву столбца, в котором нужно искать значения в файле Куда (например, Название): ")
result_col = input("Введите букву столбца, в который нужно записать результат (например, D): ")

# Создание пустого словаря для хранения уникальных значений
match_values_dict = {}
print(to_df[lookup_col])
print(to_df[to_col])

# Цикл по каждой строке в столбце "Откуда"
for index, row in from_df.iterrows():
    # Получение значения из столбца "Откуда"
    from_value = row.loc[from_col]
    
    if pd.notna(from_value):
        # Преобразование значения в строку и разделение на отдельные значения по символу "|"
        split_values = str(from_value).split("|")
        # Цикл по каждому отдельному значению из столбца "Откуда"
        for value in split_values:
            # Поиск строк в файле Куда, которые содержат искомое значение в столбце lookup_col
            match_rows = to_df[to_df[lookup_col] == value]
            if len(match_rows) == 0:
                continue  # пропустить текущую итерацию, если строка не найдена
            # Берем первую строку, содержащую искомое значение, из найденных строк в файле Куда
            match = match_rows.iloc[0]
            match_value = match[to_col]
            if not pd.isna(match_value) and match_value not in match_values_dict:
                match_values_dict[match_value] = True
        # Записываем результат в столбец result_col
        from_df.at[index, result_col] = ", ".join(match_values_dict.keys())
        # Очищаем словарь для следующей итерации
        match_values_dict.clear()

# Сохраняем изменения в файле Куда
from_df.to_excel(to_file_path, index=False)
