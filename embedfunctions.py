import discord
import json
import datetime
from datetime import timedelta
import players
import time
import random
import statsapi
import re
import dateutil.parser
import requests
import commonfunctions
import calendar
import portalocker
import os


class EmbedFunctions:
	commonFunctions = commonfunctions.CommonFunctions()

	async def scheduled_Game_Embed(self, game, message):
		# If for some reason we get a list, take the first object
		if type(game) == list:
			game = game[0]

		# Get the UTC datetime string
		gameTimeLocal = self.commonFunctions.get_Local_Time(game['game_datetime'])

		homeTeam = statsapi.lookup_team(game['home_name'])
		awayTeam = statsapi.lookup_team(game['away_name'])

		# Get the game type
		gameType = game['game_type']
		'''
		[{'id': 'S', 'description': 'Spring Training'}, {'id': 'R', 'description': 'Regular season'}, {'id': 'F', 'description': 'Wild Card Game'}, {'id': 'D', 'description': 'Division Series'}, {'id': 'L', 'description': 'League Championship Series'}, {'id': 'W', 'description': 'World Series'}, {'id': 'C', 'description': 'Championship'}, {'id': 'N', 'description': 'Nineteenth Century Series'}, {'id': 'P', 'description': 'Playoffs'}, {'id': 'A', 'description': 'All-Star game'}, {'id': 'I', 'description': 'Intrasquad'}, {'id': 'E', 'description': 'Exhibition'}]
		'''
		# contextParams = {'gamePk': game['game_id']}
		# game_contextMetrics = statsapi.get(endpoint='game_contextMetrics', params=contextParams)
		# game_contextMetrics = statsapi.schedule(game_id=game['game_id'])
		#print(game_contextMetrics)
		# game_contextMetrics = game_contextMetrics[0]
		# gameType = game_contextMetrics['gameType']

		# If the teams have been announced then read the info
		if len(homeTeam) > 0:
			homeTeamShort = homeTeam[0]['fileCode'].upper()
			# Get the probable pitchers
			homeProbable = game['home_probable_pitcher']
			homeNote = game['home_pitcher_note']
			homeNote = game['home_pitcher_note']
		else:
			homeTeamShort = 'N/A'
			homeProbable = 'N/A'
			homeNote = 'N/A'

		if len(awayTeam) > 0:
			awayTeamShort = awayTeam[0]['fileCode'].upper()
			# Get the probable pitchers
			awayProbable = game['away_probable_pitcher']
			awayNote = game['away_pitcher_note']
		else:
			awayTeamShort = 'N/A'
			awayProbable = 'N/A'
			awayNote = 'N/A'

		# Create the embed object
		scheduledEmbed = discord.Embed()
		# Regular Season
		if gameType == 'R':
			scheduledEmbed.title = '**' + game['away_name'] + '** vs **' + game['home_name'] + '**'
		# Wildcard
		elif gameType == 'F':
			contextParams = {'gamePk': game['game_id']}
			game_contextMetrics = statsapi.get(endpoint='game_contextMetrics', params=contextParams)
			# Check if the game is a tiebreaker
			if game_contextMetrics['game']['tiebreaker'] == 'N':
				scheduledEmbed.title = '**Wildcard Game**\n\n**' + game['away_name'] + '** vs **' + game[
					'home_name'] + '**'
			else:
				scheduledEmbed.title = '**Wildcard Tiebreaker Game**\n\n**' + game['away_name'] + '** vs **' + game[
					'home_name'] + '**'
		# Division Series
		elif gameType == 'D':
			contextParams = {'gamePk': game['game_id']}
			game_contextMetrics = statsapi.get(endpoint='game_contextMetrics', params=contextParams)
			homeRecordString = str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' + str(
				game_contextMetrics['game']['teams']['home']['leagueRecord']['losses'])
			awayRecordString = str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' + str(
				game_contextMetrics['game']['teams']['away']['leagueRecord']['losses'])
			scheduledEmbed.title = '**Division Series Game ' + str(
				game_contextMetrics['game']['seriesGameNumber']) + '**\n\n**' + game[
									   'away_name'] + '**(' + awayRecordString + ') vs ' + '**' + game[
									   'home_name'] + '**(' + homeRecordString + ')'
		# League Championship Series
		elif gameType == 'L':
			contextParams = {'gamePk': game['game_id']}
			game_contextMetrics = statsapi.get(endpoint='game_contextMetrics', params=contextParams)
			homeRecordString = str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' + str(
				game_contextMetrics['game']['teams']['home']['leagueRecord']['losses'])
			awayRecordString = str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' + str(
				game_contextMetrics['game']['teams']['away']['leagueRecord']['losses'])
			scheduledEmbed.title = '**League Championship Series Game ' + str(
				game_contextMetrics['game']['seriesGameNumber']) + '**\n\n**' + game[
									   'away_name'] + '**(' + awayRecordString + ') vs ' + '**' + game[
									   'home_name'] + '**(' + homeRecordString + ')'
		# World Series
		elif gameType == 'W':
			contextParams = {'gamePk': game['game_id']}
			game_contextMetrics = statsapi.get(endpoint='game_contextMetrics', params=contextParams)
			homeRecordString = str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' + str(
				game_contextMetrics['game']['teams']['home']['leagueRecord']['losses'])
			awayRecordString = str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' + str(
				game_contextMetrics['game']['teams']['away']['leagueRecord']['losses'])
			scheduledEmbed.title = '**World Series Game ' + str(
				game_contextMetrics['game']['seriesGameNumber']) + '**\n\n**' + game[
									   'away_name'] + '**(' + awayRecordString + ') vs ' + '**' + game[
									   'home_name'] + '**(' + homeRecordString + ')'
		# Spring Training
		elif gameType == 'S':
			scheduledEmbed.title = '**Spring Training**\n\n**' + game['away_name'] + '** vs **' + game[
				'home_name'] + '**'
		else:
			scheduledEmbed.title = '**' + game['away_name'] + '** vs **' + game['home_name'] + '**'

		scheduledEmbed.type = 'rich'
		# testEmbed.colour =
		scheduledEmbed.color = discord.Color.dark_blue()

		scheduledEmbed.add_field(name='Game Status:', value=game['status'], inline=False)

		# scoreEmbed.add_field(name='NAME', value='VALUE', inline=False)
		scheduledEmbed.add_field(name='Start Time:', value=gameTimeLocal.strftime('%-I:%M%p' + ' ET'), inline=False)

		# Check for returned values
		if not homeProbable:
			homeProbable = 'Unannounced'
		scheduledEmbed.add_field(name=homeTeamShort + ' Probable:', value=homeProbable, inline=True)
		# Check for returned values
		if not awayProbable:
			awayProbable = 'Unannounced'
		scheduledEmbed.add_field(name=awayTeamShort + ' Probable:', value=awayProbable, inline=True)
		# Check for returned values
		if not homeNote:
			homeNote = 'None'

		scheduledEmbed.add_field(name='Home Notes', value=homeNote, inline=False)
		# Check for returned values
		if not awayNote:
			awayNote = 'None'
		scheduledEmbed.add_field(name='Away Notes', value=awayNote, inline=False)
		await message.channel.send(content='Scheduled Game on ' + gameTimeLocal.strftime('%m/%d/%Y') + ':',
								   embed=scheduledEmbed)

	async def final_Game_Embed(self, game, message):
		# If for some reason we get a list, take the first object
		if type(game) == list:
			game = game[0]


		# Get the UTC datetime string
		gameTimeLocal = self.commonFunctions.get_Local_Time(game['game_datetime'])

		# List of status that indicate the game is over
		final_status_list = ["Final", "Game Over", "Completed Early"]
		# Game is over
		if any(game_status in game['status'] for game_status in final_status_list):

			# Create the final game embed object
			finalGameEmbed = discord.Embed()
			finalGameEmbed.type = 'rich'
			finalGameEmbed.color = discord.Color.dark_blue()

			# Add the fields with game info
			finalGameEmbed.add_field(name='**' + game['away_name'] + '** vs **' + game['home_name'] + '**\n',
									 value='```js\n' + statsapi.linescore(game['game_id']) + '```', inline=False)
			# Check for a valid key and value
			if 'winning_pitcher' in game and game['winning_pitcher'] != None:
				finalGameEmbed.add_field(name='Winning Pitcher:', value=game['winning_pitcher'], inline=True)
			if 'losing_pitcher' in game and game['losing_pitcher'] != None:
				finalGameEmbed.add_field(name='Losing Pitcher:', value=game['losing_pitcher'], inline=True)
			if 'save_pitcher' in game and game['save_pitcher'] != None:
				finalGameEmbed.add_field(name='Save:', value=game['save_pitcher'], inline=False)

			await message.channel.send(content='Final score from ' + gameTimeLocal.strftime('%m/%d/%Y'),
									   embed=finalGameEmbed, tts=False)

			# A special message if the Yankees lost
			# First check if the Yankees were playing
			if 'New York Yankees' in game['home_name'] or 'New York Yankees' in game['away_name']:
				yakeesLose = False
				# Get the scores
				homeScore = game['home_score']
				awayScore = game['away_score']
				if 'New York Yankees' in game['home_name']:
					if homeScore < awayScore:
						yakeesLose = True
				else:
					if awayScore < homeScore:
						yakeesLose = True

				if yakeesLose:
					await message.channel.send('https://youtu.be/BFD46s_JRNI')
				else:
					print('DEBUG: Boo the yankees won')


		else:
			finalScoreString = '**' + game['home_name'] + '** vs **' + game['away_name'] + '**\n'

			finalScoreString = finalScoreString + 'Game on ' + gameTimeLocal.strftime('%m/%d/%Y') + ' **' + game[
				'status'] + '**'

			await message.channel.send(content=finalScoreString, tts=False)

	async def live_Game_Embed(self, game, message):
		# If for some reason we get a list, take the first object
		if type(game) == list:
			game = game[0]

		homeTeam = statsapi.lookup_team(game['home_name'])
		awayTeam = statsapi.lookup_team(game['away_name'])

		homeTeamShort = homeTeam[0]['fileCode'].upper()
		awayTeamShort = awayTeam[0]['fileCode'].upper()
		# print(game['game_id'])
		'''
		homeScore = game['home_score']
		homeScoreString = str(homeScore)
		awayScore = game['away_score']
		awayScoreString = str(awayScore)
		
		if homeScore > awayScore:
			homeScoreString = '**' + homeScoreString + '**'
		elif awayScore > homeScore:
			awayScoreString = '**' + awayScoreString + '**'
		
		'''
		# Build the content string
		# liveScoreString = '**' +  game['home_name'] + '** vs **' + game['away_name'] + '**\n'

		# liveScoreString = liveScoreString + game['inning_state'] + ' ' + str(game['current_inning']) + '\n'

		# liveScoreString = liveScoreString + '```js\n' + statsapi.linescore(game['game_id']) + '```'

		contextParams = {'gamePk': game['game_id']}
		game_contextMetrics = statsapi.get(endpoint='game_contextMetrics', params=contextParams)
		gameType = game_contextMetrics['game']['gameType']

		# Create the embed object
		scoreEmbed = discord.Embed()

		# Regular Season
		if gameType == 'R':
			scoreEmbed.title = '**' + game['away_name'] + '** vs **' + game['home_name'] + '**'
		# Wildcard
		elif gameType == 'F':
			# Check if the game is a tiebreaker
			if game_contextMetrics['game']['tiebreaker'] == 'N':
				scoreEmbed.title = '**Wildcard Game**\n\n**' + game['away_name'] + '** vs **' + game['home_name'] + '**'
			else:
				scoreEmbed.title = '**Wildcard Tiebreaker Game**\n\n**' + game['away_name'] + '** vs **' + game[
					'home_name'] + '**'
		# Division Series
		elif gameType == 'D':
			homeRecordString = str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' + str(
				game_contextMetrics['game']['teams']['home']['leagueRecord']['losses'])
			awayRecordString = str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' + str(
				game_contextMetrics['game']['teams']['away']['leagueRecord']['losses'])
			scoreEmbed.title = '**Division Series Game ' + str(
				game_contextMetrics['game']['seriesGameNumber']) + '**\n\n**' + game[
								   'away_name'] + '**(' + awayRecordString + ') vs ' + '**' + game[
								   'home_name'] + '**(' + homeRecordString + ')'
		# League Championship Series
		elif gameType == 'L':
			homeRecordString = str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' + str(
				game_contextMetrics['game']['teams']['home']['leagueRecord']['losses'])
			awayRecordString = str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' + str(
				game_contextMetrics['game']['teams']['away']['leagueRecord']['losses'])
			scoreEmbed.title = '**League Championship Series Game ' + str(
				game_contextMetrics['game']['seriesGameNumber']) + '**\n\n**' + game[
								   'away_name'] + '**(' + awayRecordString + ') vs ' + '**' + game[
								   'home_name'] + '**(' + homeRecordString + ')'
		# World Series
		elif gameType == 'W':
			homeRecordString = str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' + str(
				game_contextMetrics['game']['teams']['home']['leagueRecord']['losses'])
			awayRecordString = str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' + str(
				game_contextMetrics['game']['teams']['away']['leagueRecord']['losses'])
			scoreEmbed.title = '**World Series Game ' + str(
				game_contextMetrics['game']['seriesGameNumber']) + '**\n\n**' + game[
								   'away_name'] + '**(' + awayRecordString + ') vs ' + '**' + game[
								   'home_name'] + '**(' + homeRecordString + ')'
		# Spring Training
		elif gameType == 'S':
			homeRecordString = str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' + str(
				game_contextMetrics['game']['teams']['home']['leagueRecord']['losses'])
			awayRecordString = str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' + str(
				game_contextMetrics['game']['teams']['away']['leagueRecord']['losses'])
			scoreEmbed.title = '**Spring Training**\n\n**' + game['away_name'] + '** vs **' + game['home_name'] + '**'
		else:
			scoreEmbed.title = '**' + game['away_name'] + '** vs **' + game['home_name'] + '**'

		scoreEmbed.type = 'rich'
		scoreEmbed.color = discord.Color.dark_blue()

		scoreEmbed.add_field(name='**' + game['inning_state'] + ' ' + str(game['current_inning']) + '**',
							 value='```js\n' + statsapi.linescore(game['game_id']) + '```', inline=False)
		# scoreEmbed.add_field(name=awayTeamShort , value=awayScoreString, inline=True)
		# scoreEmbed.add_field(name='Linescore', value='```' + statsapi.linescore(game['game_id']) + '```')

		homeWinProb = '{:.1f}'.format(game_contextMetrics['homeWinProbability'])
		awayWinProb = '{:.1f}'.format(game_contextMetrics['awayWinProbability'])

		# Show the win %
		scoreEmbed.add_field(name='**Win Probability**',
							 value=awayTeamShort + ' ' + awayWinProb + ' - ' + homeTeamShort + ' ' + homeWinProb + '%')
		# scoreEmbed.add_field(name=homeTeamShort + ' win %', value=game_contextMetrics['homeWinProbability'].format(1), inline=True)
		# scoreEmbed.add_field(name=awayTeamShort + ' win %', value=game_contextMetrics['awayWinProbability'].format(1), inline=True)

		'''
		DEBUG: game_contextMetrics
		DEBUG: %s {'game': {'gamePk': 55555, 'link': '/api/v1/game/55555/feed/live', 'gameType': 'R', 'season': '2006', 
		'gameDate': '2006-06-10T03:33:00Z', 'status': {'abstractGameState': 'Final', 'codedGameState': 'F', 
		'detailedState': 'Final', 'statusCode': 'F', 'startTimeTBD': True, 'abstractGameCode': 'F'}, 
		'teams': {'away': {'leagueRecord': {'wins': 7, 'losses': 0, 'pct': '1.000'}, 'score': 5, 
		'team': {'id': 604, 'name': 'DSL Blue Jays', 'link': '/api/v1/teams/604'}, 'isWinner': True, 
		'splitSquad': False, 'seriesNumber': 7}, 'home': {'leagueRecord': {'wins': 2, 'losses': 4, 'pct': '.333'}, 
		'score': 3, 'team': {'id': 616, 'name': 'DSL Indians', 'link': '/api/v1/teams/616'}, 'isWinner': False, 
		'splitSquad': False, 'seriesNumber': 6}}, 'venue': {'id': 401, 'name': 'Generic', 
		'link': '/api/v1/venues/401'}, 'content': {'link': '/api/v1/game/55555/content'}, 'isTie': False, 
		'gameNumber': 1, 'publicFacing': True, 'doubleHeader': 'N', 'gamedayType': 'N', 'tiebreaker': 'N', 
		'calendarEventID': '44-55555-2006-06-10', 'seasonDisplay': '2006', 'dayNight': 'day', 'scheduledInnings': 9, 
		'inningBreakLength': 0, 'gamesInSeries': 1, 'seriesGameNumber': 1, 'seriesDescription': 'Regular Season', 
		'recordSource': 'S', 'ifNecessary': 'N', 'ifNecessaryDescription': 'Normal Game', 
		'gameId': '2006/06/10/dblrok-dinrok-1'}, 'expectedStatisticsData': {}, 'leftFieldSacFlyProbability': {}, 
		'centerFieldSacFlyProbability': {}, 'rightFieldSacFlyProbability': {}, 'awayWinProbability': 100.0, 
		'homeWinProbability': 0.0}
		'''

		# If the game is not a spring training game, pull the scoring plays
		if gameType != 'S':

			scoringPlaysList = statsapi.game_scoring_play_data(game['game_id'])
			scoringPlays = scoringPlaysList['plays']
			print(*scoringPlays)


			if len(scoringPlays) > 1:
				# scoringPlaysList = scoringPlays.split('\n\n')
				# for plays in scoringPlaysList:
				#	scoreEmbed.add_field(name=str(scoringPlaysList.index(plays) + 1), value=plays, inline=False)

				# Display only the latest scoring play
				scoreEmbed.add_field(name='**Latest scoring play**', value=scoringPlays[len(scoringPlays) - 1]['result']['description'],
									 inline=False)
				if len(scoringPlays) > 2:
					# Set the footer to inform the user about additional plays
					scoreEmbed.set_footer(text='Reply with \'more\' in 30 seconds to see all scoring plays')

			# Send the message
			await message.channel.send(embed=scoreEmbed, tts=False)

			if len(scoringPlays) > 2:
				# Wait for the user response
				if await self.commonFunctions.wait_for_response(message, 'more', 30):
					# Create a new embed object to contain all scoring plays
					allPlaysEmbed = discord.Embed()
					# allPlaysEmbed.title = '**All scoring plays**'
					allPlaysEmbed.type = 'rich'
					allPlaysEmbed.color = discord.Color.dark_blue()
					scoring_plays_string = ""
					for index, plays in enumerate(scoringPlays):
						scoring_plays_string = scoring_plays_string + str(index + 1) + '. ' + plays['result']['description'] + '\n\n'
					allPlaysEmbed.add_field(name='**All scoring plays**',
											value=scoring_plays_string, inline=False)

					# for plays in scoringPlays:
					# 	allPlaysEmbed.add_field(name=str(scoringPlays.index(plays) + 1),
					# 							value=plays['result']['description'], inline=False)
					await message.channel.send(embed=allPlaysEmbed, tts=False)
					return
				else:
					return
			return
		else:
			# Send the message
			await message.channel.send(embed=scoreEmbed, tts=False)
			return

	async def generic_Game_Embed(self, game, message):
		# If for some reason we get a list, take the first object
		if type(game) == list:
			game = game[0]

		# Get the UTC datetime string
		gameTimeLocal = self.commonFunctions.get_Local_Time(game['game_datetime'])

		# Create the final game embed object
		genricGameEmbed = discord.Embed()
		genricGameEmbed.type = 'rich'
		genricGameEmbed.color = discord.Color.dark_blue()

		# Add the fields with game info
		genricGameEmbed.add_field(name='**' + game['away_name'] + '** vs **' + game['home_name'] + '**\n',
								 value='Game on ' + gameTimeLocal.strftime('%m/%d/%Y') + ' Status: ' + game['status'], inline=False)

		await message.channel.send(embed=genricGameEmbed)


	async def playoff_Series_Embed(self, series, message):
		# Create a list of the games in the series
		seriesGames = series['games']

		# Get the game ID of the last game in the series
		lastGameId = seriesGames[len(seriesGames) - 1]['gamePk']
		contextParams = {'gamePk': lastGameId}
		game_contextMetrics = statsapi.get(endpoint='game_contextMetrics', params=contextParams)

		homeRecordString = '(' + str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' + str(
			game_contextMetrics['game']['teams']['home']['leagueRecord']['losses']) + ')'

		awayRecordString = '(' + str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' + str(
			game_contextMetrics['game']['teams']['away']['leagueRecord']['losses']) + ')'

		titleString = seriesGames[0]['seriesDescription'] + '\n**' + \
					  game_contextMetrics['game']['teams']['home']['team']['name'] + homeRecordString + '** vs **' \
					  + game_contextMetrics['game']['teams']['away']['team']['name'] + awayRecordString + '**'

		# game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']

		playoffEmbed = discord.Embed()
		playoffEmbed.title = titleString
		playoffEmbed.type = 'rich'
		playoffEmbed.color = discord.Color.dark_blue()

		for games in seriesGames:

			# Get the team names from the game
			homeTeam = statsapi.lookup_team(games['teams']['home']['team']['name'])
			awayTeam = statsapi.lookup_team(games['teams']['away']['team']['name'])
			# Get the short team names
			# If the team isn't decided yet then pull it from the response
			if homeTeam:
				homeTeamShort = homeTeam[0]['fileCode'].upper()
			else:
				homeTeamShort = games['teams']['home']['team']['name']

			if awayTeam:
				awayTeamShort = awayTeam[0]['fileCode'].upper()
			else:
				awayTeamShort = games['teams']['away']['team']['name']

			if games['status']['detailedState'] == 'Final' or games['status']['detailedState'] == 'Game Over':
				homeScore = games['teams']['home']['score']
				homeScoreString = str(homeScore)
				awayScore = games['teams']['away']['score']
				awayScoreString = str(awayScore)

				if homeScore > awayScore:
					homeScoreString = '**' + homeScoreString + '**'
				elif awayScore > homeScore:
					awayScoreString = '**' + awayScoreString + '**'

				finalGameString = homeTeamShort + ' ' + homeScoreString + ' - ' + awayTeamShort + ' ' + awayScoreString + ' **F**'  # \n' + \
				# homeTeamShort + '(' + str(games['teams']['home']['leagueRecord']['wins']) + '-' + str(games['teams']['home']['leagueRecord']['losses']) + ') - ' + \
				# awayTeamShort + '(' + str(games['teams']['away']['leagueRecord']['wins']) + '-' + str(games['teams']['away']['leagueRecord']['losses']) + ')'

				playoffEmbed.add_field(name='Game ' + str(games['seriesGameNumber']), value=finalGameString,
									   inline=False)
			elif games['status']['detailedState'] == 'Scheduled' or games['status']['detailedState'] == 'Pre-Game':

				gameLocalTime = self.commonFunctions.get_Local_Time(games['gameDate'])

				valueString = awayTeamShort + ' vs ' + homeTeamShort + '\n'
				valueString = valueString + calendar.day_name[gameLocalTime.weekday()] + '\n' + gameLocalTime.strftime(
					'%m/%d/%Y') + ' at ' + gameLocalTime.strftime('%-I:%M%p') + ' EST'

				if games['ifNecessary'] == 'N':
					playoffEmbed.add_field(name='Game ' + str(games['seriesGameNumber']), value=valueString,
										   inline=False)
				else:
					playoffEmbed.add_field(name=games['description'] + ' (If Necessary)', value=valueString,
										   inline=False)
			elif games['status']['detailedState'] == 'In Progress' or games['status']['detailedState'] == 'Live':
				homeScore = games['teams']['home']['score']
				homeScoreString = str(homeScore)
				awayScore = games['teams']['away']['score']
				awayScoreString = str(awayScore)

				if homeScore > awayScore:
					homeScoreString = '**' + homeScoreString + '**'
				elif awayScore > homeScore:
					awayScoreString = '**' + awayScoreString + '**'

				liveGameString = awayTeamShort + ' ' + awayScoreString + ' - ' + homeTeamShort + ' ' + homeScoreString + '\n' + \
								 games['status']['detailedState']
				playoffEmbed.add_field(name='Game ' + str(games['seriesGameNumber']) + '\nLive Game',
									   value=liveGameString, inline=False)

		await message.channel.send(embed=playoffEmbed)

	async def helpEmbed(self, message):
		helpEmbed = discord.Embed()
		helpEmbed.title = 'BaseBot Help'
		helpEmbed.type = 'rich'
		helpEmbed.color = discord.Color.dark_blue()

		helpEmbed.add_field(name='1. basebot player `playername` `year`', value='Lookup a players stats (Defaults to current year)', inline=False)
		helpEmbed.add_field(name='2. basebot score `teamname`', value='Lookup the latest game', inline=False)
		helpEmbed.add_field(name='3. basebot highlights `teamname`', value='Lookup the latest highlights', inline=False)
		helpEmbed.add_field(name='4. basebot roster `teamname`', value='Display the team\'s current roster',
							inline=False)
		helpEmbed.add_field(name='5. basebot standings', value='Show the current league standings', inline=False)
		helpEmbed.add_field(name='6. basebot schedule `teamname`',
							value='Show the team\'s scheduled games for the next week', inline=False)
		helpEmbed.add_field(name='7. basebot schedule',
							value='Show today\'s scheduled games',
							inline=False)
		helpEmbed.add_field(name='8. basebot playoffs',
							value='Get an overview of the playoffs',
							inline=False)
		helpEmbed.add_field(name='9. basebot hockey',
							value='Show the current days hockey games. NOTE: This will move to a new bot soon',
							inline=False)
		helpEmbed.add_field(name='10. basebot listen `channelname`',
							value='Listen to commands on the given text channel. Use `all` to listen to all available channels',
							inline=False)
		helpEmbed.add_field(name='11. basebot ignore `channelname`',
							value='Ignore commands on the given text channel',
							inline=False)
		helpEmbed.add_field(name='12. basebot listchannels',
							value='Get a list of all channels currently being listened to',
							inline=False)

		await message.channel.send(embed=helpEmbed)

	# If game in progress

	# If game over

	# If game scheduled

	# If the series is over, write a message indicating such
