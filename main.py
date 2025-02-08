import tkinter as tk
from playsound import playsound
import csv
from tkinter import messagebox
import random

#色、フォント
labels_bg = "gray100"   #ラベルの色
mw_bg = "white" #背景の色
nomal_font = ("Helvetica", 20)
big_font = ("Helvetica", 30)
bw = 3  #ラベル、ボタンの枠線の太さ


# メインウィンドウの設定
root = tk.Tk()
root.title("Vocabulary-Practice")
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
text = {i: mode[i] for i in mode}
text[6]="menu"
selected_vocabularies = []
selected_question = 0   #出題する問題
selected_mode = 0   #選択した場所
answer_num = 0  #正解の場所

# CSVファイルからデータを読み込む関数
def load_data(vocabularies):
    vocabularies.clear()
    try:
        with open('words.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            vocabularies.extend({"word": row[0], "meaning": row[1], "part_of_speech": row[2]} for row in reader if row)
    except FileNotFoundError:
        messagebox.showwarning("FileNotFoundError","'words.csv' file not found  : /")

def choose(num):
    global state, selected_question, selected_mode
    if state == 0:
        selected_mode = num
        state = 1
        selected_question = random.randint(0, n_rows - 1)
        choice_generation()
    elif state == 1:
        state = 2
        if text[num] == vocabularies[selected_question]["meaning"]:
            judgement(0)
            #playsound('C:\\Users\\gon23\\OneDrive\\デスクトップ\\python\\english\\goodsound.mp3')
        else:
            judgement(1)
    elif state == 2:
        if text[num] == vocabularies[selected_question]["meaning"]:
            judgement(0)
        else:
            judgement(1)
    update_buttons()

def next():
    global state,selected_question
    button6.grid_forget()
    buttons[answer_num].config(fg="black")
    state = 1
    selected_question = random.randint(0, n_rows - 1)
    choice_generation()
    update_buttons()

def judgement(num):
    buttons[answer_num].config(fg="red")
    button6.config(text= "OK!" if num==0 else "umm...")
    button6.grid(row=10,column=1,columnspan=3)

def choice_generation():
    global selected_vocabularies,answer_num
    if selected_mode == 0:
        selected_vocabularies = random.sample(vocabularies, 6)
    elif selected_mode == 1:
        filtered_vocabularies = [v for v in vocabularies if v["part_of_speech"] == "0"]
        selected_vocabularies = random.sample(filtered_vocabularies, 6)
    for i in selected_vocabularies:
        if i == vocabularies[selected_question]:
            return 0
    answer_num = random.randint(0, 5)
    selected_vocabularies[answer_num] = vocabularies[selected_question]
    #print(selected_vocabularies)


def update_buttons():
    for i in range(len(selected_vocabularies)):
            text[i] = selected_vocabularies[i]['meaning']
    text[6]=vocabularies[selected_question]['word']
    for i,button in enumerate(buttons):
        button.config(text=text[i])
    label0.config(text=text[6])
    

# プログラム起動時に単語を読み込む
load_data(vocabularies)
n_rows=len(vocabularies)
filtered_verb = [v for v in vocabularies if v["part_of_speech"] == "0"]
filtered_noun = [v for v in vocabularies if v["part_of_speech"] == "1"]
filtered_verb = [v for v in vocabularies if v["part_of_speech"] == "2"]
filtered_adverb = [v for v in vocabularies if v["part_of_speech"] == "3"]
filtered_others = [v for v in vocabularies if v["part_of_speech"] == "4"]



label0 = tk.Label(root, text=text[6], width=15, height=2, bg=labels_bg, font=big_font, relief="solid", borderwidth=bw)
label0.grid(row=2, column=1, columnspan=3)
button0 = tk.Button(root, text=text[0], width=25, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: choose(0))
button0.grid(row=4, column=1)
button1 = tk.Button(root, text=text[1], width=25, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: choose(1))
button1.grid(row=4, column=3)
button2 = tk.Button(root, text=text[2], width=25, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: choose(2))
button2.grid(row=6, column=1)
button3 = tk.Button(root, text=text[3], width=25, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: choose(3))
button3.grid(row=6, column=3)
button4 = tk.Button(root, text=text[4], width=25, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: choose(4))
button4.grid(row=8, column=1)
button5 = tk.Button(root, text=text[5], width=25, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: choose(5))
button5.grid(row=8, column=3)
button6 = tk.Button(root, text="", width=25, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: next())
buttons = [button0,button1,button2,button3,button4,button5]

tk.Label(root, text="", width=9, bg=mw_bg, font=nomal_font).grid(row=0, column=2)

tk.Label(root, text="", width=9, bg=mw_bg, font=nomal_font).grid(row=0, column=0)
tk.Label(root, text="", width=9, bg=mw_bg, font=nomal_font).grid(row=1, column=0)
tk.Label(root, text="", width=9, height=3 ,bg=mw_bg, font=nomal_font).grid(row=3, column=0)
tk.Label(root, text="", width=9, bg=mw_bg, font=nomal_font).grid(row=5, column=0)
tk.Label(root, text="", width=9, bg=mw_bg, font=nomal_font).grid(row=7, column=0)
tk.Label(root, text="", width=9, bg=mw_bg, font=nomal_font).grid(row=9, column=0)



# メインループ
root.mainloop()