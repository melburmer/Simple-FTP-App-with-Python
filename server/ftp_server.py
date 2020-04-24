from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

server_dir = os.getcwd()

class Server():
	def __init__(self):

		self.authorizer = DummyAuthorizer()
		self.authorizer.add_user("user", "12345", server_dir, perm="elradfmw")
		self.authorizer.add_anonymous(server_dir, perm="elradfmw")

		self.handler = FTPHandler
		self.handler.authorizer = self.authorizer

		self.server = FTPServer(("127.0.0.1", 1026), self.handler)
		self.server.serve_forever()


if __name__ == "__main__":
	server = Server()