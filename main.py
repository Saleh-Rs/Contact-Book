from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from database import connect, add_contact, get_contacts, update_contact, get_contact, delete_contact, search_contacts
connect()

selected_contact = None


def save_contact():

    first_name = name_entry.get()
    last_name = surname_entry.get()
    phone = number_entry.get()

    if first_name == "":
        text_result_label.config(text=("نام را وارد کنید"))
        return

    if phone == "":
        text_result_label.config(text=("شماره تماس را وارد کنید"))
        return

    if len(phone) != 11:
        messagebox.showerror('X', "شماره تماس باید 11 رقم باشد")
        return

    add_contact(first_name, last_name, phone)

    text_result_label.config(text=("مخاطب با موفقیت ذخیره شد"))

    name_entry.delete(0, END)
    surname_entry.delete(0, END)
    number_entry.delete(0, END)

    show_contacts()


def edit_contact():

    global selected_contact

    if selected_contact is None:
        text_result_label.config(text='')
        messagebox.showwarning('!', "ابتدا یک مخاطب را انتخاب کنید")
        return

    first_name = name_entry.get()
    last_name = surname_entry.get()
    phone = number_entry.get()

    if first_name == "" or phone == "":
        text_result_label.config(text='')
        text_result_label.config(text=(0, "تمام فیلدها را پر کنید"))
        return

    if len(phone) != 11:
        text_result_label.config(text='')
        text_result_label.config(text=(0, "شماره تماس باید 11 رقم باشد"))
        return

    update_contact(selected_contact, first_name, last_name, phone)

    text_result_label.config(text='')
    text_result_label.config(text=('مخاطب ویرایش شد'))

    name_entry.delete(0, END)
    surname_entry.delete(0, END)
    number_entry.delete(0, END)

    selected_contact = None

    show_contacts()
    show_contact_count()


def show_contact_count():

    count = len(get_contacts())

    count_label.config(text=f"تعداد مخاطبین: {count}")


def show_contacts():

    for row in table.get_children():
        table.delete(row)

    contacts = get_contacts()

    for contact in contacts:
        table.insert("", "end", values=contact)

    show_contact_count()


def select_contact(event):

    global selected_contact

    selected = table.focus()

    if selected == "":
        return

    values = table.item(selected)["values"]

    selected_contact = values[0]

    contact = get_contact(selected_contact)

    name_entry.delete(0, END)
    surname_entry.delete(0, END)
    number_entry.delete(0, END)

    name_entry.insert(0, contact[0])
    surname_entry.insert(0, contact[1])
    number_entry.insert(0, contact[2])


def remove_contact():

    global selected_contact

    if selected_contact is None:
        messagebox.showwarning("!", "ابتدا یک مخاطب را انتخاب کنید")
        return

    answer = messagebox.askyesno(
        "تأیید حذف",
        "آیا از حذف این مخاطب مطمئن هستید؟"
    )

    if not answer:
        return

    delete_contact(selected_contact)

    show_contacts()
    show_contact_count()

    name_entry.delete(0, END)
    surname_entry.delete(0, END)
    number_entry.delete(0, END)

    text_result_label.config(text="مخاطب حذف شد")

    selected_contact = None


def search_contact(event=None):

    text = search_entry.get()

    if text == "" or text == '...جستجوی مخاطب':
        show_contacts()
        return

    table.delete(*table.get_children())

    contacts = search_contacts(text)

    for contact in contacts:
        table.insert("", "end", values=contact)


def clear_search(event):

    if search_entry.get() == '...جستجوی مخاطب':
        search_entry.delete(0, END)
        search_entry.config(fg="black")


def restore_search(event):

    if search_entry.get() == "":
        search_entry.insert(0, '...جستجوی مخاطب')
        search_entry.config(fg="#858585")


window = Tk()
window.title('Contact Book')
window.geometry('800x890+560+60')
window.resizable(False, False)
window.config(bg="#e4deff")


def only_number(value):
    return value.isdigit() or value == ''


vcmd = (window.register(only_number), '%P')

number_entry = Entry(window, font=('', 22, 'bold'),
                     fg='#3F008B', bd=2, justify='center', validate='key', validatecommand=vcmd)
number_entry.place(width=220, height=40, x=390, y=160)


# Labels

top_label = Label(window, bg="#3F008B")
top_label.place(width=810, height=60)

