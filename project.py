import sqlite3, sys, os
import tkinter as tk
from tkinter import ttk
import winreg
import customtkinter as ctk
from PIL import Image
import pandas as pd
from tkinter.messagebox import showerror, showinfo
import webbrowser

BOOK = ["ID Книги", "Инвентарный номер", "Название книги", "Год издания", "количество страниц", "цена","ID издетальство","ID место издания","ID автор","ID выдача","ID возврат","ID жанра",]
AUTHOR = ["ID Автора", "Имя", "Фамилия","Отчество"]
GENRE = ["ID Жанра","Название жанра"]
PUBLISH_HOUSE = ["ID Издательства","Название издетальство"]
PLACE_PUBLICATION = ["ID Место", "Город издания"]
STUDENT = ["ID Студента", "Имя", "Фамилия", "Отчество"]
EXTRADITION = ["ID Выдачи", "Дата выдачи", "ID Студента","Книга"]
REFUND = ["ID возврата","Дата возврата","ID Студента","Книга"]
SPIS = ["ID Книги", "Название книги", "Причина списания"]

ctk.set_default_color_theme("blue")
class AboutProgramWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("О программе")

        program_name_label = tk.Label(self, text="Программное средство «Студенческая библиотека»")
        program_version_label = tk.Label(self, text="Версия: beta 1.0.")
        developer_label = tk.Label(self, text="Разбработал: Базюк Максим Павлович ")
        purpose_label = tk.Label(self, text="Данное программное средство «Студенческая библиотека» разрабатывается с целью автоматизации информационной системы и улучшенной работы библиотеки")

        # Размещение компонентов на форме
        program_name_label.pack()
        program_version_label.pack()
        developer_label.pack()
        purpose_label.pack()

        # Кнопка Ок
        ok_button = tk.Button(self, text="Ок", command=self.destroy)
        ok_button.pack()

