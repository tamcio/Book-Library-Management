from tkinter import *
from tkinter import ttk
import requests
from api import app
from client import client

def server_function():
    app.run()

def interface_function():
    root = Tk()
    #root2.geometry("400x400")
    root.title('Interfejs')
    root.title('Tabela ksiazek')
    root.geometry("300x100")
    def on_button_click2():
        root2 = Tk()

        tree = ttk.Treeview(root2)
        tree['columns'] = ("ID", "Tytul", "Autor", "Rok wydania")
        tree.column("#0", width=0)
        tree.column("ID", anchor=W,width=10)
        tree.column("Tytul",width=100)
        tree.column("Autor", width = 100)
        tree.column("Rok wydania", width = 10)
        tree.heading("#0",text="")
        tree.heading("ID",text="ID")
        tree.heading("Tytul",text="Tytul")
        tree.heading("Autor",text="Autor")
        tree.heading("Rok wydania",text="Rok wydania")
        #tree.configure(width=400)
        res = requests.get("http://127.0.0.1:5000/books").json()
        for element in res:
            tree.insert(parent="",index='end',values=tuple(element))

        tree.pack(pady=10,fill='both')
        frame = Frame(root2)
        frame.pack(pady=20,fill='both')

        label1 = Label(frame,text="ID")
        label1.grid(row=1, column=0)

        label2 = Label(frame, text="Tytul")
        label2.grid(row=0, column=1)

        label3 = Label(frame, text="Autor")
        label3.grid(row=0, column=2)

        label4 = Label(frame, text="Rok wydania")
        label4.grid(row=0, column=3)

        id_box = Entry(frame)
        id_box.grid(row=2, column=0)

        title_box = Entry(frame)
        title_box.grid(row=1, column=1)

        author_box = Entry(frame)
        author_box.grid(row=1, column=2)

        year_box = Entry(frame)
        year_box.grid(row=1, column=3)

        def remove1():
            client.delete_book(id_box.get())
            id_box.delete(0, END)

        def add_record():
            client.add_book({'title': title_box.get(), 'year': year_box.get(), 'author': author_box.get()})
            # tree.insert("", "end", values=("",title_box.get(), year_box.get(), author_box.get()))
            title_box.delete(0, END)
            year_box.delete(0, END)
            author_box.delete(0, END)

        def select_record():
            id_box.delete(0,END)
            title_box.delete(0, END)
            year_box.delete(0, END)
            author_box.delete(0, END)

            selected = tree.focus()
            values = tree.item(selected,'values')
            id_box.insert(0,values[0])
            title_box.insert(0, values[1])
            author_box.insert(0, values[2])
            year_box.insert(0, values[3])


        def update_record():
            selected = tree.focus()
            client.update_book(id_box.get(),{'title': title_box.get(), 'year': year_box.get(), 'author': author_box.get()})

            id_box.delete(0,END)
            title_box.delete(0, END)
            year_box.delete(0, END)
            author_box.delete(0, END)

        def show_record():
            label=Label(frame,text="")
            label.grid(row=2)
            selected = tree.focus()
            values = tree.item(selected, 'values')
            label = Label(frame,text = f'ID Ksiazki: {values[0]}, Ksiazka pod tytulem {values[1]} napisana przez {values[2]}, wydana w roku {values[3]}')
            label.grid(row=2)

        show = Button(root2, text="Pokaz informacje o wybranym rekordzie", command=show_record)
        show.pack(pady=10)

        record = Button(root2,text="Dodaj rekord",command=add_record)
        record.pack(pady=10)

        remove_one = Button(root2,text="Usun rekord o wpisanym ID", command=remove1)
        remove_one.pack(pady=10)

        select_button = Button(root2,text="Wybierz rekod", command = select_record)
        select_button.pack(pady=10)

        update_button = Button(root2,text="Zapisz zmiany", command = update_record)
        update_button.pack(pady=10)
        root2.mainloop()


    button_show = Button(root, text="Pokaz cala tabele", command=on_button_click2)
    button_show.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=140)
    button_show.pack()
    root.mainloop()

