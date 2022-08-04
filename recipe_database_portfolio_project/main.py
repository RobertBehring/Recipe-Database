import tkinter.messagebox
from tkinter import *
from tkinter.tix import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import date
import sqlite3
import json
import pika
import uuid


def main():
    # ############ INITIALIZE ROOT WINDOW ########################################
    units = ['mg', 'g', 'kg', "oz", "lb", "ml", "l", "kl", "tsp", "tbsp", "fl oz",
             "c", "pt", "qt", "gal"]
    ingredients = ['all-purpose flour', 'baking powder', 'baking soda', 'bread flour', 'brown sugar', 'butter',
                   'carrots', 'celery', 'feta cheese', 'cheddar cheese', 'cherries', 'chocolate chips', 'cocoa',
                   'coconut', 'corn syrup', 'cranberries', 'cream', 'cream cheese', 'creme fraiche', 'dates',
                   'dried milk', 'potato flakes', 'large egg', 'figs', 'flax meal', 'minced garlic', 'peeled garlic',
                   'ghee', 'gluten-free all-purpose flour', 'granola', 'hazelnuts', 'honey', 'jam', 'preserves', 'lard',
                   'leeks', 'lemon juice', 'macadamia nuts', 'maple syrup', 'marshmallow spread', 'mini marshmallows',
                   'marzipan', 'masa harina', 'mascarpone cheese', 'mayonnaise', 'evaporated milk', 'milk', 'molasses',
                   'mushrooms', 'oat flour', 'old fashioned oats', 'olive oil', 'olives', 'onions',
                   'paleo baking flour', 'palm shortening', 'pastry flour', 'peaches', 'peanut butter', 'peanuts',
                   'pears', 'pecans', 'pine nuts', 'pineapple', 'pistachio nuts', 'pizza sauce', 'poppy seeds',
                   'quinoa', 'raisins', 'raspberries', 'rhubarb', 'rice', 'table salt', 'semolina flour',
                   'sesame seeds', 'sour cream', 'sourdough starter', 'steel cut oats', 'strawberries', 'white sugar',
                   'sweetened condensed milk', 'tahini', 'tapioca flour', 'tomato paste', 'turbinado sugar',
                   'vanilla extract', 'vegetable oil', 'vegetable shortening', 'walnuts', 'water', 'instant yeast',
                   'yogurt', 'zucchini']
    logo = r'.\images\favicon.ico'
    main_bg = 'white'
    main_size = '1540x1024'
    main_font = 'arial 10'
    main_font_underline = 'arial 10 underline'
    main_font_bold = 'arial 10 bold'
    modal_size = '270x300'
    root = Tk()
    root.title('Recipe Database')
    root.iconbitmap(logo)
    root.geometry(main_size)
    root.configure(bg=main_bg)
    root.state('zoomed')
    today = date.today()
    recipe_table_frame = Frame(root)

    # ############ MENUBAR #######################################################
    menubar = Menu(root)
    # Adding File Menu and commands
    file = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File', menu=file)
    file.add_command(label='My Recipes', command=None)
    file.add_command(label='History', command=None)
    file.add_separator()
    file.add_command(label='Exit', command=root.destroy)
    # Adding Edit Menu and commands
    edit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Edit', menu=edit)
    edit.add_command(label='Save Recipe', command=None)
    # Adding Help Menu
    help_ = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Help', menu=help_)
    help_.add_command(label='Help Page', command=None)
    help_.add_command(label='Tutorial', command=None)
    help_.add_separator()
    help_.add_command(label='About Recipe Ingredient Converter', command=None)

    # CLOSE ALL WINDOWS, RERUN MAIN
    def home():
        view_recipe.destroy()
        main()

    # ############ DATABASE CRUD FUNCTIONS #######################################
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()

    # RECIPES
    c.execute("""CREATE TABLE IF NOT EXISTS recipes (
            name text,
            serving_size real,
            date text        
    )""")

    # INGREDIENTS
    c.execute("""CREATE TABLE IF NOT EXISTS ingredients (
            recipe_id INTEGER,
            name TEXT,
            amount REAL,
            unit TEXT,
            CONSTRAINT fk_recipes 
                FOREIGN KEY (recipe_id) 
                REFERENCES recipes(oid)  
                ON DELETE CASCADE    
    )""")

    # CREATE
    def insert_recipe():
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        name = name_entry_add_recipe.get()
        serving_size = serving_size_entry_add_recipe.get()
        date = date_entry_add_recipe.get_date()
        name_isempty = name == ''
        name_isascii = name.isascii()
        serving_size_isempty = serving_size == ''
        try:
            float(serving_size)
            serving_size_isfloat = True
        except:
            serving_size_isfloat = False

        if name_isempty and serving_size_isempty:
            tkinter.messagebox.showerror('Error', 'Both Name and Serving Size fields are empty')
        elif name_isempty:
            tkinter.messagebox.showerror('Error', 'Name field is empty')
        elif serving_size_isempty:
            tkinter.messagebox.showerror('Error', 'Serving Size field is empty')
        elif not name_isascii and not serving_size_isfloat:
            tkinter.messagebox.showerror('Error', 'Both Name and Serving Size entries are invalid')
        elif not name_isascii:
            tkinter.messagebox.showerror('Error', 'Name entry is invalid')
        elif not serving_size_isfloat:
            tkinter.messagebox.showerror('Error', 'Serving Size entry is invalid')
        else:
            c.execute("INSERT INTO recipes VALUES (:name, :servings, :date)",
                      {
                          'name': name,
                          'servings': serving_size,
                          'date': date
                      })
            c.execute('SELECT oid, name FROM recipes')
            data = c.fetchall()
            oid = data[-1][0]
            name = data[-1][1]
            conn.commit()
            conn.close()
            add_recipe.destroy()
            view_recipe_window(oid, name)
            return

        conn.commit()
        conn.close()

        add_recipe.destroy()
        for widgets in recipe_table_frame.winfo_children():
            widgets.destroy()
        view_all_recipes_table()

    def insert_ingredient(recipe_id):
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        name = name_entry_add_ingredient.get()
        amount = amount_entry_add_ingredient.get()
        unit = unit_entry_add_ingredient.get()
        name_isempty = name == ''
        name_isascii = name.isascii()
        amount_isempty = amount == ''
        try:
            float(amount)
            amount_isfloat = True
        except:
            amount_isfloat = False
        unit_isempty = unit == ''
        unit_isascii = unit.isascii()

        if name_isempty and amount_isempty and unit_isempty:
            tkinter.messagebox.showerror('Error', 'All fields are empty')
        elif name_isempty:
            tkinter.messagebox.showerror('Error', 'Name field is empty')
        elif amount_isempty:
            tkinter.messagebox.showerror('Error', 'Amount field is empty')
        elif unit_isempty:
            tkinter.messagebox.showerror('Error', 'Unit field is empty')
        elif not name_isascii and not amount_isfloat and not unit_isascii:
            tkinter.messagebox.showerror('Error', 'All entries are invalid')
        elif not name_isascii:
            tkinter.messagebox.showerror('Error', 'Name entry is invalid')
        elif not amount_isfloat:
            tkinter.messagebox.showerror('Error', 'Amount entry is invalid')
        elif not unit_isascii:
            tkinter.messagebox.showerror('Error', 'Unit entry is invalid')
        else:
            c.execute("INSERT INTO ingredients VALUES (:recipe_id, :name, :amount, :unit)",
                      {
                          'recipe_id': recipe_id,
                          'name': name,
                          'amount': amount,
                          'unit': unit
                      })

        conn.commit()
        conn.close()

        add_ingredient.destroy()
        for widgets in ingredient_table_frame.winfo_children():
            widgets.destroy()
        view_ingredient_table(recipe_id)

    # READ
    def query_all_recipes():
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()

        c.execute("SELECT oid, * FROM recipes")
        data = c.fetchall()

        conn.commit()
        conn.close()
        return data

    def query_one_recipe(recipe_id):
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()

        c.execute("SELECT oid, * FROM recipes WHERE oid=" + str(recipe_id))
        data = c.fetchall()

        conn.commit()
        conn.close()
        return data

    def query_all_ingredients_for_recipe(oid):
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        c.execute("SELECT oid, recipe_id, name, amount, unit FROM ingredients WHERE recipe_id=" + str(oid))
        data = c.fetchall()

        conn.commit()
        conn.close()
        return data

    def query_one_ingredient(ingredient_id):
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()

        c.execute("SELECT oid, * FROM ingredients WHERE oid=" + str(ingredient_id))
        data = c.fetchall()

        conn.commit()
        conn.close()
        return data

    # UPDATE
    def update_one_recipe(recipe_id):
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        name = name_entry_edit_recipe.get()
        serving_size = serving_size_entry_edit_recipe.get()
        date = date_entry_edit_recipe.get_date()
        name_isempty = name == ''
        name_isascii = name.isascii()
        serving_size_isempty = serving_size == ''
        recipe_data = query_one_recipe(recipe_id)
        try:
            float(serving_size)
            serving_size_isfloat = True
        except:
            serving_size_isfloat = False
        if name_isempty and serving_size_isempty:
            tkinter.messagebox.showerror('Error', 'Both Name and Serving Size fields are empty')
        elif name_isempty:
            tkinter.messagebox.showerror('Error', 'Name field is empty')
        elif serving_size_isempty:
            tkinter.messagebox.showerror('Error', 'Serving Size field is empty')
        elif not name_isascii and not serving_size_isfloat:
            tkinter.messagebox.showerror('Error', 'Both Name and Serving Size entries are invalid')
        elif not name_isascii:
            tkinter.messagebox.showerror('Error', 'Name entry is invalid')
        elif not serving_size_isfloat:
            tkinter.messagebox.showerror('Error', 'Serving Size entry is invalid')
        elif serving_size != recipe_data[0][2]:
            serving_change = {"servings": [str(int(recipe_data[0][2])), serving_size]}
            rpc_servings_conversion(recipe_data, serving_change)
        else:
            c.execute("""UPDATE recipes SET 
                 name = :name,
                 serving_size = :serving_size,
                 date = :date
                 WHERE oid = :oid""",
                      {
                          "name": name,
                          "serving_size": serving_size,
                          "date": date,
                          "oid": recipe_id
                      }
                      )
            conn.commit()
            conn.close()
            edit_recipe.destroy()
            for widgets in recipe_table_frame.winfo_children():
                widgets.destroy()
            view_all_recipes_table()
            return
        conn.commit()
        conn.close()
        edit_recipe.destroy()

    def update_one_ingredient(ingredient_id, recipe_id):
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        name = name_entry_edit_ingredient.get()
        amount = amount_entry_edit_ingredient.get()
        unit = unit_entry_edit_ingredient.get()
        name_isempty = name == ''
        name_isascii = name.isascii()
        amount_isempty = amount == ''
        ingredient_data = query_one_ingredient(ingredient_id)
        recipe_data = query_one_recipe(recipe_id)
        ingredient_json = {str(recipe_data[0][1]): [
            {"ingredient": str(ingredient_data[0][2]), "quantity": str(ingredient_data[0][3]),
             "measure": str(ingredient_data[0][4]), "desired": str(unit)}]}
        try:
            float(amount)
            amount_isfloat = True
        except:
            amount_isfloat = False
        unit_isempty = unit == ''
        unit_isascii = unit.isascii()

        if name_isempty and amount_isempty and unit_isempty:
            tkinter.messagebox.showerror('Error', 'All fields are empty')
        elif name_isempty:
            tkinter.messagebox.showerror('Error', 'Name field is empty')
        elif amount_isempty:
            tkinter.messagebox.showerror('Error', 'Amount field is empty')
        elif unit_isempty:
            tkinter.messagebox.showerror('Error', 'Unit field is empty')
        elif not name_isascii and not amount_isfloat and not unit_isascii:
            tkinter.messagebox.showerror('Error', 'All entries are invalid')
        elif not name_isascii:
            tkinter.messagebox.showerror('Error', 'Name entry is invalid')
        elif not amount_isfloat:
            tkinter.messagebox.showerror('Error', 'Amount entry is invalid')
        elif not unit_isascii:
            tkinter.messagebox.showerror('Error', 'Unit entry is invalid')
        elif unit != ingredient_data[0][4] and float(amount) == ingredient_data[0][3]:
            send_ingredient_unit_conversion(ingredient_json)
            rec_ingredient_unit_conversion(recipe_data, ingredient_data)
        else:
            c.execute("""UPDATE ingredients SET 
                 name = :name,
                 amount = :amount,
                 unit = :unit
                 WHERE oid = :oid""",
                      {
                          "name": name,
                          "amount": amount,
                          "unit": unit,
                          "oid": ingredient_id
                      }
                      )
            conn.commit()
            conn.close()
            edit_ingredient.destroy()
            for widgets in ingredient_table_frame.winfo_children():
                widgets.destroy()
            view_ingredient_table(recipe_id)
            return
        conn.commit()
        conn.close()
        edit_ingredient.destroy()

    def update_many_ingredients_servings_conversion(recipe_id, ingredients):
        ingredient_data = query_all_ingredients_for_recipe(recipe_id)
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        ingredients = json.loads(ingredients)
        for i in range(1, len(ingredients)):
            name = ingredients[i]["ingredient"]
            amount = round(ingredients[i]["qty"], 2)
            unit = ingredients[i]["measure"]
            ingredient_id = ingredient_data[i - 1][0]
            c.execute("""UPDATE ingredients SET
                 name = :name,
                 amount = :amount,
                 unit = :unit
                 WHERE oid = :oid""",
                      {
                          "name": name,
                          "amount": amount,
                          "unit": unit,
                          "oid": ingredient_id
                      }
                      )
        name = name_entry_edit_recipe.get()
        serving_size = serving_size_entry_edit_recipe.get()
        date = date_entry_edit_recipe.get_date()
        c.execute("""UPDATE recipes SET 
             name = :name,
             serving_size = :serving_size,
             date = :date
             WHERE oid = :oid""",
                  {
                      "name": name,
                      "serving_size": serving_size,
                      "date": date,
                      "oid": recipe_id
                  }
                  )
        conn.commit()
        conn.close()
        for widgets in recipe_table_frame.winfo_children():
            widgets.destroy()
        view_all_recipes_table()

    # DELETE
    def delete_one_recipe(recipe_id):
        if not tkinter.messagebox.askokcancel('Delete Warning',
                                              'Deleting this entry is permanent.\nDo you want to continue?'):
            return
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        c.execute('DELETE FROM recipes WHERE oid=' + str(recipe_id))

        conn.commit()
        conn.close()
        for widgets in recipe_table_frame.winfo_children():
            widgets.destroy()
        view_all_recipes_table()

    def delete_one_ingredient(recipe_id, ingredient_id):
        conn = sqlite3.connect('recipes.db')
        if not tkinter.messagebox.askokcancel('Delete Warning',
                                              'Deleting this entry is permanent.\nDo you want to continue?'):
            return
        c = conn.cursor()
        c.execute('DELETE FROM ingredients WHERE oid=' + str(ingredient_id))

        conn.commit()
        conn.close()
        for widgets in ingredient_table_frame.winfo_children():
            widgets.destroy()
        view_ingredient_table(recipe_id)

    def search_for_recipe_by_name(name):
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        # c.execute()
        # recipe = c.fetchall()
        conn.commit()
        conn.close()
        # for widgets in recipe_table_frame.winfo_children():
        #     widgets.destroy()
        # view_all_recipes_table()
        # return recipe

    # ########### FUNCTIONS ######################################################
    class RpcClient(object):

        def __init__(self):
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))

            self.channel = self.connection.channel()

            result = self.channel.queue_declare(queue='', exclusive=True)
            self.callback_queue = result.method.queue

            self.channel.basic_consume(
                queue=self.callback_queue,
                on_message_callback=self.on_response,
                auto_ack=True)

            self.response = None
            self.corr_id = None

        def on_response(self, ch, method, props, body):
            if self.corr_id == props.correlation_id:
                self.response = body.decode('utf-8')

        def call(self, n):
            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(
                exchange='',
                routing_key='data',
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id,
                ),
                body=str(n))
            self.connection.process_data_events(time_limit=None)
            return self.response

    def send_ingredient_unit_conversion(ingredient_json):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='conversion request')

        channel.basic_publish(exchange='',
                              routing_key='conversion request',
                              body=json.dumps(ingredient_json)
                              )
        print(f" [x] Sent '{str(ingredient_json)}'")

        connection.close()

    def rec_ingredient_unit_conversion(recipe_data, ingredient_data):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='conversion delivery')

        def callback(ch, method, properties, body):
            ingredient_name = ingredient_data[0][2]
            recipe_name = recipe_data[0][1]
            ingredient_id = ingredient_data[0][0]
            recipe_id = recipe_data[0][0]
            body = body.decode('utf-8')
            print(" [x] Received %r" % body)
            conn = sqlite3.connect('recipes.db')
            c = conn.cursor()
            body = json.loads(body)
            c.execute("""UPDATE ingredients SET
                 name = :name,
                 amount = :amount,
                 unit = :unit
                 WHERE oid = :oid""",
                      {
                          "name": ingredient_name,
                          "amount": str(round(float(body[recipe_name][0]["quantity"]), 2)),
                          "unit": body[recipe_name][0]["measure"],
                          "oid": ingredient_id
                      }
                      )
            conn.commit()
            conn.close()
            for widgets in ingredient_table_frame.winfo_children():
                widgets.destroy()
            view_ingredient_table(recipe_id)
            channel.close()

        channel.basic_consume(queue='conversion delivery',
                              auto_ack=True,
                              on_message_callback=callback)

        print(' [*] rec_ingredient_unit_conversion() Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def rpc_servings_conversion(recipe_data, serving_change):
        recipe_id = recipe_data[0][0]
        ingredient_data = query_all_ingredients_for_recipe(recipe_id)
        conversion_request = [serving_change]
        for i in range(len(ingredient_data)):
            ingredient_request = {"ingredient": str(ingredient_data[i][2]), "qty": str(ingredient_data[i][3]),
                                  "measure": str(ingredient_data[i][4])}
            conversion_request.append(ingredient_request)
        conversion_request = json.dumps(conversion_request)
        rpc = RpcClient()
        data = rpc.call(conversion_request)
        update_many_ingredients_servings_conversion(recipe_id, data)

    # ########### RECIPE TABLES ##################################################
    def view_all_recipes_table():
        recipes_data = query_all_recipes()
        header = [('Recipe Number', 'Name', 'Serving Size', 'Date Added', 'View', 'Edit', 'Delete')]
        # headers
        for i in range(len(header)):
            for j in range(len(header[0])):
                e = Entry(recipe_table_frame, width=20, font=main_font_bold, border=2, cursor='arrow')
                e.grid(row=i, column=j, ipadx=10, ipady=10)
                e.insert(END, header[i][j])
                e.config(state='disabled')
        if recipes_data == []:
            no_recipes_label = Label(recipe_table_frame,
                                     text="There are no recipes in the database. \nAdd a recipe to continue",
                                     font='arial 24')
            no_recipes_label.grid(row=1, column=0, columnspan=4, padx=25, pady=25)
            return
        # recipes data
        for i in range(len(recipes_data)):
            for j in range(len(recipes_data[0])):
                e = Entry(recipe_table_frame, width=20, font=main_font, border=2, cursor='arrow')
                e.grid(row=i + 1, column=j, ipadx=10, ipady=10)
                e.insert(END, recipes_data[i][j])
                e.config(state='disabled')
            oid = recipes_data[i][0]
            name = recipes_data[i][1]
            view_button_add_recipe = Button(recipe_table_frame, text="View",
                                            command=lambda oid=oid, name=name: view_recipe_window(oid, name),
                                            fg='black', font=main_font_underline, borderwidth=5, cursor='hand2')
            edit_button_add_recipe = Button(recipe_table_frame, text="Edit",
                                            command=lambda oid=oid, name=name: edit_recipe_modal(oid, name),
                                            fg='black', font=main_font_underline, borderwidth=5, cursor='hand2')
            delete_button_add_recipe = Button(recipe_table_frame, text="Delete",
                                              command=lambda oid=oid: delete_one_recipe(oid), fg='black',
                                              font=main_font_underline, borderwidth=5, cursor='hand2')
            view_button_add_recipe.grid(row=i + 1, column=j + 1, ipadx=75, ipady=3)
            edit_button_add_recipe.grid(row=i + 1, column=j + 2, ipadx=75, ipady=3)
            delete_button_add_recipe.grid(row=i + 1, column=j + 3, ipadx=75, ipady=3)

    def view_one_recipe_table(recipe_id):
        recipe_data = query_one_recipe(recipe_id)
        header = [('Recipe Number', 'Name', 'Serving Size', 'Date Added')]
        # headers
        for i in range(len(header)):
            for j in range(len(header[0])):
                e = Entry(recipe_info_frame, width=20, font=main_font_bold, border=2, cursor='arrow')
                e.grid(row=i, column=j, ipadx=10, ipady=10)
                e.insert(END, header[i][j])
                e.config(state='disabled')
        # recipe data
        for i in range(len(recipe_data)):
            for j in range(len(recipe_data[0])):
                e = Entry(recipe_info_frame, width=20, font=main_font, border=2, cursor='arrow')
                e.grid(row=i + 1, column=j, ipadx=10, ipady=10)
                e.insert(END, recipe_data[i][j])
                e.config(state='disabled')

    def view_ingredient_table(recipe_id):
        recipe_data = query_all_ingredients_for_recipe(recipe_id)
        header = [('Name', 'Amount', 'Unit', 'Edit', 'Delete')]
        for i in range(len(header)):
            for j in range(len(header[0])):
                e = Entry(ingredient_table_frame, width=20, font=main_font_bold, border=2, cursor='arrow')
                e.grid(row=i, column=j, ipadx=10, ipady=10)
                e.insert(END, header[i][j])
                e.config(state='disabled')
        if recipe_data == []:
            no_ingredients_label = Label(ingredient_table_frame,
                                         text="There are no ingredients for this recipe. \nAdd an ingredient to continue",
                                         font='arial 24')
            no_ingredients_label.grid(row=1, column=0, columnspan=4, padx=25, pady=25)
            return

        for i in range(len(recipe_data)):
            for j in range(2, len(recipe_data[0])):
                e = Entry(ingredient_table_frame, width=20, font=main_font, border=2, cursor='arrow')
                e.grid(row=i + 1, column=j - 2, ipadx=10, ipady=10)
                e.insert(END, recipe_data[i][j])
                e.config(state='disabled')
            ingredient_id = recipe_data[i][0]
            recipe_id = recipe_data[i][1]
            edit_button_ingredient_table_frame = Button(ingredient_table_frame, text="Edit",
                                                        command=lambda ingredient_id=ingredient_id,
                                                                       recipe_id=recipe_id: edit_ingredient_modal(
                                                            ingredient_id, recipe_id),
                                                        fg='black',
                                                        font=main_font_underline, borderwidth=5, cursor='hand2')
            delete_button_ingredient_table_frame = Button(ingredient_table_frame, text="Delete",
                                                          command=lambda ingredient_id=ingredient_id,
                                                                         recipe_id=recipe_id: delete_one_ingredient(
                                                              recipe_id, ingredient_id), fg='black',
                                                          font=main_font_underline, borderwidth=5, cursor='hand2')
            edit_button_ingredient_table_frame.grid(row=i + 1, column=j - 1, ipadx=75, ipady=3)
            delete_button_ingredient_table_frame.grid(row=i + 1, column=j, ipadx=75, ipady=3)

    # ############ WINDOWS #######################################################
    def view_recipe_window(recipe_id, name):
        root.destroy()
        global view_recipe
        view_recipe = Tk()
        view_recipe.title(f'Viewing Recipe: {name}')
        view_recipe.geometry(main_size)
        view_recipe.iconbitmap(logo)
        view_recipe.configure(bg=main_bg)
        view_recipe.state('zoomed')
        global recipe_info_frame
        global ingredient_table_frame
        recipe_info_frame = Frame(view_recipe)
        ingredient_table_frame = Frame(view_recipe)
        view_one_recipe_table(recipe_id)
        view_ingredient_table(recipe_id)

        add_ingredient_button_view_recipe = Button(view_recipe, text="Add \nIngredient",
                                                   command=lambda: add_ingredient_modal(recipe_id),
                                                   font='arial 16 bold', bg='red', fg='white', borderwidth=7,
                                                   cursor='hand2')
        return_button_view_recipe = Button(view_recipe, text='Return \n to Recipes', command=home, font='arial 16 bold',
                                           bg='dark green', fg='white', borderwidth=7, cursor='hand2')

        recipe_info_frame.grid(row=0, column=0, columnspan=4, padx=(25, 50), pady=25, sticky='w')
        return_button_view_recipe.grid(row=0, column=5, rowspan=2, columnspan=2, pady=25, ipadx=20, ipady=20,
                                       sticky='n')
        ingredient_table_frame.grid(row=1, column=0, columnspan=5, padx=(25, 50), pady=25, sticky='w')
        add_ingredient_button_view_recipe.grid(row=1, column=5, rowspan=2, columnspan=2, pady=25, ipadx=27, ipady=20,
                                               sticky='n')

    # ############ MODAL WINDOWS #################################################
    def edit_recipe_modal(recipe_id, name):
        global edit_recipe
        edit_recipe = Tk()
        edit_recipe.title('Editing: ' + name)
        edit_recipe.geometry(modal_size)
        edit_recipe.iconbitmap(logo)
        edit_recipe.configure(bg=main_bg)
        recipe_data = query_one_recipe(recipe_id)
        date = recipe_data[0][3].split('/')

        global name_entry_edit_recipe
        global serving_size_entry_edit_recipe
        global date_entry_edit_recipe
        name_label_edit_recipe = Label(edit_recipe, text='Name', bg=main_bg)
        name_entry_edit_recipe = Entry(edit_recipe, width=30)
        name_entry_edit_recipe.insert(0, recipe_data[0][1])
        serving_size_label_edit_recipe = Label(edit_recipe, text='Serving Size', bg=main_bg)
        serving_size_entry_edit_recipe = Entry(edit_recipe, width=30)
        serving_size_entry_edit_recipe.insert(0, recipe_data[0][2])
        date_label_edit_recipe = Label(edit_recipe, text='Date', bg=main_bg)
        date_entry_edit_recipe = Calendar(edit_recipe, selectmode='day',
                                          year=int(date[2]), month=int(date[0]),
                                          day=int(date[1]))

        edit_recipe_button = Button(edit_recipe, text='Confirm', command=lambda: update_one_recipe(recipe_id), border=3,
                                    cursor='hand2')

        name_label_edit_recipe.grid(row=0, column=0, sticky='w', padx=5)
        name_entry_edit_recipe.grid(row=0, column=1)
        serving_size_label_edit_recipe.grid(row=1, column=0, sticky='w', padx=5)
        serving_size_entry_edit_recipe.grid(row=1, column=1)
        date_label_edit_recipe.grid(row=2, column=0, columnspan=2)
        date_entry_edit_recipe.grid(row=3, column=0, columnspan=2, padx=10)
        edit_recipe_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, ipadx=50)

    def add_ingredient_modal(recipe_id):
        def checkkey(event):
            value = event.widget.get()
            if value == '':
                data = ingredients
            else:
                data = []
                for item in ingredients:
                    if value.lower() in item.lower():
                        data.append(item)
            update(data)

        def update(data):
            name_entry_listbox_add_ingredient.delete(0, 'end')
            for item in data:
                name_entry_listbox_add_ingredient.insert('end', item)

        def items_selected(event):
            # get selected indices
            selected_indices = name_entry_listbox_add_ingredient.curselection()
            # get selected items
            selected_langs = ",".join([name_entry_listbox_add_ingredient.get(i) for i in selected_indices])
            name_entry_add_ingredient.delete(0, 'end')
            name_entry_add_ingredient.insert('end', selected_langs)

        global add_ingredient
        add_ingredient = Tk()
        add_ingredient.title('Add Ingredient')
        add_ingredient.geometry('583x225')
        add_ingredient.iconbitmap(logo)
        add_ingredient.configure(bg=main_bg)

        global name_entry_add_ingredient
        global amount_entry_add_ingredient
        global unit_entry_add_ingredient
        name_label_add_ingredient = Label(add_ingredient, text='Name', bg=main_bg)
        name_entry_add_ingredient = Entry(add_ingredient, width=30)
        name_entry_listbox_add_ingredient = Listbox(add_ingredient, width=30)
        amount_label_add_ingredient = Label(add_ingredient, text='Amount', bg=main_bg)
        amount_entry_add_ingredient = Entry(add_ingredient, width=30)
        unit_label_add_ingredient = Label(add_ingredient, text='Unit of Measurement', bg=main_bg)
        unit_entry_add_ingredient = ttk.Combobox(add_ingredient, width=27)
        unit_entry_add_ingredient['values'] = units

        add_ingredient_button = Button(add_ingredient, text='Add', command=lambda: insert_ingredient(recipe_id),
                                       border=3, cursor='hand2')

        name_label_add_ingredient.grid(row=0, column=0, sticky='w', padx=5)
        name_entry_add_ingredient.grid(row=1, column=0, padx=5)
        name_entry_add_ingredient.bind('<KeyRelease>', checkkey)
        name_entry_listbox_add_ingredient.grid(row=2, column=0, rowspan=3, padx=5)
        name_entry_listbox_add_ingredient.bind('<<ListboxSelect>>', items_selected)
        update(ingredients)
        amount_label_add_ingredient.grid(row=0, column=1, sticky='w', padx=5)
        amount_entry_add_ingredient.grid(row=1, column=1, padx=5)
        unit_label_add_ingredient.grid(row=0, column=2, sticky='w', padx=5)
        unit_entry_add_ingredient.grid(row=1, column=2, padx=5)
        unit_entry_add_ingredient.current(0)
        add_ingredient_button.grid(row=3, column=2, columnspan=2, padx=10, pady=10, ipadx=50, sticky='s')

    def edit_ingredient_modal(ingredient_id, recipe_id):
        def checkkey(event):
            value = event.widget.get()
            if value == '':
                data = ingredients
            else:
                data = []
                for item in ingredients:
                    if value.lower() in item.lower():
                        data.append(item)
            update(data)

        def update(data):
            name_entry_listbox_edit_ingredient.delete(0, 'end')
            for item in data:
                name_entry_listbox_edit_ingredient.insert('end', item)

        def items_selected(event):
            # get selected indices
            selected_indices = name_entry_listbox_edit_ingredient.curselection()
            # get selected items
            selected_langs = ",".join([name_entry_listbox_edit_ingredient.get(i) for i in selected_indices])
            name_entry_edit_ingredient.delete(0, 'end')
            name_entry_edit_ingredient.insert('end', selected_langs)

        global edit_ingredient
        edit_ingredient = Tk()
        edit_ingredient.title('Add Ingredient')
        edit_ingredient.geometry('583x225')
        edit_ingredient.iconbitmap(logo)
        edit_ingredient.configure(bg=main_bg)
        ingredient_data = query_one_ingredient(ingredient_id)

        global name_entry_edit_ingredient
        global amount_entry_edit_ingredient
        global unit_entry_edit_ingredient
        name_label_edit_ingredient = Label(edit_ingredient, text='Name', bg=main_bg)
        name_entry_edit_ingredient = Entry(edit_ingredient, width=30)
        name_entry_edit_ingredient.insert(0, ingredient_data[0][2])
        name_entry_listbox_edit_ingredient = Listbox(edit_ingredient, width=30)
        amount_label_edit_ingredient = Label(edit_ingredient, text='Amount', bg=main_bg)
        amount_entry_edit_ingredient = Entry(edit_ingredient, width=30)
        amount_entry_edit_ingredient.insert(0, ingredient_data[0][3])
        unit_label_edit_ingredient = Label(edit_ingredient, text='Unit of Measurement', bg=main_bg)
        unit_entry_edit_ingredient = ttk.Combobox(edit_ingredient, width=27)
        unit_entry_edit_ingredient['values'] = units
        unit_index = units.index(ingredient_data[0][4])
        unit_entry_edit_ingredient.current(unit_index)

        edit_ingredient_button = Button(edit_ingredient, text='Confirm',
                                        command=lambda: update_one_ingredient(ingredient_id, recipe_id),
                                        border=3, cursor='hand2')

        name_label_edit_ingredient.grid(row=0, column=0, sticky='w', padx=5)
        name_entry_edit_ingredient.grid(row=1, column=0, padx=5)
        name_entry_edit_ingredient.bind('<KeyRelease>', checkkey)
        name_entry_listbox_edit_ingredient.grid(row=2, column=0, rowspan=3, padx=5)
        name_entry_listbox_edit_ingredient.bind('<<ListboxSelect>>', items_selected)
        update(ingredients)
        amount_label_edit_ingredient.grid(row=0, column=1, sticky='w', padx=5)
        amount_entry_edit_ingredient.grid(row=1, column=1, padx=5)
        unit_label_edit_ingredient.grid(row=0, column=2, sticky='w', padx=5)
        unit_entry_edit_ingredient.grid(row=1, column=2, padx=5)
        edit_ingredient_button.grid(row=3, column=2, columnspan=2, padx=10, pady=10, ipadx=50, sticky='s')

    def add_recipe_modal():
        global add_recipe
        add_recipe = Tk()
        add_recipe.title('Add a Recipe')
        add_recipe.geometry(modal_size)
        add_recipe.iconbitmap(logo)
        add_recipe.configure(bg=main_bg)
        year, month, day = today.strftime('%y'), today.strftime('%m'), today.strftime('%d')

        global name_entry_add_recipe
        global serving_size_entry_add_recipe
        global date_entry_add_recipe
        name_label_add_recipe = Label(add_recipe, text='Name', bg=main_bg)
        name_entry_add_recipe = Entry(add_recipe, width=30)
        serving_size_label_add_recipe = Label(add_recipe, text='Serving Size', bg=main_bg)
        serving_size_entry_add_recipe = Entry(add_recipe, width=30)
        date_label_add_recipe = Label(add_recipe, text='Date', bg=main_bg)
        date_entry_add_recipe = Calendar(add_recipe, selectmode='day',
                                         year=int(year), month=int(month),
                                         day=int(day))

        add_recipe_button = Button(add_recipe, text='Add', command=insert_recipe, border=3, cursor='hand2')

        name_label_add_recipe.grid(row=0, column=0, sticky='w', padx=5)
        name_entry_add_recipe.grid(row=0, column=1)
        serving_size_label_add_recipe.grid(row=1, column=0, sticky='w', padx=5)
        serving_size_entry_add_recipe.grid(row=1, column=1)
        date_label_add_recipe.grid(row=2, column=0, columnspan=2)
        date_entry_add_recipe.grid(row=3, column=0, columnspan=2, padx=10)
        add_recipe_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, ipadx=50)

    # ENTRY :: ROOT
    search_bar = Entry(root, text="Search by Recipe Name", width=30)

    # BUTTONS :: ROOT
    add_recipe_button = Button(root, text="Add \nRecipe", command=add_recipe_modal, font='arial 16 bold', bg='red',
                               fg='white', borderwidth=7, cursor='hand2')
    search_bar_button = Button(root, text="Search", command=lambda : search_for_recipe_by_name(search_bar.get()))

    # POSITIONING :: ROOT
    div = Label(bg=main_bg, fg=main_bg)
    div.grid(row=0,column=0, columnspan=5)
    search_bar.grid(row=1, column=0, sticky='w', padx=25)
    search_bar_button.grid(row=2, column=0, columnspan=5, sticky='w', padx=25)
    recipe_table_frame.grid(row=3, column=0, columnspan=5, padx=(15, 50), pady=25)
    add_recipe_button.grid(row=1, rowspan=4, column=7, columnspan=2, pady=25, ipadx=20, ipady=20, sticky='n')

    view_all_recipes_table()
    root.config(menu=menubar)
    conn.commit()
    conn.close()

    root.mainloop()


if __name__ == '__main__':
    main()
