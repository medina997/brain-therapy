import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import pandas as pd
from matplotlib import pyplot as plt
from data_import import read_data
import os
import glob


class plot:
    def __init__(self, name, date, filename):
        self.filename = filename
        self.name = name
        self.date = date


def Patient(fileName):
    path = os.getcwd()

    csv_files = glob.glob(os.path.join(path, "data\*.csv"))
    print(filename)
    # path = r'C:\Users\User\PycharmProjects\brain-therapy'
    m = read_data(path)
    l = []
    c = fileName.find("_")
    cString = fileName[c-4:c]
    for i in range(len(m[cString])):
        if hasattr(m[cString][i], 'eye'):
            texts(m[cString][i].eye, 7, 1)
            break  # eye
        if hasattr(m[cString][i], 'birth_date'):
            texts(m[cString][i].birth_date, 5, 1)
            break  # date
        if hasattr(m[cString][i], 'e_type'):
            texts(m[cString][i].e_type, 5, 1)
            break  # _type
        if hasattr(m[cString][i], 'brightness') and m[cString][i].brihtness != 'NaN' :
            texts(m[cString][i].brihtness, 5, 1)
            break  # brightness of flash
        if hasattr(m[cString][i], 'color'):
            texts(m[cString][i].color, 5, 1)
            break  # brightness of flash
    texts(cString, 5, 1)  # patientID
    texts(m[cString][1].date, 6, 1)  # birthday
    texts(m[cString][1].e_type, 8, 1)  # electrode type
    texts(m[cString][1].brightness, 9,1) # brightness
    texts(m[cString][1].color, 10, 1)  # color

    for i in range(len(m[cString])):
        if hasattr(m[cString][i], 'recorded_waveform'):
            df = m[cString][i].recorded_waveform
            df = df.dropna(axis=1, how='all')
            df = df.apply(pd.to_numeric)
            df.plot(x='ms', y='uV')
            plt.savefig('Unnamed' + str(i) + '.png')
            p = plot(cString, m[cString][i].date, 'Unnamed' + str(i) + '.png')
            l.append(p)

    for i in range(len(m[cString])):
        if hasattr(m[cString][i], 'raw_waveform'):
            df = m[cString][i].raw_waveform
            df = df.dropna(axis=1, how='all')
            df = df.apply(pd.to_numeric)
            df.plot(x='ms', y='uV')
            plt.savefig('Unnamed' + str(i) + '.png')
            p = plot(cString, m[cString][i].date, 'Unnamed' + str(i) + '.png')
            l.append(p)
    return l


def texts(s, r, c, cs=1):
    """
    This is a helper function for creating text labels
    :parameter: s is the string, r is the row number, c is the column number, cs is the offset --> default is 1
    :rtype: object
    """
    label = tk.Label(text=s)
    label.grid(row=r, column=c, columnspan=cs)


def main_texts(filename):
    """
    This function is responsible for the main Gui appearance, before loading any csv file
    :rtype: object
    """
    row, col = 5, 0
    # texts
    texts("Patient ID:", row, col)
    row += 1
    texts("Patient Birthdate:", row, col)
    row += 1
    texts("Eye:", row, col)
    row += 1
    texts("Electrode type:", row, col)
    row += 1
    texts("Brightness of Flash :", row, col)
    row += 1
    texts("Color of Flash :", row, col)
    row += 1

    texts("Plot name:", 14, 2)
    row += 1
    texts("Date:", 15, 2)
    row += 1

    my_font2 = ('times', 12, 'bold')
    l1 = tk.Label(window, text='Press N for normal, press D for diseased, press C for corrupt data', width=60, font=my_font2)
    l1.grid(row=3, column=4)

    b2 = tk.Button(window, text='Previous',
                   width=20, command=lambda: prev_img())
    b2.grid(row=14, column=1)

    b1 = tk.Button(window, text='Next',
                   width=20, command=lambda: next_img())
    b1.grid(row=14, column=4)


def save_result(event):
    """
    Saving result into the file for button click and for "N" or "D" keyboard press
    :rtype: object
    """
    try:
        if len(filename) == 0:
            return
    except:
        return
    c = filename.find("_")
    fname = filename[c:]
    data1 = pd.read_csv(filename, sep=',', encoding='latin1')

    if event.char == "n":
        print("saving..." + event.char + " Normal")

        data1["Diagnoses"] = "NORMAL"
        data1.to_csv("saved_file" + fname, index=False)


    elif event.char == "d":
        print("saving..." + event.char + " Disease")
        data1["Diagnoses"] = "DISEASE"
        data1.to_csv("saved_file.csv"+ fname, index=False)

    elif event.char == "c":
        print("saving..." + event.char + " Data corrupt")
        data1["Diagnoses"] = "DATA CORRUPT"
        data1.to_csv("saved_file.csv"+ fname, index=False)


def prev_img():
    global idx
    idx -= 1
    if idx < 0:
        idx = 0
    draw_img()


def next_img():
    global idx
    idx += 1
    if idx > 6:
        idx = 6
    draw_img()


def upload_file():
    global img
    global l
    global idx
    global data1
    idx = 0

    f_types = [('CSV Files', '*.csv')]
    global filename
    filename = filedialog.askopenfilename(filetypes=f_types)
    l = Patient(filename)
    draw_img()
    main_texts(filename)


def draw_img():
    global idx
    global img
    global l
    image_file_location = l[idx].filename
    img = ImageTk.PhotoImage(file=image_file_location)
    b2 = tk.Button(window, image=img)  # using Button
    b2.grid(row=5, column=1, rowspan=8, columnspan=8)
    texts(l[idx].name, 14, 3, 1)
    texts(l[idx].date, 15, 3, 1)


window = tk.Tk()
# getting screen width and height of display
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
# setting tkinter window size
window.geometry("%dx%d" % (width, height))
window.title('gui')
my_font1 = ('times', 18, 'bold')
l1 = tk.Label(window, text='Select a patient\'s file', width=30, font=my_font1)
l1.grid(row=1, column=1)

# button
b1 = tk.Button(window, text='Upload File',
               width=20, command=lambda: upload_file())
b1.grid(row=1, column=2)
window.bind("<Key>", save_result)
window.mainloop()  # Keep the window open
