from tkinter import *
from tkinter.messagebox import *
from tkinter import font
import sqlite3

root = Tk()  # main root window
con = sqlite3.Connection('phonebook.db')  # connection with database
cur = con.cursor()
cur.execute("PRAGMA foreign_keys=ON")  # creating tables
cur.execute("create table if not exists contact(contactid integer primary key autoincrement,name varchar(15), "
            "phno number(10), emailid varchar(15))")

photo = PhotoImage(file="phonebook.gif")
photoimage = photo.subsample(5, 5)
Label(root, text='', image=photoimage).grid(row=0, column=0)
root.title('Phonebook')
Label(root, text='Phonebook', relief='ridge', font='times 30 bold italic', bg='gold').grid(row=0,
                                                                                           column=2)  # gui design
Label(root, text='Name', font='times 10').grid(row=2, column=0)
e1 = Entry(root)
e1.grid(row=2, column=2)
Label(root, text='Phone Number', font='times 10').grid(row=12, column=0)
e2 = Entry(root)
e2.grid(row=12, column=2)
Label(root, text='Email ID', font='times 10').grid(row=14, column=0)
e3 = Entry(root)
e3.grid(row=14, column=2)


def new():  # function to save contact into database
    if len(e1.get()) == 0 and len(e2.get()) == 0 and len(e3.get()) == 0:
        showerror("Wrong Info !!", "Every entry cannot be Empty")
    else:
        cur.execute("insert into contact(name, phno, emailid) values(?,?,?)", (e1.get(), e2.get(), e3.get()))
        cur.execute("select contactid curval from contact")
        con.commit()
        showinfo("Save Contact", "Contact successfully saved !!")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)

def search_sort():  # searching a contact
    root3 = Tk()
    root3.title('Search')
    root3.geometry('550x700')
    Label(root3, text='Enter name to search:').grid(row=1, column=0, columnspan=5, sticky=W)
    g = Entry(root3)
    g.grid(row=1, column=0)
    fon = font.Font(size=10)
    Lb = Listbox(root3, height='30', width='90', font=fon)
    Lb.grid()
    cur.execute("select contactid,name,phno,emailid from contact")
    s = cur.fetchall()
    global az
    az = s

    def showval(e=1):  # to search the contact whena character is typed
        Lb.delete(0, END)
        cur.execute("select contactid, name, phno, emailid from contact where (name like (?)) order by name", ('%'+g.get()+'%',))
        global az
        az = cur.fetchall()
        for i in range(len(az)):
            Lb.insert(i, az[i][1])

    def fun(e=1):  # displaying the selected contact from database
        def delete_fun():
            cur.execute('delete from contact where contactid=?', (iq,))
            con.commit()
            showinfo('Delete', 'Contact Removed Successfully !!')
            close_()

        Button(root3, text='Delete', command=delete_fun).grid(row=4, column=0)
        temp = Lb.curselection()
        iq = az[temp[0]][0]
        cur.execute("select name, phno, emailid from contact where contactid=?", (iq,))
        li2 = cur.fetchall()
        Lb.delete(0, END)
        Lb.insert(0, "Name     :  " + (str)(li2[0][0]))
        Lb.insert(1,  "Phone   : " + (str)(li2[0][1]))
        Lb.insert(2, "Email Address   : " + (str)(li2[0][2]))
    cur.execute('select contactid curval from contact')
    q = cur.fetchall()
    l = len(q)
    for i in range(l):  # loop to print all the contacts in the listbox
        cur.execute("select name from contact  where contactid=? order by name", (q[i][0],))
        s = cur.fetchall()
        if s[0][0] != '':
            Lb.insert(i, s[0])

    Lb.bind("<Double-Button-1>", fun)
    g.bind("<KeyRelease>", showval)

    def close_(e=1):
        root3.destroy()

    Button(root3, text='Close', command=close_).grid(row=3, column=0)
    root3.mainloop()


Button(root, text='Save', command=new).grid(row=17, column=0)
Button(root, text='Search', command=search_sort).grid(row=17, column=1)


def close_main(e=1):
    root.destroy()


Button(root, text='Close', command=close_main).grid(row=17, column=2)


def edit():  # function to edit the saved contacts
    root4 = Tk()
    root4.title('Search a contact to edit')
    root4.geometry('550x700')
    Label(root4, text='Enter name to search and edit:').grid(row=1, column=0, columnspan=5, sticky=W)
    g = Entry(root4)
    g.grid(row=1, column=0)
    fon = font.Font(size=10)
    Lb1 = Listbox(root4, height='30', width='90', font=fon)
    Lb1.grid()
    cur.execute("select contactid,name,phno,emailid from contact")
    s = cur.fetchall()
    global az
    az = s

    def showval1(e=1):
        Lb1.delete(0, END)
        cur.execute("select contactid,name from contact where (name like (?)) order by name", ('%' + g.get() + '%',))
        global az
        az = cur.fetchall()
        for i in range(len(az)):
            Lb1.insert(i, az[i][1])

    cur.execute('select contactid curval from contact')
    q = cur.fetchall()
    l = len(q)
    for i in range(l):
        cur.execute("select name from contact  where contactid=? order by name", (q[i][0],))
        s = cur.fetchall()
        if s[0][0] != '':
            Lb1.insert(i, s[0])

    def new_window(e=1):  # edit window
        root5 = Tk()
        root5.title('Edit Window')
        Label(root5, text='Edit Contact', relief='ridge', font='times 30 bold italic', bg='gold').grid(row=0, column=2)
        Label(root5, text='Name', font='times 10').grid(row=2, column=0)
        e1 = Entry(root5)
        e1.grid(row=2, column=2)
        Label(root5, text='Phone number', font='times 10').grid(row=12, column=0)
        e2 = Entry(root5)
        e2.grid(row=12, column=2)
        Label(root5, text='Email ID', font='times 10').grid(row=14, column=0)
        e3 = Entry(root5)
        e3.grid(row=14, column=2)
        temp = Lb1.curselection()
        iq = az[temp[0]][0]
        cur.execute("select name,phno,emailid from contact where contactid=?", (iq,))
        li2 = cur.fetchall()
        e1.insert(0, (li2[0][0]))
        e2.insert(0, (li2[0][1]))
        e3.insert(0, (li2[0][2]))

        def fillup():  # refilling the selected contact into the entry box
            fn = e1.get()
            pn = e2.get()
            em = e3.get()
            iq = az[temp[0]][0]
            cur.execute("update contact set name=(?) where contactid=(?)", (fn, iq))
            cur.execute("update contact set phno=(?) where contactid=(?)", (pn, iq))
            cur.execute("update contact set emailid=(?) where contactid=(?)", (em, iq))
            con.commit()
            showinfo('Update Details', "Contact updated Successfully !!")

        Button(root5, text='Save', command=fillup).grid(row=15, column=2)

    Lb1.bind("<Double-Button-1>", new_window)
    g.bind("<KeyRelease>", showval1)

    def close_1(e=1):
        root4.destroy()

    Button(root4, text='Close', command=close_1).grid(row=3, column=0)
    root4.mainloop()


Button(root, text='Edit', command=edit).grid(row=17, column=3)
root.mainloop()
