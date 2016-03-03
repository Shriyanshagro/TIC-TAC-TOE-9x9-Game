'''

This is the engine for the Ultimate TicTacToe Tournament. The code in this file is not for reproduction.
@author: Devansh Shah

The structure of the code is as below:
1. Header Files
2. Sample implementations of your class (Player and ManualPlayer)
3. Game Logic
4. Game simulator

In case of any queries, please post on moodle.iiit.ac.in

'''

import sys
import random
import signal
import time

global depth_limit,num,points
global more_blocks
global draw
global loss
loss =0
points = 0
depth_limit = 4
draw = 0
more_blocks = 0

def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    raise TimedOutExc()


class ManualPlayer:
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))

class Player1:

	def __init__(self):
		# You may initialize your object here and use any variables for storing throughout the game
		pass

	def move(self,temp_board,temp_block,old_move,flag):
		#List of permitted blocks, based on old move.
		blocks_allowed  = determine_blocks_allowed(old_move, temp_block)
		#Get list of empty valid cells
		cells = get_empty_out_of(temp_board, blocks_allowed,temp_block)
        # length = cells
		#Choose a move based on some algorithm, here it is a random move.
		return cells[random.randrange(len(cells))]


class Player2:

	def __init__(self):
		# You may initialize your object here and use any variables for storing throughout the game
		pass


	def move(self,temp_board,temp_block,old_move,flag):
		#List of permitted blocks, based on old move.
		blocks_allowed  = determine_blocks_allowed(old_move, temp_block)
		# print blocks_allowed
		#Get list of empty valid cells
		cells = get_empty_out_of(temp_board, blocks_allowed,temp_block)
		alpha = -100000
		beta = 10000

		global num

		if num > 0.5:
			p1 = 'x'
			p2 = 'o'
		else:
			p1 = 'o'
			p2 = 'x'

		for i in cells:
			if beta >alpha :
				temp_board[i[0]][i[1]]=p1
				# print i
				utility_child  = built_tree(temp_board,temp_block,i,1,alpha,beta,p1,p2)
				if beta > utility_child:
					beta = utility_child
					move = i
				temp_board[i[0]][i[1]]='-'

		return move

def built_tree(temp_board,temp_block,old_move,depth,alpha_p,beta_p,p1,p2):
	# making recursive tree
	# assigning alpha-beta for current node
	alpha = alpha_p
	beta = beta_p
	#List of permitted blocks, based on old move.
	blocks_allowed  = determine_blocks_allowed(old_move, temp_block)
	# print blocks_allowed
	#Get list of empty valid cells
	cells = get_empty_out_of(temp_board, blocks_allowed,temp_block)
	global depth_limit

	if depth == depth_limit+1 or cells == []:
		#define utility value
		# print "got"
		# print "blocks_allowed=",blocks_allowed,"move = ",old_move
		utility_value = utility(temp_board,temp_block,old_move,alpha,beta,p1,p2,depth)
		return utility_value

	else:
		depth += 1
		for i in cells:
			# utility(temp_board,temp_block)
			if beta > alpha :
				if (depth%2) == 1:
					# max
					temp_board[i[0]][i[1]]=p1
					# print "hello",depth
					utility_child = built_tree(temp_board,temp_block,i,depth,alpha,beta,p1,p2)
					if alpha < utility_child:
						alpha = utility_child
				else:
					# min
					temp_board[i[0]][i[1]]=p2
					utility_child = built_tree(temp_board,temp_block,i,depth,alpha,beta,p1,p2)
					if beta > utility_child:
						beta = utility_child

				temp_board[i[0]][i[1]]='-'
		depth -= 1

		if depth%2 == 1:
			return alpha
		else:
			return beta


