import tkinter as tk
import tkinter.font as tkFont
from source import utils as ut
from source import train as tr
import nltk
from source.utils import frase_corretta,predici, mostra_grafico,esistone_nuove_parole,leggi_nuove_parole,salva_nuova_frase

def elaboraFrase(modello):
   frase_default= entry.get()
   frase,frase_tokenizzata = frase_corretta(frase_default)
   for i in range(len(frase)):
       frase_default = frase_default.lower().replace(frase_tokenizzata[i],frase[i])
   entry.delete(0,tk.END)
   entry.insert(0,frase_default)

   button = []

   for testo in lower_frame.winfo_children():
       testo.destroy()
   for button in lower_frame.winfo_children():
           button.destroy()

   c=0
   scrivi = False
   for i in range(len(frase)):
        parola = frase[i]
        sinonimi,presente = predici(modello,parola)
        button.append([])
        if presente:
            if(i>8):
                c=5
            if(len(frase )<= 5):

              for j in range(5):
                  button[i].append(tk.Button(lower_frame, text=sinonimi[j], font=fontStyle, command=lambda i=i,j=j,sinonimi=sinonimi: cambiaParola(frase,i,sinonimi[j])))

              testo = tk.Label(lower_frame, font=fontStyle, text=parola)
              testo.grid(row=i%9, column=c)
              button[i][0].grid(row=(i%9), column=c + 1)
              button[i][1].grid(row=(i % 9), column=c + 2)
              button[i][2].grid(row=(i % 9), column=c + 3)
              button[i][3].grid(row=(i % 9), column=c + 4)
              button[i][4].grid(row=(i % 9), column=c + 5)

            else:
                fontStyleButton = tkFont.Font(family="Helvetica", size=12)
                for j in range(5):
                    button[i].append(tk.Button(lower_frame, text=sinonimi[j], font=fontStyleButton,command=lambda i=i: cambiaParola(frase,i,sinonimi[j])))

                testo = tk.Label(lower_frame, font=fontStyleButton, text=parola)
                testo.grid(row=i%9, column=c)
                button[i][0].grid(row=(i % 9), column=c + 1)
                button[i][1].grid(row=(i % 9), column=c + 2)
                button[i][2].grid(row=(i % 9), column=c + 3)
                button[i][3].grid(row=(i % 9), column=c + 4)
                button[i][4].grid(row=(i % 9), column=c + 5)

        else: scrivi = True

   if scrivi:
       salva_nuova_frase(frase)

def cambiaParola(frase,i,sinonimo):

    frase_default = entry.get()
    frase_default = frase_default.replace(frase[i], sinonimo)
    entry.delete(0, tk.END)
    entry.insert(0, frase_default)

#scarico il pacchetto di stopword(se non presente)
nltk.download('stopwords')

#controllo se esistono nuove parole dopo l'esecuzione precedente
if esistone_nuove_parole():

    risposta = input('Ci sono nuove parole, vuoi aggiornare il modello? s/n ->: ')
    if risposta== 's':
        nuoveParole = leggi_nuove_parole()
        print(f'Nuove parole: {nuoveParole}')
        f = open('../data/nuoveparole.txt','w')
        modello = tr.training(nuoveParole)

    else:
        #provo a leggere il modello dal file; se non esiste,lo addestro e lo scrivo su file
        try:
            modello = ut.leggi_modello()
            print('Modello gia presente')
            num = list(modello.wv.vocab)
            print(f'Dimensione vocabolario: {len(num)}')
        except FileNotFoundError:
           modello = tr.training(nuoveParole=[])
else:
    try:
        modello = ut.leggi_modello()
        print('Modello gia presente')
        num = list(modello.wv.vocab)
        print(f'Dimensione vocabolario: {len(num)}')

    except FileNotFoundError:
        modello = tr.training(nuoveParole=[])

#inizia l'applicazione

HEIGHT = 500
WIDTH = 600

root = tk.Tk()
fontStyle = tkFont.Font(family="Times", size=20)

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root, bg='#9c1f1f', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

buttoninv = tk.Button(frame, text="Invia", font=40,command=lambda: elaboraFrase(modello))
buttoninv.place(relx=0.68, relheight=1, relwidth=0.15)

button = tk.Button(frame, text="Mostra \nCluster", font=40,   command=lambda: mostra_grafico())
button.place(relx=0.85, relheight=1, relwidth=0.15)


lower_frame = tk.Frame(root, bg='#ffffff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame, font= fontStyle,bg='#ffffff',anchor= 'nw')
label.place(relwidth=1, relheight=1,anchor= 'nw')


root.mainloop()


