from tkinter import *
from tkinter.tix import *
from tkinter import ttk
from tkinter import messagebox

root = Tk()
root.title("Recipe Ingredient Converter")
root.iconbitmap(r'.\images\favicon.ico')
root.geometry('625x325')
root.eval('tk::PlaceWindow . center')
root.configure(bg="light grey")


def convert():
    ingredient = ingredient_combobox.get()
    amount = amount_entry.get()
    unit = unit_combobox.get()
    convert_unit = unit_combobox2.get()
    result_text.delete("1.0", END)
    result_text.insert(END, ingredient + ": " + amount + unit + " -->" + convert_unit)


def clear_text():
    result_text.delete("1.0", END)


def delete_row():
    messagebox.askquestion("Delete Row", "Are you sure?")


def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()


m = Menu(root, tearoff=0)
m.add_command(label="Convert", command=convert)
m.add_separator()
m.add_command(label="Clear", command=clear_text)

menubar = Menu(root)

# Adding File Menu and commands
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Profile', menu=file)
file.add_command(label='My Recipes', command=None)
file.add_command(label='History', command=None)
file.add_separator()
file.add_command(label='Exit', command=root.destroy)

# Adding Edit Menu and commands
edit = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=edit)
edit.add_command(label='Save Recipe', command=None)

run = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Run', menu=run)
run.add_command(label='Convert', command=convert)
run.add_command(label='Clear Conversion', command=clear_text)

# Adding Help Menu
help_ = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=help_)
help_.add_command(label='Help Page', command=None)
help_.add_command(label='Tutorial', command=None)
help_.add_separator()
help_.add_command(label='About Recipe Ingredient Converter', command=None)

root.config(menu=menubar)

add_button = Button(root, text="Add Ingredient")
delete_row_button = Button(root, text="-", command=delete_row, padx=5)

# drop down menu
comboEntry = StringVar()
ingredient_combobox = ttk.Combobox(root, width=27, textvariable=comboEntry)
ingredient_combobox['values'] = (' AP Flour',
                                 ' Wheat Flour',
                                 ' Salt',
                                 ' Sugar',
                                 ' Honey',
                                 ' Agave Syrup',
                                 ' Baking Soda',
                                 ' Baking Powder',
                                 ' Brown Sugar',
                                 ' Powdered Sugar',
                                 ' Buckwheat Flour',
                                 ' Rolled Oats')

ingredient_combobox.current()
ingredient_combobox.insert(0, "Choose an ingredient")

amount_entry = Entry(root, width=27, borderwidth=2)
amount_entry.insert(0, "Enter an amount")

unit_combobox = ttk.Combobox(root, width=10, textvariable=StringVar())
unit_combobox['values'] = (' lb',
                           ' oz',
                           ' Cup',
                           ' Gallon',
                           ' Quart',
                           ' Pint',
                           ' teaspoon',
                           ' tablespoons'
                           )

unit_combobox.current()
unit_combobox.insert(0, "Unit")

separator_label = Label(root, text="      |      ", bg="light grey")

unit_combobox2 = ttk.Combobox(root, width=10, textvariable=StringVar())
unit_combobox2['values'] = (' lb',
                            ' oz',
                            ' Cup',
                            ' Gallon',
                            ' Quart',
                            ' Pint',
                            ' teaspoon',
                            ' tablespoons'
                            )

unit_combobox2.current()
unit_combobox2.insert(0, "Unit")

title = Label(root, text="Recipe Ingredient Converter", font=('arial bold', 25), height=1, bg="light grey")
your_ingredients_label = Label(root, text="Your Ingredients", font='arial 15 underline', bg="light grey", height=2)
convert_to_label = Label(root, text="Convert to", font='arial 15 underline', bg="light grey")
convert_button = Button(root, text="Convert", command=convert)
clear_button = Button(root, text="Clear", command=clear_text)
result_text = Text(root, height=5, width=60, borderwidth=5)
result_text.bind('<Button-3>', do_popup)

#Create a tooltip
convert_tip= Balloon(root)
convert_tip.bind_widget(convert_button, balloonmsg="Click to convert")
ingredient_tip = Balloon(root)
ingredient_tip.bind_widget(ingredient_combobox, balloonmsg="Click on the dropdown to see a list of ingredients")
unit_tip = Balloon(root)
unit_tip.bind_widget(unit_combobox, balloonmsg="Click on the dropdown to see available units of measurement")
unit_tip.bind_widget(unit_combobox2, balloonmsg="Click on the dropdown to see available units of measurement")
amount_tip = Balloon(root)
amount_tip.bind_widget(amount_entry, balloonmsg="Enter the amount for the selected ingredient")
delete_row_tip = Balloon(root)
delete_row_tip.bind_widget(delete_row_button, balloonmsg="Click to delete this row")
add_ingredient_row_tip = Balloon(root)
add_ingredient_row_tip.bind_widget(add_button, balloonmsg="Click to add another ingredient")
clear_button_tip = Balloon(root)
clear_button_tip.bind_widget(clear_button, balloonmsg="Click to clear the last conversion")

title.grid(row=0, column=0, columnspan=6)
your_ingredients_label.grid(row=1, column=1, columnspan=2, sticky=W)
convert_to_label.grid(row=1, column=5, columnspan=2, sticky=W)

delete_row_button.grid(row=2, column=0)
ingredient_combobox.grid(row=2, column=1)
amount_entry.grid(row=2, column=2)
unit_combobox.grid(row=2, column=3)
separator_label.grid(row=2, column=4)
unit_combobox2.grid(row=2, column=5)

add_button.grid(row=3, column=1, sticky=W)

convert_button.grid(row=4, columnspan=6, sticky=S)

result_text.grid(row=5, columnspan=6)

clear_button.grid(row=6, column=1, columnspan=5, sticky=E, padx=50)

messagebox.askquestion("New User",
                       "Would you like a step-by-step tutorial to learn how to convert recipes with the Recipe "
                       "Ingredient Converter\u00a9? (~5min)")

root.mainloop()