def utility(board_game,block_stat,move,alpha,beta,p1,p2,depth):
	# determine utility value
	# 8 lines
	# decide utility value for each state
	# print_lists(board_game,block_stat)
	# command = raw_input("utility:")
	utility = 0
	utility_stat = 0
	utility_p1 = 0
	utility_p2 = 0
	# number of 'x' and 'o'
	countp1 = 0
	countp2 = 0
	# defining position of block
	tempx = move[0]/3
	tempy = move[1]/3
	# print "tempx=",tempx,"tempy=",tempy
	temp_block_cell = tempx*3 + tempy
	tempx *= 3;
	tempy *= 3
	temp_board = [[0 for x in range(3)] for x in range(3)]
	if (depth%2) == 1:
		block_stat[temp_block_cell] = p1
	# # print block_stat
	else:
		block_stat[temp_block_cell] = p2
	# print "cell =",temp_block_cell
	# temp_block = [[0 for x in range(3)] for x in range(3)]
	
	# defining new temp_board
	for i in range(3):
		for j in range(3):
			temp_board[i][j] = board_game[i+tempx][j+tempy]
			if temp_board[i][j] == p1:
				countp1 += 1
			elif temp_board[i][j] == p2:
				countp2 += 1

	# counting number of 'x' and 'o' to assign utility value
	
	# counting in a row
	for i in range(3):
		count1 = 0
		count2 = 0
		count3 = 0
		count4 = 0
		for j in range(3):
			if temp_board[i][j] == p1:
				count2 += 1
			elif temp_board[i][j] == p2:
				count1 += 1
			if block_stat[i*3+j] == p1:
				count3 += 1
			elif block_stat[i*3+j] == p2:
				count4 += 1
			# print "acha"

		# print ":done"
		if count2 == 3:
			utility_p1 += 100
		elif count2 == 2:
			utility_p1 += 10
		elif count2 == 1:
			utility_p1 += 1
		if count1 == 3:
			utility_p2 -= 100
		elif count1 == 2:
			utility_p2 -= 10
		elif count1 == 1:
			utility_p2 -= 1
		if count3 == 3:
			utility_stat += 500
		elif count3 == 2:
			utility_stat += 50
		elif count3 == 1:
			utility_stat += 5
		if count4 == 3:
			utility_stat -= 500
		elif count4 == 2:
			utility_stat -= 50
		elif count4 == 1:
			utility_stat -= 5

	for j in range(3):
		count1 = 0
		count2 = 0
		count3 = 0
		count4 = 0
		for i in range(3):
			if temp_board[i][j] == p1:
				count2 += 1
			elif temp_board[i][j] == p2:
				count1 += 1
			if block_stat[i*3+j] == p1:
				count3 += 1
			elif block_stat[i*3+j] == p2:
				count4 += 1
		if count2 == 3:
			utility += 100
		elif count2 == 2:
			utility += 10
		elif count2 == 1:
			utility += 1
		if count1 == 3:
			utility -= 100
		elif count1 == 2:
			utility -= 10
		elif count1 == 1:
			utility -= 1
		if count3 == 3:
			utility_stat += 500
		elif count3 == 2:
			utility_stat += 50
		elif count3 == 1:
			utility_stat += 5
		if count4 == 3:
			utility_stat -= 500
		elif count4 == 2:
			utility_stat -= 50
		elif count4 == 1:
			utility_stat -= 5

	count1 = 0
	count2 = 0
	count3 = 0
	count4 = 0
	for j in range(3):
		for i in range(3):
			if i==j:
				if temp_board[i][j] == p1:
					count2 += 1
				elif temp_board[i][j] == p2:
					count1 += 1
				if block_stat[i*3+j] == p1:
					count3 += 1
				elif block_stat[i*3+j] == p2:
					count4 += 1
	if count2 == 3:
		utility_p1 += 100
	elif count2 == 2:
		utility_p1 += 10
	elif count2 == 1:
		utility_p1 += 1
	if count1 == 3:
		utility_p2 -= 100
	elif count1 == 2:
		utility_p2 -= 10
	elif count1 == 1:
		utility_p2 -= 1
	if count3 == 3:
		utility_stat += 500
	elif count3 == 2:
		utility_stat += 50
	elif count3 == 1:
		utility_stat += 5
	if count4 == 3:
		utility_stat -= 500
	elif count4 == 2:
		utility_stat -= 50
	elif count4 == 1:
		utility_stat -= 5

	count1 = 0
	count2 = 0
	count3 = 0
	count4 = 0
	for j in range(3):
		for i in range(3):
			if i==1 and j==1 or i==0 and j ==2 or i==2 and j==0:
				if temp_board[i][j] == p1:
					count2 += 1
				elif temp_board[i][j] == p2:
					count1 += 1
				if block_stat[i*3+j] == p1:
					count3 += 1
				elif block_stat[i*3+j] == p2:
					count4 += 1
	if count2 == 3:
		utility_p1 += 100
	elif count2 == 2:
		utility_p1 += 10
	elif count2 == 1:
		utility_p1 += 1
	if count1 == 3:
		utility_p2 -= 100
	elif count1 == 2:
		utility_p2 -= 10
	elif count1 == 1:
		utility_p2 -= 1
	if count3 == 3:
		utility_stat += 500
	elif count3 == 2:
		utility_stat += 50
	elif count3 == 1:
		utility_stat += 5
	if count4 == 3:
		utility_stat -= 500
	elif count4 == 2:
		utility_stat -= 50
	elif count4 == 1:
		utility_stat -= 5
	
	if (depth%2) == 1:
		block_stat[temp_block_cell] = '-'
	else:
		block_stat[temp_block_cell] = '-'
		
	if utility_p1 < 6 and countp1 == 2 and utility_p2 < -12:
			utility_p1 += 250
	if utility_p2 <-6 and countp2 ==2 and utility_p1 <12:
			utility_p2 -= 250

	utility += utility_p1 + utility_p2 +utility_stat
	return utility

