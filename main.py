from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from customtkinter import *
import tkinter
import random
import pymysql
import csv
from datetime import datetime
import numpy as np
import string

window = CTk()
window.title("IRIS v0.1")
window.geometry("1024x840")
set_appearance_mode("dark")

numbers = string.digits
characters = string.ascii_uppercase

# Empty array to identify each entry
placeholderArray = ['','','','','']

# Defining the connection
def connection():
    conn = pymysql.connect(
        host = '127.0.0.1',
        user = 'root',
        password = '',
        db = 'IRIS v0.1'
    )
    return conn

conn = connection()
cursor = conn.cursor()

# Assigning the values for the elements/widgets with the placeholderArray
for i in range(0, 5):
    placeholderArray[i] = tkinter.StringVar()

# Function so the program can read and update the tree list according to information given in the database
def readData():
    cursor.connection.ping()
    sql = f'SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks ORDER BY `id` DESC'
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

# Updating the entry fields
def setfi(word, num):
    for fi in range(0, 5):
        if fi == num:
            placeholderArray[fi].set(word)

# Function to randomly generate an ITEM ID
def randomGenId():
    itemId = ''
    for i in range(0, 3):
        randoPick = random.randrange(0,(len(numbers)-1))
        itemId = itemId+str(numbers[randoPick])
    randoPick = random.randrange(0,(len(characters)-1))
    itemId = itemId + '-' + str(characters[randoPick])
    print("Generated new ID: " + itemId)
    setfi(itemId, 0)

