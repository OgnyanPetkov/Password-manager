from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip  # Package for copy/paste to/from clipboard
import json


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
    new_data = {site:
        {
            "E-mail:": username,
            "Password:": password
        }
    }
    if len(site) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title="Empty field!", message="Please fill all data!")
    else:
        check_box = messagebox.askokcancel(title="Information",
                                           message=f"This is the data entered:\nSite:{site}\nUsername:{username}\nPassword:{password}\nIs everything correct?")
        if check_box is True:
            try:  # Reading old data
                with open(file="Passwords.json", mode="r") as file:
                    data = json.load(file)
            except FileNotFoundError:  # Creating the file
                with open(file="Passwords.json", mode="w") as file:
                    json.dump(new_data, fp=file, indent=4)
            else:
                with open(file="Passwords.json", mode="r") as file:
                    data.update(new_data)  # Updating old data with new data
                with open(file="Passwords.json", mode="w") as file:
                    json.dump(data, fp=file, indent=4)  # Converting new data to json
            finally:
                site_entry.delete(0, END)
                username_entry.delete(0, END)
                password_entry.delete(0, END)


# -----------Search for password----------- #
def search_data():
    needed_data = site_entry.get().capitalize()
    try:
        with open(file="Passwords.json", mode="r") as file:
            available_data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="No data found", message=f"No data was found for {needed_data}")
    else:
        if needed_data in available_data:
            email = available_data[needed_data]["E-mail:"]
            password = available_data[needed_data]["Password:"]
            messagebox.showinfo(title=f"Credentials for {needed_data}", message=f"E-mail:{email}\nPassword:{password}")
        else:
            messagebox.showerror(title="No data found", message=f"No data was found for {needed_data}")


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
window.mainloop()
