import requests

from config import *
import json
from bs4 import BeautifulSoup as bs
from lxml import html


session = requests.session()
''' login sessions '''
r_post = session.post(url, data=data, headers=headers)
homepage = session.get(home)

def get_upcoming(session):
	"""real shit begins"""
	reminders = session.get(upcoming)
	reminders = json.loads(reminders.text)
	reminder = reminders['html'].replace("\\/", "/").encode().decode('unicode_escape')
	with open('reminders.html', 'w') as f:
		f.write(reminder)
	# print(reminder)
	with open('reminders.html', 'r') as f:
		doc = bs(f, 'html.parser')
	tags = doc.find_all(class_="date-header upcoming-event".split())
	# print(type(tags))
	reminders_to_dict = {}
	date_rn = ''
	for i, j in zip(tags, range(len(tags))):
		tree = html.fromstring(str(i))
		div_tag = tree.xpath('//div')
		tag_class = div_tag[0].get('class')

		if "date-header" in tag_class:
			date = tree.xpath('//div/h4/text()')[0]
			reminders_to_dict[date] = list()
			date_rn = str(date)
		elif "upcoming-event" in tag_class:
			reminders_to_dict[date_rn].append(
				{
					'course': tree.xpath('//div/h4/span/span/div/div/div/text()')[0],
					'type': tree.xpath('//div/h4/span/span/span/text()')[0],
					'ass_text': tree.xpath('//div/h4/span/a/text()')[0],
					'link': 'https://app.schoology.com' + tree.xpath('//div/h4/span/a/@href')[0],
					'due_time': tree.xpath('//div/h4/span/span/text()'),

				}
			)
	# div_tag = tree.xpath('//div/h4/span/span/span/text()')
	# div_tag = tree.xpath('//div/h4/span/span/div/div/div/text()')[0]
	# print(div_tag)
	# # tag_class = div_tag[0].get('class')
	# print(tag_class)
	return reminders_to_dict


def get_updates(session: requests.Session):
	# with requests.session() as session:
	# 	''' login sessions '''
	# 	r_post = session.post(url, data=data, headers=headers)
	# 	homepage = session.get(home)

	updates = session.get(update)
	with open('update.html', 'w') as f:
		f.write(updates.text)

	with open('update.html', 'r') as f:
		doc = bs(f, 'html.parser')
	tags = doc.find_all(class_="notif-date-header edge-sentence".split())

	def comments(x):
		no = ['commented', 'submission', 'your', 'grade']
		joined = ''.join(x)
		# print(joined)
		compilee = []
		for nos in no:
			if nos in joined:
				compilee.append(True)
			else:
				compilee.append(False)
		return any(compilee)

	updates = {}
	date_rn = ''
	for i, j in zip(tags, range(len(tags))):
		# print(i, j)
		tree = html.fromstring(str(i))
		htm = bs(str(i), 'html.parser')
		try:
			li_class = tree.xpath('//li')
			class_ = li_class[0].get('class')
			if "notif-date-header" in class_:
				date_rn = tree.xpath('//li/text()')[0]
				# print(date_rn)
				updates[date_rn] = list()
		except:
			span_class = tree.xpath('//span')
			span_text = tree.xpath('//span/text()')
			class_ = span_class[0].get('class')
			# print(type(span_text))
			if "edge-sentence" in class_ and comments(span_text) is False:
				as_ = htm.find_all('a')
				types_order = htm.find_all(['span'], class_="visually-hidden")
				time_commit = htm.find_all(['span'], class_="edge-time")[0].text
				# for a in as_:
				# 	print(a.text, a['href'])
				listed = [a.text for a in as_]
				links = ["https://app.schoology.com" + a['href'] for a in as_]

				# print(listed)
				types = [str(types.text)+'.' for types in types_order]
				# print(types)
				# print(types_order)

				if any(types):
					course, *attachments = listed
					# print(course)
					# print(attachments, links)
					course_link, *attachment_links = links
					updates[date_rn].append(
						{
							"course": course,
							"course_link": course_link,
							"types": types,
							"attachment": list(zip(attachments, attachment_links, types)),
							"time_commit": time_commit
						}
					)
	return updates

# print(get_updates(session))