title = Label(window, text='دفترچه مخاطبین', font=(
    '', 24, 'bold'), bg="#3F008B", fg="#e4deff")
title.place(width=230, height=55, x=485, y=4)

name_lable = Label(window, text=': نام', font=(
    '', 20, 'bold'), bg="#e4deff", fg='#3F008B')
name_lable.place(width=130, height=55, x=680, y=70)

surname_label = Label(window, text=': نام خانوادگی',
                      font=('', 20, 'bold'), bg="#e4deff", fg='#3F008B')
surname_label.place(width=140, height=55, x=330, y=70)

number_label = Label(window, text=': شماره تماس',
                     font=('', 20, 'bold'), bg="#e4deff", fg='#3F008B')
number_label.place(width=140, height=55, x=630, y=150)

result_label = Label(
    window,
    text=': نتیجه',
    font=('', 18, 'bold'),
    bg='#e4deff',
    fg='#3F008B',
)

result_label.place(width=70, height=40, x=700, y=830)


text_result_label = Label(
    window,
    text='',
    font=('', 18, 'bold'),
    fg='#3F008B',
    justify='center',
)

text_result_label.place(width=340, height=40, x=350, y=830)

count_label = Label(
    window,
    text="تعداد مخاطبین: 0",
    font=("", 17, "bold"),
    bg="#e4deff",
    fg="#3F008B"
)

count_label.place(x=70, y=830)


# Entrys

name_entry = Entry(window, font=('', 19, 'bold'),
                   fg='#3F008B', bd=2, justify='center')
name_entry.place(width=190, height=40, x=515, y=80)
name_entry.focus()

surname_entry = Entry(window, font=('', 20, 'bold'),
                      fg='#3F008B', bd=2, justify='center')
surname_entry.place(width=270, height=40, x=45, y=80)

search_entry = Entry(
    window,
    font=("", 18),
    justify="center"
)
search_entry.place(width=250, height=40, x=95, y=12)
search_entry.insert(0, '...جستجوی مخاطب')
search_entry.config(fg="#858585")

search_entry.bind("<FocusIn>", clear_search)
search_entry.bind("<FocusOut>", restore_search)
search_entry.bind("<KeyRelease>", search_contact)


# Buttons

add_button = Button(
    window,
    text="افزودن",
    font=("", 19, "bold"),
    bg="#3F008B",
    fg="white",
    bd=3,
    activebackground="#00C82B",
    activeforeground="black",
    cursor="hand2",
    command=save_contact
)

add_button.place(width=150, height=45, x=320, y=240)

update_button = Button(
    window,
    text="ویرایش",
    font=("", 19, "bold"),
    bg="#3F008B",
    fg="white",
    bd=3,
    activebackground="#e4deff",
    activeforeground="black",
    cursor="hand2",
    command=edit_contact
)

update_button.place(width=150, height=45, x=490, y=240)


delete_button = Button(
    window,
    text="حذف",
    font=("", 19, "bold"),
    bg="#3F008B",
    fg="white",
    bd=3,
    activebackground="#ff6b6b",
    cursor="hand2",
    command=remove_contact
)

delete_button.place(width=150, height=45, x=150, y=240)


style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background="white",
    foreground="#3F008B",
    rowheight=35,
    fieldbackground="white",
    font=("", 17)
)

style.configure(
    "Treeview.Heading",
    background="#3F008B",
    foreground="white",
    font=("", 14, "bold")
)

style.map(
    "Treeview",
    background=[("selected", "#e4deff")],
    foreground=[("selected", "black")]
)


# Table

table = ttk.Treeview(
    window,
    columns=("id", "name", "surname", "phone"),
    show="headings",
    height=8
)

table.heading("id", text="ID")
table.heading("name", text="نام")
table.heading("surname", text="نام خانوادگی")
table.heading("phone", text="شماره تماس")

table.column("id", width=70, anchor="center")
table.column("name", width=180, anchor="center")
table.column("surname", width=220, anchor="center")
table.column("phone", width=220, anchor="center")
table.place(x=35, y=330, width=720, height=475)


table.bind("<<TreeviewSelect>>", select_contact)
show_contacts()


# Scrollbar

scrollbar = ttk.Scrollbar(window, orient="vertical", command=table.yview)

table.configure(yscrollcommand=scrollbar.set)

scrollbar.place(x=755, y=330, height=475)


mainloop()
