# -*- coding: utf-8 -*-
"""
Chess Engine based on Garry Kasparov
Script by: Katrina Hooper

This imports the data using pandas to create a database for the data and saves
it in a database so the training data and test data stays consistent


https://erikbern.com/2014/11/29/deep-learning-for-chess.html
https://deepmind.com/blog/article/alphazero-shedding-new-light-grand-games-chess-shogi-and-go



ideas:
    given 8X8, 2 networks, 1 to chose space to move from, 1 to chose space
    to move
    
    -> 8x8 -> 1x64? -> 1x64
    
    
"""
import helpers as hp
import csv
import pandas as pd
import numpy as np
import chess
import keras.utils as ku
from sklearn.model_selection import train_test_split

# file_name = "GarryKasparov-cleaned-short.csv"
file_name = "GarryKasparov-cleaned.csv"

data = pd.read_csv(file_name)

x = [] # opponents board, input
sq_from = []
sq_to = []
move_ucis = []

w_x = []
w_sq_from = []
w_sq_to = []
w_move_ucis = []

b_x = []
b_sq_from = []
b_sq_to = []
b_move_ucis = []


for i in range(len(data)):
    board = chess.Board()
    game = data.iloc[i,:]
    moves = hp.clean_moves(game['moves']) 
    if len(moves) > 23:
        if 'Kasparov' in game['white']:
            x.append(hp.make_array_complex(board))
            b_x.append(hp.make_array_complex(board))
            count = 0 # move count          
            if len(moves) % 2 == 0:
                moves = moves[:-1]
            for move in moves:
                board.push_san(move)
                if count % 2 == 1:
                    x.append(hp.make_array_complex(board)) #do i need to attach the board??
                    b_x.append(hp.make_array_complex(board))
                else:
                    move_uci = str(board.move_stack[-1])
                    move_ucis.append(move_uci)
                    sq_from.append(hp.get_sq_index(move_uci[:2]))
                    sq_to.append(hp.get_sq_index(move_uci[2:]))     
                    b_sq_from.append(hp.get_sq_index(move_uci[:2]))
                    b_sq_to.append(hp.get_sq_index(move_uci[2:])) 
                    b_move_ucis.append(move_uci)
                count += 1
        
        else:
            if len(moves) % 2 == 1:
                moves = moves[:-1]
            count = 0
            for move in moves:
                board.push_san(move)
                black_fen_spl = board.fen().split(' ')
                black_fen_spl[0] = black_fen_spl[0][::-1]
                black_fen = " ".join(black_fen_spl)            
                temp = chess.Board(black_fen)
                if count % 2 == 0:
                    x.append(hp.make_array_complex(temp, color="black")) # so it always pretends to be white
                    w_x.append(hp.make_array_complex(temp, color="black"))
                else:
                    move_uci = str(board.move_stack[-1])
                    move_ucis.append(move_uci)
                    sq_from.append(hp.get_sq_index(move_uci[:2], color="black"))
                    sq_to.append(hp.get_sq_index(move_uci[2:], color="black"))     
                    w_sq_from.append(hp.get_sq_index(move_uci[:2], color="black"))
                    w_sq_to.append(hp.get_sq_index(move_uci[2:], color="black"))   
                    w_move_ucis.append(move_uci)
                count += 1
                
                 
# this creates a one hot encoded vector used to classify which piece was chosen
sq_from_ohe = ku.to_categorical(sq_from, num_classes=64)
sq_to_ohe = ku.to_categorical(sq_to, num_classes=64)

w_sq_from_ohe = ku.to_categorical(w_sq_from, num_classes=64)
w_sq_to_ohe = ku.to_categorical(w_sq_to, num_classes=64)

b_sq_from_ohe = ku.to_categorical(b_sq_from, num_classes=64)
b_sq_to_ohe = ku.to_categorical(b_sq_to, num_classes=64)




# # generate train and test data             
split_data = train_test_split(x, sq_from_ohe, sq_to_ohe, move_ucis)
w_split_data = train_test_split(w_x, w_sq_from_ohe, w_sq_to_ohe, w_move_ucis)
b_split_data = train_test_split(b_x, b_sq_from_ohe, b_sq_to_ohe, b_move_ucis)

# the ouput form train_test_split gave in type list, model requires type np.array


