from utils import *
assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


"""Eliminate values using the naked twins strategy.
Args:
     values(dict): a dictionary of the form {'box_name': '123456789', ...}

Returns:
     the values dictionary with the naked twins eliminated from peers.
"""
def naked_twins(puzzle):

     for box1 in puzzle:

          # only runs on box sizes of 2
          if len(puzzle[box1]) == 2:

               # go through boxes peers looking for a match of naked twins
               for peer in peers[box1]:
                    if puzzle[peer] == puzzle[box1]:
                         # we have pair of naked twins
                         # x = list(peers[box1])
                         # y = list(peers[peer])
                         to_elim = puzzle[box1]
                         # print ('units of box 1 are', units[box1])
                         for unit in units[box1]:
                              if peer in unit:
                                   super_peers = unit
                                   # print ('so the super p for', box1, peer, 'is ', super_peers)
                         if to_elim == '': continue
                         # combines peers into new list with peers for both boxes, without duplicates
                         # super_peers = (x + list(set(y) - set(x)))
                         for super_peer in super_peers:
                              if (super_peer is not box1 and super_peer is not peer) and len(puzzle[super_peer]) > 2:
                                   # eliminates to_elm if found inside super peers)
                                   if to_elim[0] in puzzle[super_peer]:
                                        new_value = puzzle[super_peer].replace(to_elim[0], '')
                                        assign_value(puzzle, super_peer, new_value)
                                        
                                   if to_elim[1] in puzzle[super_peer]:
                                        new_value = puzzle[super_peer].replace(to_elim[1], '')
                                        assign_value(puzzle, super_peer, new_value)

                                   # print ('super peer value now', puzzle[super_peer])
          #     for peer in peers[box1]
     # print ('\nthe func return puzzle')
     # display(puzzle)
     return puzzle
     pass

"""
Convert grid into a dict of {square: char} with '123456789' for empties.
Args:
     grid(string) - A grid in string form.
Returns:
     A grid in dictionary form
          Keys: The boxes, e.g., 'A1'
          Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
"""
def grid_values(grid):
     i = 0
     puzzle = dict()
     for box in boxes:
          if grid[i] == '.':
               puzzle[box] = '123456789'
          else:
               puzzle[box] = grid[i]
          i += 1
          
     return puzzle
     pass

# def display(values):
#     """
#     Display the values as a 2-D grid.
#     Args:
#         values(dict): The sudoku in dictionary form
#     """
#     pass

def eliminate(puzzle):
     for box in puzzle:
          if len(puzzle[box]) == 1:
               digit_to_eliminate = puzzle[box]
               peers_to_check = peers[box]
               # print ('found a box with 1 value', digit_to_eliminate)
               # # print ('peers to check are', peers_to_check)
               for peer in peers_to_check:
                    if digit_to_eliminate in puzzle[peer]:
                         # puzzle[peer] = puzzle[peer].replace(digit_to_eliminate, '')
                         new_value = puzzle[peer].replace(digit_to_eliminate, '')
                         assign_value(puzzle, peer, new_value)
          x = 0
     return puzzle
     # print ('unit list', unitlist)
     # print ('units', units['A1'])
     pass
#     pass

def only_choice(puzzle):
     for unit in unitlist:
          for digit in '123456789':
               # recreates a grid of a unit (all peers) filled only with 
               # boxes that contain current digit
               boxes_that_have_digit = [box for box in unit if digit in puzzle[box]]
               # print (boxes_that_have_digit)
               # if there is only 1 box in the unit that can have the current digit,
               # that digit must be a solution.
               if len(boxes_that_have_digit) == 1:
                    # puzzle[boxes_that_have_digit[0]] = digit
                    for box in boxes_that_have_digit:
                        assign_value(puzzle, box, digit)

     return puzzle
     pass