class WindowMain(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Студенческая библиотека')
        self.last_headers = None


        # Создание фрейма для отображения таблицы
        self.table_frame = ctk.CTkFrame(self, width=700, height=400)
        self.table_frame.grid(row=0, column=0, padx=5, pady=5)

        # Загрузка фона
        bg = ctk.CTkImage(Image.open("res\\images\\bg.png"), size=(700, 400))
        lbl = ctk.CTkLabel(self.table_frame, image=bg,)
        lbl.place(relwidth=1, relheight=1)

        # Создание меню
        self.menu_bar = tk.Menu(self, background='#555', foreground='white')

        # Меню "Файл"
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Выход", command=self.quit)
        self.menu_bar.add_cascade(label="Файл", menu=file_menu)


 # Меню "Справочники"
        references_menu = tk.Menu(self.menu_bar, tearoff=0)
        references_menu.add_command(label="Книги", command=lambda: self.show_table("SELECT * FROM book", BOOK))
        references_menu.add_command(label="Авторы", command=lambda: self.show_table("SELECT * FROM author", AUTHOR))
        references_menu.add_command(label="Жанр", command=lambda: self.show_table("SELECT * FROM genre", GENRE))
        references_menu.add_command(label="Издательство", command=lambda: self.show_table("SELECT * FROM publish_house", PUBLISH_HOUSE))
        references_menu.add_command(label="Место издательство", command=lambda: self.show_table("SELECT * FROM place_publication", PLACE_PUBLICATION))
        references_menu.add_command(label="Студент", command=lambda: self.show_table("SELECT * FROM student", STUDENT))
        self.menu_bar.add_cascade(label="Справочники", menu=references_menu)

        # Меню "Таблицы"
        tables_menu = tk.Menu(self.menu_bar, tearoff=0)
        tables_menu.add_command(label="Выдача", command=lambda: self.show_table("SELECT * FROM extradition", EXTRADITION))
        tables_menu.add_command(label="Возврат", command=lambda: self.show_table("SELECT * FROM refund", REFUND))
        tables_menu.add_command(label="Списания книг", command=lambda: self.show_table("SELECT * FROM spis", SPIS))
        self.menu_bar.add_cascade(label="Таблицы", menu=tables_menu)

        # Меню "Отчёты"
        reports_menu = tk.Menu(self.menu_bar, tearoff=0)
        reports_menu.add_command(label="Создать Отчёт", command=self.to_xlsx)
        self.menu_bar.add_cascade(label="Отчёты", menu=reports_menu)

        # Меню "Сервис"
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Руководство пользователя", command=self.open_my_website)
        help_menu.add_command(label="O программе", command=self.open_about_window)
        self.menu_bar.add_cascade(label="Сервис", menu=help_menu)

        
 # Настройка цветов меню
        file_menu.configure(bg='#555', fg='white')
        references_menu.configure(bg='#555', fg='white')
        tables_menu.configure(bg='#555', fg='white')
        reports_menu.configure(bg='#555', fg='white')
        help_menu.configure(bg='#555', fg='white')

        # Установка меню в главное окно
        self.config(menu=self.menu_bar)

        btn_width = 150
        pad = 5

        # Создание кнопок и виджетов для поиска и редактирования данных
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "image\\image icon")
        self.deletes = ctk.CTkImage(Image.open(os.path.join(image_path, "delete.png")),size=(30, 30))
        self.change_add = ctk.CTkImage(Image.open(os.path.join(image_path, "2.png")), size=(20, 20))
        self.searchs = ctk.CTkImage(Image.open(os.path.join(image_path, "3.png")), size=(20, 20))
        self.cancellation = ctk.CTkImage(Image.open(os.path.join(image_path, "4.png")), size=(20, 20))
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "5.png")) ,size=(26, 26))
        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=15)
        self.navigation_frame.grid(row=0, column=1, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # редактирование
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="Редактирование", image=self.logo_image, compound="right", font=ctk.CTkFont(size=18, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # создание тем
        self.appearance_mode_label = ctk.CTkLabel(self.navigation_frame, text="Тема", anchor="w", font=ctk.CTkFont(size=13, weight="bold"))
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        #тема у умолчанию
        self.appearance_mode_optionemenu.set("System")

        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=0, column=1)
        ctk.CTkButton(btn_frame, text="Добавить", font=ctk.CTkFont(size=15), image=self.change_add, compound="right", width=btn_width, command=self.add).pack(pady=pad)
        ctk.CTkButton(btn_frame, text="Удалить", font=ctk.CTkFont(size=15), image=self.deletes, compound="right", width=btn_width, command=self.delete).pack(pady=pad)
        ctk.CTkButton(btn_frame, text="Изменить", font=ctk.CTkFont(size=15), image=self.change_add, compound="right", width=btn_width, command=self.change).pack(pady=pad)

        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=1, column=0, pady=pad)
        self.search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Поиск строк")
        self.search_entry.grid(row=0, column=0, padx=pad)
        ctk.CTkButton(search_frame, text="Поиск", image=self.searchs, compound="right", width=50, font=ctk.CTkFont(size=13), command=self.search).grid(row=0, column=1, padx=pad)
        ctk.CTkButton(search_frame, text="Искать далее", width=50, font=ctk.CTkFont(size=13), command=self.search_next).grid(row=0, column=2, padx=pad)
        ctk.CTkButton(search_frame, text="Сброс", image=self.cancellation, compound="right", width=50, font=ctk.CTkFont(size=13), command=self.reset_search).grid(row=0, column=3, padx=pad)
    def open_my_website(self):
        url = "M:\TRPO\project\HTML\main.html"  # Замените на адрес вашего сайта
        webbrowser.open(url)

    def open_about_window(self):
        about_window = AboutProgramWindow(self)
        about_window.geometry("850x200")  # Установите размер окна по вашему усмотрению
        about_window.focus_set()
        about_window.grab_set()
        self.wait_window(about_window)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def search_in_table(self, table, search_terms, start_item=None):
        table.selection_remove(table.selection())  # Сброс предыдущего выделения

        items = table.get_children('')
        start_index = items.index(start_item) + 1 if start_item else 0

        for item in items[start_index:]:
            values = table.item(item, 'values')
            for term in search_terms:
                if any(term.lower() in str(value).lower() for value in values):
                    table.selection_add(item)
                    table.focus(item)
                    table.see(item)
                    return item  # Возвращаем найденный элемент



    def reset_search(self):
        if self.last_headers:
            self.table.selection_remove(self.table.selection())
        self.search_entry.delete(0, 'end')

    def search(self):
        if self.last_headers:
            self.current_item = self.search_in_table(self.table, self.search_entry.get().split(','))

    def search_next(self):
        if self.last_headers:
            if self.current_item:
                self.current_item = self.search_in_table(self.table, self.search_entry.get().split(','), start_item=self.current_item)
    
    
    def to_xlsx(self):
        if self.last_headers == BOOK:
            sql_query = "SELECT * FROM book"
            table_name = "book"
        elif self.last_headers == AUTHOR:
            sql_query = "SELECT * FROM author"
            table_name = "author"
        elif self.last_headers == GENRE:
            sql_query = "SELECT * FROM genre"
            table_name = "genre"
        elif self.last_headers == PUBLISH_HOUSE:
            sql_query = "SELECT * FROM publish_house"
            table_name = "publish_house"
        elif self.last_headers == PLACE_PUBLICATION:
            sql_query = "SELECT * FROM place_publication"
            table_name = "publication"
        elif self.last_headers == STUDENT:
            sql_query = "SELECT * FROM student"
            table_name = "student"
        elif self.last_headers == EXTRADITION:
            sql_query = "SELECT * FROM extradition"
            table_name = "extradition"
        elif self.last_headers == REFUND:
            sql_query = "SELECT * FROM refund"
            table_name = "refund"
        elif self.last_headers == SPIS:
            sql_query = "SELECT * FROM spis"
            table_name = "spis"
        else: return

        dir = sys.path[0] + "\\export"
        os.makedirs(dir, exist_ok=True)
        path = dir + f"\\{table_name}.xlsx"

        # Подключение к базе данных SQLite
        conn = sqlite3.connect("res\\students_bd.db")
        cursor = conn.cursor()
        # Получите данные из базы данных
        cursor.execute(sql_query)
        data = cursor.fetchall()
        # Создайте DataFrame из данных
        df = pd.DataFrame(data, columns=self.last_headers)
        # Создайте объект writer для записи данных в Excel
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        # Запишите DataFrame в файл Excel
        df.to_excel(writer, 'Лист 1', index=False)
        # Сохраните результат
        writer.close()

        showinfo(title="Успешно", message=f"Данные экспортированы в {path}")

    def show_table(self, sql_query, headers = None):# Очистка фрейма перед отображением новых данных
        for widget in self.table_frame.winfo_children(): widget.destroy()

        # Подключение к базе данных SQLite
        conn = sqlite3.connect("res\\students_bd.db")
        cursor = conn.cursor()

        # Выполнение SQL-запроса
        cursor.execute(sql_query)
        self.last_sql_query = sql_query

        # Получение заголовков таблицы и данных
        if headers == None: # если заголовки не были переданы используем те что в БД
            table_headers = [description[0] for description in cursor.description]
        else: # иначе используем те что передали
            table_headers = headers
            self.last_headers = headers
        table_data = cursor.fetchall()

        # Закрытие соединения с базой данных
        conn.close()
            
        canvas = ctk.CTkCanvas(self.table_frame, width=865, height=480)
        canvas.pack(fill="both", expand=True)

        x_scrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal", command=canvas.xview)
        x_scrollbar.pack(side="bottom", fill="x")

        canvas.configure(xscrollcommand=x_scrollbar.set)

        self.table = ttk.Treeview(self.table_frame, columns=table_headers, show="headings", height=23)
        for header in table_headers: 
            self.table.heading(header, text=header)
            self.table.column(header, width=len(header) * 10 + 100) # установка ширины столбца исходя длины его заголовка
            if header == "№":
                self.table.column(header, width=0)
        for row in table_data: self.table.insert("", "end", values=row)

        canvas.create_window((0, 0), window=self.table, anchor="nw")

        self.table.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


    def update_table(self):
        self.show_table(self.last_sql_query, self.last_headers)

    def add(self):
        if self.last_headers == BOOK:
            WindowBook("add")
        elif self.last_headers == AUTHOR:
            WindowAuthor("add")
        elif self.last_headers == GENRE:
            WindowGenre("add")
        elif self.last_headers == PUBLISH_HOUSE:
            WindowPubHouse("add")
        elif self.last_headers == PLACE_PUBLICATION:
            WindowPlacePub("add")
        elif self.last_headers == STUDENT:
            WindowStudent("add")
        elif self.last_headers == EXTRADITION:
            WindowExtradition("add")
        elif self.last_headers == REFUND:
            WindowRefund("add")
        elif self.last_headers == SPIS:
            WindowSpis("add")

        else: return

    def delete(self):
        if self.last_headers:
            select_item = self.table.selection()
            if select_item:
                item_data = self.table.item(select_item[0])["values"]
            else:
                showerror(title="Ошибка", message="He выбранна запись")
                return
        else:
            return

        if self.last_headers == BOOK:
            WindowBook("delete", item_data)
        elif self.last_headers == AUTHOR:
            WindowAuthor("delete", item_data)
        elif self.last_headers == GENRE:
            WindowGenre("delete", item_data)
        elif self.last_headers == PUBLISH_HOUSE:
            WindowPubHouse("delete", item_data)
        elif self.last_headers == PLACE_PUBLICATION:
            WindowPlacePub("delete", item_data)
        elif self.last_headers == STUDENT:
            WindowStudent("delete", item_data)
        elif self.last_headers == EXTRADITION:
            WindowExtradition("delete", item_data)
        elif self.last_headers == REFUND:
            WindowRefund("delete", item_data)
        elif self.last_headers == SPIS:
            WindowSpis("delete", item_data)
        else: return
        
    def change(self):
        if self.last_headers:
            select_item = self.table.selection()
            if select_item:
                item_data = self.table.item(select_item[0])["values"]
            else:
                showerror(title="Ошибка", message="He выбранна запись")
                return
        else:
            return

        if self.last_headers == BOOK:
            WindowBook("change", item_data)
        elif self.last_headers == AUTHOR:
            WindowAuthor("change", item_data)
        elif self.last_headers == GENRE:
            WindowGenre("change", item_data)
        elif self.last_headers == PUBLISH_HOUSE:
            WindowPubHouse("change", item_data)
        elif self.last_headers == PLACE_PUBLICATION:
            WindowPlacePub  ("change", item_data)
        elif self.last_headers == STUDENT:
            WindowStudent("change", item_data)
        elif self.last_headers == EXTRADITION:
            WindowExtradition("change", item_data)
        elif self.last_headers == REFUND:
            WindowRefund("change", item_data)
        elif self.last_headers == SPIS:
            WindowSpis("change", item_data)
        else: return

