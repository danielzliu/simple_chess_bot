# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 16:20:20 2021

@author: Daniel
"""

import framework
import tree_structure



def convert_input(input_str):
    
    #return piece_name, from_x, from_y, to_x, to_y, castle
    
    x_dict = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    y_dict = {'1':0, '2':1, '3':2, '4':3, '5':4, '6':5, '7':6, '8':7}
    
    if input_str == 'castle queenside white':
        return 'king', 4, 0, 2, 0, True
    
    elif input_str == 'castle kingside white':
        return 'king', 4, 0, 6, 0, True
    
    elif input_str == 'castle queenside black':
        return 'king', 4, 7, 2, 7, True
    
    elif input_str == 'castle queenside black':
        return 'king', 4, 7, 6, 7, True
    
    else:
        try:
            input_lst = input_str.split()
            piece_name = input_lst[0]
            
            from_square = input_lst[1]
            to_square = input_lst[2]
            
            from_x = x_dict[from_square[0]]
            to_x = x_dict[to_square[0]]
            
            from_y = y_dict[from_square[1]]
            to_y = y_dict[to_square[1]]
            
            castle = False
            
            return piece_name, from_x, from_y, to_x, to_y, castle
            
        except:
            print('Invalid input. Try again.')
            
            return None,None,None,None,None, None
        
    
    
def check_if_piece_exists(board_obj, piece_name, xpos, ypos):
    if board_obj.board[xpos][ypos] != None:
        if board_obj.board[xpos][ypos].name == piece_name:
            return True
            
    return False


    
def test1(board_obj):
    node = tree_structure.Node(0, 4, board_obj) 
    node.suggest_move()
    
    


#Create board
board_obj = framework.load_starting_state()

#board_obj.display()
print('')



while True:
#White moves
    node = tree_structure.Node(0, 4, board_obj) 
    node.suggest_move()
    print('')
    
    board_obj = node.optimal_child.current_state
    board_obj.display()
    print('')
    
    
    
    input_ok = False
    
    while input_ok == False:
    
        input_str = input('Your turn: ')
        
        piece_name, from_xpos, from_ypos, to_xpos, to_ypos, castle = convert_input(input_str)
    
        if piece_name != None:
            piece_exists = check_if_piece_exists(board_obj, piece_name, from_xpos, from_ypos)
            
            if piece_exists == False:
                print('There is no ' + piece_name + ' on ' + 'the selected square!')
    
            else:
                input_ok = True
                
    board_obj.move_piece(from_xpos, from_ypos, to_xpos, to_ypos, castle = castle)
                


#input_text = input('Make a move: ')