from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip  # Package for copy/paste to/from clipboard
import sqlite3 as sql

# -----------Password Generator--------- #
def pass_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_lt = [choice(letters) for letter in range(randint(8, 10))]
    password_sy = [choice(symbols) for symbol in range(randint(2, 4))]
    password_nm = [choice(numbers) for number in range(randint(2, 4))]
    password = password_nm + password_sy + password_lt
    shuffle(password)
    f_password = "".join(password)
    if len(password_entry.get()) == 0:
        password_entry.insert(0, f_password)
        pyperclip.copy(f_password)
    else:
        password_entry.delete(0, END)
        password_entry.insert(0, f_password)
        pyperclip.copy(f_password)


# ---------------Data saving---------------#
def add_info():
    site = site_entry.get().capitalize()
    username = username_entry.get()
    password = password_entry.get()
    params = (site, username, password)
    if len(site) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title="Empty field!", message="Please fill all data!")
    else:
        # Checking if entry exists
        check_query = db.execute(f"SELECT id, site, username FROM passwords")
        records=check_query.fetchall()
        for row in records:
            if str(row[1]) == site and str(row[2]) == username:
                update_info = messagebox.askyesno(title="Error", message=f'{username} exists for {site}. Do you want to change the password?')
                if update_info:
                    db.execute(f"UPDATE passwords SET site=?, username = ?, password = ? WHERE id = {row[0]}", params)
                    db.commit()
                    break
                else:
                    break
        else:
            check_box = messagebox.askokcancel(title="Information",
                                           message=f"This is the data entered:\nSite:{site}\nUsername:{username}\nPassword:{password}\nIs everything correct?")
            if check_box is True:

                db.execute('INSERT INTO passwords(site, username, password) VALUES(?,?,?)', params)
                db.commit()
                site_entry.delete(0, END)
                username_entry.delete(0, END)
                password_entry.delete(0, END)
            else:
                pass


# -----------Search for password----------- #
def search_data():
    needed_site = site_entry.get().capitalize()
    needed_username = username_entry.get()
    check_query = db.execute(f"SELECT * FROM passwords")
    records = check_query.fetchall()
    if len(site) == 0 or len(username) == 0:
        messagebox.showerror(title="Empty field!", message="Please fill site and username!")
    else:
        for row in records:
            if str(row[1]) == needed_site and str(row[2]) == needed_username:
                messagebox.showinfo(title=f"Credentials for {row[1]}", message=f"E-mail:{row[2]}\nPassword:{row[3]}")
                break
        else:
            messagebox.showerror(title="No data found", message=f"No data was found for {needed_site}")

# -------------User interface------------- #

FONT = "Arial"
window = Tk()
window.title("Password Manager")
window.config(padx=75, pady=75)

# Logo setup
logo = PhotoImage(file="logo.png")
canvas = Canvas(width=250, height=250)
canvas.create_image(125, 125, image=logo)
canvas.grid(column=1, row=0)

# Labels
site_label = Label(text="Site:", font=(FONT, 18, "normal"))
site_label.grid(column=0, row=1)
username_label = Label(text="E-mail/Username:", font=(FONT, 18, "normal"))
username_label.grid(column=0, row=2)
password_label = Label(text="Password:", font=(FONT, 18, "normal"))
password_label.grid(column=0, row=3)

# Entries
site_entry = Entry(font=(FONT, 15, "normal"), width=23)
site_entry.grid(column=1, row=1)
site_entry.focus()  # To instantly activate the entry widget

username_entry = Entry(font=(FONT, 15, "normal"), width=34)
username_entry.grid(column=1, row=2, columnspan=2)
username_entry.insert(0, "ogikrpetkov@gmail.com")  # Pre-insert my usual e-mail

password_entry = Entry(font=(FONT, 15, "normal"), width=23)
password_entry.grid(column=1, row=3)

# Buttons
generate_button = Button(text="Generate password", font=(FONT, 10, "normal"), width=13, command=pass_gen)
generate_button.grid(column=2, row=3)
add_button = Button(text="Add info", font=(FONT, 10, "normal"), width=46, command=add_info)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", font=(FONT, 10, "normal"), width=13, command=search_data)
search_button.grid(column=2, row=1)

if __name__ == "__main__":
    db = sql.Connection("pass-manager.db")
    db.execute("CREATE TABLE IF NOT EXISTS passwords (id  INTEGER PRIMARY KEY NOT NULL, site, username, password)")
    window.mainloop()
