from pprint import pprint
from config import *
from methods import *
import requests, json


def main(instruction):
	global data, url, home, upcoming, headers

	with requests.session() as session:
		''' login sessions '''
		r_post = session.post(url, data=data, headers=headers)
		homepage = session.get(home)
		# # print(lol.text)
		# # print(r_post.status_code)
		# with open('index.html', 'w') as f:
		# 	f.write(homepage.text)
		if instruction == "upcoming":
			return get_upcoming(session)
		elif instruction == "update":
			return get_updates(session)



if __name__ == "__main__":
	print(main('upcoming'))
