# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 15:32:24 2021

@author: Daniel
"""

import copy


#TODO_
#en passant
#promoted pawn - OK can only do queen for now
#first take king first win - does this matter though?
#castling - OK


class Board:
    
    def __init__(self):
        
        #Create empty board 
        
        self.board = [[None] * 8 for i in range(8)]
        self.players_turn = 'white'
        self.castling_available_w_ks = True #If enpassant is available for white kingside
        self.castling_available_w_qs = True
        self.castling_available_b_ks = True
        self.castling_available_b_qs = True
    
    def copy(self):
        new_obj = Board()
        
        for row in self.board:
            for piece in row:
                if piece != None:
                    color = piece.color
                    name = piece.name
                    xpos = piece.xpos
                    ypos = piece.ypos
                    
                    new_obj.place_piece(color, name, xpos, ypos)
            
        

        new_obj.players_turn = self.players_turn
        new_obj.castling_available_w_ks = self.castling_available_w_ks
        new_obj.castling_available_w_qs = self.castling_available_w_qs
        new_obj.castling_available_b_ks = self.castling_available_b_ks
        new_obj.castling_available_b_qs = self.castling_available_b_qs
        
        return new_obj
    
        
        
    
    def score_board(self):
        
        white_score = 0
        black_score = 0
        
        for xpos in range(8):
            for ypos in range(8):
                
                #Material
                if self.board[xpos][ypos] != None:
                    
                    if self.board[xpos][ypos].color == 'white':
                        white_score = white_score + self.board[xpos][ypos].get_piece_value()
                        
                    elif self.board[xpos][ypos].color == 'black':
                        black_score = black_score + self.board[xpos][ypos].get_piece_value()
                        
                #Center control
                if ypos == 4 and xpos in [3,4]:
                    if self.board[xpos][ypos] == None:
                        white_score = white_score + 0.1
                        
                    elif self.board[xpos][ypos] != None:
                        if self.board[xpos][ypos].color != 'black':
                            white_score = white_score + 0.1
                            
                elif ypos == 3 and xpos in [3,4]:
                    if self.board[xpos][ypos] == None:
                        black_score = black_score + 0.1
                        
                    elif self.board[xpos][ypos] != None:
                        if self.board[xpos][ypos].color != 'white':
                            black_score = black_score + 0.1
                            
                #Development of minor pieces
                elif ypos == 0 and xpos in [1,2,5,6]:
                    if self.board[xpos][ypos] == None:
                        white_score = white_score + 0.05
                        
                elif ypos == 7 and xpos in [1,2,5,6]:
                    if self.board[xpos][ypos] == None:
                        black_score = black_score + 0.05
                
        score = white_score - black_score
        
        return score
        
    
    
    def find_all_feasible_moves(self):
        #Finds all feasible moves for the player whom has their turn
        all_feasible_moves = []
        
        color = self.players_turn
        
        for row in self.board:
            for piece in row:
                if piece != None:
                    if piece.color == color:
                        feasible_moves = piece.calculate_feasible_moves(self)
                        all_feasible_moves.extend(feasible_moves)
        
        return all_feasible_moves
            
    
    def display(self):
        
        #Reverses the board so it becomes more intuitive
        
        reversed_board = list(map(list, zip(*self.board)))
        
        reversed_board = list(reversed(reversed_board))
            
        for row in reversed_board:
            print('{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}'.format(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5]),str(row[6]),str(row[7])))

            
            
    
    
    def place_test(self, xpos, ypos):
        
        self.board[xpos][ypos] = 1
        
    
    
    
    def place_piece(self, color, name, xpos, ypos):
        
        if name == 'pawn':
            self.board[xpos][ypos] = Pawn(color, name, xpos, ypos)
        
        elif name == 'rook':
            self.board[xpos][ypos] = Rook(color, name, xpos, ypos)
        
        elif name == 'knight':
            self.board[xpos][ypos] = Knight(color, name, xpos, ypos)
        
        elif name == 'bishop':
            self.board[xpos][ypos] = Bishop(color, name, xpos, ypos)
        
        elif name == 'queen':
            self.board[xpos][ypos] = Queen(color, name, xpos, ypos)
        
        elif name == 'king':
            self.board[xpos][ypos] = King(color, name, xpos, ypos)
       
        
       
    def remove_piece(self, xpos, ypos):
        
        self.board[xpos][ypos] = None
    
    
    def move_piece(self, from_xpos, from_ypos, to_xpos, to_ypos, print_move = True, promote_to = 'queen', castle = False):
        
        moving_piece = self.board[from_xpos][from_ypos]
        
        moving_piece.xpos = to_xpos
        moving_piece.ypos = to_ypos
        
        self.remove_piece(from_xpos, from_ypos)
        self.remove_piece(to_xpos, to_ypos)
        
        #If pawn reaches back rank, promote it
        if (moving_piece.name == 'pawn' and to_ypos == 7 and moving_piece.color == 'white') or (moving_piece.name == 'pawn' and to_ypos == 0 and moving_piece.color == 'black'):
            self.board[to_xpos][to_ypos] = Queen(moving_piece.color, promote_to, to_xpos, to_ypos)
        
        #If king moves
        elif moving_piece.name == 'king':
            
            #Disable castling
            if moving_piece.color == 'white':        
                self.castling_available_w_ks = False
                self.castling_available_w_qs = False
        
            elif moving_piece.color =='black':
                self.castling_available_b_ks = False
                self.castling_available_w_qs = False
                
            if castle == True:
                
                if to_xpos == 2:
                    rook = self.board[0][from_ypos]
                    #Move the king
                    self.board[to_xpos][from_ypos] = moving_piece
                    
                    #Move the rook
                    rook.xpos = 3
                    self.remove_piece(0, from_ypos)
                    self.board[3][from_ypos] = rook
                    
                elif to_xpos == 6:
                    rook = self.board[7][from_ypos]
                    
                    #Move the king
                    self.board[to_xpos][from_ypos] = moving_piece
                    #Move the rook
                    rook.xpos = 5
                    self.remove_piece(7, from_ypos)
                    self.board[5][from_ypos] = rook
                
            else:
                self.board[to_xpos][to_ypos] = moving_piece
                
        #If rook moves
        elif moving_piece.name == 'rook':
            moving_piece.rook_can_castle = False
            self.board[to_xpos][to_ypos] = moving_piece
            
        else:
            self.board[to_xpos][to_ypos] = moving_piece
            
        self.pass_turn()
        
        
        
        
    def promote_pawn(self, xpos, ypos, promote_to):
        
        color = self.board[xpos][ypos].color
        
        self.remove_piece(xpos, ypos)
        self.place_piece(color, promote_to, xpos, ypos)
        
        
        
    def pass_turn(self):
        #Passes the turn over to the other player
        #Figurativelty hits the clock
        
        if self.players_turn == 'white':
            self.players_turn = 'black'
                
        elif self.players_turn == 'black':
            self.players_turn = 'white'
            
        
        




class Piece:
    
    def __init__(self, color, name, xpos, ypos):
        
        self.color = color #white, black
        self.name = name#pawn, rook, knight, bishop, queen, king
        self.xpos = xpos #0 to 7
        self.ypos = ypos #0 to 7
        self.pawn_just_doublemoved = False
        self.rook_can_castle = True
        
    def __repr__(self):
        
        return self.color + '.' + self.name
    
    def __str__(self):
        return self.color + '.' + self.name
                
        
    def get_piece_value(self):
        #Returns the value of a piece
        
        if self.name == 'pawn':
            piece_value = 1
        
        elif self.name == 'rook':
            piece_value = 5
        
        elif self.name == 'knight':
            piece_value = 3
        
        elif self.name == 'bishop':
            piece_value = 3
        
        elif self.name == 'queen':
            piece_value = 9
        
        elif self.name == 'king':
            piece_value = 1000
            
        return piece_value
        

    def calculate_feasible_moves(self, board_obj):
        #Calculates feasible moves a piece can make
        #Returns moves and feasible board states
        
        pass


class Pawn(Piece):
    
    
    def calculate_feasible_moves(self, board_obj):
        
        feasible_moves = []
        
        from_xpos = self.xpos
        from_ypos = self.ypos
        
        
        if self.color == 'white':
            
            #Can move forward one square if the square is not taken
            if board_obj.board[from_xpos][from_ypos + 1] == None:

                to_xpos = from_xpos
                to_ypos = from_ypos + 1 
                
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos, to_ypos)
                feasible_moves.append([command, new_board_obj])
                
            #Can move diagonally left if there is a black piece there (assuming not at the edge of the board)
            if from_xpos != 0:
                if board_obj.board[from_xpos - 1][from_ypos + 1] != None :
                    if board_obj.board[from_xpos - 1][from_ypos + 1].color == 'black':
                        to_xpos = from_xpos - 1
                        to_ypos = from_ypos + 1                        
                        
                        new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos, to_ypos)
                        feasible_moves.append([command, new_board_obj])
                        
            #Can move diagonally right if there is a black piece there (assuming not at the edge of the board)
            if from_xpos != 7:
                if board_obj.board[from_xpos + 1][from_ypos + 1] != None :
                    if board_obj.board[from_xpos + 1][from_ypos + 1].color == 'black':
                        to_xpos = from_xpos + 1
                        to_ypos = from_ypos + 1                        
                        
                        new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos, to_ypos)
                        feasible_moves.append([command, new_board_obj])
                        
            #Can move 2 steps if it is on the starting row
            
            if from_ypos == 1:
                if board_obj.board[from_xpos][from_ypos + 1] == None and board_obj.board[from_xpos][from_ypos + 2] == None:
                    to_xpos = from_xpos
                    to_ypos = from_ypos + 2 
                    
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos, to_ypos)
                    feasible_moves.append([command, new_board_obj])
            
            
            
            #en passant not implemented yet
            
        
        
        
        elif self.color == 'black':
            
            #Can move down one square if the square is not taken
            if board_obj.board[from_xpos][from_ypos - 1] == None:
                to_xpos = from_xpos
                to_ypos = from_ypos - 1 
                
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos, to_ypos)
                feasible_moves.append([command, new_board_obj])
                
            #Can move diagonally left if there is a black piece there (assuming not at the edge of the board)
            if from_xpos != 0:
                if board_obj.board[from_xpos - 1][from_ypos - 1] != None :
                    if board_obj.board[from_xpos - 1][from_ypos - 1].color == 'white':
                        to_xpos = from_xpos - 1
                        to_ypos = from_ypos -1                        
                        
                        new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos, to_ypos)
                        feasible_moves.append([command, new_board_obj])
                        
            #Can move diagonally right if there is a black piece there (assuming not at the edge of the board)
            if from_xpos != 7:
                if board_obj.board[from_xpos + 1][from_ypos - 1] != None :
                    if board_obj.board[from_xpos + 1][from_ypos - 1].color == 'white':
                        to_xpos = from_xpos + 1
                        to_ypos = from_ypos - 1                        
                        
                        new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos, to_ypos)
                        feasible_moves.append([command, new_board_obj])
                        
            #Can move 2 steps if it is on the starting row
            
            if from_ypos == 6:
                if board_obj.board[from_xpos][from_ypos - 1] == None and board_obj.board[from_xpos][from_ypos - 2] == None:
                    to_xpos = from_xpos
                    to_ypos = from_ypos - 2 
                    
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos, to_ypos)
                    feasible_moves.append([command, new_board_obj])
        
        
        return feasible_moves
        
        

class Rook(Piece):
    
    def calculate_feasible_moves(self, board_obj):
    
        feasible_moves = []
            
        from_xpos = self.xpos
        from_ypos = self.ypos
        
        
        
        #Move upwards until stopped
        to_ypos_potential = from_ypos + 1
        searching = True
        
        while searching == True and 0 <= to_ypos_potential <= 7:
            
            if board_obj.board[from_xpos][to_ypos_potential] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, from_xpos, to_ypos_potential)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[from_xpos][to_ypos_potential] != None:
                
                if board_obj.board[from_xpos][to_ypos_potential].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, from_xpos, to_ypos_potential)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_ypos_potential = to_ypos_potential + 1
                
            
            
        #Move downwards until stopped
        to_ypos_potential = from_ypos - 1
        searching = True
        
        while searching == True and 0 <= to_ypos_potential <= 7:
            
            if board_obj.board[from_xpos][to_ypos_potential] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, from_xpos, to_ypos_potential)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[from_xpos][to_ypos_potential] != None:
                
                if board_obj.board[from_xpos][to_ypos_potential].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, from_xpos, to_ypos_potential)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_ypos_potential = to_ypos_potential - 1



        #Move left until stopped
        to_xpos_potential = from_xpos - 1
        searching = True
        
        while searching == True and 0 <= to_xpos_potential <= 7:
            
            if board_obj.board[to_xpos_potential][from_ypos] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, from_ypos)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[to_xpos_potential][from_ypos] != None:
                
                if board_obj.board[to_xpos_potential][from_ypos].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, from_ypos)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_xpos_potential = to_xpos_potential - 1
            


        #Move right until stopped
        to_xpos_potential = from_xpos + 1
        searching = True
        
        while searching == True and 0 <= to_xpos_potential <= 7:
            
            if board_obj.board[to_xpos_potential][from_ypos] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, from_ypos)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[to_xpos_potential][from_ypos] != None:
                
                if board_obj.board[to_xpos_potential][from_ypos].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, from_ypos)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_xpos_potential = to_xpos_potential + 1
                
            
            
        return feasible_moves
                    
        
        



class Knight(Piece):
    
    def calculate_feasible_moves(self, board_obj):
        
        potential_knight_moves = [[1,2],[1,-2], [2,1], [2,-1], [-1,2], [-1,-2], [-2,1], [-2,-1]]
        feasible_moves = []
        
        from_xpos = self.xpos
        from_ypos = self.ypos
    
        #Evaluate all potential moves to see if they are feasible
        for potential_move in potential_knight_moves:
            
           to_xpos_potential = from_xpos + potential_move[0]
           to_ypos_potential = from_ypos + potential_move[1]
           
           if 0 <= to_xpos_potential <= 7 and 0 <= to_ypos_potential <= 7:
             
               #Can move to square if empty
               if board_obj.board[to_xpos_potential][to_ypos_potential] == None:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                    feasible_moves.append([command, new_board_obj])
               
                #Can move to square if there is a piece of the other color
               elif board_obj.board[to_xpos_potential][to_ypos_potential] != None:
                    if board_obj.board[to_xpos_potential][to_ypos_potential].color != self.color:
                        new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                        feasible_moves.append([command, new_board_obj])
                    
        return feasible_moves
            
                 
           
            

class Bishop(Piece):
    
    def calculate_feasible_moves(self, board_obj):
        
        feasible_moves = []
            
        from_xpos = self.xpos
        from_ypos = self.ypos
        
        #Move northeast until stopped
        
        to_xpos_potential = from_xpos + 1
        to_ypos_potential = from_ypos + 1
        searching = True
        
        while searching == True and 0 <= to_ypos_potential <= 7 and 0 <= to_xpos_potential <= 7:
            
            if board_obj.board[to_xpos_potential][to_ypos_potential] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[to_xpos_potential][to_ypos_potential] != None:
                
                if board_obj.board[to_xpos_potential][to_ypos_potential].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_xpos_potential = to_xpos_potential + 1
            to_ypos_potential = to_ypos_potential + 1
            
        #Move southeast until stopped
        
        to_xpos_potential = from_xpos + 1
        to_ypos_potential = from_ypos - 1
        searching = True
        
        while searching == True and 0 <= to_ypos_potential <= 7 and 0 <= to_xpos_potential <= 7:
            
            if board_obj.board[to_xpos_potential][to_ypos_potential] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[to_xpos_potential][to_ypos_potential] != None:
                
                if board_obj.board[to_xpos_potential][to_ypos_potential].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_xpos_potential = to_xpos_potential + 1
            to_ypos_potential = to_ypos_potential - 1
            
        #Move southwest until stopped
        
        to_xpos_potential = from_xpos - 1
        to_ypos_potential = from_ypos - 1
        searching = True
        
        while searching == True and 0 <= to_ypos_potential <= 7 and 0 <= to_xpos_potential <= 7:
            
            if board_obj.board[to_xpos_potential][to_ypos_potential] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[to_xpos_potential][to_ypos_potential] != None:
                
                if board_obj.board[to_xpos_potential][to_ypos_potential].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_xpos_potential = to_xpos_potential - 1
            to_ypos_potential = to_ypos_potential - 1
            
        #Move northwest until stopped
        
        to_xpos_potential = from_xpos - 1
        to_ypos_potential = from_ypos + 1
        searching = True
        
        while searching == True and 0 <= to_ypos_potential <= 7 and 0 <= to_xpos_potential <= 7:
            
            if board_obj.board[to_xpos_potential][to_ypos_potential] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[to_xpos_potential][to_ypos_potential] != None:
                
                if board_obj.board[to_xpos_potential][to_ypos_potential].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_xpos_potential = to_xpos_potential - 1
            to_ypos_potential = to_ypos_potential + 1

        return feasible_moves



class Queen(Piece):
    
    def calculate_feasible_moves(self, board_obj):
        
        feasible_moves = []
            
        from_xpos = self.xpos
        from_ypos = self.ypos
        
        #Move north until stopped
        to_ypos_potential = from_ypos + 1
        searching = True
        
        while searching == True and 0 <= to_ypos_potential <= 7:
            
            if board_obj.board[from_xpos][to_ypos_potential] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, from_xpos, to_ypos_potential)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[from_xpos][to_ypos_potential] != None:
                
                if board_obj.board[from_xpos][to_ypos_potential].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, from_xpos, to_ypos_potential)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_ypos_potential = to_ypos_potential + 1
                
            
            
        #Move south until stopped
        to_ypos_potential = from_ypos - 1
        searching = True
        
        while searching == True and 0 <= to_ypos_potential <= 7:
            
            if board_obj.board[from_xpos][to_ypos_potential] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, from_xpos, to_ypos_potential)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[from_xpos][to_ypos_potential] != None:
                
                if board_obj.board[from_xpos][to_ypos_potential].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, from_xpos, to_ypos_potential)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_ypos_potential = to_ypos_potential - 1



        #Move west until stopped
        to_xpos_potential = from_xpos - 1
        searching = True
        
        while searching == True and 0 <= to_xpos_potential <= 7:
            
            if board_obj.board[to_xpos_potential][from_ypos] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, from_ypos)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[to_xpos_potential][from_ypos] != None:
                
                if board_obj.board[to_xpos_potential][from_ypos].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, from_ypos)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_xpos_potential = to_xpos_potential - 1
            


        #Move east until stopped
        to_xpos_potential = from_xpos + 1
        searching = True
        
        while searching == True and 0 <= to_xpos_potential <= 7:
            
            if board_obj.board[to_xpos_potential][from_ypos] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, from_ypos)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[to_xpos_potential][from_ypos] != None:
                
                if board_obj.board[to_xpos_potential][from_ypos].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, from_ypos)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_xpos_potential = to_xpos_potential + 1
            
        #Move northeast until stopped
        
        to_xpos_potential = from_xpos + 1
        to_ypos_potential = from_ypos + 1
        searching = True
        
        while searching == True and 0 <= to_ypos_potential <= 7 and 0 <= to_xpos_potential <= 7:
            
            if board_obj.board[to_xpos_potential][to_ypos_potential] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[to_xpos_potential][to_ypos_potential] != None:
                
                if board_obj.board[to_xpos_potential][to_ypos_potential].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_xpos_potential = to_xpos_potential + 1
            to_ypos_potential = to_ypos_potential + 1
            
        #Move southeast until stopped
        
        to_xpos_potential = from_xpos + 1
        to_ypos_potential = from_ypos - 1
        searching = True
        
        while searching == True and 0 <= to_ypos_potential <= 7 and 0 <= to_xpos_potential <= 7:
            
            if board_obj.board[to_xpos_potential][to_ypos_potential] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[to_xpos_potential][to_ypos_potential] != None:
                
                if board_obj.board[to_xpos_potential][to_ypos_potential].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_xpos_potential = to_xpos_potential + 1
            to_ypos_potential = to_ypos_potential - 1
            
        #Move southwest until stopped
        
        to_xpos_potential = from_xpos - 1
        to_ypos_potential = from_ypos - 1
        searching = True
        
        while searching == True and 0 <= to_ypos_potential <= 7 and 0 <= to_xpos_potential <= 7:
            
            if board_obj.board[to_xpos_potential][to_ypos_potential] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[to_xpos_potential][to_ypos_potential] != None:
                
                if board_obj.board[to_xpos_potential][to_ypos_potential].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_xpos_potential = to_xpos_potential - 1
            to_ypos_potential = to_ypos_potential - 1
            
        #Move northwest until stopped
        
        to_xpos_potential = from_xpos - 1
        to_ypos_potential = from_ypos + 1
        searching = True
        
        while searching == True and 0 <= to_ypos_potential <= 7 and 0 <= to_xpos_potential <= 7:
            
            if board_obj.board[to_xpos_potential][to_ypos_potential] == None:
                new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                feasible_moves.append([command, new_board_obj])
                
            elif board_obj.board[to_xpos_potential][to_ypos_potential] != None:
                
                if board_obj.board[to_xpos_potential][to_ypos_potential].color != self.color:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                    feasible_moves.append([command, new_board_obj])
                    
                searching = False
                
            to_xpos_potential = to_xpos_potential - 1
            to_ypos_potential = to_ypos_potential + 1
            
        return feasible_moves
        
    
class King(Piece):
    
    def calculate_feasible_moves(self, board_obj):
        
        potential_knight_moves = [[1,1],[1,0], [1,-1], [0,1], [0,-1], [-1,1], [-1,0], [-1,-1]]
        feasible_moves = []
        
        from_xpos = self.xpos
        from_ypos = self.ypos
    
        #Evaluate all potential moves to see if they are feasible
        for potential_move in potential_knight_moves:
            
           to_xpos_potential = from_xpos + potential_move[0]
           to_ypos_potential = from_ypos + potential_move[1]
           
           if 0 <= to_xpos_potential <= 7 and 0 <= to_ypos_potential <= 7:
             
               #Can move to square if empty
               if board_obj.board[to_xpos_potential][to_ypos_potential] == None:
                    new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                    feasible_moves.append([command, new_board_obj])
               
               #Can move to square if there is a piece of the other color
               elif board_obj.board[to_xpos_potential][to_ypos_potential] != None:
                    if board_obj.board[to_xpos_potential][to_ypos_potential].color != self.color:
                        new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, to_xpos_potential, to_ypos_potential)
                        feasible_moves.append([command, new_board_obj])
                        
        #Castle if possible
        if self.color == 'white' and self.xpos ==4 and self.ypos == 0:
            if board_obj.castling_available_w_ks == True:
                if board_obj.board[5][0] == None and board_obj.board[6][0] == None and board_obj.board[7][0] != None:
                     if board_obj.board[7][0].name == 'rook' and board_obj.board[7][0].rook_can_castle == True:
                         new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, 6, from_ypos, castle = True)
                         feasible_moves.append([command, new_board_obj])
                         
            if board_obj.castling_available_w_qs == True:
                if board_obj.board[3][0] == None and board_obj.board[2][0] == None and board_obj.board[1][0] == None and board_obj.board[0][0] != None:
                     if board_obj.board[0][0].name == 'rook' and board_obj.board[0][0].rook_can_castle == True:
                         new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, 2, from_ypos, castle = True)
                         feasible_moves.append([command, new_board_obj])
                         
        elif self.color == 'black' and self.xpos == 4 and self.ypos == 7:
            if board_obj.castling_available_b_ks == True:
                if board_obj.board[5][7] == None and board_obj.board[6][7] == None and board_obj.board[7][7] != None:
                     if board_obj.board[7][7].name == 'rook' and board_obj.board[7][7].rook_can_castle == True:
                         new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, 6, from_ypos, castle = True)
                         feasible_moves.append([command, new_board_obj])
                         
            if board_obj.castling_available_b_qs == True:
                if board_obj.board[3][7] == None and board_obj.board[2][7] == None and board_obj.board[1][7] == None and board_obj.board[0][7] != None:
                     if board_obj.board[0][7].name == 'rook' and board_obj.board[0][7].rook_can_castle == True:
                         new_board_obj, command = create_following_board(board_obj, from_xpos, from_ypos, 2, from_ypos, castle = True)
                         feasible_moves.append([command, new_board_obj])






        return feasible_moves





def get_square_name(xpos, ypos):
    
    x_dict = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
    y_dict = {0:'1', 1:'2', 2:'3', 3:'4', 4:'5', 5:'6', 6:'7', 7:'8'}
    
    square_name = x_dict[xpos] + y_dict[ypos]
    
    return square_name


def create_following_board(board_obj, from_xpos, from_ypos, to_xpos, to_ypos, castle = False):
    #Input: Board and move
    #Output: new board state
    
    color = board_obj.board[from_xpos][from_ypos].color

    #Castle
    if castle == True:
        if to_xpos == 2:
            command = color + ': castle queenside'
        elif to_xpos == 6:
            command = color + ': castle kingside'

        
    #Move to empty square
    elif board_obj.board[to_xpos][to_ypos] == None:
        command = color + ': ' + board_obj.board[from_xpos][from_ypos].name + ' ' + get_square_name(from_xpos, from_ypos) + ' to ' + get_square_name(to_xpos, to_ypos)
    
    #Capture piece
    else:
        command = color + ': ' + board_obj.board[from_xpos][from_ypos].name + ' ' + get_square_name(from_xpos, from_ypos) + ' captures ' + board_obj.board[to_xpos][to_ypos].name + ' '+  get_square_name(to_xpos, to_ypos)
    
    new_board_obj = board_obj.copy()
    new_board_obj.move_piece(from_xpos, from_ypos, to_xpos, to_ypos, print_move = False, castle = castle)
    
    return new_board_obj, command



def load_starting_state():
    
    board_obj = Board()
    
    board_obj.place_piece('white', 'rook', 0,0)
    board_obj.place_piece('white', 'knight', 1,0)
    board_obj.place_piece('white', 'bishop', 2,0)
    board_obj.place_piece('white', 'queen', 3,0)
    board_obj.place_piece('white', 'king', 4,0)
    board_obj.place_piece('white', 'bishop', 5,0)
    board_obj.place_piece('white', 'knight', 6,0)
    board_obj.place_piece('white', 'rook', 7,0)
    board_obj.place_piece('white', 'pawn', 0,1)
    board_obj.place_piece('white', 'pawn', 1,1)
    board_obj.place_piece('white', 'pawn', 2,1)
    board_obj.place_piece('white', 'pawn', 3,1)
    board_obj.place_piece('white', 'pawn', 4,1)
    board_obj.place_piece('white', 'pawn', 5,1)
    board_obj.place_piece('white', 'pawn', 6,1)
    board_obj.place_piece('white', 'pawn', 7,1)
    
    board_obj.place_piece('black', 'rook', 0,7)
    board_obj.place_piece('black', 'knight', 1,7)
    board_obj.place_piece('black', 'bishop', 2,7)
    board_obj.place_piece('black', 'queen', 3,7)
    board_obj.place_piece('black', 'king', 4,7)
    board_obj.place_piece('black', 'bishop', 5,7)
    board_obj.place_piece('black', 'knight', 6,7)
    board_obj.place_piece('black', 'rook', 7,7)
    board_obj.place_piece('black', 'pawn', 0,6)
    board_obj.place_piece('black', 'pawn', 1,6)
    board_obj.place_piece('black', 'pawn', 2,6)
    board_obj.place_piece('black', 'pawn', 3,6)
    board_obj.place_piece('black', 'pawn', 4,6)
    board_obj.place_piece('black', 'pawn', 5,6)
    board_obj.place_piece('black', 'pawn', 6,6)
    board_obj.place_piece('black', 'pawn', 7,6)
    
    return board_obj


# board_obj = Board()
# board_obj.place_piece('white', 'rook', 0,0)
# board_obj.place_piece('black', 'king', 0,7)