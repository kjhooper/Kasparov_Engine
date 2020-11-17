# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 10:41:44 2020

@author: hoope
"""

import GUI_helpers as gh
import helpers as hp
import tkinter as tk
import chess
# import numpy as np
# import glob
# import PIL
# from PIL import ImageTk, Image

move_counter = 1


def clicked_2Player():
    game = Game_2Player()
    game_play = GamePlay_2Player(game)
    game_play.play()

def replay():
    """ current is of class GamePlay
    """
    gui = GameStart()
    gui.play()
    

class Game_Kasparov:
    
    def __init__(self, color):
        """ color: ['white', 'black']
        """
        self.color = color
        self.kasparov = "black"
        self.board = chess.Board()
        self.p_board = chess.Board()
        self.move_counter = 0
        self.moveFrom = gh.load_model("move from")
        self.moveTo = gh.load_model("move to")
        
        if color == 'black':
            self.kasparov = "white"
            fen = chess.Board().fen().split()
            fen[0] = fen[0][::-1]
            start_fen = " ".join(fen)
            self.p_board = chess.Board(fen=start_fen)
            self.move_counter = 1
            
class Game_2Player:
    
    def __init__(self):
        """ color: ['white', 'black']
        """
        self.color = "white"
        self.board = chess.Board()
        self.p_board = chess.Board()
        self.move_counter = 0


class mainStart:
    """ Uses tkinter
    """
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('ML Chess GUI')
        self.window.geometry('280x100')
        lbl = tk.Label(self.window, text='Choose your Game!')
        lbl.grid(column=1, row=0)
        
        btn_w = tk.Button(self.window, text='Verse Garry Kasparov', bg='white', fg='black', 
                          command=self._end_Kasparov)
        btn_w.grid(column=0, row=1)
        btn_b = tk.Button(self.window, text='2 Player', bg='white', fg='black', 
                          command=self._end_2player)
        btn_b.grid(column=2, row=1)
        
        
    def play(self):
        self.window.mainloop()
    def _end_2player(self):
        self.window.destroy()
        clicked_2Player()
    def _end_Kasparov(self):
        self.window.destroy()
        Kasparov_GameStart().window.mainloop()
        

class Kasparov_GameStart:
            
    def __init__(self):
        
        self.window = tk.Tk()
        self.window.title('ML Chess GUI')
        lbl = tk.Label(self.window, text='What colour do you want to be?')
        lbl.grid(column=1, row=0)
        self.window.geometry('280x100')
        btn_w = tk.Button(self.window, text='White', bg='white', fg='black', 
                          command=self._end_w)
        btn_w.grid(column=0, row=1)
        btn_b = tk.Button(self.window, text='Black', bg='black', fg='white', 
                          command=self._end_b)
        btn_b.grid(column=2, row=1)   
        

    def _end_b(self):
        self.window.destroy()
        game = Game_Kasparov('black')
        game_play = GamePlay_Kasparov(game)
        game_play.play()
    
    def _end_w(self):
        self.window.destroy()
        game = Game_Kasparov('white')
        game_play = GamePlay_Kasparov(game)
        game_play.play()
    
        
        
class GamePlay_Kasparov:
    
    """ Uses tkinter
    """
    
    def __init__(self, game):
        self.game = game
        self.window = tk.Tk()
        self.b = None
        self.entry = None
        self.submit = None
        self.Listbox = None
        self.scroll = None
        self.move_counter = 1
        
            
        def make_move(*event):
            gh.kasparov_game(self)

        if game.kasparov == "white":
                gh.build_game_window(self, self._replay, "white", "green", 
                                     make_move, full_build=False)
                gh.kasparov_first_move(self)
        else:
            gh.build_game_window(self, self._replay, "white", "green", make_move)
            

    def play(self):
        self.window.mainloop()
        
    def _replay(self):
        self.window.destroy()
        new_game=mainStart()
        new_game.play()

class GamePlay_2Player:
    
    """ Uses tkinter
    """
    
    def __init__(self, game):
        self.game = game
        self.window = tk.Tk()
        self.b = None
        self.entry = None
        self.submit = None
        self.Listbox = None
        self.scroll = None
        self.move_counter = 1
            
        def make_move(*event):
            gh.player_move(self)                
            
        gh.build_game_window(self, self._replay, "white", "green", make_move)
        
        
    def play(self):
        self.window.mainloop()
        
    def _replay(self):
        self.window.destroy()
        new_game=mainStart()
        new_game.play()
        global move_counter
        move_counter = 1
  
if __name__ == "__main__":
    gui = mainStart()
    gui.play()