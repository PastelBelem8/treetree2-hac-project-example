import socket
import _thread
import sys
import pickle
from player import Player, Game, screen_dimensions

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

players = [
	Player(screen_x / 4, 0, 30, 30, (255, 0, 0)), 
	Player(screen_x / 4, screen_y - 30, 30, 30, (0, 125, 125))
]


# To continuously run while our client is connected
def threaded_client(conn, player_id):
	conn.send(pickle.dumps(players[player_id]))
	reply = ""
	while True:
		try:
			data = pickle.loads(conn.recv(2048))
			print("Received: ", data)
			players[player_id] = data

			if not data:
				print("Disconnected")
				break
			else:
				print("Determining which player to retrieve")
				if player_id == 1:
					reply = players[0]
				else: 
					reply = players[1]

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