class WindowBook(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="Инвентарный номер").grid(row=1, column=0)
            self.inv_number = tk.Entry(self, width=20)
            self.inv_number.grid(row=1, column=1)

            tk.Label(self, text="Название книги").grid(row=2, column=0)
            self.name_book = tk.Entry(self, width=20)
            self.name_book.grid(row=2, column=1)

            tk.Label(self, text="Год издания").grid(row=3, column=0)
            self.year_publish = tk.Entry(self, width=20)
            self.year_publish.grid(row=3, column=1)

            tk.Label(self, text="Количество страниц").grid(row=4, column=0)
            self.count_strok = tk.Entry(self, width=20)
            self.count_strok.grid(row=4, column=1)

            tk.Label(self, text="Цена").grid(row=5, column=0)
            self.price = tk.Entry(self, width=20)
            self.price.grid(row=5, column=1)

            tk.Label(self, text="ID Издательство").grid(row=6, column=0)
            self.id_publish = tk.Entry(self, width=20)
            self.id_publish.grid(row=6, column=1)
            
            tk.Label(self, text="ID Место издания").grid(row=7, column=0)
            self.id_pub_house = tk.Entry(self, width=20)
            self.id_pub_house.grid(row=7, column=1)

            tk.Label(self, text="ID Автора").grid(row=8, column=0)
            self.id_author = tk.Entry(self, width=20)
            self.id_author.grid(row=8, column=1)

            tk.Label(self, text="ID Выдачи").grid(row=9, column=0)
            self.id_ext = tk.Entry(self, width=20)
            self.id_ext.grid(row=9, column=1)

            tk.Label(self, text="ID Возврата").grid(row=10, column=0)
            self.id_ref = tk.Entry(self, width=20)
            self.id_ref.grid(row=10, column=1)

            tk.Label(self, text="ID Жанр").grid(row=11, column=0)
            self.id_genres = tk.Entry(self, width=20)
            self.id_genres.grid(row=11, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=12, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=12, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Книги'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[1]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текушее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="Инвентарный номер").grid(row=1, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=1, column=1)
            self.inv_number = tk.Entry(self, width=20)
            self.inv_number.grid(row=1, column=2)

            tk.Label(self, text="Название Книги").grid(row=2, column=0)
            tk.Label(self, text=self.select_row[2]).grid(row=2, column=1)
            self.name_book = tk.Entry(self, width=20)
            self.name_book.grid(row=2, column=2)

            tk.Label(self, text="Год издания").grid(row=3, column=0)
            tk.Label(self, text=self.select_row[3]).grid(row=3, column=1)
            self.year_publish = tk.Entry(self, width=20)
            self.year_publish.grid(row=3, column=2)

            tk.Label(self, text="Количество страниц").grid(row=4, column=0)
            tk.Label(self, text=self.select_row[4]).grid(row=4, column=1)
            self.count_strok = tk.Entry(self, width=20)
            self.count_strok.grid(row=4, column=2)

            tk.Label(self, text="Цена").grid(row=5, column=0)
            tk.Label(self, text=self.select_row[5]).grid(row=5, column=1)
            self.price = tk.Entry(self, width=20)
            self.price.grid(row=5, column=2)

            tk.Label(self, text="ID Издательство").grid(row=6, column=0)
            tk.Label(self, text=self.select_row[6]).grid(row=6, column=1)
            self.id_publish = tk.Entry(self, width=20)
            self.id_publish.grid(row=6, column=2)

            tk.Label(self, text="ID Место издания").grid(row=7, column=0)
            tk.Label(self, text=self.select_row[7]).grid(row=7, column=1)
            self.id_pub_house = tk.Entry(self, width=20)
            self.id_pub_house.grid(row=7, column=2)

            tk.Label(self, text="ID Автора").grid(row=8, column=0)
            tk.Label(self, text=self.select_row[8]).grid(row=8, column=1)
            self.id_author = tk.Entry(self, width=20)
            self.id_author.grid(row=8, column=2)

            tk.Label(self, text="ID Выдачи").grid(row=9, column=0)
            tk.Label(self, text=self.select_row[9]).grid(row=9, column=1)
            self.id_ext = tk.Entry(self, width=20)
            self.id_ext.grid(row=9, column=2)

            tk.Label(self, text="ID Возврата").grid(row=9, column=0)
            tk.Label(self, text=self.select_row[10]).grid(row=9, column=1)
            self.id_ref = tk.Entry(self, width=20)
            self.id_ref.grid(row=10, column=2)

            tk.Label(self, text="ID Жанр").grid(row=10, column=0)
            tk.Label(self, text=self.select_row[11]).grid(row=10, column=1)
            self.id_genres = tk.Entry(self, width=20)
            self.id_genres.grid(row=10, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=11, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=11, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        inv_number = self.inv_number.get()
        name_book = self.name_book.get()
        year_publish = self.year_publish.get()
        count_strok = self.count_strok.get()
        price = self.price.get()
        id_publish = self.id_publish.get()
        id_pub_house = self.id_pub_house.get()
        id_author = self.id_author.get()
        id_ext = self.id_ext.get()
        id_ref = self.id_ref.get()
        id_genres = self.id_genres.get()
        if inv_number and name_book and year_publish and count_strok and price and id_publish and id_pub_house and id_author and id_ext and id_ref and id_genres:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO book (invenatrni_nomer, name_book, god_izdaniya, kolvo_stranic, price, id_izdatelstvo, id_mesto_izdaniya, id_author, id_vidacha, id_vozvrat, id_ganre) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (inv_number, name_book, year_publish, count_strok, price, id_publish, id_pub_house, id_author, id_ext, id_ref, id_genres))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM book WHERE id_book = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) 

    def change(self):
        inv_number = self.inv_number.get() or self.select_row[1]
        name_book = self.name_book.get() or self.select_row[2]
        year_publish = self.year_publish.get() or self.select_row[3]
        count_strok = self.count_strok.get() or self.select_row[4]
        price = self.price.get() or self.select_row[5]
        id_publish = self.id_publish.get() or self.select_row[6]
        id_pub_house = self.id_pub_house.get() or self.select_row[7]
        id_author = self.id_author.get() or self.select_row[8]
        id_ext = self.id_ext.get() or self.select_row[9]
        id_ref = self.id_ref.get() or self.select_row[10] 
        id_genres = self.id_genres.get() or self.select_row[11]
        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                           UPDATE book SET (invenatrni_nomer, name_book, god_izdaniya, kolvo_stranic, price, id_izdatelstvo, id_mesto_izdaniya, id_author, id_vidacha, id_vozvrat, id_ganre) = (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
                           WHERE id_book = {self.select_row[0]}''', (inv_number, name_book, year_publish, count_strok, price, id_publish, id_pub_house, id_author, id_ext, id_ref, id_genres))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

class WindowAuthor(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="Имя").grid(row=1, column=0)
            self.name_aut = tk.Entry(self, width=20)
            self.name_aut.grid(row=1, column=1)

            tk.Label(self, text="Фамилия").grid(row=2, column=0)
            self.surname = tk.Entry(self, width=20)
            self.surname.grid(row=2, column=1)

            tk.Label(self, text="Отчество").grid(row=3, column=0)
            self.otc = tk.Entry(self, width=20)
            self.otc.grid(row=3, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=4, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=4, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Автор'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[1]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текущее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="Имя").grid(row=1, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=1, column=1)
            self.name_aut = tk.Entry(self, width=20)
            self.name_aut.grid(row=1, column=2)

            tk.Label(self, text="Фамилия").grid(row=2, column=0)
            tk.Label(self, text=self.select_row[2]).grid(row=2, column=1)
            self.surname = tk.Entry(self, width=20)
            self.surname.grid(row=2, column=2)

            tk.Label(self, text="Отчество").grid(row=3, column=0)
            tk.Label(self, text=self.select_row[3]).grid(row=3, column=1)
            self.otc = tk.Entry(self, width=20)
            self.otc.grid(row=3, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=4, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=4, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        name_aut = self.name_aut.get()
        surname = self.surname.get()
        otc = self.otc.get()
        if name_aut and surname and otc:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO author (name, familiya, otchestvo) VALUES (?, ?, ?)",
                            (name_aut, surname, otc))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM author WHERE id_author = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) #or self.select_row[1]

    def change(self):
        name_aut = self.name_aut.get() or self.select_row[1]
        surname = self.surname.get() or self.select_row[2]
        otc = self.otc.get() or self.select_row[3]
        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                           UPDATE author SET name = ?, familiya = ?, otchestvo = ? 
                           WHERE id_author = {self.select_row[0]}''', (name_aut, surname, otc))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

