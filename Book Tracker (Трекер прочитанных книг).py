"""
PROJECT: Book Tracker - Трекер прочитанных книг
AUTHOR: Суроян Роман Асланович, 8 класс (соавтор)
CO-AUTHOR: Басырова Элина Алмазовна, 9 класс
TEACHER: Сафин Динис Разитович, преподаватель информатики
YEAR: 2026
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class BookTracker:
    
    def __init__(self, r):
        self.r = r
        self.r.title("Book Tracker - Трекер прочитанных книг")
        self.r.geometry("900x700")
        self.r.resizable(True, True)
        self.r.configure(bg='#2E3440')  # Тёмный фон Nordic
        
        self.b = []
        
        self.show_instructions()
        
        self.load_data()
        self.create_widgets()
        self.update_list()
        self.show_authors()
    
    def show_instructions(self):
        instr = tk.Toplevel(self.r)
        instr.title("Инструкция по использованию")
        instr.geometry("550x550")
        instr.configure(bg='#2E3440')
        instr.resizable(False, False)
        
        instr.transient(self.r)
        instr.grab_set()
        
        main_frame = tk.Frame(instr, bg='#2E3440')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        title = tk.Label(main_frame, text="ДОБРО ПОЖАЛОВАТЬ В BOOK TRACKER!", 
                        font=('Arial', 14, 'bold'), bg='#2E3440', fg='#88C0D0')
        title.pack(pady=10)
        
        line = tk.Frame(main_frame, bg='#5E81AC', height=2)
        line.pack(fill='x', pady=5)
        
        canvas = tk.Canvas(main_frame, bg='#2E3440', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2E3440')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        text = """
ОСНОВНЫЕ ФУНКЦИИ ПРОГРАММЫ:

1. ДОБАВЛЕНИЕ КНИГИ:
   - Введите название книги
   - Введите автора
   - Выберите жанр из выпадающего списка
   - Укажите количество страниц (только число)
   - Нажмите кнопку "ДОБАВИТЬ КНИГУ"

2. ПРОСМОТР КНИГ:
   - Все добавленные книги отображаются в таблице
   - В таблице показаны: название, автор, жанр, страницы
   - Количество книг отображается в заголовке окна

3. ФИЛЬТРАЦИЯ КНИГ:
   - По жанру: выберите жанр из списка и нажмите "ПРИМЕНИТЬ ФИЛЬТР"
   - По страницам: введите минимальное количество страниц
   - Можно использовать оба фильтра одновременно
   - Нажмите "СБРОСИТЬ ФИЛЬТР" чтобы показать все книги

4. СТАТИСТИКА:
   - Нажмите кнопку "СТАТИСТИКА"
   - Вы увидите: общее количество книг, общее число страниц,
     среднее количество страниц, распределение по жанрам,
     самую толстую и самую тонкую книгу

5. СОХРАНЕНИЕ И ЗАГРУЗКА:
   - Нажмите "СОХРАНИТЬ В JSON" - все данные сохранятся в файл books.json
   - При следующем запуске данные загрузятся автоматически
   - Нажмите "ЗАГРУЗИТЬ ИЗ JSON" чтобы загрузить последнее сохранение

6. ОЧИСТКА ДАННЫХ:
   - Нажмите "ОЧИСТИТЬ ВСЕ" чтобы удалить все книги
   - Программа запросит подтверждение перед удалением

ПРАВИЛА ВВОДА ДАННЫХ:

   - Название книги: не может быть пустым
   - Автор: не может быть пустым
   - Жанр: обязательно выберите из списка
   - Страницы: только целое положительное число (например: 350)

ПРИМЕРЫ ПРАВИЛЬНОГО ВВОДА:

   Название: Мастер и Маргарита
   Автор: Михаил Булгаков
   Жанр: Роман
   Страницы: 480

   Название: Гарри Поттер
   Автор: Джоан Роулинг
   Жанр: Фэнтези
   Страницы: 350

ПРИМЕРЫ ФИЛЬТРАЦИИ:

   - Показать все романы: выберите жанр "Роман" и нажмите фильтр
   - Показать книги с более чем 500 страниц: введите 500 в поле страниц
   - Показать фэнтези с более чем 300 страниц: выберите жанр "Фэнтези" и введите 300

