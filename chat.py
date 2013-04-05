import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4

class Message(object):
	
	callbacks = []
	roomnameofsender = '' 
	
	def contentrecorder(self,content,uid,username,roomname):
		cont = content
		user = username
		room = roomname 
		roomnameofsender = room
		self.notifyCallbacks(cont,user,room)
		
	def notifyCallbacks(self,cont,user,room):
		self.callbacks[:] = [c for c in self.callbacks if self.callbackHelper(c,cont,user,room)]
	
	def callbackHelper(self, callback , cont, user ,room):
		#if room == self.roomnameofsender:
				callback(cont, user,room)
				return False					
		
		
	
	def register(self, callback):
		self.callbacks.append(callback)

class Onclick(tornado.web.RequestHandler):
	def post(self):
		content = self.get_argument('content')
		uid = self.get_argument('uid')
		username = self.get_argument('username')
		roomname = self.get_argument('room')
		
		if not uid:
			self.set_status(400)
			return
		self.application.messageinit.contentrecorder(content ,uid,username , roomname)
		
		
class Onload(tornado.web.RequestHandler):
	def get(self):
		uid = uuid4()
		roomname = self.get_argument('roomname')
		self.render("index.html", uid=uid, count="you are connected to this room",name="anonym", roomname=roomname)

class MessageHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.application.messageinit.register(self.async_callback(self.on_messagereceiving))

		
	def on_messagereceiving(self, content,user,room):
		dict1 = {"content":content}
		dict2 = {"user":user}
		dict3 = {"room" : room}
		z = dict(dict1.items() + dict2.items() + dict3.items())
		self.write(z)
		self.finish()
		
class Application(tornado.web.Application):
	def __init__(self):
		self.messageinit = Message()
		
		handlers = [
			(r'/', Onload),
			(r'/cart/registercallback', MessageHandler),
			(r'/chat/messagecomes',Onclick)
		]
		
		settings = {
			'template_path': 'templates',
			'static_path': 'static'
		}
		
		tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = Application()
	server = tornado.httpserver.HTTPServer(app)
	server.listen(3333)
	tornado.ioloop.IOLoop.instance().start()