# determine which blocks are allowed to move-in
def determine_blocks_allowed(old_move, block_stat):
	blocks_allowed = []
	if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
		blocks_allowed = [1,3]
	elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
		blocks_allowed = [1,5]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
		blocks_allowed = [3,7]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
		blocks_allowed = [5,7]
	elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
		blocks_allowed = [0,2]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
		blocks_allowed = [0,6]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
		blocks_allowed = [6,8]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
		blocks_allowed = [2,8]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
		blocks_allowed = [4]
	else:
		sys.exit(1)
	final_blocks_allowed = []
	for i in blocks_allowed:
		if block_stat[i] == '-':
			final_blocks_allowed.append(i)
	return final_blocks_allowed

#Initializes the game
def get_init_board_and_blockstatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)

	block_stat = ['-']*9
	return board, block_stat

# Checks if player has messed with the board. Don't mess with the board that is passed to your move function.
def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state

# Checks if player has messed with the block. Don't mess with the block array that is passed to your move function.
def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat

#Gets empty cells from the list of possible blocks. Hence gets valid moves.
def get_empty_out_of(gameb, blal,block_stat):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3 #determine row
		id2 = idb%3 # determine column
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))
    # If all the possible blocks are full, you can move anywhere
	if cells == []:
		new_blal = []
		all_blal = [0,1,2,3,4,5,6,7,8]
		for i in all_blal:
			if block_stat[i]=='-':
				new_blal.append(i)

		for idb in new_blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))
        return cells

# Returns True if move is valid
def check_valid_move(game_board, block_stat, current_move, old_move):

	# first we need to check whether current_move is tuple of not
	# old_move is guaranteed to be correct
	if type(current_move) is not tuple:
		return False

	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	#Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True

	#List of permitted blocks, based on old move.
	blocks_allowed  = determine_blocks_allowed(old_move, block_stat)
	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
	cells = get_empty_out_of(game_board, blocks_allowed, block_stat)
	#Checks if you made a valid move.
	if current_move in cells:
		return True
	else:
		return False

def update_lists(game_board, block_stat, move_ret, fl):

	game_board[move_ret[0]][move_ret[1]] = fl

	block_no = (move_ret[0]/3)*3 + move_ret[1]/3
	id1 = block_no/3
	id2 = block_no%3
	mflg = 0

	flag = 0
	for i in range(id1*3,id1*3+3):
		for j in range(id2*3,id2*3+3):
			if game_board[i][j] == '-':
				flag = 1

	if flag == 0:
		block_stat[block_no] = 'D'

	if block_stat[block_no] == '-':
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
			mflg=1
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
			mflg=1
		if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-' and game_board[id1*3][i] != 'D':
                                mflg = 1
                                break
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-' and game_board[i][id2*3] != 'D':
                                mflg = 1
                                break
	if mflg == 1:
		block_stat[block_no] = fl

	return mflg

#Check win
def terminal_state_reached(game_board, block_stat,point1,point2):
	### we are now concerned only with block_stat
	bs = block_stat
	## Row win
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='D') or (bs[3]!='-' and bs[3]!='D' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='D' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		return True, 'W'
	## Col win
	elif (bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-' and bs[0]!='D') or (bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-' and bs[4]!='D') or (bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-' and bs[5]!='D'):
		return True, 'W'
	## Diag win
	elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='D') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='D'):
		return True, 'W'
	else:
		smfl = 0
		for i in range(9):
			if block_stat[i] == '-':
				smfl = 1
				break
		if smfl == 1:
			return False, 'Continue'

		else:
			if point1>point2:
				return True, 'P1'
			elif point2>point1:
				return True, 'P2'
			else:
				return True, 'D'


def decide_winner_and_get_message(player,status, message):
	if status == 'P1':
		return ('P1', 'MORE BLOCKS')
	elif status == 'P2':
		return ('P2', 'MORE BLOCKS')
	elif player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NONE','DRAW')
	return


def print_lists(gb, bs):
	# print '=========== Game Board ==========='
	# for i in range(9):
	# 	if i > 0 and i % 3 == 0:
	# 		print
	# 	for j in range(9):
	# 		if j > 0 and j % 3 == 0:
	# 			print " " + gb[i][j],
	# 		else:
	# 			print gb[i][j],
	#
	# 	print
	# print "=================================="
	#
	# print "=========== Block Status ========="
	# for i in range(0, 9, 3):
	# 	print bs[i] + " " + bs[i+1] + " " + bs[i+2]
	# print "=================================="
	# print
	return


