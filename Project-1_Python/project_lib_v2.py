import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create a connection to the SQLite database

def init_database():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (title TEXT, author TEXT, year INTEGER, isbn TEXT, issued INTEGER)''')
    conn.commit()
    conn.close()

# init_database()

def search_books(title='', author='', isbn=''):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?",
              ('%' + title + '%', '%' + author + '%', '%' + isbn + '%'))
    result = c.fetchall()
    conn.close()

    # Clear the listbox before displaying new results
    listbox.delete(0, tk.END)
    for row in result:
        listbox.insert(tk.END, row)

def add_book(title, author, year, isbn):
    if title and author and year:
        conn = sqlite3.connect('books.db')
        c = conn.cursor()
        c.execute("INSERT INTO books VALUES (?, ?, ?, ?)", (title, author, year, isbn))
        conn.commit()
        conn.close()
        search_books(title, author, isbn)
        clear_entries()
    else:
        messagebox.showerror('Error', 'Title, author, and year are required.')

def issue_book(index):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("UPDATE books SET issued = 1 WHERE rowid = ?", (index + 1,))
    conn.commit()
    conn.close()
    search_books(listbox.get(index)[:3])

def delete_book(index):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE rowid = ?", (index + 1,))
    conn.commit()
    conn.close()
    search_books()

def update_book(index, title, author, year, isbn):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("UPDATE books SET title = ?, author = ?, year = ?, isbn = ? WHERE rowid = ?",
              (title, author, year, isbn, index + 1))
    conn.commit()
    conn.close()
    search_books()

def clear_entries():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)

# Initialize the main window and the database
init_database()

window = tk.Tk()
window.title('Library Book Management System')

# Frames
main_frame = tk.Frame(window)
main_frame.grid(row=0, column=0, padx=10, pady=10)

# Widgets
title_label = tk.Label(main_frame, text='Book Title:')
title_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
title_entry = tk.Entry(main_frame, width=40)
# Widgets (continuation)
title_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

author_label = tk.Label(main_frame, text='Author:')
author_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
author_entry = tk.Entry(main_frame, width=40)
author_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

year_label = tk.Label(main_frame, text='Year:')
year_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
year_entry = tk.Entry(main_frame, width=10)
year_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

isbn_label = tk.Label(main_frame, text='ISBN:')
isbn_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
isbn_entry = tk.Entry(main_frame, width=20)
isbn_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

# Functions bindings for buttons
search_button = tk.Button(main_frame, text='Search', command=lambda: search_books(title_entry.get(), author_entry.get(), isbn_entry.get()))
search_button.grid(row=4, column=0, padx=5, pady=5, sticky='w')
add_button = tk.Button(main_frame, text='Add', command=lambda: add_book(title_entry.get(), author_entry.get(), year_entry.get(), isbn_entry.get()))
add_button.grid(row=4, column=1, padx=5, pady=5)

# Scrollbar and Listbox
scrollbar = tk.Scrollbar(window)
scrollbar.grid(row=1, column=3, sticky='ns')

listbox = tk.Listbox(window, height=12, width=50, yscrollcommand=scrollbar.set)
listbox.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')
scrollbar.config(command=listbox.yview)

# Functions bindings for Listbox
def listbox_click(event):
    selected_index = listbox.curselection()
    if len(selected_index) > 0:
        index = int(selected_index[0])
        selected_book = listbox.get(index)
        title_entry.delete(0, tk.END)
        title_entry.insert(tk.END, selected_book[0])
        author_entry.delete(0, tk.END)
        author_entry.insert(tk.END, selected_book[1])
        year_entry.delete(0, tk.END)
        year_entry.insert(tk.END, selected_book[2])
        isbn_entry.delete(0, tk.END)
        isbn_entry.insert(tk.END, selected_book[3])

listbox.bind('<<ListboxSelect>>', listbox_click)

# Functions bindings for Menu
def issue_books():
    selected_index = listbox.curselection()
    if len(selected_index) > 0:
        issue_book(int(selected_index[0]))

def delete_books():
    selected_index = listbox.curselection()
    if len(selected_index) > 0:
        delete_book(int(selected_index[0]))

# Functions bindings for Menu (continuation)
def update_books():
    selected_index = listbox.curselection()
    if len(selected_index) > 0:
        title = title_entry.get()
        author = author_entry.get()
        year = year_entry.get()
        isbn = isbn_entry.get()
        update_book(int(selected_index[0]), title, author, year, isbn)

def reset_entries():
    clear_entries()
    listbox.delete(0, tk.END)

# Menu
menu = tk.Menu(window)
window.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Add", command=lambda: add_book(title_entry.get(), author_entry.get(), year_entry.get(), isbn_entry.get()))
file_menu.add_command(label="Search", command=lambda: search_books(title_entry.get(), author_entry.get(), isbn_entry.get()))
file_menu.add_separator()
file_menu.add_command(label="Reset", command=reset_entries)

edit_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Issue", command=issue_books)
edit_menu.add_command(label="Delete", command=delete_books)
edit_menu.add_command(label="Update", command=update_books)

# Initialize the main window and the database
init_database()

# Start the main loop
window.mainloop()