class WindowGenre(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="Название жанра").grid(row=1, column=0)
            self.n_genre = tk.Entry(self, width=20)
            self.n_genre.grid(row=1, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=2, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=2, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Жанр'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[0]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текушее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="Название Жанра").grid(row=2, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=2, column=1)
            self.n_genre = tk.Entry(self, width=20)
            self.n_genre.grid(row=2, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=3, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=3, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        n_genre = self.n_genre.get()
        if n_genre:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO genre (name_genre) VALUES (?)",
                            (n_genre,))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM genre WHERE id_genre = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) #or self.select_row[1]

    def change(self):
        n_genre = self.n_genre.get() or self.select_row[1]

        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                        UPDATE genre SET name_genre = ? 
                        WHERE id_genre = {self.select_row[0]}''', (n_genre,))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

class WindowPubHouse(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="Название издательство").grid(row=1, column=0)
            self.n_pub = tk.Entry(self, width=20)
            self.n_pub.grid(row=1, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=4, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=4, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Издательство'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[0]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текушее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="Название издательство").grid(row=2, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=2, column=1)
            self.n_pub = tk.Entry(self, width=20)
            self.n_pub.grid(row=2, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=3, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=3, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        n_pub = self.n_pub.get()
        if n_pub:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO publish_house (name_publish) VALUES (?)",
                            (n_pub,))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM publish_house WHERE id_publish = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) #or self.select_row[1]

    def change(self):
        n_pub = self.n_pub.get() or self.select_row[1]

        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                        UPDATE publish_house SET name_publish = ? 
                        WHERE id_publish = {self.select_row[0]}''', (n_pub,))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

