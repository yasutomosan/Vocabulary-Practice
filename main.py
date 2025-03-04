import tkinter as tk
import csv
from tkinter import messagebox
import random

#色、フォント
labels_bg = "gray100"   #ラベルの色
mw_bg = "white" #背景の色
nomal_font = ("Helvetica", 20)
big_font = ("Helvetica", 30)
small_font = ("Helvetica", 10)
bw = 3  #ラベル、ボタンの枠線の太さ
#words_file = "words.csv"
words_file = "toeic.csv"

# メインウィンドウの設定
root = tk.Tk()
root.title("Vocabulary-Practice")
root.state("zoomed")
root.config(bg=mw_bg)

#タイトルバーアイコン
photo1 = tk.PhotoImage(file = "pencil.png")  
root.iconphoto(False, photo1)

#ホームボタン用画像
photo2 = tk.PhotoImage(file="home.gif")
photo2 = photo2.subsample(40, 40) #圧縮比率

# データの保存用配列
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
        with open(words_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            vocabularies.extend({"number": row[0], "word": row[1], "meaning": row[2], "part_of_speech": row[3], "check": row[4]} for row in reader if row)
    except FileNotFoundError:
        messagebox.showwarning("FileNotFoundError","'words.csv' file not found  : /")
    #print(vocabularies)

        
def save_data(vocabularies):
    try:
        with open(words_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ["number","word", "meaning", "part_of_speech", "check"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            #writer = csv.DictWriter(file)

            #writer.writeheader()
            writer.writerows(vocabularies)
    except FileNotFoundError:
        messagebox.showwarning("FileNotFoundError","'words.csv' file not found  : /")

def choose(num):
    global state, selected_question, selected_mode
    buttons[num]
    if state == 0:
        selected_mode = num
        button7.grid(row=0,column=0)
        state = 1
        choice_generation()
        update_buttons()
    elif state == 1:
        if text[num] == filter[selected_mode][selected_question]["meaning"]:
            judgement(0)
        else:
            judgement(1)

def next():
    global state,selected_question
    button6.grid_forget()
    buttons[answer_num].config(fg="black")
    state = 1
    choice_generation()
    update_buttons()

def go_to_home():
    global state,selected_question
    button6.grid_forget()
    button7.grid_forget()
    state = 0
    buttons[answer_num].config(fg="black")
    text = {i: mode[i] for i in mode}
    text[6]="menu"
    for i,button in enumerate(buttons):
        button.config(text=text[i])
    label0.config(text=text[6])
    save_data(vocabularies)

def judgement(num):
    buttons[answer_num].config(fg="red")
    button6.config(text= "true" if num==0 else "false")
    #if text[num] == filter[selected_mode][selected_question]["meaning"]:
    #vocabularies.
    button6.grid(row=10,column=1,columnspan=5,rowspan=3)

def choice_generation():
    global selected_vocabularies,selected_question,answer_num
    answer_num = random.randint(0, 5)

    selected_question = random.randint(0, len(filter[selected_mode]) - 1)
    selected_vocabularies = random.sample(filter[selected_mode], 6)
    for i,vocabulary in enumerate(selected_vocabularies):
        if vocabulary == filter[selected_mode][selected_question]:
            answer_num=i
            return 0
    selected_vocabularies[answer_num] = filter[selected_mode][selected_question]
    

def update_buttons():
    for i in range(len(selected_vocabularies)):
            text[i] = selected_vocabularies[i]['meaning']
    text[6]=filter[selected_mode][selected_question]['word']
    for i,button in enumerate(buttons):
        button.config(text=text[i])
    label0.config(text=text[6])

# プログラム起動時に単語を読み込む
load_data(vocabularies)
n_rows=len(vocabularies)

#品詞毎に配列を作成
filtered_verb = [v for v in vocabularies if v["part_of_speech"] == "0"]
filtered_noun = [v for v in vocabularies if v["part_of_speech"] == "1"]
filtered_adjective = [v for v in vocabularies if v["part_of_speech"] == "2"]
filtered_adverb = [v for v in vocabularies if v["part_of_speech"] == "3"]
filtered_others = [v for v in vocabularies if v["part_of_speech"] == "4"]
filter = [vocabularies,filtered_verb,filtered_noun,filtered_adjective,filtered_adverb,filtered_others]


#問を出すラベル
label0 = tk.Label(root, text=text[6], width=15, height=2, bg=labels_bg, font=big_font, relief="solid", borderwidth=bw)
label0.grid(row=2, column=2, columnspan=3, rowspan=2)
#選択肢用ボタン
button0 = tk.Button(root, text=text[0], width=30, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: choose(0))
button0.grid(row=5, column=1, columnspan=2)
button1 = tk.Button(root, text=text[1], width=30, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: choose(1))
button1.grid(row=5, column=4, columnspan=2)
button2 = tk.Button(root, text=text[2], width=30, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: choose(2))
button2.grid(row=7, column=1, columnspan=2)
button3 = tk.Button(root, text=text[3], width=30, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: choose(3))
button3.grid(row=7, column=4, columnspan=2)
button4 = tk.Button(root, text=text[4], width=30, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: choose(4))
button4.grid(row=9, column=1, columnspan=2)
button5 = tk.Button(root, text=text[5], width=30, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: choose(5))
button5.grid(row=9, column=4, columnspan=2)
#次へ行くボタン
button6 = tk.Button(root, text="", width=25, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: next())
#ホームボタン
button7 = tk.Button(root, image=photo2, width=50,height=50, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: go_to_home())
buttons = [button0,button1,button2,button3,button4,button5]


#button6.grid(row=11,column=1,columnspan=5,rowspan=2)

#button6.grid_forget()

#レイアウト調整用の空白ラベル
tk.Label(root, text="", width=9, bg=mw_bg, font=nomal_font, height=2).grid(row=0, column=3)
tk.Label(root, text="", width=4, bg=mw_bg, font=nomal_font).grid(row=1, column=0)
tk.Label(root, text="", width=4, bg=mw_bg, font=nomal_font, height=2).grid(row=4, column=0)
tk.Label(root, text="", width=4, bg=mw_bg, font=nomal_font).grid(row=6, column=0)
tk.Label(root, text="", width=4, bg=mw_bg, font=nomal_font).grid(row=8, column=0)
tk.Label(root, text="", width=4, bg=mw_bg, font=nomal_font).grid(row=10, column=0)

tk.Label(root, text="", width=4, bg=mw_bg, font=nomal_font).grid(row=13, column=0)

# メインループ
root.mainloop()