ВОЗМОЖНЫЕ ОШИБКИ:

   - Если не заполнить все поля: появится сообщение об ошибке
   - Если ввести буквы в поле страниц: появится сообщение об ошибке
   - Если файл JSON повреждён: программа покажет ошибку

ИНФОРМАЦИЯ О РАЗРАБОТЧИКАХ:

   Автор: Суроян Роман Асланович, 8 класс
   Соавтор: Басырова Элина Алмазовна, 9 класс
   Преподаватель: Сафин Динис Разитович
   Год разработки: 2026
        """
        
        label = tk.Label(scrollable_frame, text=text, font=('Arial', 10), 
                        bg='#2E3440', fg='#D8DEE9', justify='left')
        label.pack(pady=10, padx=15)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        btn_frame = tk.Frame(main_frame, bg='#2E3440')
        btn_frame.pack(pady=15)
        
        btn_start = tk.Button(btn_frame, text="НАЧАТЬ РАБОТУ", command=instr.destroy,
                             bg='#A3BE8C', fg='#2E3440', font=('Arial', 11, 'bold'), 
                             padx=25, pady=8)
        btn_start.pack()
        
        self.r.wait_window(instr)
    
    def show_authors(self):
        f_a = tk.LabelFrame(self.r, text="Информация о разработчиках", 
                           font=('Arial', 10, 'bold'), bg='#2E3440', 
                           fg='#88C0D0', padx=10, pady=10)
        f_a.pack(side='bottom', fill='x', padx=10, pady=5)
        
        authors_frame = tk.Frame(f_a, bg='#2E3440')
        authors_frame.pack()
        
        author_text = "Автор: Суроян Роман Асланович, 8 класс"
        co_author_text = "Соавтор: Басырова Элина Алмазовна, 9 класс"
        teacher_text = "Преподаватель: Сафин Динис Разитович"
        year_text = "Год разработки: 2026"
        
        l1 = tk.Label(authors_frame, text=author_text, font=('Arial', 10, 'bold'), 
                     fg='#A3BE8C', bg='#2E3440')
        l1.pack(anchor='w')
        
        l1b = tk.Label(authors_frame, text=co_author_text, font=('Arial', 10, 'bold'), 
                      fg='#81A1C1', bg='#2E3440')
        l1b.pack(anchor='w', pady=2)
        
        l2 = tk.Label(authors_frame, text=teacher_text, font=('Arial', 10), 
                     fg='#88C0D0', bg='#2E3440')
        l2.pack(anchor='w', pady=2)
        
        l3 = tk.Label(authors_frame, text=year_text, font=('Arial', 9), 
                     fg='#D8DEE9', bg='#2E3440')
        l3.pack(anchor='w')
    
    def create_widgets(self):
        
        f1 = tk.LabelFrame(self.r, text="Добавление новой книги", 
                           font=('Arial', 11, 'bold'), bg='#3B4252', 
                           fg='#88C0D0', padx=10, pady=10)
        f1.pack(fill='x', padx=10, pady=5)
        
        tk.Label(f1, text="Название книги:", bg='#3B4252', fg='#D8DEE9', font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.e_title = tk.Entry(f1, width=30, font=('Arial', 10), bg='#4C566A', fg='#ECEFF4', insertbackground='#ECEFF4')
        self.e_title.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(f1, text="Автор:", bg='#3B4252', fg='#D8DEE9', font=('Arial', 10)).grid(row=0, column=2, sticky='w', padx=(15,0), pady=5)
        self.e_author = tk.Entry(f1, width=20, font=('Arial', 10), bg='#4C566A', fg='#ECEFF4', insertbackground='#ECEFF4')
        self.e_author.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(f1, text="Жанр:", bg='#3B4252', fg='#D8DEE9', font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        
        genres = ["Роман", "Детектив", "Фантастика", "Фэнтези", "Научная литература", 
                  "Поэзия", "Драма", "Комедия", "Приключения", "Триллер", "Ужасы", "Другое"]
        self.genre_var = tk.StringVar()
        self.genre_combo = ttk.Combobox(f1, textvariable=self.genre_var, values=genres, width=15, font=('Arial', 10))
        self.genre_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.genre_combo.set("Выберите жанр")
        
        tk.Label(f1, text="Количество страниц:", bg='#3B4252', fg='#D8DEE9', font=('Arial', 10)).grid(row=1, column=2, sticky='w', padx=(15,0), pady=5)
        self.e_pages = tk.Entry(f1, width=10, font=('Arial', 10), bg='#4C566A', fg='#ECEFF4', insertbackground='#ECEFF4')
        self.e_pages.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        
        btn_add = tk.Button(f1, text="ДОБАВИТЬ КНИГУ", command=self.add_book,
                           bg='#A3BE8C', fg='#2E3440', font=('Arial', 11, 'bold'), padx=20, pady=5)
        btn_add.grid(row=2, column=0, columnspan=4, pady=15)
        
        f2 = tk.LabelFrame(self.r, text="Фильтрация книг", 
                           font=('Arial', 11, 'bold'), bg='#3B4252', 
                           fg='#88C0D0', padx=10, pady=10)
        f2.pack(fill='x', padx=10, pady=5)
        
        tk.Label(f2, text="Фильтр по жанру:", bg='#3B4252', fg='#D8DEE9', font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        
        filter_genres = ["Все жанры"] + genres
        self.f_genre_var = tk.StringVar()
        self.f_genre_combo = ttk.Combobox(f2, textvariable=self.f_genre_var, values=filter_genres, width=15, font=('Arial', 10))
        self.f_genre_combo.grid(row=0, column=1, padx=5, pady=5)
        self.f_genre_combo.set("Все жанры")
        
        tk.Label(f2, text="Страниц больше чем:", bg='#3B4252', fg='#D8DEE9', font=('Arial', 10)).grid(row=0, column=2, sticky='w', padx=(15,0), pady=5)
        self.f_pages = tk.Entry(f2, width=8, font=('Arial', 10), bg='#4C566A', fg='#ECEFF4', insertbackground='#ECEFF4')
        self.f_pages.grid(row=0, column=3, padx=5, pady=5)
        
        btn_filter = tk.Button(f2, text="ПРИМЕНИТЬ ФИЛЬТР", command=self.apply_filter,
                              bg='#5E81AC', fg='#ECEFF4', font=('Arial', 10, 'bold'), padx=10)
        btn_filter.grid(row=0, column=4, padx=15, pady=5)
        
        btn_reset = tk.Button(f2, text="СБРОСИТЬ ФИЛЬТР", command=self.reset_filter,
                             bg='#D08770', fg='#2E3440', font=('Arial', 10, 'bold'), padx=10)
        btn_reset.grid(row=0, column=5, padx=5, pady=5)
        
        f3 = tk.Frame(self.r, bg='#2E3440')
        f3.pack(fill='both', expand=True, padx=10, pady=10)
        
        cols = ('title', 'author', 'genre', 'pages')
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", background="#3B4252", fieldbackground="#3B4252", foreground="#D8DEE9", rowheight=25)
        style.map('Treeview', background=[('selected', '#5E81AC')])
        style.configure("Treeview.Heading", background="#4C566A", foreground="#ECEFF4", font=('Arial', 10, 'bold'))
        
        self.tree = ttk.Treeview(f3, columns=cols, show='headings', height=12)
        
        self.tree.heading('title', text='НАЗВАНИЕ КНИГИ')
        self.tree.heading('author', text='АВТОР')
        self.tree.heading('genre', text='ЖАНР')
        self.tree.heading('pages', text='СТРАНИЦ')
        
        self.tree.column('title', width=300)
        self.tree.column('author', width=180)
        self.tree.column('genre', width=120, anchor='center')
        self.tree.column('pages', width=90, anchor='center')
        
        scroll = ttk.Scrollbar(f3, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        
        f4 = tk.Frame(self.r, bg='#2E3440')
        f4.pack(pady=10)
        
        btn_save = tk.Button(f4, text="СОХРАНИТЬ В JSON", command=self.save_json,
                            bg='#B48EAD', fg='#2E3440', font=('Arial', 11, 'bold'), padx=20, pady=5)
        btn_save.pack(side='left', padx=10)
        
        btn_load = tk.Button(f4, text="ЗАГРУЗИТЬ ИЗ JSON", command=self.load_json,
                            bg='#81A1C1', fg='#2E3440', font=('Arial', 11, 'bold'), padx=20, pady=5)
        btn_load.pack(side='left', padx=10)
        
        btn_stats = tk.Button(f4, text="СТАТИСТИКА", command=self.show_stats,
                             bg='#BF616A', fg='#ECEFF4', font=('Arial', 11, 'bold'), padx=20, pady=5)
        btn_stats.pack(side='left', padx=10)
        
        btn_clear = tk.Button(f4, text="ОЧИСТИТЬ ВСЕ", command=self.clear_all,
                             bg='#D08770', fg='#2E3440', font=('Arial', 11, 'bold'), padx=20, pady=5)
        btn_clear.pack(side='left', padx=10)
    
    def add_book(self):
        
        title = self.e_title.get().strip()
        author = self.e_author.get().strip()
        genre = self.genre_var.get().strip()
        pages = self.e_pages.get().strip()
        
        if not title or not author:
            messagebox.showerror("Ошибка", "Заполните название книги и автора!")
            return
        
        if genre == "Выберите жанр" or not genre:
            messagebox.showerror("Ошибка", "Выберите жанр книги!")
            return
        
        if not pages:
            messagebox.showerror("Ошибка", "Укажите количество страниц!")
            return
        
        try:
            p = int(pages)
            if p <= 0:
                messagebox.showerror("Ошибка", "Количество страниц должно быть больше 0!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом! Пример: 350")
            return
        
        self.b.append({
            "title": title,
            "author": author,
            "genre": genre,
            "pages": p
        })
        
        self.e_title.delete(0, tk.END)
        self.e_author.delete(0, tk.END)
        self.genre_combo.set("Выберите жанр")
        self.e_pages.delete(0, tk.END)
        
        self.update_list()
        
        messagebox.showinfo("Успех", f"Книга добавлена!\n\nНазвание: {title}\nАвтор: {author}\nЖанр: {genre}\nСтраниц: {p}")
    
    def update_list(self, f_list=None):
        
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        show = f_list if f_list is not None else self.b
        
        for book in show:
            try:
                self.tree.insert("", tk.END, values=(
                    book.get("title", "Нет названия"), 
                    book.get("author", "Нет автора"), 
                    book.get("genre", "Нет жанра"), 
                    f"{book.get('pages', 0)} стр."
                ))
            except Exception as e:
                continue
        
        count = len(show)
        total_pages = 0
        for book in show:
            try:
                total_pages += book.get("pages", 0)
            except:
                pass
        
        if count == 0:
            self.r.title("Book Tracker - Нет книг")
        else:
            self.r.title(f"Book Tracker - {count} книг | Всего страниц: {total_pages}")
    
    def apply_filter(self):
        
        f_genre = self.f_genre_var.get().strip()
        f_pages = self.f_pages.get().strip()
        
        res = self.b.copy()
        
        if f_genre and f_genre != "Все жанры":
            res = [x for x in res if x.get("genre", "") == f_genre]
        
        if f_pages:
            try:
                p = int(f_pages)
                res = [x for x in res if x.get("pages", 0) > p]
            except ValueError:
                messagebox.showerror("Ошибка", "Количество страниц в фильтре должно быть числом!")
                return
        
        self.update_list(res)
        
        if len(res) == 0:
            messagebox.showinfo("Результат", "Книг, соответствующих фильтру, не найдено.")
        else:
            messagebox.showinfo("Результат", f"Найдено книг: {len(res)}")
    
    def reset_filter(self):
        self.f_genre_combo.set("Все жанры")
        self.f_pages.delete(0, tk.END)
        self.update_list()
        messagebox.showinfo("Фильтр сброшен", "Показываются все книги")
    
    def show_stats(self):
        if not self.b:
            messagebox.showinfo("Статистика", "Нет добавленных книг. Добавьте хотя бы одну книгу для статистики.")
            return
        
        valid_books = [book for book in self.b if "title" in book and "pages" in book]
        
        if not valid_books:
            messagebox.showinfo("Статистика", "Нет корректных данных для статистики.")
            return
        
        total_books = len(valid_books)
        total_pages = sum(book.get("pages", 0) for book in valid_books)
        avg_pages = total_pages // total_books if total_books > 0 else 0
        
        genres_count = {}
        for book in valid_books:
            g = book.get("genre", "Другое")
            genres_count[g] = genres_count.get(g, 0) + 1
        
        if genres_count:
            most_popular = max(genres_count, key=genres_count.get)
            most_popular_count = genres_count[most_popular]
        else:
            most_popular = "Нет"
            most_popular_count = 0
        
        thickest = max(valid_books, key=lambda x: x.get("pages", 0))
        thinnest = min(valid_books, key=lambda x: x.get("pages", 0))
        
        stats_text = f"""