class WindowPlacePub(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="Город издания").grid(row=1, column=0)
            self.pl_pub = tk.Entry(self, width=20)
            self.pl_pub.grid(row=1, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=2, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=2, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Место издания'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[0]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текушее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="Город издания").grid(row=2, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=2, column=1)
            self.pl_pub = tk.Entry(self, width=20)
            self.pl_pub.grid(row=2, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=3, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=3, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        pl_pub = self.pl_pub.get()
        if pl_pub:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO place_publication (name_place) VALUES (?)",
                            (pl_pub,))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM place_publication WHERE id_place = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) #or self.select_row[1]

    def change(self):
        pl_pub = self.pl_pub.get() or self.select_row[2]

        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                            UPDATE place_publication SET name_place = ? 
                            WHERE id_place = {self.select_row[0]}''', (pl_pub,))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

class WindowStudent(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="Имя").grid(row=1, column=0)
            self.name_stud = tk.Entry(self, width=20)
            self.name_stud.grid(row=1, column=1)

            tk.Label(self, text="Фамилия").grid(row=2, column=0)
            self.surname_stud = tk.Entry(self, width=20)
            self.surname_stud.grid(row=2, column=1)

            tk.Label(self, text="Группа").grid(row=3, column=0)
            self.group_stud = tk.Entry(self, width=20)
            self.group_stud.grid(row=3, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=4, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=4, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Студент'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[1]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текушее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="Имя").grid(row=2, column=0)
            tk.Label(self, text=self.select_row[0]).grid(row=2, column=1)
            self.name_stud = tk.Entry(self, width=20)
            self.name_stud.grid(row=2, column=2)

            tk.Label(self, text="Фамилия").grid(row=3, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=3, column=1)
            self.surname_stud = tk.Entry(self, width=20)
            self.surname_stud.grid(row=3, column=2)

            tk.Label(self, text="Группа").grid(row=4, column=0)
            tk.Label(self, text=self.select_row[2]).grid(row=4, column=1)
            self.group_stud = tk.Entry(self, width=20)
            self.group_stud.grid(row=4, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=5, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=5, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        name_stud = self.name_stud.get()
        surname_stud = self.surname_stud.get()
        group_stud = self.group_stud.get()
        if name_stud and surname_stud and group_stud:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO student (name, surname, patronymic) VALUES (?, ?, ?)",
                            (name_stud, surname_stud, group_stud))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM student WHERE id_student = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) #or self.select_row[1]

    def change(self):
        name_stud = self.name_stud.get() or self.select_row[1]
        surname_stud = self.surname_stud.get() or self.select_row[2]
        group_stud = self.group_stud.get() or self.select_row[3]

        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                           UPDATE student SET (name, surname, patronymic) VALUES (?, ?, ?) 
                           WHERE id_student = {self.select_row[0]}''', (name_stud, surname_stud, group_stud))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

