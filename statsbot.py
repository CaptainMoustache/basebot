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

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged on as', self.user)
		await self.change_presence(activity=discord.Game(name='with myself'))
	
	
	
	async def on_message(self, message):
		# don't respond to ourselves
		if message.author == self.user:
			return
		else:
				#Split the message at whitespace
				messageArray = message.content.split()
				#Bot was called with enough arguments
				if messageArray[0].upper() == 'STATSBOT' and len(messageArray) >= 2:
					#if the first message part is 'player' lookup the players stats
					if messageArray[1].upper() == 'PLAYER':
						#Set the year to lookup to the current year
						now = datetime.datetime.now()
						statYear = now.year
						#check if the input is empty
						if len(messageArray) < 2:
							await message.channel.send('I need at least a name to search yah dingus.')
							return
						#There is a search string
						else:
							#search for the playerid
							#create a list of mention strings
							mentionList = []
							for users in self.guilds[0].members:
								mentionList.append(users.mention)
							
							#if someone is being a smartass
							if messageArray[2].upper() == 'PENIS':
								await message.channel.send('My penis is currently batting 1000 with your mom')
								return
							elif messageArray[2].upper() == 'KAPPA':
								await message.channel.send(u'\u0028 \u0361 \u00B0 \u035C \u0296 \u0361 \u00B0 \u0029')
								return
							#if trying to use a channel member
							elif messageArray[2].upper() in mentionList:
								#Print random insult
								#index = random.randint(1, 20)
								
								insultList = []
								insultList.append('%s is so bad they couldn\'t hit the ground if they fell off a ladder')
								insultList.append('%s gets less hits than an Amish website')
								insultList.append('%s hasn\'t reached second base since prom')
								insultList.append('%s loves playing catcher...')
								insultList.append('A toaster throws more heat than %s')
								insultList.append('Yoko Ono has better pitch control than %s')
								insultList.append('%s couldn\'t even save a word file')
								insultList.append('%s couldn\'t buy a cup of coffee with their batting average')
								insultList.append('I just named my new dog %s, because he gets beaten every day')
								insultList.append('%s couldn\'t beat the Helen Keller School Team')
								insultList.append('%s is a Butterface Cock Box')
								insultList.append('%s is a triple bagger, one for me, one for them, and one for anyone walking by')
								insultList.append('%s is so ugly their mother breast fed them through a straw')
								insultList.append('%s looks like they were drawn with my left hand')
								insultList.append('I would call %s\'s aim cancer, but cancer kills people')

								await message.channel.send(insultList[random.randint(0, len(insultList) - 1)] % messageArray[2])
								return
							#We might have an actual name to search
							else:
								#Parse year if supplied after a name or names
								if messageArray[len(messageArray) - 1].isdigit() and len(messageArray) > 3:
									#print ('DEBUG: Year detected')
									#The last part of the message is a year
									if int(messageArray[len(messageArray) - 1]) > now.year:
										await message.channel.send('I wish I could predict the future, for now try a year before %s' % now.year)
										return
									elif int(messageArray[len(messageArray) - 1]) < 1900:
										await message.channel.send('Right now I don\'t work with dates pre 1900. Sorry')
										return
									else:
										statYear = messageArray[len(messageArray) - 1]

								#Get the name and ignore the year
								if messageArray[len(messageArray) - 1].isdigit():
									#name is one part
									if len(messageArray) - 1 == 3:
										nameToSearch = messageArray[2] + '%25'
										displayNameToSearch = messageArray[2]
									#name is two parts
									elif len(messageArray) - 1 == 4:
										nameToSearch = messageArray[2] + ' ' + messageArray[3]
										displayNameToSearch = nameToSearch
									else:
										print('DEBUG: I couldn\'t figure the name out with the year :(')
								#Get the name, no year supplied
								else:
									#name is one part
									if len(messageArray) == 3:
										nameToSearch = messageArray[2] + '%25'
										displayNameToSearch = messageArray[2]
									#name is two parts
									elif len(messageArray) == 4:
										nameToSearch = messageArray[2] + ' ' + messageArray[3]
										displayNameToSearch = nameToSearch
									else:
										print('DEBUG: I couldn\'t figure the name out without the year :(')
						#Check that we have a valid name to search
						if nameToSearch == None or nameToSearch == '':
							await message.channel.send('I didn\'t get a name to search. Something went wrong, Sorry')
							return
						
							
						#build the playerSearchURL
						activePlayerSearchURL = 'http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=\'mlb\'&active_sw=\'Y\'&name_part=\'' + nameToSearch + '\''
						#build the headers
						playerSearchHeaders = {'Content-Type': 'application/json'}
						#Send the get request
						playerSearch = requests.get(activePlayerSearchURL, playerSearchHeaders)
						#parse the json response
						playerSearchJson = json.loads(playerSearch.text)
						
						#get the number of players found
						playersFoundCount = playerSearchJson['search_player_all']['queryResults']['totalSize']
						
						#Create a list of PlayerSearchInfo objects
						playerSearchResultsList = []
						
						#Populate the list of PlayerSearchInfo objects with all players returned
						for searchIndex in range(int(playersFoundCount)):
							foundPlayer = players.PlayerSearchInfo()
							foundPlayer.ParseJson(playerSearchJson, searchIndex)
							playerSearchResultsList.append(foundPlayer)
						
						#We have multiple matches, list them and prompt for number
						if len(playerSearchResultsList) > 1:
							#Make sure the list isn't too big
							if len(playerSearchResultsList) > 50:
								await message.channel.send('I found over 50 matches for ' + displayNameToSearch + '. \n Try being a little more specific')
								return
							
							#TODO make this dynamically list the team and position based on year
							playerGenInfoList = []
							
							for player in playerSearchResultsList:
								playerGenInfoLoop = players.PlayerInfo()
								#Send GET to download player info
								# http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id='493316'
								playerInfoURL = 'http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code=\'mlb\'&player_id=\'' + player.player_id + '\''
								playerInfoHeader = {'Content-Type': 'application/json'}
								playerInfoRequest = requests.get(playerInfoURL, playerInfoHeader)
								playerInfoJson = json.loads(playerInfoRequest.text)
								playerGenInfoLoop.ParseJson(playerInfoJson)
								#Append the playerInfo to the list
								playerGenInfoList.append(playerGenInfoLoop)
							

							#Build the display string
							discordFormattedString = '>>> I found ' + str(len(playerSearchResultsList)) + ' players matching **' + displayNameToSearch + '** in ' + str(statYear) + '\n Enter the number for the player you want \n\n'
							
							
							#Build the string to display the found players
							for index in range(len(playerSearchResultsList)):
								#Add a newline for the next list item
								if index < len(playerSearchResultsList):
									appendString = ' ' + str(index + 1) + ': ' + playerGenInfoList[index].name_display_first_last + ' - ' + playerGenInfoList[index].team_name + ' (' + playerGenInfoList[index].primary_position_txt + ')' + '\n'
								else:
									appendString = ' ' + str(index + 1) + ': ' + playerGenInfoList[index].name_display_first_last + ' - ' + playerGenInfoList[index].team_name + ' (' + playerGenInfoList[index].primary_position_txt + ')'
								discordFormattedString = discordFormattedString + appendString
						
							#Send the message to the channel
							await message.channel.send(discordFormattedString)
							messageTime = datetime.datetime.utcnow()
							time.sleep(2)
							
							#Initialize a new PlayerInfo object
							playerGenInfo = players.PlayerInfo()
							
							#Wait 10 seconds to get an answer
							for wait in range(1, 10):
								if playerGenInfo.player_id != '':
									break;
							
								time.sleep(1)
								#Get the last ten messages
								messageList = await message.channel.history(limit=2).flatten()
								
								#if the name hasn't been selected yet
								if playerGenInfo.player_id == '':
									#loop through the past 2 messages
									for history in range (0, len(messageList)):
										#The user who requested the list responded
										if messageList[history].author == message.author:
											#check if the message was sent after the list of names
											if messageList[history].created_at > messageTime:
												#The user responded with a number
												if messageList[history].content.isdigit():
													#The number is valid
													if int(messageList[history].content) <= len(playerSearchResultsList) and int(messageList[history].content) != 0:
														playerSelected = int(messageList[history].content)
														playerGenInfo = playerGenInfoList[playerSelected - 1]
														
														#selectedNameToSearch = playerGenInfoList[playerSelected - 1].name_display_first_last
														break
													else:
														await message.channel.send('%s is not a valid number, start over' % str(messageList[history].content))
														return
												else:
													await message.channel.send('%s is not a number, start over' % messageList[history].content)
													return
							#if the loop completes without a selection inform the user
							if 	playerGenInfo.player_id == '':
									await message.channel.send('I\'m getting bored waiting for you, start over when you\'re ready.')
									return
							
						#Only one player was returned from the search
						elif len(playerSearchResultsList) == 1:
							#Initialize a new PlayerSearchInfo object
							playerGenInfo = players.PlayerInfo()
							
							playerInfoURL = 'http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code=\'mlb\'&player_id=\'' + playerSearchResultsList[0].player_id + '\''
							playerInfoHeader = {'Content-Type': 'application/json'}
							playerInfoRequest = requests.get(playerInfoURL, playerInfoHeader)
							playerInfoJson = json.loads(playerInfoRequest.text)
							
							#Parse the json info and populate all the properties
							playerGenInfo.ParseJson(playerInfoJson)
						elif len(playerSearchResultsList) == 0:
							await message.channel.send('I couldn\'t find any players with the name %s ' % displayNameToSearch)
							return
						
						#print('DEBUG: PlayerID = %s' % playerGenInfo.player_id)
						
						#player is NOT a pitcher
						if playerGenInfo.primary_position_txt != 'P':
							#Get their stats
							#Right now this is hardcoded for the regular season
							playerStatsURL = 'http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id=\'mlb\'&game_type=\'R\'&season=\'' + str(statYear) + '\'&player_id=\'' + playerGenInfo.player_id + '\''
							playerStatsHeader = {'Content-Type': 'application/json'}
							playerStatsRequest = requests.get(playerStatsURL, playerStatsHeader)
							playerStatsJson = json.loads(playerStatsRequest.text)
							
							if int(playerStatsJson['sport_hitting_tm']['queryResults']['totalSize']) == 0:
								await message.channel.send('%s doesn\'t appear to have any stats for %s' % (playerGenInfo.name_display_first_last, statYear))
								return
							
							#Create a new SeasonBattingStats object
							seasonBattingInfo = players.SeasonBattingStats()
							#Parse the season batting stats
							seasonBattingInfo.ParseJson(playerStatsJson)
							
							#Send the message back to the channel
							await message.channel.send('>>> **%s\'s** (%s) Stats for **%s**\n' \
							' Batting Avg: %s\n' \
							' HomeRuns: %s\n' \
							' Slugging: %s\n' \
							' OPS: %s\n' \
							' RBI: %s' % (playerGenInfo.name_display_first_last, seasonBattingInfo.team_abbrev, statYear, seasonBattingInfo.avg, seasonBattingInfo.hr, seasonBattingInfo.slg, seasonBattingInfo.ops, seasonBattingInfo.rbi))
						else:
							#Get their stats
							#Right now this is hardcoded for the regular season
							playerStatsURL = 'http://lookup-service-prod.mlb.com/json/named.sport_pitching_tm.bam?league_list_id=\'mlb\'&game_type=\'R\'&season=\'' + str(statYear) + '\'&player_id=\'' + playerGenInfo.player_id + '\''
							playerStatsHeader = {'Content-Type': 'application/json'}
							playerStatsRequest = requests.get(playerStatsURL, playerStatsHeader)
							playerStatsJson = json.loads(playerStatsRequest.text)
							
							if int(playerStatsJson['sport_pitching_tm']['queryResults']['totalSize']) == 0:
								await message.channel.send('%s doesn\'t appear to have any stats for %s' % (playerGenInfo.name_display_first_last, statYear))
								return
							
							#Create a new SeasonBattingStats object
							seasonPitchingInfo = players.SeasonPitchingStats()
							#Parse the season batting stats
							seasonPitchingInfo.ParseJson(playerStatsJson)
							
							#Send the message back to the channel
							await message.channel.send('>>> **%s\'s** (%s) Stats for **%s**\n' \
							' ERA: %s\n' \
							' Wins/Losses: %s/%s\n' \
							' Games: %s\n' \
							' WHIP: %s' % (playerGenInfo.name_display_first_last, seasonPitchingInfo.team_abbrev, statYear, seasonPitchingInfo.era, seasonPitchingInfo.w, seasonPitchingInfo.l, seasonPitchingInfo.gs, seasonPitchingInfo.whip))

					elif messageArray[1].upper() == 'SCORE':
						targetDateTime = datetime.datetime.now()
					
						#Get the team
						teamSelected = await self.get_team(messageArray[2], message)
						
						#Get that teams most recent game
						most_recent_game = statsapi.last_game(int(teamSelected['id']))
						
						#Set the target game to the value returned from statsapi.last_game
						target_game = statsapi.schedule(game_id=most_recent_game)
						#Get the game previous to the returned game
						
						#Get a list of games a week in the past
						pastDay = datetime.datetime.today()
						pastWeek = datetime.datetime.today() - timedelta(7)
						pastGames = statsapi.schedule(start_date=pastWeek.strftime('%m/%d/%Y'), end_date=pastDay.strftime('%m/%d/%Y'), team=teamSelected['id'])
						
						#Get a list of games a week in the future
						nextDay = datetime.datetime.today() + timedelta(1)
						NextWeek = datetime.datetime.today() + timedelta(7)
						nextGames = statsapi.schedule(start_date=nextDay.strftime('%m/%d/%Y'), end_date=NextWeek.strftime('%m/%d/%Y'), team=teamSelected['id'])
						
						
						#TODO handle no previous games returned
						print('Past Games')
						for games in pastGames:
							print('game_id = %s | game_datetime = %s ' % (games['game_datetime'], games['game_datetime']))
						
						print('Next Games')
						for games in nextGames:
							print('game_id = %s | game_datetime = %s ' % (games['game_datetime'], games['game_datetime']))
						
						#TODO If the target game is the same as the most recent pastGames[n] then access pastGames[n - 1]
						
						if len(pastGames) > 0:
							prev_game = pastGames[len(pastGames) - 1]
						
						#Check if the previous game is still 'In Progress' and if so set that as the target game
						#Apprently sometimes the MLB api returns the next game sometimes
						if prev_game['status'] == 'In Progress' and target_game[0]['status'] == 'Scheduled':
							target_game = prev_game
						else:
							target_game = target_game[0]
						
						#Game is over
						if target_game['status'] == 'Final':
							await self.final_Game_Embed(target_game, message)
						#Game is scheduled	
						elif target_game['status'] == 'Scheduled' or target_game['status'] == 'Pre-Game':	
							await self.scheduled_Game_Embed(target_game, message)
							await self.final_Game_Embed(pastGames[len(pastGames) - 1], message)
						elif target_game['status'] == 'In Progress':
							await self.live_Game_Embed(target_game, message)
						
					elif messageArray[1].upper() == 'HIGHLIGHTS':
						teamSelected = await self.get_team(messageArray[2], message)

						pastDay = datetime.datetime.today()

						#Get the last game
						lastGameInfo = statsapi.last_game(teamSelected['id'])
						
						#Get the highlights for the last game
						highlights = statsapi.game_highlights(lastGameInfo)
						
						#If no highlights are returned then check the previous dates for a game
						if len(highlights) == 0:
						
							#Look back one week for highlights
							for day in range(0, 7):
								pastDay = datetime.datetime.today() - timedelta(day)
								schedule = statsapi.schedule(date=pastDay.strftime('%m/%d/%Y'), team=teamSelected['id'])
								#TODO check for a double header
								nextToLastGameInfo = schedule[0]['game_id']
								highlights = statsapi.game_highlights(nextToLastGameInfo)
								if len(highlights) > 0:
									break
							
							#Attempt to get the next to last game highlights
							# = datetime.datetime.today() - timedelta(1)
							#schedule = statsapi.schedule(date=yesterday.strftime('%m/%d/%Y'), team=teamSelected['id'])
							
							#TODO support double headers
							#nextToLastGameInfo = schedule[0]['game_id']
							
							#Get the highlights for the last game
							highlights = statsapi.game_highlights(nextToLastGameInfo)
						
						if len(highlights) > 0:
						
							#split the highlights on the line breaks of the video links returned
							highlightsList = highlights.split('\n\n')
							#split each highlight on the newline to get 0. Short description 1. Long description 2. Video Link
							splitHighlightsList = []
							for listItem in highlightsList:
								splitHighlightsList.append(listItem.split('\n'))
							
							#discordFormattedString = '>>> Here are the latest highlights from the **' +  teamSelected['name'] + '** on ' + pastDay.strftime('%m/%d/%Y') + '\n'
							
							#Create the embed object
							highlightEmbed = discord.Embed()
							highlightEmbed.title = '**' +  teamSelected['name'] + '** highlights from ' + pastDay.strftime('%m/%d/%Y')
							highlightEmbed.type = 'rich'
							#testEmbed.colour = 
							highlightEmbed.color = discord.Color.dark_blue()
							
							
							#Loop through all the returned highlights and format the strings
							for index in range(0, len(highlightsList) - 1):
								#Replace https with <https
								#splitHighlightsList[index][2] = splitHighlightsList[index][2].replace('https', '<https')
								#Replace .mp4 with .mp4>
								#splitHighlightsList[index][2] = splitHighlightsList[index][2].replace('.mp4', '.mp4>')
								
								#If we haven't hit the character limit yet, add the next highlight
								if len(highlightEmbed) < 6000:
									highlightEmbed.add_field(name=splitHighlightsList[index][0], value='[' + splitHighlightsList[index][2][:27]  + '...]' + '(' + splitHighlightsList[index][2] + ')', inline=False)
															

							await message.channel.send(embed=highlightEmbed)
						else:
							await message.channel.send('Sorry, I couldn\'t find any highlights for the past week')
							
							
					
					elif messageArray[1].upper() == 'ROSTER':
						teamSelected = await self.get_team(messageArray[2], message)
						
						print ('DEBUG: teamSelected in ROSTER = %s' % teamSelected)
						
						await message.channel.send('>>> Here is the current roster for the **' + teamSelected['name'] + '**:\n ' + statsapi.roster(int(teamSelected['id'])))
						
						
					elif messageArray[1].upper() == 'GIBBY':
						#Create the embed
						#https://i.imgur.com/NXWswde.png
						
						
						#Create the embed object
						gibbyEmbed = discord.Embed()
						gibbyEmbed.title = '**BRUDDA**'
						gibbyEmbed.type = 'rich'
						#testEmbed.colour = 
						gibbyEmbed.color = discord.Color.dark_blue()
						
						pewPewId = '<@&607777470208540710>'
						
						gibbyEmbed.set_image(url='https://i.imgur.com/kqGHmdi.jpg')
						gibbyEmbed.image.width = 500
						gibbyEmbed.image.height = 600
						
						#await message.channel.send('%s' % pewPewId)
						await message.channel.send(content=pewPewId,embed=gibbyEmbed)
						
						
						roles = []
						roles = message.role_mentions
						for index in range(0, len(roles)):
							print(roles[index].id)
							print(roles[index].mention)

					#Display the help message
					elif messageArray[1].upper() == 'HELP':
						await message.channel.send('>>> use \'statsbot player PLAYERNAME\' to lookup a players stats. \n use \'statsbot highlights TEAMNAME\' to lookup the latest highlights. \n')
					else:
						await message.channel.send('Sorry all I support right now is player stats.')
				#Bot was called without enough arguments
				elif messageArray[0].upper() == 'STATSBOT' and len(messageArray) < 1:
					await message.channel.send('I like it when you say my name, but I need more instructions.')
				else:
					return
					
	async def get_team(self, searchName, message):
		teamsReturned = statsapi.lookup_team(searchName)
		if len(teamsReturned) > 1:
			teamSelected = await self.prompt_team(message, searchName, teamsReturned)
		elif len(teamsReturned) == 1:
			teamSelected = teamsReturned[0]
		elif len(teamsReturned) == 0:
			await message.channel.send('Hmmm I couldn\'t find and teams using \'' + searchName + '\'')
			return
		return teamSelected
	
	#Identify which team is being requested by prompting the users with all returned results
	async def prompt_team(self, message, searchTerm, teams):
		#Check that more than one team was passed in
		if len(teams) > 1:
			#Build the string of teams to display
			discordFormattedString = '>>> I found ' + str(len(teams)) + ' matches for \'' + searchTerm + '\' Enter the number for the team you want \n'
			#Build the string to display the found players
			for index in range(len(teams)):
				#Add a newline for the next list item
				if index < len(teams):
					appendString = ' ' + str(index + 1) + ': ' + teams[index]['name'] + '\n'
				else:
					appendString = ' ' + str(index + 1) + ': ' + teams[index]['name']
				discordFormattedString = discordFormattedString + appendString
			await message.channel.send(discordFormattedString)
			
			messageTime = datetime.datetime.utcnow()
			time.sleep(2)
			teamSelectedIndex = 0
			
			#Wait 10 seconds to get an answer
			for wait in range(1, 10):
				if teamSelectedIndex != 0:
					break;
			
				time.sleep(1)
				#Get the last ten messages
				messageList = await message.channel.history(limit=2).flatten()
				
				#if the name hasn't been selected yet
				if teamSelectedIndex == 0:
					#loop through the past 2 messages
					for history in range (0, len(messageList)):
						#The user who requested the list responded
						if messageList[history].author == message.author:
							#check if the message was sent after the list of names
							if messageList[history].created_at > messageTime:
								#The user responded with a number
								if messageList[history].content.isdigit():
									#The number is valid
									if int(messageList[history].content) <= len(teams) and int(messageList[history].content) != 0:
										teamSelectedIndex = int(messageList[history].content)
										teamSelected = teams[teamSelectedIndex - 1]
										break
									else:
										await message.channel.send('%s is not a valid number, start over' % str(messageList[history].content))
										return
								else:
									await message.channel.send('%s is not a number, start over' % messageList[history].content)
									return
			#if the loop completes without a selection inform the user
			if 	teamSelectedIndex == 0:
				await message.channel.send('I\'m getting bored waiting for you, start over when you\'re ready.')
				return
			else:
				return teamSelected
	
	def get_Local_Time(self, dateTimeString):
		gameTimeUTC = dateutil.parser.parse(dateTimeString)
		# Tell the datetime object that it's in UTC time zone since 
		# datetime objects are 'naive' by default
		gameTimeUTC = gameTimeUTC.replace(tzinfo=dateutil.tz.tzutc())
		#Convert to localtime
		return gameTimeUTC.astimezone(dateutil.tz.tzlocal())
	
	async def scheduled_Game_Embed(self, game, message):
		#Get the UTC datetime string
		gameTimeLocal = self.get_Local_Time(game['game_datetime'])
		
		homeTeam = statsapi.lookup_team(game['home_name'])
		awayTeam = statsapi.lookup_team(game['away_name'])
		
		homeTeamShort = homeTeam[0]['fileCode'].upper() 
		awayTeamShort = awayTeam[0]['fileCode'].upper()
		
		#Get the probable pitchers
		homeProbable = game['home_probable_pitcher']
		awayProbable = game['away_probable_pitcher']
		
		#Create the embed object
		scheduledEmbed = discord.Embed()
		scheduledEmbed.title = '**' +  game['home_name'] + '** vs **' + game['away_name'] + '**'
		scheduledEmbed.type = 'rich'
		#testEmbed.colour = 
		scheduledEmbed.color = discord.Color.dark_blue()
		
		#scoreEmbed.add_field(name='NAME', value='VALUE', inline=False)
		scheduledEmbed.add_field(name='Start Time:', value=gameTimeLocal.strftime('%-I:%M%p') + ' EST', inline=False)
		scheduledEmbed.add_field(name=homeTeamShort + ' Probable:' , value=homeProbable, inline=True)
		scheduledEmbed.add_field(name=awayTeamShort+ ' Probable:' , value=awayProbable, inline=True)
		scheduledEmbed.add_field(name='Home Notes' , value=game['home_pitcher_note'], inline=False)
		scheduledEmbed.add_field(name='Away Notes' , value=game['away_pitcher_note'], inline=False)
		await message.channel.send(content='Scheduled Game on ' + gameTimeLocal.strftime('%m/%d/%Y') + ':',embed=scheduledEmbed)
		
	async def final_Game_Embed(self, game, message):
		#Get the UTC datetime string
		gameTimeLocal = self.get_Local_Time(game['game_datetime'])
		
		homeTeam = statsapi.lookup_team(game['home_name'])
		awayTeam = statsapi.lookup_team(game['away_name'])
		
		homeTeamShort = homeTeam[0]['fileCode'].upper() 
		awayTeamShort = awayTeam[0]['fileCode'].upper()
		
		#Get the scores
		homeScore = game['home_score']
		homeScoreString = str(homeScore)
		awayScore = game['away_score']
		awayScoreString = str(awayScore)
		
		#Set the higher score to BOLD
		if homeScore > awayScore:
			homeScoreString = '**' + homeScoreString + '**'
		else:
			awayScoreString = '**' + awayScoreString + '**'
		
		discordFormattedString = ''
		
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
	
	async def live_Game_Embed(self, game, message):
		homeTeam = statsapi.lookup_team(game['home_name'])
		awayTeam = statsapi.lookup_team(game['away_name'])
		
		homeTeamShort = homeTeam[0]['fileCode'].upper() 
		awayTeamShort = awayTeam[0]['fileCode'].upper()
	
		homeScore = game['home_score']
		homeScoreString = str(homeScore)
		awayScore = game['away_score']
		awayScoreString = str(awayScore)
		
		if homeScore > awayScore:
			homeScoreString = '**' + homeScoreString + '**'
		elif awayScore > homeScore:
			awayScoreString = '**' + awayScoreString + '**'
		
		#Create the embed object
		scoreEmbed = discord.Embed()
		scoreEmbed.title = '**' +  game['home_name'] + '** vs **' + game['away_name'] + '**'
		scoreEmbed.type = 'rich'
		#testEmbed.colour = 
		scoreEmbed.color = discord.Color.dark_blue()
		
		scoreEmbed.add_field(name='Inning:', value=game['inning_state'] + ' ' + str(game['current_inning']), inline=False)
		scoreEmbed.add_field(name=homeTeamShort , value=homeScoreString, inline=True)
		scoreEmbed.add_field(name=awayTeamShort , value=awayScoreString, inline=True)
		
		await message.channel.send(content='Live Game:',embed=scoreEmbed)

def ReadTokenFile(filename):
	#Read the token from a file
	try:
		key_file = open(filename, "r")
		token = key_file.read()
		key_file.close()
		return token
	except:
		print("Error loading %s" % filename)
		sys.exit(1)
	else:
		print("No %s file found!" % filename)

def main():
	client = MyClient()
	token = ReadTokenFile('auth')
	client.run(token)
	
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('Stopping Statsbot')
		pass