============================================================
                    СТАТИСТИКА КНИГ                    
============================================================

  Всего книг: {total_books}                            
  Всего страниц: {total_pages}                         
  Среднее кол-во страниц: {avg_pages}                  

  Распределение по жанрам:                             """
        
        for g, c in sorted(genres_count.items(), key=lambda x: x[1], reverse=True):
            stats_text += f"\n     - {g}: {c} книг"
        
        stats_text += f"""

  Самый популярный жанр: {most_popular} ({most_popular_count} книг)

  Самая толстая книга:                                 
     - {thickest.get('title', 'Нет названия')} - {thickest.get('pages', 0)} стр.     

  Самая тонкая книга:                                  
     - {thinnest.get('title', 'Нет названия')} - {thinnest.get('pages', 0)} стр.     

============================================================
        """
        
        messagebox.showinfo("Статистика прочитанных книг", stats_text)
    
    def save_json(self):
        try:
            with open("books.json", "w", encoding="utf-8") as f:
                json.dump(self.b, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Успех", f"Данные сохранены в файл books.json\n\nСохранено книг: {len(self.b)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл!\nОшибка: {e}")
    
    def load_json(self):
        if not os.path.exists("books.json"):
            messagebox.showerror("Ошибка", "Файл books.json не найден!\nСначала сохраните данные.")
            return
        
        try:
            with open("books.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                messagebox.showerror("Ошибка", "Файл повреждён! Начните заново.")
                return
            
            new_books = []
            for book in data:
                if isinstance(book, dict):
                    new_book = {
                        "title": book.get("title", book.get("name", "Без названия")),
                        "author": book.get("author", "Неизвестный автор"),
                        "genre": book.get("genre", "Другое"),
                        "pages": book.get("pages", book.get("page", 100))
                    }
                    new_books.append(new_book)
            
            if new_books:
                self.b = new_books
                self.update_list()
                messagebox.showinfo("Успех", f"Данные загружены из books.json\n\nЗагружено книг: {len(self.b)}")
            else:
                messagebox.showwarning("Предупреждение", "Файл пуст или имеет неверный формат.")
                
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Файл books.json повреждён!\nУдалите его и сохраните заново.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке файла!\nОшибка: {e}")
    
    def clear_all(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить ВСЕ книги?"):
            self.b = []
            self.update_list()
            messagebox.showinfo("Готово", "Все книги удалены!")
    
    def load_data(self):
        if os.path.exists("books.json"):
            try:
                with open("books.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                if isinstance(data, list):
                    new_books = []
                    for book in data:
                        if isinstance(book, dict):
                            new_book = {
                                "title": book.get("title", book.get("name", "Без названия")),
                                "author": book.get("author", "Неизвестный автор"),
                                "genre": book.get("genre", "Другое"),
                                "pages": book.get("pages", book.get("page", 100))
                            }
                            new_books.append(new_book)
                    self.b = new_books
            except:
                self.b = []


if __name__ == "__main__":
    r = tk.Tk()
    app = BookTracker(r)
    r.mainloop()