class WindowExtradition(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="Дата выдачи").grid(row=1, column=0)
            self.date_ext = tk.Entry(self, width=20)
            self.date_ext.grid(row=1, column=1)

            tk.Label(self, text="ID Студента").grid(row=2, column=0)
            self.id_stud = tk.Entry(self, width=20)
            self.id_stud.grid(row=2, column=1)

            tk.Label(self, text="Книга").grid(row=3, column=0)
            self.book = tk.Entry(self, width=20)
            self.book.grid(row=3, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=4, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=4, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Выдача'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[1]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текушее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="Дата выдачи").grid(row=2, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=2, column=1)
            self.date_ext = tk.Entry(self, width=20)
            self.date_ext.grid(row=2, column=2)

            tk.Label(self, text="ID Студент").grid(row=3, column=0)
            tk.Label(self, text=self.select_row[2]).grid(row=3, column=1)
            self.id_stud = tk.Entry(self, width=20)
            self.id_stud.grid(row=3, column=2)

            tk.Label(self, text="Книга").grid(row=4,column=0)
            tk.Label(self, text=self.select_row[3]).grid(row=4, column=1)
            self.book = tk.Entry(self, width=20)
            self.book.grid(row=4, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=5, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=5, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        book = self.book.get()
        id_stud = self.id_stud.get()
        date_ext = self.date_ext.get()
        if id_stud and date_ext and book:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO extradition (date, id_student, book) VALUES (?, ?, ?)",
                            (id_stud, date_ext,book))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM extradition WHERE id_extradition = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) #or self.select_row[1]

    def change(self):
        id_stud = self.id_stud.get() or self.select_row[1]
        date_ext = self.date_ext.get() or self.select_row[2]
        book = self.book.get() or self.select_row[3]


        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                           UPDATE extradition SET (date, id_student) VALUES (?, ?, ?) 
                           WHERE id_extradition = {self.select_row[0]}''', (id_stud, date_ext, book))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

class WindowRefund(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="Дата возврата").grid(row=1, column=0)
            self.date_ref = tk.Entry(self, width=20)
            self.date_ref.grid(row=1, column=1)

            tk.Label(self, text="ID Студента").grid(row=2, column=0)
            self.id_studnt = tk.Entry(self, width=20)
            self.id_studnt.grid(row=2, column=1)

            tk.Label(self, text="Книга").grid(row=3, column=0)
            self.bookl = tk.Entry(self, width=20)
            self.bookl.grid(row=3, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=4, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=4, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Возврат'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[1]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текушее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="Дата возврата").grid(row=2, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=2, column=1)
            self.date_ref = tk.Entry(self, width=20)
            self.date_ref.grid(row=2, column=2)

            tk.Label(self, text="ID Студента").grid(row=3, column=0)
            tk.Label(self, text=self.select_row[2]).grid(row=3, column=1)
            self.id_stud = tk.Entry(self, width=20)
            self.id_stud.grid(row=3, column=2)

            tk.Label(self, text="Книга").grid(row=4,column=0)
            tk.Label(self, text=self.select_row[3]).grid(row=4, column=1)
            self.book = tk.Entry(self, width=20)
            self.book.grid(row=4, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=5, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=5, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        date_ref = self.date_ref.get()
        id_studnt = self.id_studnt.get()
        bookl = self.bookl.get()
        if date_ref and id_studnt and bookl:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO refund (date, id_student,book) VALUES (?, ?, ?)",
                            (date_ref,id_studnt, bookl))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM refund WHERE id_refund = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) #or self.select_row[1]

    def change(self):
        date_ref = self.date_ref.get() or self.select_row[1]
        id_studnt = self.id_studnt.get() or self.select_row[2]
        bookl = self.bookl.get() or self.select_row[3]


        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                            UPDATE refund SET date = ?, id_student = ?, book = ? 
                            WHERE id_refund = {self.select_row[0]}''', (date_ref, id_studnt, bookl))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

