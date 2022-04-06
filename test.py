import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import pandas as pd
from matplotlib import pyplot as plt


class plot:
    def __init__(self, name, date, filename):
        self.filename = filename
        self.name = name
        self.date = date


def Patient(fileName):
    # data1 = pd.read_csv("Example Reteval.csv", sep=',', usecols=[6,7], skiprows=28, names=columns )
    # data1 = data1.dropna(how='any')

    l = []
    data1 = pd.read_csv(fileName, sep=',', encoding='latin1')
    texts(data1.iloc[2,2], 5, 2)
    texts(data1.iloc[0,2], 4, 2)
    texts(data1.iloc[5, 2], 6, 2)
    texts(data1.iloc[6, 2], 7, 2)
    date = data1.iloc[1,2]

    cString = data1.columns[2]
    texts(cString, 3, 2)

    i = data1.loc[data1['PatientID'] == 'Reported Waveform'].index.values
    j = data1.loc[data1['PatientID'] == 'Raw Waveform'].index.values
    k = data1.loc[data1['PatientID'] == 'Pupil Waveform'].index.values

    data2 = data1.iloc[i[0] + 1:j[0], :]  # splitting the datasets
    data3 = data1.iloc[j[0] + 1:k[0], :]
    data4 = data1.iloc[k[0] + 1:, :]

    # dropping the columns that does not have values
    data2 = data2.dropna(axis=1, how='all')
    data3 = data3.dropna(axis=1, how='all')
    data4 = data4.dropna(axis=1, how='all')
    # converting the column values to numeric data
    data2 = data2.apply(pd.to_numeric)
    data3 = data3.apply(pd.to_numeric)
    data4 = data4.apply(pd.to_numeric)

    print(data4.columns)
    print(data4)
    #  plotting

    data2.plot(x=f'{cString}', y='Unnamed: 3')
    plt.savefig('Unnamed3.png')
    p = plot(f'{cString} ', date, 'Unnamed3.png')
    l.append(p)

    data2.plot(x=f'{cString}.2', y='Unnamed: 7')
    plt.savefig('Unnamed7.png')
    p = plot(f'{cString}.2', date, 'Unnamed7.png')
    l.append(p)

    data2.plot(x=f'{cString}.4', y='Unnamed: 11')
    plt.savefig('Unnamed11.png')
    p = plot(f'{cString}.4', date, 'Unnamed11.png')
    l.append(p)

    data3.plot(x=f'{cString}', y='Unnamed: 3')
    plt.savefig('Unnamed3.1.png')
    p = plot(f'{cString} ', date, 'Unnamed3.1.png')
    l.append(p)

    data3.plot(x=f'{cString}.2', y='Unnamed: 7')
    plt.savefig('Unnamed7.1.png')
    p = plot(f'{cString}.2', date, 'Unnamed7.1.png')
    l.append(p)

    data3.plot(x=f'{cString}.4', y='Unnamed: 11')
    plt.savefig('Unnamed11.1.png')
    p = plot(f'{cString}.4', date, 'Unnamed11.1.png')
    l.append(p)
    # plt.show()

    data4.plot(x=f'{cString}.13', y=f'{cString}.15')
    plt.savefig('Unnamed15.png')
    p = plot(f'{cString}.13', date, 'Unnamed15.png')
    l.append(p)
    # plt.show()
    return l


def texts(s, r, c, cs=1):
    label = tk.Label(text=s)
    label.grid(row=r, column=c, columnspan=cs)


def main_texts():
    row, col = 3, 1
    # texts
    texts("Patient ID:", row, col)
    row += 1
    texts("Patient Birthdate:", row, col)
    row += 1
    texts("Eye:", row, col)
    row += 1
    texts("Flash:", row, col)
    row += 1
    texts("Flash color:", row, col)
    row += 1

    texts("Plot name:", 9, 4)
    row += 1
    texts("Date:", 10, 4)
    row += 1

    OPTIONS = [
        "Evaluate",
        "Normal",
        "Disease",
        "data corrupt"
    ]
    variable = tk.StringVar(window)
    variable.set(OPTIONS[0])  # default value
    w = tk.OptionMenu(window, variable, *OPTIONS)
    w.grid(row=0, column=0)

    save = tk.Button(window, text='Save evaluation',
                   width=20, command=lambda: save_result())
    save.grid(row=1, column=0)

    b2 = tk.Button(window, text='Previous',
                   width=20, command=lambda: prev_img())
    b2.grid(row=9, column=3 )

    b1 = tk.Button(window, text='Next',
                   width=20, command=lambda: next_img())
    b1.grid(row=9, column=8)


def save_result(event):
    if event.char == "a":
        print("saving..."+ event.char+ " normal")
        # ide jöhet a fáljba irás
    elif event.char == "d":
        print("saving..." + event.char + " Diseas")
        #ide pedig egy másik fajta fájlba írás


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
    idx = 0
    # f_types = [('Jpg Files', '*.jpg')]
    # filename = filedialog.askopenfilename(filetypes=f_types)
    # img = ImageTk.PhotoImage(file=filename)
    # b2 = tk.Button(window, image=img)  # using Button
    # b2.grid(row=3, column=3, rowspan=6, columnspan=6)

    f_types = [('CSV Files', '*.csv')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    l = Patient(filename)
    draw_img()
    main_texts()


def draw_img():
    global idx
    global img
    global l
    image_file_location = l[idx].filename
    img = ImageTk.PhotoImage(file=image_file_location)
    b2 = tk.Button(window, image=img)  # using Button
    b2.grid(row=3, column=3, rowspan=6, columnspan=6)
    texts(l[idx].name, 9, 5, 3)
    texts(l[idx].date, 10, 5, 3)



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