def reduce_puzzle(puzzle):
     stalled = False
     while not stalled:
          # Check how many boxes have a determined value
          solved_values_before = len([box for box in puzzle.keys() if len(puzzle[box]) == 1])

          # Use the Eliminate Strategy
          puzzle = eliminate(puzzle)

          # Use the Only Choice Strategy
          puzzle = only_choice(puzzle)


          # Check how many boxes have a determined value, to compare
          solved_values_after = len([box for box in puzzle.keys() if len(puzzle[box]) == 1])
          # If no new values were added, stop the loop.
          stalled = solved_values_before == solved_values_after
          # Sanity check, return False if there is a box with zero available values:
          if len([box for box in puzzle.keys() if len(puzzle[box]) == 0]):
               return False
     return puzzle
     pass

def search(puzzle):
     # "Using depth-first search and propagation, create a search tree and solve the sudoku."
     # First, reduce the puzzle using the previous function
     puzzle = reduce_puzzle(puzzle)
     if puzzle is False:
          return False ## Failed earlier
     if all(len(puzzle[s]) == 1 for s in boxes): 
          return puzzle ## Solved! End recursive calls
     
     # Choose one of the unfilled squares with the fewest possibilities
     least_possibilities = 9
     least_box = None
     for box in puzzle:
          if len(puzzle[box]) < least_possibilities and len(puzzle[box]) != 1:
               least_possibilities = len(puzzle[box])
               least_box = box
               # the min we can start is 2, so if 2 then break
               if least_possibilities == 2: break
               
     # Now use recursion to solve each one of the resulting sudokus,
     # by choosing the box with minimum possible values, and then
     # creating a new puzzle with one of the possible values inserted 
     for digit in puzzle[least_box]:
          new_sedoku = puzzle.copy()
          new_sedoku[least_box] = digit
          attempt = search(new_sedoku)
          if attempt:
               return attempt
pass


"""
Find the solution to a Sudoku grid.
Args:
     grid(string): a string representing a sudoku grid.
          Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
Returns:
     The dictionary representation of the final sudoku grid. False if no solution exists.
"""
def solve(grid):
     puzzle = grid_values(grid)
     answer = search(puzzle)
     return answer
     pass




# possible_solutions_1 = [
#         {'G7': '6', 'G6': '3', 'G5': '2', 'G4': '9', 'G3': '1', 'G2': '8', 'G1': '7', 'G9': '5', 'G8': '4', 'C9': '1',
#          'C8': '5', 'C3': '8', 'C2': '237', 'C1': '23', 'C7': '9', 'C6': '6', 'C5': '37', 'A4': '2357', 'A9': '8',
#          'A8': '6', 'F1': '6', 'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'F6': '125', 'F7': '35', 'F8': '9',
#          'F9': '7', 'B4': '27', 'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'C4': '4',
#          'B8': '3', 'B9': '4', 'I9': '9', 'I8': '7', 'I1': '23', 'I3': '23', 'I2': '6', 'I5': '5', 'I4': '8', 'I7': '1',
#          'I6': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'E8': '1', 'A7': '27', 'A6': '257', 'E5': '347',
#          'E4': '6', 'E7': '345', 'E6': '579', 'E1': '8', 'E3': '79', 'E2': '37', 'H8': '2', 'H9': '3', 'H2': '9',
#          'H3': '5', 'H1': '4', 'H6': '17', 'H7': '8', 'H4': '17', 'H5': '6', 'D8': '8', 'D9': '6', 'D6': '279',
#          'D7': '34', 'D4': '237', 'D5': '347', 'D2': '1', 'D3': '79', 'D1': '5'},
#         {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8', 'H5': '6', 'F9': '7',
#          'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8', 'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23',
#          'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5', 'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9',
#          'A4': '2357', 'A7': '27', 'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
#          'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2', 'F6': '125',
#          'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '79', 'F1': '6', 'F2': '4', 'F3': '23', 'F4': '1235',
#          'F5': '8', 'E2': '3', 'F7': '35', 'F8': '9', 'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17',
#          'D3': '79', 'B4': '27', 'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6',
#          'D6': '279', 'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}
#         ]


# before_naked_twins_1 = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
#                          'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
#                          'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
#                          'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
#                          'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
#                          'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
#                          'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
#                          'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
#                          'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
#                          'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
#                          'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')