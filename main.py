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
bw = 3  #ラベル、ボタンの枠f線の太さ
words_file = "words.csv"
#words_file = "toeic.csv"
#words_file = "toeic_test.csv"

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
filtered_verb = None 
filtered_noun = None 
filtered_adjective = None 
filtered_adverb = None 
filtered_checked = None 
filtered_others = None 
filtered_vocabularies = None

#モード管理
state = 0
mode = {0: "shuffle", 1: "verb", 2: "noun", 3: "adjective", 4: "adverb", 5: "checked"}
text = {i: mode[i] for i in mode}
text[6]="menu"
selected_vocabularies = []
selected_question = None   #出題する問題 vocaのnumを選択
selected_mode = None   #選択した場所
answer_num = None  #正解の場所
selected_column = None

# CSVファイルからデータを読み込む関数
def load_data(vocabularies):
    global filtered_verb,filtered_noun,filtered_adjective,filtered_adverb,filtered_checked,filtered_others,filtered_vocabularies
    vocabularies.clear()
    try:
        with open(words_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            vocabularies.extend({"number": row[0], "word": row[1], "meaning": row[2], "part_of_speech": row[3], "check": row[4]} for row in reader if row)
    except FileNotFoundError:
        messagebox.showwarning("FileNotFoundError","'words.csv' file not found  : /")
    #print(vocabularies)
    #品詞毎に配列を作成
    filtered_verb = [v for v in vocabularies if v["part_of_speech"] == "0"]
    filtered_noun = [v for v in vocabularies if v["part_of_speech"] == "1"]
    filtered_adjective = [v for v in vocabularies if v["part_of_speech"] == "2"]
    filtered_adverb = [v for v in vocabularies if v["part_of_speech"] == "3"]
    filtered_checked = [v for v in vocabularies if v["check"] == "1"]
    filtered_others = [v for v in vocabularies if v["part_of_speech"] == "4"]
    filtered_vocabularies = [vocabularies,filtered_verb,filtered_noun,filtered_adjective,filtered_adverb,filtered_checked,filtered_others]


        
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
    #print("filtered_checked:",filtered_checked)
    buttons[num]
    if state == 0:
        selected_mode = num
        button7.grid(row=0,column=0)
        state = 1
        choice_generation()
        update_buttons()
    elif state == 1:
        #print("s_q:",selected_question)
        #print("vo",vocabularies)
        index = next((i for i, item in enumerate(vocabularies) if int(item["number"]) == selected_question), None)


        test = [item for item in vocabularies if int(item["number"]) == selected_question]
        #print(test[0]['meaning'],"==",text[num])
        if text[num] == test[0]['meaning']:

            judgement(0)
            vocabularies[index]["check"]=0
        else:
            judgement(1)
            vocabularies[index]["check"]=1


def next_question():
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
    #if text[num] == filtered_vocabularies[selected_mode][selected_question]["meaning"]:
    #vocabularies.
    button6.grid(row=10,column=1,columnspan=5,rowspan=3)

def choice_generation():
    global selected_vocabularies,selected_question,answer_num,selected_column
    answer_num = random.randint(0, 5)

    selected_column = random.randint(0, len(filtered_vocabularies[selected_mode]) - 1)
    selected_question = int(filtered_vocabularies[selected_mode][selected_column]["number"])

    selected_vocabularies = random.sample(filtered_vocabularies[selected_mode], 6)
    for i,vocabulary in enumerate(selected_vocabularies):
        #if vocabulary == filtered_vocabularies[selected_mode][selected_question]:
        if vocabulary == filtered_vocabularies[selected_mode][selected_column]:
            answer_num=i
            return 0
    selected_vocabularies[answer_num] = filtered_vocabularies[selected_mode][selected_column]
    

def update_buttons():
    for i in range(len(selected_vocabularies)):
            text[i] = selected_vocabularies[i]['meaning']
    text[6]=filtered_vocabularies[selected_mode][selected_column]['word']
    for i,button in enumerate(buttons):
        button.config(text=text[i])
    label0.config(text=text[6])

# プログラム起動時に単語を読み込む
load_data(vocabularies)
n_rows=len(vocabularies)

##品詞毎に配列を作成
#filtered_verb = [v for v in vocabularies if v["part_of_speech"] == "0"]
#filtered_noun = [v for v in vocabularies if v["part_of_speech"] == "1"]
#filtered_adjective = [v for v in vocabularies if v["part_of_speech"] == "2"]
#filtered_adverb = [v for v in vocabularies if v["part_of_speech"] == "3"]
#filtered_checked = [v for v in vocabularies if v["check"] == "1"]
#filtered_others = [v for v in vocabularies if v["part_of_speech"] == "4"]
#filtered_vocabularies = [vocabularies,filtered_verb,filtered_noun,filtered_adjective,filtered_adverb,filtered_checked,filtered_others]


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
button6 = tk.Button(root, text="", width=25, bg=labels_bg, font=nomal_font, relief="solid", borderwidth=bw, command=lambda: next_question())
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

tk.Label(root, text="", width=4, bg=mw_bg, font=nomal_font).grid(row=12, column=0)
tk.Label(root, text="", width=4, bg=mw_bg, font=nomal_font).grid(row=11, column=0)

# メインループ
root.mainloop()