import io
import os
from PIL import Image, ImageTk #pip install --upgrade Pillow 
import numpy as np
from FFT import get_2D_dct, get_2d_idct
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def get_image_array(image_file):
    image = Image.open(image_file)
    img_grey = image.convert('L')
    img = np.array(img_grey, dtype=np.float)
    return img

def get_reconstructed_image(raw):
    img = raw.clip(0, 255)
    img = img.astype('uint8')
    img = Image.fromarray(img)
    return img

def display_images(img_input_path, img_output_path):
    win_img = tk.Toplevel(window)
    win_img.state("zoomed")
    win_img.title("MCS images")
    win_img.grid_columnconfigure(0, weight=1)
    win_img.grid_columnconfigure(1, weight=1)
    lb01 = tk.Label(win_img, text="Before: ", font=("Arial", 15))
    lb01.grid(row=0, column=0, pady=5)
    input_image = Image.open(img_input_path)
    input_img_show = ImageTk.PhotoImage(image=input_image)
    input_img_lb = tk.Label(win_img, image=input_img_show)
    input_img_lb.grid(row=1, column=0, padx=5)
    Image.Image.close(input_image)
    lb02 = tk.Label(win_img, text="After: ", font=("Arial", 15))
    lb02.grid(row=0, column=1, pady=5)
    output_image = Image.open(img_output_path)
    output_img_show = ImageTk.PhotoImage(image=output_image)
    output_img_lb = tk.Label(win_img, image=output_img_show)
    output_img_lb.grid(row=1, column=1)
    Image.Image.close(output_image)
    win_img.mainloop()

def solving():
    img_input_path = input_path.get()
    folder_output_path = output_path.get()
    # se immagine e cartella esistono
    if os.path.isfile(img_input_path) and os.path.isdir(
        folder_output_path):
        # "calcolo" il nome dell’immagine in output
        v1 = img_input_path.split('/')
        v2 = v1[len(v1) - 1].split('.')
        filename = ""
        for i in range(len(v2) - 1):
            filename += v2[i]
            if i < len(v2) - 2:
                filename += '.'
        img_output_path = folder_output_path + '/' + filename + '_dct.' +v2[len(v2) - 1]
        # inizializzo F d e conv
        F = 8
        d = 4
        conv = False
        # se non riesco a convertire F e d in interi mostro un errore
        try:
            F = int(F_spin.get())
            d = int(d_spin.get())
            conv = True
        except:
            conv = False
        # converto l’immagine in un array di float
        img = get_image_array(img_input_path)
        x_size = img.shape[0]
        y_size = img.shape[1]

        if conv == True and F >= 1 and F <= x_size and F <= y_size and d >= 0 and d <= (2 * F) - 2:
            # faccio la DCT2 dell’intera immagine
            dct = get_2D_dct(img)
            # inizializzo la matrice per la ricostruzione a 0
            reconstructed_image = np.zeros(img.shape)
            # prendo "blocchi" fi dimensione FxF
            for x in list(range(0, x_size, F)):
                for y in list(range(0, y_size, F)):
                    if x + F > x_size or y + F > y_size:
                        continue
                    # faccio la DCT2 del blocco
                    dct = get_2D_dct(img[x: x + F, y: y + F])
                    # elimino le frequenze Ckl dove k+l>=d
                    (k, l) = np.indices((F, F))
                    index = k + l >= d
                    dct[index] = 0
                    # faccio la IDCT2
                    dct_inverse = get_2d_idct(dct)
                    # ricostruisco il blocco
                    reconstructed_image[x: x + F, y: y + F] = dct_inverse
                    # ricostruisco l’immagine
                    reconstructed_image = get_reconstructed_image(reconstructed_image)
                    # salvo l’immagine ricostruita
                    reconstructed_image.save(img_output_path)
                    # confronto le 2 immagini
                    display_images(img_input_path, img_output_path)
            else:
                tk.messagebox.showerror("Error", "Incorrect F and parameters")
        else:
            tk.messagebox.showerror("Error", "Incorrect image paths")

def browseimage():
    # apro la finestra di dialogo
    filename = tk.filedialog.askopenfilename(filetypes=[("BMP image", "*.bmp")])
    # se esiste l’immagine
    if os.path.isfile(filename):
        input_path.configure(state="normal")
        input_path.delete(0, tk.END)
        input_path.insert(0, filename)
        input_path.configure(state="readonly")

def browsefolder():
    # apro la finestra di dialogo
    foldername = tk.filedialog.askdirectory()
    if os.path.isdir(foldername):
        output_path.configure(state="normal")
        output_path.delete(0, tk.END)
        output_path.insert(0, foldername)
        output_path.configure(state="readonly")

# inizializzo la finestra
window = tk.Tk()
# definisco la dimensione di default
window.geometry("900x350")
# definisco il titolo
window.title("Compressore immagini progetto 2 MCS")
# la rendo non responsive
window.resizable(False, False)
# calcolo la risuoluzione in base allo schermo dell’utente
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = screen_width / 2 - 900 / 2
y = screen_height / 2 - 350 / 2
window.geometry("+%d+%d" % (x, y))

lb1 = tk.Label(window, text="Scegli una immagine BITMAP: ", font=("Arial", 15))
lb1.grid(row=0, column=1, sticky="E", padx=5, pady=5)

img_btn = tk.Button(text="Apri", font=("Arial", 15), command=browseimage)
img_btn.grid(row=0, column=2, sticky="W", pady=5)
input_path = tk.Entry(font=("Arial", 15), width=80, justify="center")
input_path.configure(state="readonly")
input_path.grid(row=1, column=0, sticky="W", padx=5, pady=5, columnspan=4)

lb3 = tk.Label(window, text="Scegli cartella di Output: ", font=("Arial", 15))
lb3.grid(row=2, column=1, sticky="E", padx=5, pady=5)

img_btn = tk.Button(text="Salva", font=("Arial", 15), command=browsefolder)
img_btn.grid(row=2, column=2, sticky="W", pady=10)
output_path = tk.Entry(font=("Arial", 15), width=80, justify="center")
output_path.configure(state="readonly")
output_path.grid(row=3, column=0, sticky="W", padx=5, pady=5, columnspan=4)

lb5 = tk.Label(window, text="Imposta F >= 1: ", font=("Arial", 15))
lb5.grid(row=4, column=1, sticky="E", padx=5, pady=10)
F_spin = tk.Spinbox(from_=1, to=10000, font=("Arial", 15), width=10)
F_spin.grid(row=4, column=2, sticky="W", pady=5)

lb5 = tk.Label(window, text="Imposta d [0; 2F-2]: ", font=("Arial", 15))
lb5.grid(row=5, column=1, sticky="E", padx=5, pady=10)
d_spin = tk.Spinbox(from_=0, to=19998, font=("Arial", 15), width=10)
d_spin.grid(row=5, column=2, sticky="W", pady=5)

compute_btn = tk.Button(text="Calcola", font=("Arial", 15), command=
solving)
compute_btn.grid(row=6, column=1, sticky="E", padx=5, pady=10)
if __name__ == "__main__":
    # esegui la GUI
    window.mainloop()