import socket
import pickle # Serialize objects


class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = "194.210.228.4" 
		self.port = 5556

		self.addr = (self.server, self.port)
		self.game = self.connect()
		
	def getGame(self):
		return self.game

	def connect(self):
		try:
			self.client.connect(self.addr)
			# Load Byte Data
			return pickle.loads(self.client.recv(2048))
		except:
			print("Could not connect")
			pass

	def send(self, data):
		self.client.send(pickle.dumps(data))
		data = self.client.recv(2048)
		return pickle.loads(data)
