from random import randint,random
from tkinter import *
from tkinter import messagebox
import random , pyperclip , json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


    # Generate individual lists for each type of character
    letters_list = [random.choice(letters) for _ in range(randint(8,10))]
    symbols_list = [random.choice(symbols) for _ in range(randint(2,4))]
    numbers_list = [random.choice(numbers) for _ in range(randint(2,4))]

    # Combine all the characters into a single flat list
    temp = letters_list + symbols_list + numbers_list

    # Shuffle the list
    random.shuffle(temp)

    # Join the shuffled list into a string
    password = ''.join(temp)
    password_entry.insert(0,password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = name_entry.get()
    password = password_entry.get()
    new_data = {
        website : {
            "email" : email,
            "password" : password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="oops!",message="Please don't leave any fields Empty!")
    else :
        if len(website) == 0 or len(password) == 0:
            messagebox.showinfo(title="Oops!", message="Please don't leave any fields empty!")
        else:
            try:
                with open("data.json", "r") as data_file:
                    # Read the file content first to check if it's empty
                    content = data_file.read().strip()
                    if content:
                        # If content exists, parse it as JSON
                        data = json.loads(content)
                    else:
                        # If file is empty, start with an empty dictionary
                        data = {}
            except FileNotFoundError:
                # If file doesn't exist, start with an empty dictionary
                data = {}
            except json.JSONDecodeError:
                # If file contains invalid JSON, start with an empty dictionary
                data = {}

            # Update the data with new entry
            data.update(new_data)

            # Write the updated data back to the file
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

            # Clear the entry fields
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- find Password ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError :
        messagebox.showinfo(title="Error",message="No data file found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"email : {email}\n password : {password}")
        else:
            messagebox.showinfo(title="Error",message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)
canvas = Canvas(height="200",width="200")
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100,100,image=logo_img)
canvas.grid(column=1,row=0)

website_txt = Label(text="Website:")
website_txt.grid(column=0,row=1)

website_entry = Entry(width=25)
website_entry.grid(column=1,row=1,sticky="E")
website_entry.focus()

search_btn = Button(text="Search",width=15,command=find_password)
search_btn.grid(column = 2,row=1,sticky="W")

name = Label(text="Email/Username:")
name.grid(column=0,row=2)

name_entry = Entry(width=44)
name_entry.grid(column=1,row=2,columnspan=2)
name_entry.insert(0,"akshat@gmail.com")

password_txt = Label(text="Password:")
password_txt.grid(column=0,row=3)

password_entry = Entry(width=25)
password_entry.grid(column=1,row=3,sticky="E")

gen_btn = Button(text="Generate Password",command=generate_password)
gen_btn.grid(column=2,row=3,sticky="W")

add_btn = Button(text="Add",width=41,command=save)
add_btn.grid(column=1,row=4,columnspan=2)

window.mainloop()