# np.save('x_train_short.npy', np.array(split_data[0]), allow_pickle=True)
# np.save('x_test_short.npy', np.array(split_data[1]), allow_pickle=True)
# np.save('sq_from_train_short.npy', np.array(split_data[2]), allow_pickle=True)
# np.save('sq_from_test_short.npy', np.array(split_data[3]), allow_pickle=True)
# np.save('sq_to_train_short.npy', np.array(split_data[4]), allow_pickle=True)
# np.save('sq_to_test_short.npy', np.array(split_data[5]), allow_pickle=True)
# np.save('ucis_train_short.npy', np.array(split_data[6]), allow_pickle=True)
# np.save('ucis_test_short.npy', np.array(split_data[7]), allow_pickle=True)

# np.save('w_x_train_short.npy', np.array(w_split_data[0]), allow_pickle=True)
# np.save('w_x_test_short.npy', np.array(w_split_data[1]), allow_pickle=True)
# np.save('w_sq_from_train_short.npy', np.array(w_split_data[2]), allow_pickle=True)
# np.save('w_sq_from_test_short.npy', np.array(w_split_data[3]), allow_pickle=True)
# np.save('w_sq_to_train_short.npy', np.array(w_split_data[4]), allow_pickle=True)
# np.save('w_sq_to_test_short.npy', np.array(w_split_data[5]), allow_pickle=True)
# np.save('w_ucis_train_short.npy', np.array(w_split_data[6]), allow_pickle=True)
# np.save('w_ucis_test_short.npy', np.array(w_split_data[7]), allow_pickle=True)

# np.save('b_x_train_short.npy', np.array(b_split_data[0]), allow_pickle=True)
# np.save('b_x_test_short.npy', np.array(b_split_data[1]), allow_pickle=True)
# np.save('b_sq_from_train_short.npy', np.array(b_split_data[2]), allow_pickle=True)
# np.save('b_sq_from_test_short.npy', np.array(b_split_data[3]), allow_pickle=True)
# np.save('b_sq_to_train_short.npy', np.array(b_split_data[4]), allow_pickle=True)
# np.save('b_sq_to_test_short.npy', np.array(b_split_data[5]), allow_pickle=True)
# np.save('b_ucis_train_short.npy', np.array(b_split_data[6]), allow_pickle=True)
# np.save('b_ucis_test_short.npy', np.array(b_split_data[7]), allow_pickle=True)


np.save('x_train_complex.npy', np.array(split_data[0]), allow_pickle=True)
np.save('x_test_complex.npy', np.array(split_data[1]), allow_pickle=True)
np.save('sq_from_train_complex.npy', np.array(split_data[2]), allow_pickle=True)
np.save('sq_from_test_complex.npy', np.array(split_data[3]), allow_pickle=True)
np.save('sq_to_train_complex.npy', np.array(split_data[4]), allow_pickle=True)
np.save('sq_to_test_complex.npy', np.array(split_data[5]), allow_pickle=True)
np.save('ucis_train_complex.npy', np.array(split_data[6]), allow_pickle=True)
np.save('ucis_test_complex.npy', np.array(split_data[7]), allow_pickle=True)


np.save('w_x_train_complex.npy', np.array(w_split_data[0]), allow_pickle=True)
np.save('w_x_test_complex.npy', np.array(w_split_data[1]), allow_pickle=True)
np.save('w_sq_from_train_complex.npy', np.array(w_split_data[2]), allow_pickle=True)
np.save('w_sq_from_test_complex.npy', np.array(w_split_data[3]), allow_pickle=True)
np.save('w_sq_to_train_complex.npy', np.array(w_split_data[4]), allow_pickle=True)
np.save('w_sq_to_test_complex.npy', np.array(w_split_data[5]), allow_pickle=True)
np.save('w_ucis_train_complex.npy', np.array(w_split_data[6]), allow_pickle=True)
np.save('w_ucis_tes_complext.npy', np.array(w_split_data[7]), allow_pickle=True)

np.save('b_x_train_complex.npy', np.array(b_split_data[0]), allow_pickle=True)
np.save('b_x_test_complex.npy', np.array(b_split_data[1]), allow_pickle=True)
np.save('b_sq_from_train_complex.npy', np.array(b_split_data[2]), allow_pickle=True)
np.save('b_sq_from_test_complex.npy', np.array(b_split_data[3]), allow_pickle=True)
np.save('b_sq_to_train_complex.npy', np.array(b_split_data[4]), allow_pickle=True)
np.save('b_sq_to_test_complex.npy', np.array(b_split_data[5]), allow_pickle=True)
np.save('b_ucis_train_complex.npy', np.array(b_split_data[6]), allow_pickle=True)
np.save('b_ucis_test_complex.npy', np.array(b_split_data[7]), allow_pickle=True)

        