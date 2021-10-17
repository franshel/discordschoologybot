import discord
from discord import Client, Game, Embed
from discord.ext import commands
from discord.ext import tasks
from config import *
from methods import *

activity = Game('sch', type=3)
client = commands.Bot(command_prefix="sch ", activity=activity)

emoji_to_user = {
	'Assignment.': ":writing_hand:",
	'Event.': ":calendar_spiral:",
	'Notebook': ':notebook_with_decorative_cover:',
	'Time': ':timer:',
	'Web Link.': ':link:',
	'File.': ":page_facing_up:",
	'Discussion.': ":speech_balloon:"
}

session = requests.session()
''' login sessions '''
r_post = session.post(url, data=data, headers=headers)
homepage = session.get(home)


@client.event
async def on_ready():
	channel = client.get_channel(id=12345687890)
	get_updt.start(channel=channel)
	print('Bot ready!')


@tasks.loop(minutes=10)
async def refresh_session():
	global session, r_post, homepage
	session = requests.session()
	''' login sessions '''
	r_post = session.post(url, data=data, headers=headers)
	homepage = session.get(home)
	print('Session refreshed!')



@tasks.loop(seconds=30)
async def get_updt(channel):
	dates = get_updates(session)
	final = ''
	for date in reversed(dates):
		objs = dates[date]
		for obj in objs:
			course = obj["course"]
			course_link = obj['course_link']
			attachments = obj['attachment']
			time_commit = obj['time_commit']

			base = f'[{course}]({course_link}) posted '
			atachee = f''
			for attachment, ind in zip(attachments, range(len(attachments))):
				attachment_name, attachment_link, attachment_type = attachment
				atachee = atachee + f'{emoji_to_user[attachment_type]} [{attachment_name}]({attachment_link})'
				if ind + 1 == len(attachments):
					atachee = atachee + f' ({time_commit})\n'
				else:
					atachee = atachee + ', '
			poster = base + atachee

			file = open('update.txt', 'r+')
			content = file.readlines()
			if poster not in content:
				print('Schoology course update incoming!')
				file = open('update.txt', 'a+')
				file.write(poster)
				embedded = Embed(color=discord.Color.green(), description=poster)
				await channel.send(embed=embedded)
				print(poster)
			else:
				pass

			# await ctx.send(poster)

			# final = final + poster


	# print(final)


@client.command()
async def upcoming(ctx):
	user = ctx.author
	channel = client.get_channel(123456789)
	embed = Embed(title='UPCOMING', color=user.color)
	upcoming_bekend = get_upcoming(session)
	for events in upcoming_bekend:
		ups = [up for up in upcoming_bekend[events]]
		final = ''

		for i in ups:
			due_time = ''
			if i["due_time"]:
				due_time = i["due_time"][0]
			final = final + f'\n\n {emoji_to_user[i["type"]]}: [**{i["ass_text"]}**]({i["link"]}) \n ' \
							f'{emoji_to_user["Notebook"]}: {i["course"]} \n' \
							f'{emoji_to_user["Time"]}: {due_time} \n\n'
		embed.add_field(name=events, value=final, inline=False)
	await channel.send(embed=embed)
	print(f'{user} requested upcoming!')


refresh_session.start()

client.run('NzcxNzAzNDc3OTkwMzI2Mjgy.X5v-3g.IdYw90UuwmgbPUen2MmCsoReC_U')
