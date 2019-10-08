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


class CommonFunctions():
	async def scheduled_Game_Embed(self, game, message):
		#Get the UTC datetime string
		gameTimeLocal = self.get_Local_Time(game['game_datetime'])
		
		homeTeam = statsapi.lookup_team(game['home_name'])
		awayTeam = statsapi.lookup_team(game['away_name'])
		
		#Get the game type
		'''
		[{'id': 'S', 'description': 'Spring Training'}, {'id': 'R', 'description': 'Regular season'}, {'id': 'F', 'description': 'Wild Card Game'}, {'id': 'D', 'description': 'Division Series'}, {'id': 'L', 'description': 'League Championship Series'}, {'id': 'W', 'description': 'World Series'}, {'id': 'C', 'description': 'Championship'}, {'id': 'N', 'description': 'Nineteenth Century Series'}, {'id': 'P', 'description': 'Playoffs'}, {'id': 'A', 'description': 'All-Star game'}, {'id': 'I', 'description': 'Intrasquad'}, {'id': 'E', 'description': 'Exhibition'}]
		'''
		contextParams = {'gamePk': game['game_id']}
		game_contextMetrics = statsapi.get(endpoint='game_contextMetrics', params=contextParams)
		gameType = game_contextMetrics['game']['gameType']
		
		
		
		#If the teams have been announced then read the info
		if len(homeTeam) > 0:
			homeTeamShort = homeTeam[0]['fileCode'].upper()
			#Get the probable pitchers
			homeProbable = game['home_probable_pitcher']
			homeNote = game['home_pitcher_note']
			homeNote = game['home_pitcher_note']
		else:
			homeTeamShort = 'N/A'
			homeProbable = 'N/A'
			homeNote = 'N/A'
			
		if len(awayTeam) > 0:
			awayTeamShort = awayTeam[0]['fileCode'].upper()
			#Get the probable pitchers
			awayProbable = game['away_probable_pitcher']
			awayNote = game['away_pitcher_note']
		else:
			awayTeamShort = 'N/A'
			awayProbable = 'N/A'
			awayNote = 'N/A'
		
		#Create the embed object
		scheduledEmbed = discord.Embed()
		#Regular Season
		if gameType == 'R':
			scheduledEmbed.title = '**' +  game['home_name'] + '** vs **' + game['away_name'] + '**'
		#Wildcard
		elif gameType == 'F':
			#Check if the game is a tiebreaker
			if game_contextMetrics['game']['tiebreaker'] == 'N':
				scheduledEmbed.title = '**Wildcard Game**\n\n**' +  game['home_name'] + '** vs **' + game['away_name'] + '**'
			else:
				scheduledEmbed.title = '**Wildcard Tiebreaker Game**\n\n**' +  game['home_name'] + '** vs **' + game['away_name'] + '**'
		#Division Series
		elif gameType == 'D':
			homeRecordString = str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' +  str(game_contextMetrics['game']['teams']['home']['leagueRecord']['losses'])
			awayRecordString = str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' +  str(game_contextMetrics['game']['teams']['away']['leagueRecord']['losses'])
			scheduledEmbed.title = '**Division Series Game ' + str(game_contextMetrics['game']['seriesGameNumber']) + '**\n\n**' +  game['home_name'] + '**(' + homeRecordString + ') vs ' + '**' + game['away_name'] + '**(' + awayRecordString + ')'
		#League Championship Series
		elif gameType == 'L':
			homeRecordString = str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' +  str(game_contextMetrics['game']['teams']['home']['leagueRecord']['losses'])
			awayRecordString = str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' +  str(game_contextMetrics['game']['teams']['away']['leagueRecord']['losses'])
			scheduledEmbed.title = '**League Championship Series Game ' + str(game_contextMetrics['game']['seriesGameNumber']) + '**\n\n**' +  game['home_name'] + '**(' + homeRecordString + ') vs ' + '**' + game['away_name'] + '**(' + awayRecordString + ')'
		#World Series
		elif gameType == 'W':
			homeRecordString = str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' +  str(game_contextMetrics['game']['teams']['home']['leagueRecord']['losses'])
			awayRecordString = str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' +  str(game_contextMetrics['game']['teams']['away']['leagueRecord']['losses'])
			scheduledEmbed.title = '**World Series Game ' + str(game_contextMetrics['game']['seriesGameNumber']) + '**\n\n**' +  game['home_name'] + '**(' + homeRecordString + ') vs ' + '**' + game['away_name'] + '**(' + awayRecordString + ')'
		#Spring Training
		elif gameType == 'S':
			scheduledEmbed.title = '**Spring Training**\n\n**' +  game['home_name'] + '** vs **' + game['away_name'] + '**'
		else:
			scoreEmbed.title = '**' +  game['home_name'] + '** vs **' + game['away_name'] + '**'
		
		
			
		scheduledEmbed.type = 'rich'
		#testEmbed.colour = 
		scheduledEmbed.color = discord.Color.dark_blue()
		
		#scoreEmbed.add_field(name='NAME', value='VALUE', inline=False)
		scheduledEmbed.add_field(name='Start Time:', value=gameTimeLocal.strftime('%-I:%M%p') + ' EST', inline=False)
		
		#Check for returned values
		if not homeProbable:
			homeProbable = 'Unannounced'
		scheduledEmbed.add_field(name=homeTeamShort + ' Probable:' , value=homeProbable, inline=True)
		#Check for returned values
		if not awayProbable:
			awayProbable = 'Unannounced'
		scheduledEmbed.add_field(name=awayTeamShort+ ' Probable:' , value=awayProbable, inline=True)
		#Check for returned values
		if not homeNote:
			homeNote = 'None'

		scheduledEmbed.add_field(name='Home Notes' , value=homeNote, inline=False)
		#Check for returned values
		if not awayNote:
			awayNote = 'None'
		scheduledEmbed.add_field(name='Away Notes' , value=awayNote, inline=False)
		await message.channel.send(content='Scheduled Game on ' + gameTimeLocal.strftime('%m/%d/%Y') + ':',embed=scheduledEmbed)
		
	async def final_Game_Embed(self, game, message):
		#Get the UTC datetime string
		gameTimeLocal = self.get_Local_Time(game['game_datetime'])
		
		if game['status'] == 'Final' or game['status'] == 'Game Over':
			'''
			homeTeam = statsapi.lookup_team(game['home_name'])
			awayTeam = statsapi.lookup_team(game['away_name'])
			
			homeTeamShort = homeTeam[0]['fileCode'].upper() 
			awayTeamShort = awayTeam[0]['fileCode'].upper()
			'''
			'''
			#Get the scores
			homeScore = game['home_score']
			homeScoreString = str(homeScore)
			awayScore = game['away_score']
			awayScoreString = str(awayScore)
			'''
			
			#Create the embed object
			finalEmbed = discord.Embed()
			finalEmbed.type = 'rich'
			finalEmbed.color = discord.Color.dark_blue()
			
			finalEmbed.add_field(name='Winning Pitcher:', value=game['winning_pitcher'] , inline=True)
			finalEmbed.add_field(name='Losing Pitcher:', value=game['losing_pitcher'] , inline=True)
			if game['save_pitcher'] != None:
				finalEmbed.add_field(name='Save:', value=game['save_pitcher'] , inline=False)
			
			'''
			#Build the content string
			finalScoreString = '**' +  game['home_name'] + '** vs **' + game['away_name'] + '**\n'
			
			finalScoreString = finalScoreString + 'Final score from ' + gameTimeLocal.strftime('%m/%d/%Y')
			
			finalScoreString = finalScoreString + '```js\n' + statsapi.linescore(game['game_id']) + '```'
			
			await message.channel.send(content=finalScoreString, embed=finalEmbed, tts=False)
			'''
			#Create the final game embed object
			finalGameEmbed = discord.Embed()
			finalGameEmbed.type = 'rich'
			finalGameEmbed.color = discord.Color.dark_blue()
			
			
			#Add the fields with game info
			finalGameEmbed.add_field(name='**' +  game['home_name'] + '** vs **' + game['away_name'] + '**\n', value='```js\n' + statsapi.linescore(game['game_id']) + '```', inline=False)
						
			finalGameEmbed.add_field(name='Winning Pitcher:', value=game['winning_pitcher'] , inline=True)
			finalGameEmbed.add_field(name='Losing Pitcher:', value=game['losing_pitcher'] , inline=True)
			if game['save_pitcher'] != None:
				finalGameEmbed.add_field(name='Save:', value=game['save_pitcher'] , inline=False)
			
			await message.channel.send(content='Final score from ' + gameTimeLocal.strftime('%m/%d/%Y'), embed=finalGameEmbed, tts=False)
		
		else:
			finalScoreString = '**' +  game['home_name'] + '** vs **' + game['away_name'] + '**\n'
			
			finalScoreString = finalScoreString + 'Game on ' + gameTimeLocal.strftime('%m/%d/%Y') + ' **' + game['status'] + '**'
		
			await message.channel.send(content=finalScoreString, tts=False)
		
		'''
		#Format a string to display the score
		appendString = homeTeamShort + ' ' + homeScoreString + ' F' + '\n'
		discordFormattedString = discordFormattedString + appendString
		
		appendString = awayTeamShort + ' ' + awayScoreString + '\n'
		discordFormattedString = discordFormattedString + appendString
		
		#Create the embed object
		finalEmbed = discord.Embed()
		finalEmbed.title = '**' +  game['home_name'] + '** vs **' + game['away_name'] + '**'
		finalEmbed.type = 'rich'
		finalEmbed.color = discord.Color.dark_blue()
		
		finalEmbed.add_field(name='Score:', value=discordFormattedString, inline=False)
		finalEmbed.add_field(name='Winning Pitcher:', value=game['winning_pitcher'] , inline=True)
		finalEmbed.add_field(name='Losing Pitcher:', value=game['losing_pitcher'] , inline=True)
		if game['save_pitcher'] != None:
			finalEmbed.add_field(name='Save:', value=game['save_pitcher'] , inline=False)
		
		await message.channel.send(content='Final Score from ' + gameTimeLocal.strftime('%m/%d/%Y') + ':',embed=finalEmbed)
		'''
	
	async def live_Game_Embed(self, game, message):
	
		homeTeam = statsapi.lookup_team(game['home_name'])
		awayTeam = statsapi.lookup_team(game['away_name'])
		
		homeTeamShort = homeTeam[0]['fileCode'].upper() 
		awayTeamShort = awayTeam[0]['fileCode'].upper()
	
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
		#Build the content string
		#liveScoreString = '**' +  game['home_name'] + '** vs **' + game['away_name'] + '**\n'
		
		#liveScoreString = liveScoreString + game['inning_state'] + ' ' + str(game['current_inning']) + '\n'
		
		#liveScoreString = liveScoreString + '```js\n' + statsapi.linescore(game['game_id']) + '```'
		
		
		#Get the scoring plays
		scoringPlays = statsapi.game_scoring_plays(game['game_id'])
		
		contextParams = {'gamePk': game['game_id']}
		game_contextMetrics = statsapi.get(endpoint='game_contextMetrics', params=contextParams)
		gameType = game_contextMetrics['game']['gameType']
		
		#Create the embed object
		scoreEmbed = discord.Embed()
		
		#Regular Season
		if gameType == 'R':
			scoreEmbed.title = '**' +  game['home_name'] + '** vs **' + game['away_name'] + '**'
		#Wildcard
		elif gameType == 'F':
			#Check if the game is a tiebreaker
			if game_contextMetrics['game']['tiebreaker'] == 'N':
				scoreEmbed.title = '**Wildcard Game**\n\n**' +  game['home_name'] + '** vs **' + game['away_name'] + '**'
			else:
				scoreEmbed.title = '**Wildcard Tiebreaker Game**\n\n**' +  game['home_name'] + '** vs **' + game['away_name'] + '**'
		#Division Series
		elif gameType == 'D':
			homeRecordString = str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' +  str(game_contextMetrics['game']['teams']['home']['leagueRecord']['losses'])
			awayRecordString = str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' +  str(game_contextMetrics['game']['teams']['away']['leagueRecord']['losses'])
			scoreEmbed.title = '**Division Series Game ' + str(game_contextMetrics['game']['seriesGameNumber']) + '**\n\n**' +  game['home_name'] + '**(' + homeRecordString + ') vs ' + '**' + game['away_name'] + '**(' + awayRecordString + ')'
		#League Championship Series
		elif gameType == 'L':
			homeRecordString = str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' +  str(game_contextMetrics['game']['teams']['home']['leagueRecord']['losses'])
			awayRecordString = str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' +  str(game_contextMetrics['game']['teams']['away']['leagueRecord']['losses'])
			scoreEmbed.title = '**League Championship Series Game ' + str(game_contextMetrics['game']['seriesGameNumber']) + '**\n\n**' +  game['home_name'] + '**(' + homeRecordString + ') vs ' + '**' + game['away_name'] + '**(' + awayRecordString + ')'
		#World Series
		elif gameType == 'W':
			homeRecordString = str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' +  str(game_contextMetrics['game']['teams']['home']['leagueRecord']['losses'])
			awayRecordString = str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' +  str(game_contextMetrics['game']['teams']['away']['leagueRecord']['losses'])
			scoreEmbed.title = '**World Series Game ' + str(game_contextMetrics['game']['seriesGameNumber']) + '**\n\n**' +  game['home_name'] + '**(' + homeRecordString + ') vs ' + '**' + game['away_name'] + '**(' + awayRecordString + ')'
		#Spring Training
		elif gameType == 'S':
			homeRecordString = str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' +  str(game_contextMetrics['game']['teams']['home']['leagueRecord']['losses'])
			awayRecordString = str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' +  str(game_contextMetrics['game']['teams']['away']['leagueRecord']['losses'])
			scoreEmbed.title = '**Spring Training**\n\n**' +  game['home_name'] + '** vs **' + game['away_name'] + '**'
		else:
			scoreEmbed.title = '**' +  game['home_name'] + '** vs **' + game['away_name'] + '**'
		
		
		scoreEmbed.type = 'rich'
		scoreEmbed.color = discord.Color.dark_blue()
		
		scoreEmbed.add_field(name='**' + game['inning_state'] + ' ' + str(game['current_inning']) + '**', value='```js\n' + statsapi.linescore(game['game_id']) + '```', inline=False)
		#scoreEmbed.add_field(name=awayTeamShort , value=awayScoreString, inline=True)
		#scoreEmbed.add_field(name='Linescore', value='```' + statsapi.linescore(game['game_id']) + '```')
		
		homeWinProb = '{:.1f}'.format(game_contextMetrics['homeWinProbability'])
		awayWinPro = '{:.1f}'.format(game_contextMetrics['awayWinProbability'])
		
		#Show the win %
		scoreEmbed.add_field(name='**Win Probability**', value=homeTeamShort + ' ' + homeWinProb + ' - ' + awayTeamShort + ' ' + awayWinPro + '%')
		#scoreEmbed.add_field(name=homeTeamShort + ' win %', value=game_contextMetrics['homeWinProbability'].format(1), inline=True)
		#scoreEmbed.add_field(name=awayTeamShort + ' win %', value=game_contextMetrics['awayWinProbability'].format(1), inline=True)
		
		'''
		DEBUG: game_contextMetrics
		DEBUG: %s {'game': {'gamePk': 55555, 'link': '/api/v1/game/55555/feed/live', 'gameType': 'R', 'season': '2006', 'gameDate': '2006-06-10T03:33:00Z', 'status': {'abstractGameState': 'Final', 'codedGameState': 'F', 'detailedState': 'Final', 'statusCode': 'F', 'startTimeTBD': True, 'abstractGameCode': 'F'}, 'teams': {'away': {'leagueRecord': {'wins': 7, 'losses': 0, 'pct': '1.000'}, 'score': 5, 'team': {'id': 604, 'name': 'DSL Blue Jays', 'link': '/api/v1/teams/604'}, 'isWinner': True, 'splitSquad': False, 'seriesNumber': 7}, 'home': {'leagueRecord': {'wins': 2, 'losses': 4, 'pct': '.333'}, 'score': 3, 'team': {'id': 616, 'name': 'DSL Indians', 'link': '/api/v1/teams/616'}, 'isWinner': False, 'splitSquad': False, 'seriesNumber': 6}}, 'venue': {'id': 401, 'name': 'Generic', 'link': '/api/v1/venues/401'}, 'content': {'link': '/api/v1/game/55555/content'}, 'isTie': False, 'gameNumber': 1, 'publicFacing': True, 'doubleHeader': 'N', 'gamedayType': 'N', 'tiebreaker': 'N', 'calendarEventID': '44-55555-2006-06-10', 'seasonDisplay': '2006', 'dayNight': 'day', 'scheduledInnings': 9, 'inningBreakLength': 0, 'gamesInSeries': 1, 'seriesGameNumber': 1, 'seriesDescription': 'Regular Season', 'recordSource': 'S', 'ifNecessary': 'N', 'ifNecessaryDescription': 'Normal Game', 'gameId': '2006/06/10/dblrok-dinrok-1'}, 'expectedStatisticsData': {}, 'leftFieldSacFlyProbability': {}, 'centerFieldSacFlyProbability': {}, 'rightFieldSacFlyProbability': {}, 'awayWinProbability': 100.0, 'homeWinProbability': 0.0}
		'''
							
		
		if len(scoringPlays) > 1:
			scoringPlaysList = scoringPlays.split('\n\n')
			#for plays in scoringPlaysList:
			#	scoreEmbed.add_field(name=str(scoringPlaysList.index(plays) + 1), value=plays, inline=False)
	
			#Display only the latest scoring play
			scoreEmbed.add_field(name='**Latest scoring play**', value=scoringPlaysList[len(scoringPlaysList) - 1], inline=False)
			if len(scoringPlaysList) > 1:
				#Set the footer to inform the user about additional plays
				scoreEmbed.set_footer(text='Reply with \'more\' in 30 seconds to see all scoring plays')
		
		#Send the message
		await message.channel.send(embed=scoreEmbed, tts=False)
		
		if len(scoringPlaysList) > 1:
			#Wait for the user response
			if await self.wait_for_response(message, 'more', 30):
				#Create a new embed object to contain all scoring plays
				allPlaysEmbed = discord.Embed()
				allPlaysEmbed.title = '**All scoring plays**'
				allPlaysEmbed.type = 'rich'
				allPlaysEmbed.color = discord.Color.dark_blue()
				for plays in scoringPlaysList:
					allPlaysEmbed.add_field(name=str(scoringPlaysList.index(plays) + 1), value=plays, inline=False)
				await message.channel.send(embed=allPlaysEmbed, tts=False)