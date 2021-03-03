import random

def lands_in():
	wedge_types = ["cash","bankrupt","loseturn"]
	wedge_type = random.sample(wedge_types,1)
	return wedge_type 

def input_players():
	stop_input = False
	while not stop_input:
		try:
			num_human = input("Input the number of players: ")
			num_human = int(num_human)
			if num_human < 2:
				print("Game needs at least 2 players")
			else:
				print("Number of human players: {}".format(num_human))
				stop_input = True
		except ValueError:
			print('"{}" is not an integer'.format(num_human))
		players = []
	for i in range(num_human):
		player = input("Enter name of player {}: ".format(i+1))
		players.append(player)
	random.shuffle(players)
	return players

players = input_players()