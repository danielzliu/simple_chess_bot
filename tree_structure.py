# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 12:06:30 2021

@author: Daniel
"""
import framework 


class Node:
    
    global_cnt = 0
    
    def __init__(self, depth, max_depth, current_state, previous_move= None, alpha = -2000, beta = 2000 ):
        
        Node.global_cnt = Node.global_cnt + 1


           
        self.depth = depth             #What the depth of the current node is
        self.max_depth = max_depth     #The max depth to consider
        self.current_state = current_state #The current state, Board object
        self.previous_move = previous_move #str
        self.players_turn = current_state.players_turn #white or black
        
        
        self.alpha = alpha #score of white's best move (highest score)
        self.beta = beta #score of black's best move (lowest score)
        
        
        self.minmax_value = None
        self.optimal_child = None
        
        self.calculate_minmax()
        
    
    
    
    def calculate_minmax(self):
        #We calculate minmax with alpha-beta pruning
        #https://www.youtube.com/watch?v=l-hh51ncgDI
        
        
        #If we are  on the lowest level, calculate the value of the current board
        if self.depth == self.max_depth:
            self.minmax_value = self.current_state.score_board()
            
        
        
        elif self.depth < self.max_depth:
            next_generation_info = self.current_state.find_all_feasible_moves() #in format [[move str, board_state], ...]
            
            if len(next_generation_info) ==  0:
                self.minmax_value = self.current_state.score_board()
                
            else: 
            
                    if self.players_turn == 'white':
                        
                        best_child_so_far = None
                        best_value_so_far = -2000
                        
                        for move in next_generation_info:
                            move_str = move[0]
                            next_state = move[1]
                            
                            child_node = Node(self.depth + 1, self.max_depth, next_state, previous_move = move_str, alpha = self.alpha, beta = self.beta)
                            
                            #The parent is the worst of its childs
                            
        
                            
                            if child_node.minmax_value > best_value_so_far:
                                
                                best_child_so_far = child_node
                                best_value_so_far = child_node.minmax_value
                                
                            #If the the move is better than whites best move, then of course white will make that move
                            if best_value_so_far > self.alpha:
                                self.alpha = best_value_so_far
                                
                            #However, if the move means black will get a worse position, then black will not allow the move to be made
                            if self.alpha >= self.beta:
                                break
                            
                        self.optimal_child = best_child_so_far
                        self.minmax_value = best_value_so_far
                        
                        
                        
                    elif self.players_turn == 'black':
                        best_child_so_far = None
                        best_value_so_far = 2000
                        
                        for move in next_generation_info:
                            
                            move_str = move[0]
                            next_state = move[1]
                            
                            child_node = Node(self.depth + 1, self.max_depth, next_state, previous_move = move_str, alpha = self.alpha, beta = self.beta)
                            
                            if child_node.minmax_value < best_value_so_far:
                                
                                best_child_so_far = child_node
                                best_value_so_far = child_node.minmax_value
                                
                            if best_value_so_far < self.beta:
                                self.beta = best_value_so_far
                                
                            if self.alpha >= self.beta:
                                break
                        
                        self.optimal_child = best_child_so_far
                        self.minmax_value = best_value_so_far
    
    
    
    def suggest_move(self):
        
        print(self.optimal_child.previous_move + '. ' + str(self.minmax_value))
        



# board_obj = framework.Board()

# board_obj.place_piece('white', 'rook', 0,0)
# board_obj.place_piece('white', 'knight', 1,0)
# board_obj.place_piece('white', 'bishop', 2,0)
# board_obj.place_piece('white', 'king', 4,0)
# board_obj.place_piece('white', 'bishop', 2,3)
# board_obj.place_piece('white', 'rook', 7,0)
# board_obj.place_piece('white', 'pawn', 0,1)
# board_obj.place_piece('white', 'pawn', 1,1)
# board_obj.place_piece('white', 'pawn', 2,1)
# board_obj.place_piece('white', 'pawn', 3,1)
# board_obj.place_piece('white', 'pawn', 4,1)
# board_obj.place_piece('white', 'pawn', 6,1)
# board_obj.place_piece('white', 'pawn', 7,1)

# board_obj.place_piece('black', 'rook', 0,7)
# board_obj.place_piece('black', 'knight', 2,5)
# board_obj.place_piece('black', 'bishop', 2,7)
# board_obj.place_piece('black', 'queen', 3,4)
# board_obj.place_piece('black', 'king', 6,7)
# board_obj.place_piece('black', 'bishop', 5,7)
# board_obj.place_piece('black', 'rook', 7,7)
# board_obj.place_piece('black', 'pawn', 0,6)
# board_obj.place_piece('black', 'pawn', 1,6)
# board_obj.place_piece('black', 'pawn', 2,6)
# board_obj.place_piece('black', 'pawn', 4,4)
# board_obj.place_piece('black', 'pawn', 6,6)
# board_obj.place_piece('black', 'pawn', 7,6)


# #node = Node(0, 6, board_obj)      

# import timeit
# #s = timeit.timeit(stmt = lambda: board_obj.copy(), number = 10000)

# s = timeit.timeit(stmt = lambda: Node(0, 6, board_obj) , number = 1)
# print(s)  