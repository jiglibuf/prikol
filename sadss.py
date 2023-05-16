import io
import base64
import pandas as pd
import streamlit as st

 #для онлайн юза
def main():
    st.title("Преобразование данных из Excel файлов")
    
    # Загрузка первого Excel файла
    st.header("Шаг 1: Загрузка файла с ключами")
    uploaded_file1 = st.file_uploader("Выберите первый файл в формате Excel", type="xlsx")
    if uploaded_file1 is not None:
        df1 = pd.read_excel(uploaded_file1)
        st.success("Файл успешно загружен.")
        st.write(df1.head())

        # Выбор столбцов для первого файла
        key_col = st.selectbox("Выберите столбец с ключами", options=df1.columns)
        value_col = st.selectbox("Выберите столбец со значениями", options=df1.columns)

        # Загрузка второго Excel файла
        st.header("Шаг 2: Загрузка файла, где надо преобразовать значения")
        uploaded_file2 = st.file_uploader("Выберите второй файл в формате Excel", type="xlsx")
        if uploaded_file2 is not None:
            df2 = pd.read_excel(uploaded_file2)
            st.success("Файл успешно загружен.")
            st.write(df2.head())

            # Выбор столбца для преобразования
            values_col = st.selectbox("Выберите столбец для преобразования", options=df2.columns)
            # Ввод разделителя
            delimiter = repr(st.text_input("Введите разделитель значений в столбце для преобразования", "|",key='delimiter_input'))

            # Преобразование значений
            my_dict = dict(zip(df1[key_col], df1[value_col]))
            split_values = df2[values_col].astype(str).str.split(delimiter)
            transformed_values = split_values.apply(lambda x: delimiter.join(filter(lambda y: y != '', [my_dict.get(y, '') for y in x])))

            # Сохранение результата в новый файл
            st.header("Шаг 3: Сохранение результата")
            if st.button("Сохранить результат"):
                df2['New Column'] = transformed_values
                st.write(df2)
                st.write("Сохранение в файл...")
                output = io.BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df2.to_excel(writer, index=False)
                writer.close()
                processed_data = output.getvalue()
                b64 = base64.b64encode(processed_data).decode()
                href = f'<a href="data:application/vnd.ms-excel;base64,{b64}" download="new_file.xlsx"></a>'
                st.markdown(href, unsafe_allow_html=True)
                st.download_button(label="Скачать файл", data=base64.b64decode(b64), file_name="new_file.xlsx", mime="application/vnd.ms-excel")
                st.success("Файл успешно сохранен.")
                
            else:
                st.warning("Чтобы сохранить результат, нажмите соответствующую кнопку.")
    
if __name__ == '__main__':
    main()