from time import time
from threading import Thread
from time import sleep
import requests

class Status:

	def __init__(self,token):
		self.token = token
		self.v = "5.131"

	def get(self):
		response = requests.get("https://api.vk.com/method/status.get",
							   params = {"access_token": self.token,
							   			 "v": self.v})
		return response.json()['response']['text']

	def set(self,status):
		response = requests.get("https://api.vk.com/method/status.set",
							   params = {"access_token": self.token,
							   			 "v": self.v,
							   			 "text":status})

class TimeStatus:

	def __init__(self,token):
		self.status = Status(token)
		self.do = True

	def run(self):
		self.pastatus = self.status.get()
		thread = Thread(target = self._run)
		thread.run()

	def stop(self):
		self.do = False
		sleep(0.1)
		self.status.set(self.pastatus)

	def _run(self):
		try:
			minute = 61
			while self.do:
				second = int(time()) % 86400
				pastminute = str(second % 3600 // 60) 

				if pastminute != minute:
					hour = str(((second // 3600) + 3) % 24)
					minute = str(pastminute)

					if len(hour) == 1:
						hour = "0" + hour
					if len(minute) == 1:
						minute = "0" + minute

					self.status.set(str(hour) + ":" + str(minute))
					sleep(60 - time() % 60)

		except KeyboardInterrupt:
			pass
		self.stop()



if __name__ == "__main__":
	token = str(open("token.txt","rt").read().replace(" ",""))
	stat = TimeStatus(token)
	stat.run()