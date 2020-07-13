from FFT import get_2D_dct, get_2d_idct
import io
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk 

def get_image_array(image_file):
    #funzione che estrae l'immagine e la mette in un array
    image = Image.open(image_file)
    img_grey = image.convert('L')
    img = np.array(img_grey, dtype=np.float)
    return img

def get_reconstructed_image(raw):
    #funzione che prende un array e lo trasforma in un'immagine
    img = raw.clip(0, 255)
    img = img.astype('uint8')
    img = Image.fromarray(img)
    return img

def display_images(img_input_path, img_output_path):
    #per visualizzare le immagini affiancate in una nuova finestra
    win_img = tk.Toplevel(window)
    win_img.state("zoomed")
    win_img.title("Risultato Compressione")
    win_img.grid_columnconfigure(0, weight=1)
    win_img.grid_columnconfigure(1, weight=1)
    lb01 = tk.Label(win_img, text="Originale: ", font=("Courier", 15))
    lb01.grid(row=0, column=0, pady=5)
    input_image = Image.open(img_input_path)
    input_img_show = ImageTk.PhotoImage(image=input_image)
    input_img_lb = tk.Label(win_img, image=input_img_show)
    input_img_lb.grid(row=1, column=0, padx=5)
    Image.Image.close(input_image)
    lb02 = tk.Label(win_img, text="Compressa: ", font=("Courier", 15))
    lb02.grid(row=0, column=1, pady=5)
    output_image = Image.open(img_output_path)
    output_img_show = ImageTk.PhotoImage(image=output_image)
    output_img_lb = tk.Label(win_img, image=output_img_show)
    output_img_lb.grid(row=1, column=1)
    Image.Image.close(output_image)
    win_img.mainloop()

def solving():
    #prendo l'immagine di input e la cartella di output
    img_input_path = input_path.get()
    folder_output_path = output_path.get()
    if os.path.isfile(img_input_path) and os.path.isdir(
        folder_output_path):
        v1 = img_input_path.split('/')
        v2 = v1[len(v1) - 1].split('.')
        filename = ""
        for i in range(len(v2) - 1):
            filename += v2[i]
            if i < len(v2) - 2:
                filename += '.'
        img_output_path = folder_output_path + '/' + filename + '_dctResult.' +v2[len(v2) - 1]
        F = 8
        d = 4
        conv = False
        try:
            F = int(F_spin.get())
            d = int(d_spin.get())
            conv = True
        except:
            conv = False
        img = get_image_array(img_input_path)
        x_size = img.shape[0]
        y_size = img.shape[1]

        if conv == True and F >= 1 and F <= x_size and F <= y_size and d >= 0 and d <= (2 * F) - 2:
            dct = get_2D_dct(img)
            reconstructed_image = np.zeros(img.shape)
            c = 0
            #eseguo dividendo per blocchi
            for x in list(range(0, x_size, F)):
                for y in list(range(0, y_size, F)):
                    print(c)
                    c = c + 1
                    if x + F > x_size or y + F > y_size:
                        continue
                    dct = get_2D_dct(img[x: x + F, y: y + F])
                    (k, l) = np.indices((F, F))
                    index = k + l >= d
                    dct[index] = 0
                    dct_inverse = get_2d_idct(dct)
                    reconstructed_image[x: x + F, y: y + F] = dct_inverse
            #una volta ricostruita l'immagine la salvo
            reconstructed_image = get_reconstructed_image(reconstructed_image)
            reconstructed_image.save(img_output_path)
            display_images(img_input_path, img_output_path)
        else:
            tk.messagebox.showerror("Errore", "Errore nei valori dei parametri")
    else:
        tk.messagebox.showerror("Errore", "Errore nel caricamento dell'immagine")

#funzioni per visualizzare la scelta dell'immagine e della cartella di output
def getimage():
    filename = tk.filedialog.askopenfilename(filetypes=[("BMP image", "*.bmp")])
    if os.path.isfile(filename):
        input_path.configure(state="normal")
        input_path.delete(0, tk.END)
        input_path.insert(0, filename)
        input_path.configure(state="readonly")

def getfolder():
    foldername = tk.filedialog.askdirectory()
    if os.path.isdir(foldername):
        output_path.configure(state="normal")
        output_path.delete(0, tk.END)
        output_path.insert(0, foldername)
        output_path.configure(state="readonly")

# main window
window = tk.Tk()

window.geometry("600x375")
window.title("Progetto 2 - pt.2 Modelli del Calcolo Scientifico")
window.resizable(True, True)
window.grid_columnconfigure(0, weight=1)

lb1 = tk.Label(window, text="Scegli un'immagine Bitmap (*.bmp): ", font=("Courier", 15))
lb1.grid(row=0, column=1, sticky="W", padx=10, pady=10)
img_btn = tk.Button(text="Apri", bg="blue", fg="white", font=("Courier", 15), command=getimage)
img_btn.grid(row=0, column=2, sticky="W", pady=10)
input_path = tk.Entry(font=("Courier", 15), justify="center")
input_path.configure(state="readonly")
input_path.grid(row=1, column=0, sticky="WE", padx=10, pady=10, columnspan=4)

lb3 = tk.Label(window, text="Scegli dove salvare i risultati: ", font=("Courier", 15))
lb3.grid(row=2, column=1, sticky="W", padx=10, pady=10)
img_btn = tk.Button(text="Salva", bg="blue", fg="white", font=("Courier", 15), command=getfolder)
img_btn.grid(row=2, column=2, sticky="W", pady=10)
output_path = tk.Entry(font=("Courier", 15), justify="center")
output_path.configure(state="readonly")
output_path.grid(row=3, column=0, sticky="WE", padx=10, pady=10, columnspan=4)

lb5 = tk.Label(window, text="Imposta (F >= 1): ", font=("Courier", 15))
lb5.grid(row=4, column=1, sticky="W", padx=10, pady=10)
F_spin = tk.Spinbox(from_=1, to=10000, font=("Courier", 15), width=10)
F_spin.grid(row=4, column=2, sticky="W", pady=10)

lb5 = tk.Label(window, text="Imposta d [0; 2F-2]: ", font=("Courier", 15))
lb5.grid(row=5, column=1, sticky="W", padx=10, pady=10)
d_spin = tk.Spinbox(from_=0, to=19998, font=("Courier", 15), width=10)
d_spin.grid(row=5, column=2, sticky="W", pady=10)

compute_btn = tk.Button(text="Calcola", bg="red", fg="white", font=("Courier", 15), command=
solving)
compute_btn.grid(row=6, column=1, sticky="N", padx=10, pady=10)

if __name__ == "__main__":
    window.mainloop()