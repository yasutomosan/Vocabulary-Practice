import tkinter as tk
from playsound import playsound
import csv
from tkinter import messagebox
import random
import time

#色関係
labels_bg = "gray100"
mw_bg = "white"

# メインウィンドウの設定
root = tk.Tk()
root.title("English")
root.state("zoomed")
root.config(bg=mw_bg)

#タイトルバーアイコン
photo = tk.PhotoImage(file = "pencil.png")  
root.iconphoto(False, photo)

# データの保存
vocabularies = []

#モード管理
state = 0
mode = {0: "shuffle", 1: "verb", 2: "noun", 3: "adjective", 4: "adverb", 5: "others"}
text = {}
selected_vocabularies = []
selected_question = 0
selected_mode = 0

for i in mode:
        text[i] = mode[i]
        #print(text[i])
text[6]="menu"

# CSVファイルからデータを読み込む関数
def load_data(vocabularies):
    vocabularies.clear()
    try:
        with open('words.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    vocabularies.append({"word": row[0], "meaning": row[1], "part_of_speech": row[2]})
    except FileNotFoundError:
        messagebox.showwarning("FileNotFoundError","'words.csv' file not found  : /")


def choose(num):
    #print("aa")
    global state, mode, selected_question, text, selected_mode
    #print(state)
    if state == 0:
        button6.grid_forget
        selected_mode = num
        state = 1
        choice_generation()
        print("state0->1")
        #print(text)
    elif state == 1:
        button6.grid_forget
        state = 2
        print("state1->2")
        #print(text[num],vocabularies[selected_question]["meaning"])
        if text[num] == vocabularies[selected_question]["meaning"]:
            tochuu(0)
            print("OK!")
            #playsound('C:\\Users\\gon23\\OneDrive\\デスクトップ\\python\\english\\goodsound.mp3')
        else:
            tochuu(1)
        #print(text)
    elif state == 2:
        if num == 6:
            button6.grid_forget
            state = 1
            selected_question = random.randint(0, n_rows - 1)
            choice_generation()
        elif text[num] == vocabularies[selected_question]["meaning"]:
            tochuu(0)
            print("OK!")
            #playsound('C:\\Users\\gon23\\OneDrive\\デスクトップ\\python\\english\\goodsound.mp3')
        else:
            tochuu(1)
    #elif state == 3:
    #    button6.grid_forget
    #    state = 1
    #    selected_question = random.randint(0, n_rows - 1)
    #    choice_generation()
    update_buttons()
    #print("aa")
    #time.sleep(1)
    label0.config(fg="black")

def tochuu(num):
    if num == 0:
        button6.config(text="OK!")
    elif num ==1:
        button6.config(text="umm!")
    button6.grid(row=10,column=1,columnspan=3)

def choice_generation():
    global selected_vocabularies
    if selected_mode == 0:
        selected_vocabularies = random.sample(vocabularies, 6)
    elif selected_mode == 1:
        filtered_vocabularies = [v for v in vocabularies if v["part_of_speech"] == "0"]
        selected_vocabularies = random.sample(filtered_vocabularies, 6)
    for i in selected_vocabularies:
            if i == vocabularies[selected_question]:
                return 0
    answer_num = random.randint(0, 5)
    selected_vocabularies[answer_num]=vocabularies[selected_question]
    #print(selected_vocabularies)

def update_buttons():
    for i in range(len(selected_vocabularies)):
            text[i] = selected_vocabularies[i]['meaning']
    text[6]=vocabularies[selected_question]['word']
    button0.config(text=text[0])
    button1.config(text=text[1])
    button2.config(text=text[2])
    button3.config(text=text[3])
    button4.config(text=text[4])
    button5.config(text=text[5])
    label0.config(text=text[6])


label0 = tk.Label(root, text=text[6], width=15, height=2, bg=labels_bg, font=("Helvetica", 30), relief="solid")
label0.grid(row=2, column=1, columnspan=3)
#label1 = tk.Label(root, text="", width=15, height=1, bg=labels_bg, font=("Helvetica", 30), relief="solid")
#label1.grid(row=3, column=1, columnspan=3)
button0 = tk.Button(root, text=text[0], width=25, bg=labels_bg, font=("Helvetica", 20), relief="solid", command=lambda: choose(0))
button0.grid(row=4, column=1)
button1 = tk.Button(root, text=text[1], width=25, bg=labels_bg, font=("Helvetica", 20), relief="solid", command=lambda: choose(1))
button1.grid(row=4, column=3)
button2 = tk.Button(root, text=text[2], width=25, bg=labels_bg, font=("Helvetica", 20), relief="solid", command=lambda: choose(2))
button2.grid(row=6, column=1)
button3 = tk.Button(root, text=text[3], width=25, bg=labels_bg, font=("Helvetica", 20), relief="solid", command=lambda: choose(3))
button3.grid(row=6, column=3)
button4 = tk.Button(root, text=text[4], width=25, bg=labels_bg, font=("Helvetica", 20), relief="solid", command=lambda: choose(4))
button4.grid(row=8, column=1)
button5 = tk.Button(root, text=text[5], width=25, bg=labels_bg, font=("Helvetica", 20), relief="solid", command=lambda: choose(5))
button5.grid(row=8, column=3)
button6 = tk.Button(root, text="", width=25, bg=labels_bg, font=("Helvetica", 20), relief="solid", command=lambda: choose(6))


tk.Label(root, text="", width=9, bg=mw_bg, font=("Helvetica", 20)).grid(row=0, column=2)

tk.Label(root, text="", width=9, bg=mw_bg, font=("Helvetica", 20)).grid(row=0, column=0)
tk.Label(root, text="", width=9, bg=mw_bg, font=("Helvetica", 20)).grid(row=1, column=0)
tk.Label(root, text="", width=9, height=3 ,bg=mw_bg, font=("Helvetica", 20)).grid(row=3, column=0)
tk.Label(root, text="", width=9, bg=mw_bg, font=("Helvetica", 20)).grid(row=5, column=0)
tk.Label(root, text="", width=9, bg=mw_bg, font=("Helvetica", 20)).grid(row=7, column=0)
tk.Label(root, text="", width=9, bg=mw_bg, font=("Helvetica", 20)).grid(row=9, column=0)


# プログラム起動時に本を読み込む
load_data(vocabularies)
n_rows=len(vocabularies)


# メインループ
root.mainloop()