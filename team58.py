class Player58:

	def __init__(self):
		# You may initialize your object here and use any variables for storing throughout the game
		pass


	def move(self,temp_board,temp_block,old_move,flag):
		#List of permitted blocks, based on old move.
		blocks_allowed  = determine_blocks_allowed(old_move, temp_block)
		#Get list of empty valid cells
		cells = get_empty_out_of(temp_board, blocks_allowed,temp_block)
		alpha = -100000
		beta = 10000
		
		countp1 = 0
		countp2 = 0
		for i in range(9):
			for j in range(9):
				if temp_board[i][j] == 'o':
					countp1 += 1
				elif temp_board[i][j] == 'x':
					countp2 += 1

		if countp1 > countp2 :
			p1 = 'x'
			p2 = 'o'
		else:
			p1 = 'o'
			p2 = 'x'

		for i in cells:
			if beta >alpha :
				temp_board[i[0]][i[1]]=p1
				utility_child  = built_tree(temp_board,temp_block,i,0,alpha,beta,p1,p2)
				# print utility_child
				# if beta > utility_child:
				# 	beta = utility_child
				# 	possible_moves = []
				# 	possible_moves.append(i)
				# elif beta == utility_child:
				# 	possible_moves.append(i)
				if alpha < utility_child:
					alpha = utility_child
					move = i
					# possible_moves = []
					# possible_moves.append(i)
				# elif alpha == utility_child:
				# 	possible_moves.append(i)
					
				temp_board[i[0]][i[1]]='-'

		# if len(possible_moves)>1:
		# 	move = possible_moves[random.randrange(len(possible_moves))]
		# 	# print possible_moves
		# 	return move
		# else:
		# 	return possible_moves[0]
		
		# print move
		return move

def built_tree(temp_board,temp_block,old_move,depth,alpha_p,beta_p,p1,p2):
	# making recursive tree
	# assigning alpha-beta for current node
	depth_limit = 3
	alpha = alpha_p
	beta = beta_p
	#List of permitted blocks, based on old move.
	blocks_allowed  = determine_blocks_allowed(old_move, temp_block)
	#Get list of empty valid cells
	cells = get_empty_out_of(temp_board,blocks_allowed,temp_block)
	if depth == depth_limit or cells == []:
		utility_value = utility(temp_board,temp_block,old_move,alpha,beta,p1,p2,depth)
		return utility_value
	else:
		depth += 1
		for i in cells:
			# utility(temp_board,temp_block)
			# if beta > alpha :
				if ((depth)%2) == 1:
					# max
					temp_board[i[0]][i[1]]=p2
					utility_child = built_tree(temp_board,temp_block,i,depth,alpha,beta,p1,p2)
					# if alpha < utility_child:
					# 	alpha = utility_child
					if beta > utility_child:
							beta = utility_child
							
				else:
					# min
					temp_board[i[0]][i[1]]=p1
					utility_child = built_tree(temp_board,temp_block,i,depth,alpha,beta,p1,p2)
					if alpha < utility_child:
						alpha = utility_child

				temp_board[i[0]][i[1]]='-'
		# depth -= 1
		
		if depth%2 == 1:
			depth -= 1
			return beta
		else:
			depth -= 1
			return alpha


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
	tempx *= 3
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
		utilityarray = define_utility(count1,count2,count3,count4)
		utility_p1 += utilityarray[0]
		utility_p2 += utilityarray[1]
		utility_stat += utilityarray[2]
		
	# counting in a column
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

		utilityarray = define_utility(count1,count2,count3,count4)
		utility_p1 += utilityarray[0]
		utility_p2 += utilityarray[1]
		utility_stat += utilityarray[2]
		
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
	utilityarray = define_utility(count1,count2,count3,count4)
	utility_p1 += utilityarray[0]
	utility_p2 += utilityarray[1]
	utility_stat += utilityarray[2]

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

	utilityarray = define_utility(count1,count2,count3,count4)
	utility_p1 += utilityarray[0]
	utility_p2 += utilityarray[1]
	utility_stat += utilityarray[2]
	
	if (depth%2) == 1:
		block_stat[temp_block_cell] = '-'
	else:
		block_stat[temp_block_cell] = '-'
		
	if utility_p1 < 6 and countp1 == 2 and utility_p2 > -12:
			utility_p1 += 250
	if utility_p2 <-6 and countp2 ==2 and utility_p1 <12:
			utility_p2 -= 250

	utility += utility_p1 + utility_p2 +(utility_stat)/10
	# print_lists(board_game,block_stat)
	# print "utility = ",utility,"utility_p1 =",utility_p1,"utility_p2 =",utility_p2,"utility_stat = ",utility_stat
	return utility

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

def define_utility(count1,count2,count3,count4):

		utility_p1 = utility_p2 = utility_stat = 0
		if count2 == 3:
			utility_p1 += 300
			
		elif count2 == 2:
			utility_p1 += 10
		elif count2 == 2 and count1 == 1:
			utility_p1 -= 9.5
		
		elif count2 == 1:
			utility_p1 += 1
		elif count2 == 1 and count1 == 2:
			utility_p1 += 50
		
		
		# opponent
		if count1 == 3:
			utility_p2 -= 300

		elif count1 == 2:
			utility_p2 -= 10
		elif count1 == 2 and count2 == 1:
			utility_p2 += 9.5

		elif count1 == 1:
			utility_p2 -= 0
		elif count2 == 2 and count1 == 1:
			utility_p2 -= 50

			# board stat
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

		utilityarray = [utility_p1,utility_p2,utility_stat]
		return utilityarray

def print_lists(gb, bs):
	command = raw_input("??")
	# time.sleep(1)
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],
		print
	
	print "=================================="
	
	print "=========== Block Status ========="
	for i in range(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2]
	print "=================================="
	print
	return