# Function to save item information from the entry fields and store it in the tree list, this is what will run when you press the SAVE button
def save():
    itemId = str(itemIdEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    qnt = str(qntEntry.get())
    categ = str(categoryCombo.get())
    valid = True
    # If information on one of the fields is missing
    if not (itemId and itemId.strip()) or not (name and name.strip()) or not (price and price.strip()) or not (qnt and qnt.strip()) or not (categ and categ.strip()):
        messagebox.showwarning("Information Error","Please fill all fields.")
        return
    # If the ITEM ID is shorter than 5 characters, return error
    if len(itemId) < 5:
        messagebox.showwarning("ID Error Instance:1","Invalid Item Id.")
        return
    # If there is no '-' on the ID, return invalid
    if (not(itemId[3] == '-')):
        valid = False
    # If the first 3 characters of the ID are not numbers, return invalid
    for i in range(0,3):
        if(not(itemId[i] in numbers)):
            valid = False
            break
    # If the last character of the ID is not an alphanumeric character, return invalid
    if(not(itemId[4] in characters)):
        valid = False
    # Show error message
    if not(valid):
        messagebox.showwarning("ID Error Instance:1","Invalid Item Id.")
        return
    # Try for saving all entered information
    try:
        cursor.connection.ping()
        sql = f'SELECT * FROM stocks WHERE `item_id` = "{itemId}" '
        cursor.execute(sql)
        checkItemNo = cursor.fetchall()
        # Throw out error if the ITEM ID is already in use
        if len(checkItemNo) > 0:
            messagebox.showwarning("ID Error Instance:2", "Item Id already used.")
        # if nothing is wrong, save the information
        else:
            cursor.connection.ping()
            sql = f"INSERT INTO stocks (`item_id`, `name`, `price`, `quantity`, `category`) VALUES ('{itemId}','{name}','{price}','{qnt}','{categ}')"
            cursor.execute(sql)
        conn.commit()
        conn.close
        # Clear all fields when item is saved/created
        for num in range (0, 5):
            setfi('', (num))
    # If anything were to go wrong, throw out error
    except:
        messagebox.showwarning("Error", "Error while saving.")
        return
    # Refresh the tree list to the display the newly saved item and its information (refer to the refreshTable function)
    refreshTable()

# Update function, this will run when you press the UPDATE button
def update():
    selectedItemId = ''
    try:
        selectedItem = my_tree.selection()[0]
        selectedItemId = str(my_tree.item(selectedItem)['values'][0])
    except:
        messagebox.showwarning("Selection Error", "Please select a data row.")
    print(selectedItemId)
    itemId = str(itemIdEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    qnt = str(qntEntry.get())
    categ = str(categoryCombo.get())
    if not (itemId and itemId.strip()) or not (name and name.strip()) or not (price and price.strip()) or not (qnt and qnt.strip()) or not (categ and categ.strip()):
        messagebox.showwarning("Empty Fields","Please fill all fields")
        return
    # If the ID of the selected item does not match with the ID in the item information field, throw error
    if(selectedItemId != itemId):
        messagebox.showwarning("ID Error Instance:3", "You can't change the Item ID.")
        return
    # Try to update the information of the selected item
    try:
        cursor.connection.ping()
        sql = f'UPDATE stocks SET `name` = "{name}", `price` = "{price}", `quantity` = "{qnt}", `category` = "{categ}" WHERE `item_id` = "{itemId}" '
        cursor.execute(sql)
        conn.commit()
        conn.close
        for num in range (0, 5):
            setfi('', (num))
    # If anything were to go wrong, throw out error
    except Exception as err:
        messagebox.showwarning("Error", "Error occured ref: " + str(err))
        return
    # Refresh the tree list to the display the newly update information (refer to the refreshTable function)
    refreshTable()

# Delete any selected item, this will run when pressing the DELETE button
def delete():
    try:
        # Confirmation of data deletion
        if(my_tree.selection()[0]):
            decision = messagebox.askquestion("CONFIRM DELETION", "Delete the selected data?")
            if (decision != 'yes'):
                return
            else:
                selectedItem = my_tree.selection()[0]
                itemId = str(my_tree.item(selectedItem)['values'][0])
                try:
                    cursor.connection.ping()
                    sql = f'DELETE FROM stocks WHERE `item_id` = "{itemId}" '
                    cursor.execute(sql)
                    conn.commit()
                    conn.close
                    messagebox.showinfo("Success", "Data has been succesfully deleted.")
                # If anything were to go wrong, throw out error
                except:
                    messagebox.showinfo("Error", "An error has occured when deleting data.")
                refreshTable()
    # If no item selected, throw error
    except:
        messagebox.showwarning("Selection Error", "Please select a data row.")

# Input all information of selected item into the info fields, this will run when pressing the SELECT button
def select():
    try:
        selectedItem = my_tree.selection()[0]
        itemId = str(my_tree.item(selectedItem)['values'][0])
        name = str(my_tree.item(selectedItem)['values'][1])
        price = str(my_tree.item(selectedItem)['values'][2])
        qnt = str(my_tree.item(selectedItem)['values'][3])
        categ = str(my_tree.item(selectedItem)['values'][4])
        setfi(itemId, 0)
        setfi(name, 1)
        setfi(price, 2)
        setfi(qnt, 3)
        setfi(categ, 4)
    # If no item selected, throw error
    except:
        messagebox.showwarning("Selection Error", "Please select a data row.")

# Find an item based on details entered in any field
def find():
    itemId = str(itemIdEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    qnt = str(qntEntry.get())
    categ = str(categoryCombo.get())
    cursor.connection.ping()
    if(itemId and itemId.strip()):
        sql = f'SELECT `item_id`, `name`, `price`, `quantity`, `category` FROM stocks WHERE `item_id` LIKE "%{itemId}%" '
    elif(name and name.strip()):
        sql = f'SELECT `item_id`, `name`, `price`, `quantity`, `category` FROM stocks WHERE `name` LIKE "%{name}%" '
    elif(price and price.strip()):
        sql = f'SELECT `item_id`, `name`, `price`, `quantity`, `category` FROM stocks WHERE `price` LIKE "%{price}%" '
    elif(qnt and qnt.strip()):
        sql = f'SELECT `item_id`, `name`, `price`, `quantity`, `category` FROM stocks WHERE `quantity` LIKE "%{qnt}%" '
    elif(categ and categ.strip()):
        sql = f'SELECT `item_id`, `name`, `price`, `quantity`, `category` FROM stocks WHERE `category` LIKE "%{categ}%" '
    else:
        messagebox.showwarning("Search Error", "Please enter information on a field to base the search on.")
        return
    cursor.execute(sql)
    try:
        result = cursor.fetchall()
        for num in range(0, 5):
            setfi(result[0][num], (num))
        conn.commit()
        conn.close()
    except:
        messagebox.showwarning("Search Error", "No data found with this information.")

# Clear information from entry fields, this will run when pressing the CLEAR button
def clear():
    for num in range (0, 5):
            setfi('', (num))

# Function to export all items into an Excel sheet, this will run when pressing the EXPORT EXCEL button
def exportExcel():
    cursor.connection.ping()
    sql = f'SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks ORDER BY `id` DESC'
    cursor.execute(sql)
    dataraw = cursor.fetchall()
    date = str(datetime.now())
    date = date.replace(' ', '_')
    date = date.replace(':', '-')
    dateFinal = date[0:16]
    with open("stocks_" + dateFinal + ".csv", 'a', newline = '') as f:
        w = csv.writer(f, dialect = 'excel')
        for record in dataraw:
            w.writerow(record)
    print("Saved: stocks_" + dateFinal + ".csv")
    conn.commit()
    conn.close()
    messagebox.showinfo("Excel Download", "Excel file successfully downloaded.")

# The frame where all buttons and other tkinter widgets will be added
frame = Frame(window, background = "#25323d")
frame.pack(fill = X)
# Center widgets inside frame
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Color for all buttons so they're the same
### otherBtnColor = "#f5dad3" ###

title = CTkLabel(frame, text = "Welcome to IRIS v0.1", font = ("Roboto", 16))
title.grid(row = 0, column = 0, pady = [22, 0], ipadx=[6])

# Frame and it's items for entering product information
entriesFrame = tkinter.LabelFrame(frame, borderwidth = 0, bg = "#25323d")
entriesFrame.grid(row = 1, column = 0, pady = [22, 0], ipadx=[6])
### entriesFrame.grid(row = 0, column = 0, pady = [0, 20], ipadx=[6]) ###

# Labels for all ENTRY form fields
itemIdLabel = CTkLabel(entriesFrame, text = "ITEM ID", font = ("Roboto", 14))
nameLabel = CTkLabel(entriesFrame, text = "NAME", font = ("Roboto", 14))
priceLabel = CTkLabel(entriesFrame, text = "PRICE", font = ("Roboto", 14))
qntLabel = CTkLabel(entriesFrame, text = "QUANTITY", font = ("Roboto", 14))
categoryLabel = CTkLabel(entriesFrame, text = "CATEGORY", font = ("Roboto", 14))

# Padding and positioning for all the labels for ENTRY form fields
itemIdLabel.grid(row = 0, column = 0, sticky = E, padx = 10)
nameLabel.grid(row = 1, column = 0, sticky = E, padx = 10)
priceLabel.grid(row = 2, column = 0, sticky = E, padx = 10)
qntLabel.grid(row = 3, column = 0, sticky = E, padx = 10)
categoryLabel.grid(row = 4, column = 0, sticky = E, padx = 10)

# List of values for the CATEGORY combobox
categoryArray = ['Networking Tools', 'Computer Parts', 'Repair Tools', 'Gadgets']

# Entry fields for the ENTRY form
itemIdEntry = CTkEntry(entriesFrame, width = 350, textvariable = placeholderArray[0])
nameEntry = CTkEntry(entriesFrame, width = 350, textvariable = placeholderArray[1])
priceEntry = CTkEntry(entriesFrame, width = 350, textvariable = placeholderArray[2])
qntEntry = CTkEntry(entriesFrame, width = 350, textvariable = placeholderArray[3])
# Combobox so we're able to pick the values listed in categoryArray
categoryCombo = CTkComboBox(entriesFrame, width = 350,variable = placeholderArray[4], values = categoryArray)

# Padding and positioning for all the entry elements
itemIdEntry.grid(row = 0, column = 1, padx = 5, pady = 5)
nameEntry.grid(row = 1, column = 1, padx = 5, pady = 5)
priceEntry.grid(row = 2, column = 1, padx = 5, pady = 5)
qntEntry.grid(row = 3, column = 1, padx = 5, pady = 5)
categoryCombo.grid(row = 4, column = 1, padx = 5, pady = 5)

# Button for ID generation
generateIdBtn = CTkButton(entriesFrame, text = "GENERATE ID", width = 100, font = ("Roboto", 14), command = randomGenId)
generateIdBtn.grid(row = 0, column = 3, padx = 5, pady = 5)

# Frame and it's items for actions
manageFrame = tkinter.LabelFrame(frame, borderwidth = 0, bg = "#25323d")
manageFrame.grid(row = 2, column = 0, pady = [22, 0], ipadx=[6])
### manageFrame.grid(row = 1, column = 0, pady = 20, ipadx=[6]) ###

# Buttons for the MANAGE section
saveBtn = CTkButton(manageFrame, text = "SAVE", width = 100, fg_color = "#29a41f", hover_color = "#1f7b17", font = ("Roboto", 14), command = save)
deleteBtn = CTkButton(manageFrame, text = "DELETE", width = 100, fg_color = "#a41f29", hover_color = "#7b171f", font = ("Roboto", 14), command = delete)
updateBtn = CTkButton(manageFrame, text = "UPDATE", width = 100, font = ("Roboto", 14), command = update)
selectBtn = CTkButton(manageFrame, text = "SELECT", width = 100, font = ("Roboto", 14), command = select)
findBtn = CTkButton(manageFrame, text = "FIND", width = 100, font = ("Roboto", 14), command = find)
clearBtn = CTkButton(manageFrame, text = "CLEAR", width = 100, font = ("Roboto", 14), command = clear)
exportBtn = CTkButton(manageFrame, text = "EXPORT EXCEL", width = 120, fg_color = "#127f45", hover_color = "#0e5f34", font = ("Roboto", 14), command = exportExcel)

# Padding and positioning for all MANAGE buttons
exportBtn.grid(row = 0, column = 0, padx = 5, pady = 5)
clearBtn.grid(row = 0, column = 1, padx = 5, pady = 5)
selectBtn.grid(row = 0, column = 2, padx = 5, pady = 5)
findBtn.grid(row = 0, column = 3, padx = 5, pady = 5)
updateBtn.grid(row = 0, column = 4, padx = 5, pady = 5)
deleteBtn.grid(row = 0, column = 5, padx = 5, pady = 5)
saveBtn.grid(row = 0, column = 6, padx = 5, pady = 5)

treeFrame = CTkFrame(frame)
treeFrame.grid(row = 3, column = 0, pady = [20, 105], ipadx=[6])

my_tree = ttk.Treeview(treeFrame, show = 'headings', height = 15)
style = ttk.Style()

# Function so the treeview refreshes and displays items correctly
def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)
    for array in readData():
        my_tree.insert(parent = '', index = 'end', iid = array, text = '', values = (array), tag = 'orow')
    my_tree.tag_configure('orow', background = "#353738")
    my_tree.pack()

style.configure(window)

style.theme_use('classic')
style.configure("Treeview",
    fieldbackground = "#353738",
    rowheight = 25,
    lightcolor = "#565a5f", darkcolor = "#565a5f", bordercolor = "#565a5f",
    highlightthickness = 0, borderwidth = 0, relief = 2,
    font = ("Roboto", 9),
    foreground = "#dde4ef", selected = "#17507b",
    )

style.configure("Treeview.Heading", font = ("Arial", 11),
    foreground = "#dde4ef",
    background = "#1f6ba4",
    lightcolor = "#353738", darkcolor = "#353738", bordercolor = "#353738",
    borderwidth = 0, padding = 5
    )
### style.map() ###

my_tree['columns'] = ("Item Id", "Name", "Price", "Quantity", "Category", "Date")
# List of columns in the treeview
my_tree.column("#0", width = 0, stretch = NO)
my_tree.column("Item Id", anchor = W, width = 100)
my_tree.column("Name", anchor = W, width = 175)
my_tree.column("Price", anchor = W, width = 145)
my_tree.column("Quantity", anchor = W, width = 145)
my_tree.column("Category", anchor = W, width = 145)
my_tree.column("Date", anchor = W, width = 135)
# List of headings in the treeview
my_tree.heading("Item Id", text = "Item ID", anchor = W)
my_tree.heading("Name", text = "Name", anchor = W)
my_tree.heading("Price", text = "Price", anchor = W)
my_tree.heading("Quantity", text = "Quantity", anchor = W)
my_tree.heading("Category", text = "Category", anchor = W)
my_tree.heading("Date", text = "Date", anchor = W)

my_tree.tag_configure('orow', background = "#eee")
my_tree.pack(fill = BOTH, expand = True)

refreshTable()

# Mainloop so program runs
window.resizable(False, False)
window.mainloop()