class WindowSpis(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="Название книги").grid(row=1, column=0)
            self.nam_b = tk.Entry(self, width=20)
            self.nam_b.grid(row=1, column=1)

            tk.Label(self, text="Причина списания").grid(row=2, column=0)
            self.spis = tk.Entry(self, width=20)
            self.spis.grid(row=2, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=4, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=4, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Возврат'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[1]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текушее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="Название книги").grid(row=2, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=2, column=1)
            self.nam_b = tk.Entry(self, width=20)
            self.nam_b.grid(row=2, column=2)

            tk.Label(self, text="Причина списания").grid(row=3, column=0)
            tk.Label(self, text=self.select_row[2]).grid(row=3, column=1)
            self.spis = tk.Entry(self, width=20)
            self.spis.grid(row=3, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=5, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=5, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        nam_b = self.nam_b.get()
        spis = self.spis.get()
        if nam_b and spis:
            try:
                conn = sqlite3.connect("res\\students_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO spis (name_book, prich_spis) VALUES (?, ?)",
                            (nam_b,spis))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM spis WHERE id_wrofbook = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) #or self.select_row[1]

    def change(self):
        nam_b = self.nam_b.get() or self.select_row[1]
        spis = self.spis.get() or self.select_row[2]

        try:
            conn = sqlite3.connect("res\\students_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                            UPDATE spis SET name_book = ?, prich_spis = ? 
                            WHERE id_wrofbook = {self.select_row[0]}''', (nam_b, spis))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

if __name__ == "__main__":
    win = WindowMain()
    win.mainloop()
