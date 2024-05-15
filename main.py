import sqlite3
import csv
from tkinter import *
from tkinter import messagebox
from tkinter import Button


# Lager en database tilkobling
conn = sqlite3.connect('kundeDatabase.db')

# lager en cursor
c = conn.cursor()

# Lager en sql table
c.execute("""CREATE TABLE IF NOT EXISTS Kunder (
            kundenummer integer,
            fname text,
            ename text,
            epost text,
            tlf text,
            postnummer text,
            poststed text
            )""")

# lagrer endringer
conn.commit()

# laster postnummer og poststeder i fra csv
postnummer_csv = {}
with open('postnummer.csv', 'r') as f:
    reader = csv.reader(f, delimiter=';')
    next(reader)  # hopper over øverste rad
    for row in reader:
        if len(row) >= 2:
            postnummer_csv[row[0]] = row[1]

def Lastkunder():
    with open('kunder.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  # skip the header row
        for row in reader:
            if len(row) >= 5:
                kundenummer, fname, ename, epost, tlf, postnummer = row
                poststed = postnummer_csv.get(postnummer, "")
                
                # Sjekker om kunden finnes i databasen
                c.execute("SELECT * FROM Kunder WHERE kundenummer = :kundenummer", {'kundenummer': kundenummer})
                if c.fetchone() is None:
                    # Hvis kunden ikke finnes i databasen så blir den lagt til
                    c.execute("INSERT INTO Kunder (kundenummer, fname, ename, epost, tlf, postnummer, poststed) VALUES (:kundenummer, :fname, :ename, :epost, :tlf, :postnummer, :poststed)",
                              {
                                  'kundenummer': kundenummer,
                                  'fname': fname,
                                  'ename': ename,
                                  'epost': epost,
                                  'tlf': tlf,
                                  'postnummer': postnummer,
                                  'poststed': poststed
                              })
                    conn.commit()

Lastkunder()
# Definer funksjoner for databasehåndtering
def LeggTilKunder():
    if postnummer.get() in postnummer and postnummer[postnummer.get()] == poststed.get():
        c.execute("INSERT INTO Kunder Verdier (:kundenummer, :fname, :ename, :epost, :tlf, :postnummer, :poststed)",
                  {
                      'kundenummer': kundenummer.get(),
                      'fname': fname.get(),
                      'ename': ename.get(),
                      'epost': epost.get(),
                      'tlf': tlf.get(),
                      'postnummer': postnummer.get(),
                      'poststed': poststed.get()
                  })
        conn.commit()
    else:
        messagebox.showerror("Error", "Dette postnummeret eller poststedet er ikke gyldig")

def SlettKunder():
    c.execute("SELECT * FROM Kunder WHERE kundenummer=?", (delete_box.get(),))
    if c.fetchone() is not None:
        c.execute("DELETE from Kunder WHERE kundenummer=?", (delete_box.get(),))
        messagebox.showinfo("Velykket", "Kunden er slettet")
    else:
        messagebox.showerror("Error", "Denne kunden er ikke funnet")
    delete_box.delete(0, END)
    conn.commit()

def query():
    c.execute("SELECT *, oid FROM Kunder WHERE kundenummer=? OR fname=? OR ename=? OR epost=? OR tlf=?", 
              (search_box.get(), search_box.get(), search_box.get(), search_box.get()))
    records = c.fetchall()
    if records:
        print_records = ''
        for record in records:
            print_records += str(record) + "\n"
        query_label = Label(root, text=print_records)
        query_label.grid(row=12, column=0, columnspan=2)
    else:
        messagebox.showerror("Error", "Denne kunden er ikke funnet")
    conn.commit()
    conn.close()

# Lag GUI med Tkinter
root = Tk()
root.title('Kunde Database')

# Lag tekst boks
kundenummer = Entry(root, width=30)
kundenummer.grid(row=0, column=1, padx=20)
fname = Entry(root, width=30)
fname.grid(row=1, column=1)
ename = Entry(root, width=30)
ename.grid(row=2, column=1)
epost = Entry(root, width=30)
epost.grid(row=3, column=1)
tlf = Entry(root, width=30)
tlf.grid(row=4, column=1)
postnummer = Entry(root, width=30)
postnummer.grid(row=5, column=1)
poststed = Entry(root, width=30)
poststed.grid(row=6, column=1)

delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)

search_box = Entry(root, width=30)
search_box.grid(row=11, column=1, pady=5)

# Lag tekst box bakgrunnstekst
kundenummer_label = Label(root, text="Kundenummer")
kundenummer_label.grid(row=0, column=0)
fname_label = Label(root, text="Fornavn")
fname_label.grid(row=1, column=0)
ename_label = Label(root, text="Etternavn")
ename_label.grid(row=2, column=0)
epost_label = Label(root, text="Epost")
epost_label.grid(row=3, column=0)
tlf_label = Label(root, text="Telefonnummer")
tlf_label.grid(row=4, column=0)
postnummer_label = Label(root, text="Postnummer")
postnummer_label.grid(row=5, column=0)
poststed = Label(root, text="Poststed")
poststed.grid(row=6, column=0)

delete_box_label = Label(root, text="Slett kunde")
delete_box_label.grid(row=9, column=0)

search_box_label = Label(root, text="Søk etter kunde")
search_box_label.grid(row=11, column=0)

# Lag en submit knapp
submit_btn = Button(root, text="Legg kunde til i databasen", command=LeggTilKunder)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Lag en delete knapp
delete_btn = Button(root, text="Slett kunde", command=SlettKunder)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=136)

# lag en query knapp
query_btn = Button(root, text="Søk etter kunde", command=query)
query_btn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=143)

root.mainloop()