def simulate(obj1,obj2):

	# Game board is a 9x9 list of lists & block_stat is a list of 9 elements indicating if a block has been won.
	game_board, block_stat = get_init_board_and_blockstatus()

	pl1 = obj1
	pl2 = obj2

	# Player with flag 'x' will start the game
	pl1_fl = 'x'
	pl2_fl = 'o'

	old_move = (-1, -1) # For the first move

	WINNER = ''
	MESSAGE = ''
	TIMEALLOWED = 12
	p1_pts=0
	p2_pts=0

	print_lists(game_board, block_stat)

	while(1): # Main game loop

		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]

		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		#		ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)

		try:
			ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)
		except:
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'TIMED OUT')
		#	print MESSAGE
			break
		signal.alarm(0)

		# Check if list is tampered.
		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break

		# Check if the returned move is valid
		if not check_valid_move(game_board, block_stat, ret_move_pl1, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MADE AN INVALID MOVE')
			break


		# print "Player 1 made the move:", ret_move_pl1, 'with', pl1_fl
		# Update the 'game_board' and 'block_stat' move
		p1_pts += update_lists(game_board, block_stat, ret_move_pl1, pl1_fl)

		gamestatus, mesg =  terminal_state_reached(game_board, block_stat,p1_pts,p2_pts)
		if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P1', mesg,  'COMPLETE')
			break


		old_move = ret_move_pl1
		print_lists(game_board, block_stat)

        	temp_board_state = game_board[:]
        	temp_block_stat = block_stat[:]

        	signal.signal(signal.SIGALRM, handler)
        	signal.alarm(TIMEALLOWED)

        	try:
           		ret_move_pl2 = pl2.move(temp_board_state, temp_block_stat, old_move, pl2_fl)
        	except:
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'TIMED OUT')
			break
        	signal.alarm(0)

        	if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MODIFIED CONTENTS OF LISTS')
			break

        	if not check_valid_move(game_board, block_stat, ret_move_pl2, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MADE AN INVALID MOVE')
			break

        	# print "Player 2 made the move:", ret_move_pl2, 'with', pl2_fl

        	p2_pts += update_lists(game_board, block_stat, ret_move_pl2, pl2_fl)

        	# Now check if the last move resulted in a terminal state
        	gamestatus, mesg =  terminal_state_reached(game_board, block_stat,p1_pts,p2_pts)
        	if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P2', mesg,  'COMPLETE' )
			break
        	else:
			old_move = ret_move_pl2
			print_lists(game_board, block_stat)

	# print WINNER
	# print MESSAGE
	# print p2_pts,p1_pts
	# print WINNER,MESSAGE
	global points
	global more_blocks
	global draw
	global loss
	global num
	if num > 0.5:
		# print "you are player1"
		# if MESSAGE == "MORE BLOCKS" and WINNER == "P1":
		# 	points += 1
		if MESSAGE == "DRAW":
			draw += 1
		elif WINNER == "P1" :
			points += 1
		else:
			loss += 1
			print WINNER,MESSAGE
	else:
		# if MESSAGE == "MORE BLOCKS":
		# 	more_blocks += 1
		if MESSAGE == "DRAW":
			draw += 1
		elif WINNER == "P2":
			points += 1
		else:
			loss += 1
			print WINNER,MESSAGE
	if MESSAGE == "MADE AN INVALID MOVE"	or MESSAGE == "TIMED OUT":
		print MESSAGE

	# command = raw_input("points:")

if __name__ == '__main__':
	## get game playing objects

	#  a nice to ay handle errors**
	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)

	obj1 = ''
	obj2 = ''
	option = sys.argv[1]
	if option == '1':
		obj1 = Player1()
		obj2 = Player2()

	elif option == '2':
		obj1 = Player1()
		obj2 = ManualPlayer()
	elif option == '3':
		obj1 = ManualPlayer()
		obj2 = ManualPlayer()
	else:
		print 'Invalid option'
		sys.exit(1)

	t = 1

	global num
	while t != 51:
		print "Game_play ",t

		num = random.uniform(0,1)
		if num > 0.5:
			# command = raw_input("command :")
			simulate(obj2, obj1)
			# print "you are player1"
		else:
			# command = raw_input("command :")
			simulate(obj1, obj2)
			# print "you are player2"
		t+=1
	print "your points = " , points
	print "draw = " , draw
	# print "more_blocks = " , more_blocks
	print "you loss = ",loss
