# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:05:43 2020

@author: hoope
"""
import numpy as np
import chess

square_dict = {1:2}

def make_array_complex(board, color="white"):
    """
    converts a type chess.Board to a 6x8x8x1 array based on piece

    Parameters
    ----------
    board : chess.Board
        chess board.

    Returns
    -------
    b_array : 6x8x8x1 dimensional array

    """        
    s = board.fen().split('/')
    s[-1] = s[-1][:8]
    b_array = np.zeros((8, 8))
 
    
    pawn_arr = np.zeros((8,8))
    knight_arr = np.zeros((8,8))
    bishop_arr = np.zeros((8,8))
    rook_arr = np.zeros((8,8))
    queen_arr = np.zeros((8,8))
    king_arr = np.zeros((8,8))
    
    row_index = 0
    for row in s:
        row = row.split(' ')[0]
        index = 0
        if not row.isnumeric():
            for char in row:
                if char.isnumeric():
                    for i in range(int(char)):
                        pawn_arr[row_index, index] = 0
                        knight_arr[row_index, index] = 0
                        bishop_arr[row_index, index] = 0
                        rook_arr[row_index, index] = 0
                        queen_arr[row_index, index] = 0
                        king_arr[row_index, index] = 0
                        index += 1
                elif char in 'pbnrqkPBNRQK':
                    val = 1
                    if char.islower():
                        val = -1
                    char = char.lower()
                    if char == 'p':
                        pawn_arr[row_index, index] = val
                    elif char == 'b':
                        bishop_arr[row_index, index] = val
                    elif char == 'n':
                        knight_arr[row_index, index] = val
                    elif char == 'r':
                        rook_arr[row_index, index] = val
                    elif char == 'q':
                        queen_arr[row_index, index] = val
                    elif char == 'k':
                        king_arr[row_index, index] = val
                    index += 1     
        row_index += 1
    if color == "black":
        pawn_arr = pawn_arr[:, ::-1]
        knight_arr = knight_arr[:, ::-1]
        bishop_arr = bishop_arr[:, ::-1]
        rook_arr = rook_arr[:, ::-1]
        queen_arr = queen_arr[:, ::-1]
        king_arr = king_arr[:, ::-1]
        
    b_array = np.array([pawn_arr.reshape((8,8,1)), bishop_arr.reshape((8,8,1)), 
                        knight_arr.reshape((8,8,1)), rook_arr.reshape((8,8,1)), 
                        queen_arr.reshape((8,8,1)), king_arr.reshape((8,8,1))])
    return b_array

def make_array_simple(board, color="white"):
    """
    converts a type chess.Board to a 6x8x8x1 array based on piece

    Parameters
    ----------
    board : chess.Board
        chess board.

    Returns
    -------
    b_array : 8x8 dimensional array

    """        
    piece_dict = {'p' : -1, 'P' : 1, 'b' : -2, 'B' : 2, 'n' : -3, 'N' : 3, 
                  'r' : -5, 'R' : 5, 'q' : -9, 'Q' : 9, 'k' : -50, 'K' : 50}
    
    s = board.fen().split('/')
    s[-1] = s[-1][:8]
    b_array = np.zeros((8, 8))

    row_index = 0
    for row in s:
        row = row.split(' ')[0]
        index = 0
        if not row.isnumeric():
            for char in row:
                if char.isnumeric():
                    for i in range(int(char)):
                        b_array[row_index, index] = 0
                        index += 1
                elif char in 'pbnrqkPBNRQK':
                    b_array[row_index, index] = piece_dict[char]
                    index += 1           
        row_index += 1
    if color == "black":
        b_array = b_array[:, ::-1]
        
    return b_array.reshape((64,))

# print(make_array_simple(chess.Board()), np.shape(make_array_simple(chess.Board())))



def make_move(board, move, color="white"):
    board.push_san(move)
    return make_array_simple(board, color=color)

def clean_moves(str_of_moves):
    """
    creates a list of strings of moves where white player moves are [::2] 
    and black player moves are [1::2]

    Parameters
    ----------
    str_of_moves : str
        moves as shown in pgn file.

    Returns
    -------
    spl : list
        list of individual moves.

    """
    
    spl = str_of_moves.split(' ')
    for item in spl:
        if '.' in item:
            spl.remove(item)
    return spl


def get_sq_index(sq_str, color="white"):
    index_dict = {"a": 0, "b": 1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    if color == "black":
        sq_index = 0
        sq_index += index_dict[sq_str[0]]
        return sq_index + (int(sq_str[1]) - 1) * 8
    else:
        sq_index = 63
        sq_index -= index_dict[sq_str[0]]
        return sq_index - (int(sq_str[1]) - 1) * 8

def index2sq(index, color):
    sq_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
    sq = ""
    if color == "black":
        sq += sq_list[index%8]
        return sq + str(index // 8 + 1)
    else:
        sq += sq_list[::-1][index%8]
        return sq + str(-(index // 8) + 8)
