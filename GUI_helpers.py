# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 10:41:25 2020

@author: hoope
"""

import helpers as hp
from tensorflow import keras
import keras.models as km
import keras.layers as kl
from keras import metrics
import chess
import numpy as np
import GUI_helpers as gh
import helpers as hp
import tkinter as tk
import chess
import numpy as np
import glob
import PIL
from PIL import ImageTk, Image


def load_model(model_choice):
    
    model = km.Sequential()
    model.add(kl.Conv3D(64, kernel_size=(6, 5, 5), 
                               input_shape=(6, 8, 8, 1), activation='tanh'))
    model.add(kl.Conv3D(64, kernel_size=(1, 3, 3), 
                               input_shape=(6, 8, 8, 1), activation='tanh'))
    model.add(kl.Conv3D(64, kernel_size=(1, 1, 1), 
                               input_shape=(6, 8, 8, 1), activation='tanh'))
    model.add(kl.Flatten())
    model.add(kl.Dense(name='output', units=64))
    model.compile(optimizer='rmsprop', 
                         metrics=['accuracy','categorical_accuracy'],
                         loss='mean_squared_error')
    
    if model_choice == "move from":
        model.load_weights('Kasparov_moveFrom_complex_400.hdf5')
    else:
        model.load_weights('Kasparov_moveTo_complex_400.hdf5')
    
    return (model)

def build_board(game, b, window):
    pieces = [ImageTk.PhotoImage(Image.open(name)) for name in glob.glob("piece_pngs/*")]
    
    pieces_dict = {"b": pieces[0], "B": pieces[1], "k": pieces[2], 
               "K": pieces[3], "n" : pieces[4], "N": pieces[5], 
               "p" : pieces[6], "P": pieces[7], "q": pieces[8], 
               "Q": pieces[9], "r": pieces[10], "R": pieces[11]}
    
    sq_color = {True: "white", False: "green", "white":True, "black":False}
    turn = sq_color[game.color]
    letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
    x_vals = np.arange(50, 450, 50)
    y_vals = np.arange(75, 475, 50)
    nums = np.arange(8, 0, -1)
    if not turn:
        letters = letters[::-1]
        nums = nums[::-1]
        turn = not turn
        
    for i in range(8):
        b.create_text(x_vals[i], 465, text=letters[i], tags=("axis"))
        
    for i in range(8):
        b.create_text(15, y_vals[i], text=str(nums[i]), tags=("axis"))  
    board = game.board.fen().split(" ")[0]
    if game.color == "black":
        board = board[::-1]
    
    x, y= 50, 75  
    for char in board:
        try:
            b.create_image(x, y, image=pieces_dict[char], tags=("pieces", char))
            x += 50
        except KeyError:
            if char == "/":
                x = 50
                y += 50
            elif char.isdigit():
                x += 50 * int(char)
    window.mainloop()

# define fn to build chess board
def create_board_base(b, game, light_sq_color, dark_sq_color):
        sq_color = {True: light_sq_color, False: dark_sq_color, 
                    "white":True, "black":False}
        turn = sq_color[game.color]
        x_vals = np.arange(50, 450, 50)
        y_vals = np.arange(75, 475, 50)

        for x in np.arange(25, 425, 50):
            for y in np.arange(50, 450, 50):
                b.create_rectangle(x, y, x+50, y+50, fill=sq_color[turn])
                turn = not turn
            turn = not turn 
        b.pack()

def build_game_window_base(window, replay_command):
        window.title('ML Chess GUI')
        window.resizable(width="false", height="false")
        window.minsize(width=650, height=500)
        window.maxsize(width=650, height=500)
        menu = tk.Menu(window)
        menu.add_command(label='New Game', command=replay_command)
        window.config(menu=menu)

def build_game_window(gameplay, replay_command, 
                      light_sq_color, dark_sq_color, move_command, 
                      full_build=True):

        build_game_window_base(gameplay.window, replay_command)
        
        gameplay.b = tk.Canvas(gameplay.window, width=610, height=500)
        gameplay.b.create_text(225, 25, text='You Vs Garry Kasparov Chess Engine')
        create_board_base(gameplay.b, gameplay.game, light_sq_color, 
                          dark_sq_color)
        
        gameplay.entry = tk.Entry(gameplay.window)
        gameplay.b.create_window(450, 50, window=gameplay.entry, anchor="nw")
        gameplay.submit = tk.Button(text="Move", command=move_command)
        gameplay.window.bind("<Return>", move_command)
        gameplay.b.create_window(580, 45, window=gameplay.submit, anchor="nw")
        
        gameplay.Listbox = tk.Listbox(gameplay.window, width=25, height=16)
        gameplay.scroll = tk.Scrollbar(gameplay.window, orient="vertical", 
                          command=gameplay.Listbox.yview)
        gameplay.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        gameplay.b.create_window(450, 75, window=gameplay.Listbox, anchor="nw")
        gameplay.b.create_window(585, 77, window=gameplay.scroll, anchor="nw")
        gameplay.b.create_text(450, 350, anchor="nw", 
                           text="Rules:\n1) You must enter the SAN \n"+5*" " + 
                           "version of your move\n2) if you are going to " + 
                           "promote\n" + 5*" "+"a piece you must in t"+"he\n" +
                           5*" "+"form of the example:\n"+21*" "+"c8=q")
        if full_build:
            build_board(gameplay.game, gameplay.b, gameplay.window)
        

# define fn to help in make_move method
def change_board(game, move):
    try:
        game.board.push_san(move)
    except:
        return(False)


def insert_valid_in_listbox(gameplay):
    san = chess.Board().variation_san(gameplay.game.board.move_stack).split(".")
    move_print = san[-2][-1] +"." + san[-1]
    if gameplay.Listbox != None:
        if gameplay.Listbox.get(tk.END) == "ILLEGAL MOVE":
            gameplay.Listbox.delete(tk.END)
        if len(gameplay.Listbox.get(tk.END).split(" ")) == 2:
            gameplay.Listbox.delete(tk.END)

    
    gameplay.b.pack()     
    gameplay.Listbox.insert(tk.END, move_print)
    gameplay.Listbox.configure(yscrollcommand=gameplay.scroll.set)
    gameplay.scroll.configure(command=gameplay.Listbox.yview)
    
    gameplay.move_counter += 1
    
    
def move_invalid(gameplay):
    if gameplay.Listbox.get(tk.END) != "ILLEGAL MOVE":
        gameplay.Listbox.insert(tk.END, "ILLEGAL MOVE")
    gameplay.Listbox.see(tk.END)
    gameplay.entry.delete(0, "end")
    gameplay.b.pack()
    gameplay.Listbox.configure(yscrollcommand=gameplay.scroll.set)
    gameplay.scroll.configure(command=gameplay.Listbox.yview)


def update_display(gameplay):
    gameplay.b.delete("pieces")
    gameplay.b.delete("axis")
    gameplay.b.pack()

    if gameplay.move_counter%2 == 0:
        gameplay.game.color = "black"
    else:
        gameplay.game.color = "white"
    build_board(gameplay.game, gameplay.b, gameplay.window)
    

def player_move(gameplay):
    move = gameplay.entry.get() 
    gameplay.entry.delete(0, "end")
    updated = change_board(gameplay.game, move)
    
    if updated != False:
        insert_valid_in_listbox(gameplay)
        update_display(gameplay)
    else:
        move_invalid(gameplay)

 
def get_move_predict(board, color, model_from, model_to):
    """
    Parameters
    ----------
    board : chess.Board
        DESCRIPTION.
    color : str
        allowed options: "white" or "black"
    model_from : keras.model.Sequential
        DESCRIPTION.
    model_to : keras.model.Sequential
        DESCRIPTION.

    Returns
    -------
    d_from : dict
        dictionary of confidence vs selected ohe.
    d_to : dict
        dictionary of confidence vs selected ohe.

    """
        
    board_array = np.array([hp.make_array_complex(board, color=color)], 
                           dtype="int32")
    legal_moves = [str(move) for move in board.legal_moves]
    move_from_ohe = model_from.predict(board_array)[0]
    move_to_ohe = model_to.predict(board_array)[0]
    
    
    
    legal_start_sq = [hp.get_sq_index(str(move)[:2], 
                                   color) for move in board.legal_moves]
    legal_end_sq = [hp.get_sq_index(str(move)[2:], 
                                   color) for move in board.legal_moves]
    
    d_from = {}
    d_to = {}
    
    # makes dictionary of confidence vs selected ohe
    
    for i in range(64):
        if i in legal_start_sq:
            if move_from_ohe[i] not in d_from:
                d_from[move_from_ohe[i]] = [i]
            else:
                d_from[move_from_ohe[i]].append(i)
        if i in legal_end_sq:
            if move_to_ohe[i] not in d_to:
                d_to[move_to_ohe[i]] = [i]
            else:
                d_to[move_to_ohe[i]].append(i)
    return d_from, d_to

    
def choose_kasparov_move(board, color, model_from, model_to):
    d_from, d_to = get_move_predict(board, color, model_from, model_to)
    
    legal_moves = board.legal_moves
    
    guess_uci = hp.index2sq(d_from[max(d_from)][0], color) + hp.index2sq(d_to[max(d_to)][0], color)
    move_uci = chess.Move.from_uci(guess_uci)
    
    while move_uci not in legal_moves:
  
        if max(d_from) > max(d_to): #decide based on model accuracy
            
            if len(d_to[max(d_to)]) == 1:
                d_to.pop(max(d_to))
                guess_uci = guess_uci[:2] + hp.index2sq(d_to[max(d_to)][0], color)
                move_uci = chess.Move.from_uci(guess_uci)
            else:
                d_to[max(d_to)].pop(0)
                guess_uci = guess_uci[:2] + hp.index2sq(d_to[max(d_to)][0], color)
                move_uci = chess.Move.from_uci(guess_uci)
        else:
            if len(d_from[max(d_from)]) == 1:
                d_from.pop(max(d_from))
                guess_uci = hp.index2sq(d_from[max(d_from)][0],
                                     color) + guess_uci[2:]
                move_uci = chess.Move.from_uci(guess_uci)
            else:
                d_from[max(d_from)].pop(0)
                guess_uci = hp.index2sq(d_from[max(d_from)][0], 
                                     color) + guess_uci[2:]
                move_uci = chess.Move.from_uci(guess_uci)    
        
    return guess_uci 
           
 
def kasparov_game(gameplay):
    move = gameplay.entry.get() 
    gameplay.entry.delete(0, "end")
    updated = change_board(gameplay.game, move)
    
    if updated != False:
        insert_valid_in_listbox(gameplay)
        k_move = choose_kasparov_move(gameplay.game.board, gameplay.game.kasparov, 
                              gameplay.game.moveFrom, gameplay.game.moveTo)
        gameplay.game.board.push_uci(k_move)
        insert_valid_in_listbox(gameplay)
        gameplay.b.delete("pieces")
        build_board(gameplay.game, gameplay.b, gameplay.window)
        
    else:
        move_invalid(gameplay)
        

def kasparov_first_move(gameplay):
    
    k_move = choose_kasparov_move(gameplay.game.board, gameplay.game.kasparov, 
                          gameplay.game.moveFrom, gameplay.game.moveTo)
    gameplay.game.board.push_uci(k_move)
    insert_valid_in_listbox(gameplay)
    
    gameplay.b.delete("pieces")
    build_board(gameplay.game, gameplay.b, gameplay.window)
    
    