import socket
import _thread
import sys
import pickle
from player import Player, Game, screen_dimensions, offset_y

server = "194.210.228.4" # ip address (discover with ipconfig)
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.bind((server, port))
except socket.error as e:
	print(e)

# Wait / Listen for connections
s.listen() # Parameter (unlimited vs n people connecting)
print("Waiting for a connection, Server Started")


screen_x, screen_y = screen_dimensions
player_dims = (20, 30)
h = player_dims[1]

players = [
	Player(screen_x / 4, screen_y - h - offset_y, *player_dims, (255, 0, 0)), 
	Player(screen_x / 5, screen_y - h - offset_y, *player_dims, (0, 125, 125))
]


# To continuously run while our client is connected
def threaded_client(conn, player_id):
	game = Game(players, player_id)
	conn.send(pickle.dumps(game))
	reply = ""
	while True:
		try:
			game = pickle.loads(conn.recv(2048))
			print("Received: ", game)
			players[player_id] = game.get_player()

			if not game:
				print("Disconnected")
				break
			else:
				print("Updating the Game object to send")
				reply = Game(players, player_id)
				print("Sending : ", reply)
			conn.sendall(pickle.dumps(reply))
		except:
			print("Unexpected Error at the Server!")
			break

	print("Lost connection")
	conn.close()


currentPlayer = 0
while True: # Continuously check for connections
	conn, addr = s.accept()
	print("Connected to:", addr)

	print("Player", currentPlayer, "connected!")
	_thread.start_new_thread((threaded_client), (conn, currentPlayer % len(players)))
	print("Waiting for player", currentPlayer)
	currentPlayer += 1
