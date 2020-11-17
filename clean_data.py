# -*- coding: utf-8 -*-
"""
Chess Engine based on Garry Kasparov
Script by: Katrina Hooper

This code is to take in, organize and clean training/test data into a usable 
set
"""

from chess import pgn
import csv


#pgn_file = open('GarryKasparov-short.pgn')
pgn_file = open('GarryKasparov.pgn')

# this is similar to the read funtion for documents, but reads whole games
game = pgn.read_game(pgn_file)
next_game = pgn.read_game(pgn_file)


with open('GarryKasparov-cleaned.csv', 'a') as csvfile:
#with open('GarryKasparov-cleaned-short2.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    # Writes headers for columns
    writer.writerow(['white', 'black', 'result', 'moves'])
    # Iterates through file to parse data to find important data and writes into a csv file
    while next_game != None:
        # ensures all games have moves and Garry Kasparov as one of the players
        if game.headers['White'] != '?' and game.headers['Black'] != '?':
            writer.writerow([str(game.headers['White']), str(game.headers['Black']), 
                        str(game.headers['Result']), game.mainline()])
        game = next_game
        next_game = pgn.read_game(pgn_file)
                
pgn_file.close()