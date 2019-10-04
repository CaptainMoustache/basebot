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

class BaseballBot(discord.Client):
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
				if len(messageArray) > 0:
					#Bot was called with enough arguments
					if 'STATSBOT' in messageArray[0].upper() and len(messageArray) > 1:
						#if the first message part is 'player' lookup the players stats
						if 'PLAYER' in messageArray[1].upper():
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
								for users in message.channel.members:
									if users.bot == False:
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
							
							#Send the GET
							playerSearch = await self.sendGetRequest(activePlayerSearchURL)
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
									playerGenInfo = players.PlayerInfo()
									#Send GET to download player info
									# http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id='493316'
									
									playerInfoURL = 'http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code=\'mlb\'&player_id=\'' + player.player_id + '\''
									#Send the GET
									playerInfoRequest = await self.sendGetRequest(playerInfoURL)
									playerInfoJson = json.loads(playerInfoRequest.text)
									playerGenInfo.ParseJson(playerInfoJson)
									#Append the playerInfo to the list
									playerGenInfoList.append(playerGenInfo)
								

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
								
								
								
								
								'''
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
								'''	
								playerSelectedIndex = await self.wait_for_number(message, len(playerSearchResultsList), 30)
								
								if playerSelectedIndex:
									playerGenInfo = playerGenInfoList[playerSelectedIndex - 1]
								else:
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
								
								#Create the embed object
								playerEmbed = discord.Embed()
								playerEmbed.title = '**' + playerGenInfo.name_display_first_last + '\'s** Stats for **' +  str(statYear) + '**'
								playerEmbed.type = 'rich'
								#testEmbed.colour = 
								playerEmbed.color = discord.Color.dark_blue()
								
								for index in range(0, seasonBattingInfo.totalSize):
									valueString = ' Batting Avg: %s\n' \
									' HomeRuns: %s\n' \
									' Slugging: %s\n' \
									' OPS: %s\n' \
									' RBI: %s' % (seasonBattingInfo.avg[index], seasonBattingInfo.hr[index], seasonBattingInfo.slg[index], seasonBattingInfo.ops[index], seasonBattingInfo.rbi[index])
									playerEmbed.add_field(name=seasonBattingInfo.team_abbrev[index], value=valueString)
								
								await message.channel.send(embed=playerEmbed)
								'''
								#Send the message back to the channel
								await message.channel.send('>>> **%s\'s** (%s) Stats for **%s**\n' \
								' Batting Avg: %s\n' \
								' HomeRuns: %s\n' \
								' Slugging: %s\n' \
								' OPS: %s\n' \
								' RBI: %s' % (playerGenInfo.name_display_first_last, seasonBattingInfo.team_abbrev, statYear, seasonBattingInfo.avg, seasonBattingInfo.hr, seasonBattingInfo.slg, seasonBattingInfo.ops, seasonBattingInfo.rbi))
								'''
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
																				
								#Create the embed object
								pitcherEmbed = discord.Embed()
								pitcherEmbed.title = '**' + playerGenInfo.name_display_first_last + '\'s** Stats for **' +  str(statYear) + '**'
								pitcherEmbed.type = 'rich'
								#testEmbed.colour = 
								pitcherEmbed.color = discord.Color.dark_blue()
								
								for index in range(0, seasonPitchingInfo.totalSize):
									valueString = ' ERA: %s\n' \
									' Wins/Losses: %s/%s\n' \
									' Games: %s\n' \
									' WHIP: %s' % (seasonPitchingInfo.era[index], seasonPitchingInfo.w[index], seasonPitchingInfo.l[index], seasonPitchingInfo.gs[index], seasonPitchingInfo.whip[index])
									pitcherEmbed.add_field(name=seasonPitchingInfo.team_abbrev[index], value=valueString)
								
								await message.channel.send(embed=pitcherEmbed)
								'''
								#Send the message back to the channel
								await message.channel.send('>>> **%s\'s** (%s) Stats for **%s**\n' \
								' ERA: %s\n' \
								' Wins/Losses: %s/%s\n' \
								' Games: %s\n' \
								' WHIP: %s' % (playerGenInfo.name_display_first_last, seasonPitchingInfo.team_abbrev[0], statYear, seasonPitchingInfo.era[0], seasonPitchingInfo.w[0], seasonPitchingInfo.l[0], seasonPitchingInfo.gs[0], seasonPitchingInfo.whip[0]))
								'''
								return

						elif 'SCORE' in messageArray[1].upper():
						
							#Set the target day
							targetDateTime = datetime.datetime.now()
						
							#Get the team
							teamSelected = await self.get_team(messageArray[2], message)
							
							# Get the schedule for the selected date
							queriedSchedule = statsapi.schedule(date=targetDateTime.strftime('%Y-%m-%d'), team=int(teamSelected['id']))
							
							
							
							#Get a list of games a week in the past
							pastDay = datetime.datetime.today() - timedelta(1)
							pastWeek = datetime.datetime.today() - timedelta(7)
							pastGames = statsapi.schedule(start_date=pastWeek.strftime('%m/%d/%Y'), end_date=pastDay.strftime('%m/%d/%Y'), team=teamSelected['id'])
							
							#Get a list of games a week in the future
							nextDay = datetime.datetime.today() + timedelta(1)
							NextWeek = datetime.datetime.today() + timedelta(7)
							nextGames = statsapi.schedule(start_date=nextDay.strftime('%m/%d/%Y'), end_date=NextWeek.strftime('%m/%d/%Y'), team=teamSelected['id'])
							
							if len(pastGames) > 0:
								prev_game = pastGames[len(pastGames) - 1]
								
							
							
							#Check for a double header
							if len(queriedSchedule) == 2:
							
							#TODO Handle games past midnight
							
								#Game 1 is over
								if queriedSchedule[0]['status'] == 'Final' or queriedSchedule[0]['status'] == 'Game Over':
									await self.final_Game_Embed(queriedSchedule[0], message)
								#Game is scheduled	
								elif queriedSchedule[0]['status'] == 'Scheduled' or queriedSchedule[0]['status'] == 'Pre-Game':	
									await self.scheduled_Game_Embed(queriedSchedule[0], message)
									#await self.final_Game_Embed(pastGames[len(pastGames) - 1], message)
								elif queriedSchedule[0]['status'] == 'In Progress':
									await self.live_Game_Embed(queriedSchedule[0], message)
								else:
									print('ERROR: Unknown game state returned. Game Status = %s' % queriedSchedule['status'])
									
								#Game 2 is over
								if queriedSchedule[1]['status'] == 'Final' or queriedSchedule[1]['status'] == 'Game Over':
									await self.final_Game_Embed(queriedSchedule[1], message)
								#Game is scheduled	
								elif queriedSchedule[1]['status'] == 'Scheduled' or queriedSchedule[1]['status'] == 'Pre-Game':	
									await self.scheduled_Game_Embed(queriedSchedule[1], message)
									await self.final_Game_Embed(prev_game, message)
								elif queriedSchedule[1]['status'] == 'In Progress':
									await self.live_Game_Embed(queriedSchedule[1], message)
								else:
									print('ERROR: Unknown game state returned. Game Status = %s' % queriedSchedule['status'])
							#A single game was returned
							elif len(queriedSchedule) == 1:
								if len(pastGames) > 0:
									prev_game = pastGames[len(pastGames) - 1]
							
								#Check if the previous game is still 'In Progress' and if so set that as the target game
								#Apparently the MLB api returns the next game sometimes
								if prev_game['status'] == 'In Progress' and queriedSchedule[0]['status'] == 'Scheduled':
									queriedSchedule = prev_game
							
								#Game is over
								if queriedSchedule[0]['status'] == 'Final' or queriedSchedule[0]['status'] == 'Game Over':
									await self.final_Game_Embed(queriedSchedule[0], message)
									#If there is a game in the next week, return it
									if len(nextGames) > 0:
										await self.scheduled_Game_Embed(nextGames[0], message)
								#Game is scheduled	
								elif queriedSchedule[0]['status'] == 'Scheduled' or queriedSchedule[0]['status'] == 'Pre-Game':	
									await self.scheduled_Game_Embed(queriedSchedule[0], message)
									await self.final_Game_Embed(prev_game, message)
								elif queriedSchedule[0]['status'] == 'In Progress':
									await self.live_Game_Embed(queriedSchedule[0], message)
								else:
									print('ERROR: Unknown game state returned. Game Status = %s' % queriedSchedule['status'])
							#No games were returned for the day
							elif len(queriedSchedule) <= 0:
								if len(pastGames) > 0:
									#Return the most recent game
									prev_game = pastGames[len(pastGames) - 1]
								else:
									#No games were returned
									await message.channel.send('Sorry, there are no current or recent games')
									return
								#Check if the previous game is still 'In Progress' and if so set that as the target game
								#Apparently the MLB api returns the next game sometimes
								if prev_game['status'] == 'In Progress':
									print('DEBUG: Previous game still in progress!')
									await self.live_Game_Embed(prev_game, message)
								#Game is over
								elif prev_game['status'] == 'Final' or prev_game['status'] == 'Game Over':
									await self.final_Game_Embed(prev_game, message)
									#If there is a game in the next week, return it
									if len(nextGames) > 0:
										await self.scheduled_Game_Embed(nextGames[0], message)
								else:
									print('ERROR: Unknown game state returned. Game Status = %s' % queriedSchedule['status'])
							#Uhh more than 2 games in a day?
							else:
								print('DEBUG: statsapi.schedule(date=' + targetDateTime.strftime('%Y-%m-%d') + ',team=' +
								str(team=int(teamSelected['id'])) + ')) returned more than 2 games')
							
							'''
							
							
							#Get that teams most recent game
							most_recent_game = statsapi.last_game(int(teamSelected['id']))
							
							#Set the target game to the value returned from statsapi.last_game
							queriedSchedule[0] = statsapi.schedule(game_id=most_recent_game)
							#Get the game previous to the returned game
							
							print(targetDateTime.strftime('%Y-%m-%d'))
							todaySchedule = statsapi.schedule(date=targetDateTime.strftime('%Y-%m-%d'), team=int(teamSelected['id']))
							#jsonData = json.loads(todaySchedule)
							
							#print(jsonData)
							
							#Get a list of games a week in the past
							pastDay = datetime.datetime.today()
							pastWeek = datetime.datetime.today() - timedelta(7)
							pastGames = statsapi.schedule(start_date=pastWeek.strftime('%m/%d/%Y'), end_date=pastDay.strftime('%m/%d/%Y'), team=teamSelected['id'])
							
							#Get a list of games a week in the future
							nextDay = datetime.datetime.today() + timedelta(1)
							NextWeek = datetime.datetime.today() + timedelta(7)
							nextGames = statsapi.schedule(start_date=nextDay.strftime('%m/%d/%Y'), end_date=NextWeek.strftime('%m/%d/%Y'), team=teamSelected['id'])
							'''
							'''
							#TODO handle no previous games returned
							print('Past Games')
							for games in pastGames:
								print('game_id = %s | game_datetime = %s ' % (games['game_datetime'], games['game_datetime']))
							
							print('Next Games')
							for games in nextGames:
								print('game_id = %s | game_datetime = %s ' % (games['game_datetime'], games['game_datetime']))
							'''
							#TODO If the target game is the same as the most recent pastGames[n] then access pastGames[n - 1]
							'''
							if len(pastGames) > 0:
								prev_game = pastGames[len(pastGames) - 1]
							
							#Check if the previous game is still 'In Progress' and if so set that as the target game
							#Apparently the MLB api returns the next game sometimes
d								queriedSchedule[0] = queriedSchedule[0][0]
							
							#Game is over
							if queriedSchedule[0]['status'] == 'Final' or queriedSchedule[0]['status'] == 'Game Over':
								await self.final_Game_Embed(queriedSchedule[0], message)
							#Game is scheduled	
							elif queriedSchedule[0]['status'] == 'Scheduled' or queriedSchedule[0]['status'] == 'Pre-Game':	
								await self.scheduled_Game_Embed(queriedSchedule[0], message)
								await self.final_Game_Embed(pastGames[len(pastGames) - 1], message)
							elif queriedSchedule[0]['status'] == 'In Progress':
								await self.live_Game_Embed(queriedSchedule[0], message)
							else:
								await message.channel.send('Game Status = %s' % queriedSchedule[0]['status'])
							'''
							
						elif 'HIGHLIGHTS' in messageArray[1].upper():
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
								
						elif 'ROSTER' in messageArray[1].upper():
							teamSelected = await self.get_team(messageArray[2], message)
							
							print ('DEBUG: teamSelected in ROSTER = %s' % teamSelected)
							
							#Create the embed object
							rosterEmbed = discord.Embed()
							rosterEmbed.type = 'rich'
							rosterEmbed.color = discord.Color.dark_blue()

							rosterEmbed.add_field(name='Current Roster for the **' + teamSelected['name'] + '**', value='```' + statsapi.roster(int(teamSelected['id'])) + '```')
							await message.channel.send(embed=rosterEmbed)
							
						elif 'STANDINGS' in messageArray[1].upper():
						
							#league IDs
						
							#103 = American
							#104 = National
							
							#Division IDs
							
							#AL East - 201
							#AL Central = 202
							#AL West = 200
							
							#NL East - 204
							#NL Central - 205
							#NL West - 203
							
							#alEastStandingsString = statsapi.standings(leagueId='103', division='201', standingsTypes='byDivision')
							#alCentralStandingsString = statsapi.standings(leagueId='103', division='202', standingsTypes='byDivision')
							#alWestStandingsString = statsapi.standings(leagueId='103', division='200', standingsTypes='byDivision')
							
							#nlEastStandingsString = statsapi.standings(leagueId=104, division='204')
							#nlCentralStandingsString = statsapi.standings(leagueId='104', division='205', standingsTypes='byDivision')
							#nlWestStandingsString = statsapi.standings(leagueId='104', division='203', standingsTypes='byDivision')
							
							alStandingsString = statsapi.standings(leagueId='103', standingsTypes='byDivision', include_wildcard=False)
							
							alStandingsArray = alStandingsString.split('\n\n')
							
							nlStandingsString = statsapi.standings(leagueId='104', standingsTypes='byDivision', include_wildcard=False)
							
							nlStandingsArray = nlStandingsString.split('\n\n')
							
							
							#Create the embed object
							standingsEmbed = discord.Embed()
							standingsEmbed.type = 'rich'
							#testEmbed.colour = 
							standingsEmbed.color = discord.Color.dark_blue()
							standingsEmbed.add_field(name='**AL East**',value='```' + alStandingsArray[1] + '```', inline=True)
							standingsEmbed.add_field(name='**AL Central**',value='```' + alStandingsArray[2] + '```', inline=False)
							standingsEmbed.add_field(name='**AL West**',value='```' + alStandingsArray[0] + '```', inline=False)
							
							standingsEmbed.add_field(name='**NL East**',value='```' + nlStandingsArray[2] + '```', inline=False)
							standingsEmbed.add_field(name='**NL Central**',value='```' + nlStandingsArray[0] + '```', inline=False)
							standingsEmbed.add_field(name='**NL West**',value='```' + nlStandingsArray[1] + '```', inline=False)
							
							await message.channel.send(embed=standingsEmbed)
						
						elif 'SCHEDULE' in messageArray[1].upper():
							#Set the target day
							targetDateTime = datetime.datetime.now()
						
							#TODO analyze messageArray[2] and check if its a date
							#targetDateTime = datetime.datetime.strptime(messageArray[2], '%Y-%m-%d')
						
							#If there is a team supplied
							if len(messageArray) > 2:
						
								#Get the team
								teamSelected = await self.get_team(messageArray[2], message)
								
								# Get the schedule for the selected date
								queriedSchedule = statsapi.schedule(date=targetDateTime.strftime('%Y-%m-%d'), team=int(teamSelected['id']))
								
								#Get a list of games a week in the past
								pastDay = datetime.datetime.today() - timedelta(1)
								pastWeek = datetime.datetime.today() - timedelta(7)
								pastGames = statsapi.schedule(start_date=pastWeek.strftime('%m/%d/%Y'), end_date=pastDay.strftime('%m/%d/%Y'), team=teamSelected['id'])
								
								#Get a list of games a week in the future
								nextDay = datetime.datetime.today() + timedelta(1)
								NextWeek = datetime.datetime.today() + timedelta(7)
								nextGames = statsapi.schedule(start_date=nextDay.strftime('%m/%d/%Y'), end_date=NextWeek.strftime('%m/%d/%Y'), team=teamSelected['id'])
								
								#Create the schedule embed
								scheduleEmbed = discord.Embed()
								scheduleEmbed = discord.Embed()
								scheduleEmbed.title = '**' + teamSelected['name'] + '**\'s games for the next week'
								scheduleEmbed.type = 'rich'
								#testEmbed.colour = 
								scheduleEmbed.color = discord.Color.dark_blue()
								
								#scoreEmbed.add_field(name='NAME', value='VALUE', inline=False)
								#scheduleEmbed.add_field(name=gameTimeLocal.strftime('%m/%d/%Y'), value= + ' EST', inline=False)
								
								if len(pastGames) > 0:
									prev_game = pastGames[len(pastGames) - 1]
									
								#Check for a double header
								if len(queriedSchedule) == 2:
								
								#TODO Handle games past midnight
								
									#Game is scheduled
									if queriedSchedule[0]['status'] == 'Scheduled' or queriedSchedule[0]['status'] == 'Pre-Game':
										#Add the game to the list
										nextGames.insert(0, queriedSchedule[0])
										
									#Game is scheduled	
									if queriedSchedule[1]['status'] == 'Scheduled' or queriedSchedule[1]['status'] == 'Pre-Game':
										#Add the game to the list
										nextGames.insert(0, queriedSchedule[1])
								#A single game was returned
								elif len(queriedSchedule) == 1:
									if len(pastGames) > 0:
										prev_game = pastGames[len(pastGames) - 1]
								
									#Check if the previous game is still 'In Progress' and if so set that as the target game
									#Apparently the MLB api returns the next game sometimes
									if prev_game['status'] == 'In Progress' and queriedSchedule[0]['status'] == 'Scheduled':
										queriedSchedule = prev_game
								
									#Game is scheduled	
									if queriedSchedule[0]['status'] == 'Scheduled' or queriedSchedule[0]['status'] == 'Pre-Game':
										#Add the game to the list
										nextGames.insert(0, queriedSchedule[0])
								#No games were returned for the day
								elif len(queriedSchedule) <= 0:
									if len(pastGames) > 0:
										prev_game = pastGames[len(pastGames) - 1]
										
										#Game is still scheduled	
										if prev_game['status'] == 'Scheduled' or prev_game['status'] == 'Pre-Game':
											#Add the game to the list
											nextGames.insert(0, queriedSchedule)
						
									
										
									'''
									if len(pastGames) > 0:
										#Return the most recent game
										prev_game = pastGames[len(pastGames) - 1]
									else:
										#No games were returned
										await message.channel.send('Sorry, there are no current or recent games')
										return
									#Check if the previous game is still 'In Progress' and if so set that as the target game
									#Apparently the MLB api returns the next game sometimes
									if prev_game['status'] == 'In Progress':
										print('DEBUG: Previous game still in progress!')
										await self.live_Game_Embed(prev_game, message)
									#Game is over
									elif prev_game['status'] == 'Final' or prev_game['status'] == 'Game Over':
										await self.final_Game_Embed(prev_game, message)	
									'''
								#Uhh more than 2 games in a day?
								else:
									print('DEBUG: statsapi.schedule(date=' + targetDateTime.strftime('%Y-%m-%d') + ',team=' +
									str(team=int(teamSelected['id'])) + ')) returned more than 2 games')	
								
								#Add each game from the nextGames list to the embed
								for games in nextGames:
									homeTeam = statsapi.lookup_team(games['home_name'])
									awayTeam = statsapi.lookup_team(games['away_name'])
									if len(homeTeam) > 0:
										homeTeamShort = homeTeam[0]['fileCode'].upper()
									else:
										homeTeamShort = 'N/A'
									if len(awayTeam) > 0:
										awayTeamShort = awayTeam[0]['fileCode'].upper()
									else:
										awayTeamShort = 'N/A'
									gameTimeLocal = self.get_Local_Time(games['game_datetime'])
									scheduleEmbed.add_field(name=gameTimeLocal.strftime('%m/%d/%Y') + ' @ ' + gameTimeLocal.strftime('%-I:%M%p') + ' EST', value=homeTeamShort + ' vs ' + awayTeamShort, inline=False)
									
								await message.channel.send(embed=scheduleEmbed)
							#List all games found for the target date
							else:
								#For now assume the target date is today
								
								# Get the schedule for the selected date
								queriedSchedule = statsapi.schedule(date=targetDateTime.strftime('%Y-%m-%d'))
								
								scheduledGamesList = []
								inProgressGamesList = []
								finalGameList = [] 
								
								#More than one game was returned
								if len(queriedSchedule) >= 1:
									
									#Loop through all the games and add them to the list
									for index in range(0, len(queriedSchedule)):
										#If the game isn't in progress add it
										if queriedSchedule[index]['status'] == 'Scheduled' or queriedSchedule[index]['status'] == 'Pre-Game':
											scheduledGamesList.insert(0, queriedSchedule[index])
										elif queriedSchedule[index]['status'] == 'In Progress':
											inProgressGamesList.insert(0, queriedSchedule[index])
										elif queriedSchedule[index]['status'] == 'Final' or queriedSchedule[index]['status'] == 'Game Over':
											finalGameList.insert(0, queriedSchedule[index])
	
								#A single game was returned
								elif len(queriedSchedule) == 1:
									#Game is scheduled	
									if queriedSchedule['status'] == 'Scheduled' or queriedSchedule['status'] == 'Pre-Game':
										scheduledGamesList.insert(0, queriedSchedule)
									elif queriedSchedul['status'] == 'In Progress':
										inProgressGamesList.insert(0, queriedSchedule)
									elif queriedSchedule['status'] == 'Final' or queriedSchedule['status'] == 'Game Over':
										finalGameList.insert(0, queriedSchedule)
										
								#No games were returned for the day
								elif len(queriedSchedule) <= 0:
									await message.channel.send('Sorry, I didn\'t find any games on %s' % targetDateTime.strftime('%Y-%m-%d'))
									return
								
								#Create the schedule embed
								scheduledEmbed = discord.Embed()
								scheduledEmbed.title = '**Scheduled Games on ' + targetDateTime.strftime('%Y-%m-%d') + '**'
								scheduledEmbed.type = 'rich'
								#testEmbed.colour = 
								scheduledEmbed.color = discord.Color.dark_blue()
								
								for games in scheduledGamesList:
									homeTeam = statsapi.lookup_team(games['home_name'])
									awayTeam = statsapi.lookup_team(games['away_name'])
									if len(homeTeam) > 0:
										homeTeamShort = homeTeam[0]['fileCode'].upper()
									else:
										homeTeamShort = 'N/A'
									if len(awayTeam) > 0:
										awayTeamShort = awayTeam[0]['fileCode'].upper()
									else:
										awayTeamShort = 'N/A'
									gameTimeLocal = self.get_Local_Time(games['game_datetime'])
									scheduledEmbed.add_field(name=gameTimeLocal.strftime('%m/%d/%Y') + ' @ ' + gameTimeLocal.strftime('%-I:%M%p') + ' EST', value=homeTeamShort + ' vs ' + awayTeamShort, inline=False)
									
								#Create the live embed
								inProgressEmbed = discord.Embed()
								inProgressEmbed.title = '**Live Games on ' + targetDateTime.strftime('%Y-%m-%d') + '**'
								inProgressEmbed.type = 'rich'
								#testEmbed.colour = 
								inProgressEmbed.color = discord.Color.dark_blue()
								
								for games in inProgressGamesList:
									homeTeam = statsapi.lookup_team(games['home_name'])
									awayTeam = statsapi.lookup_team(games['away_name'])
									if len(homeTeam) > 0:
										homeTeamShort = homeTeam[0]['fileCode'].upper()
									else:
										homeTeamShort = 'N/A'
									if len(awayTeam) > 0:
										awayTeamShort = awayTeam[0]['fileCode'].upper()
									else:
										awayTeamShort = 'N/A'
									
									homeScore = games['home_score']
									homeScoreString = str(homeScore)
									awayScore = games['away_score']
									awayScoreString = str(awayScore)
									
									if homeScore > awayScore:
										homeScoreString = '**' + homeScoreString + '**'
									elif awayScore > homeScore:
										awayScoreString = '**' + awayScoreString + '**'
										
									nameString = '**' + games['home_name']+ '** vs **' + games['away_name'] + '**'
									#Add the scores
									valueString = homeTeamShort + ' ' + homeScoreString + ' - ' + awayTeamShort + ' ' + awayScoreString + '\n'
									valueString = valueString + games['inning_state'] + ' ' + str(games['current_inning'])
									
									inProgressEmbed.add_field(name=nameString, value=valueString, inline=False)
									
								#Create the final embed
								finalEmbed = discord.Embed()
								finalEmbed.title = '**Final Games on ' + targetDateTime.strftime('%Y-%m-%d') + '**'
								finalEmbed.type = 'rich'
								#testEmbed.colour = 
								finalEmbed.color = discord.Color.dark_blue()								
								
								for games in finalGameList:
									homeTeam = statsapi.lookup_team(games['home_name'])
									awayTeam = statsapi.lookup_team(games['away_name'])
									if len(homeTeam) > 0:
										homeTeamShort = homeTeam[0]['fileCode'].upper()
									else:
										homeTeamShort = 'N/A'
									if len(awayTeam) > 0:
										awayTeamShort = awayTeam[0]['fileCode'].upper()
									else:
										awayTeamShort = 'N/A'
									
									homeScore = games['home_score']
									homeScoreString = str(homeScore)
									awayScore = games['away_score']
									awayScoreString = str(awayScore)
									
									if homeScore > awayScore:
										homeScoreString = '**' + homeScoreString + '**'
									elif awayScore > homeScore:
										awayScoreString = '**' + awayScoreString + '**'
										
									nameString = '**' + games['home_name']+ '** vs **' + games['away_name'] + '**'
									#Add the scores
									valueString = homeTeamShort + ' ' + homeScoreString + ' - ' + awayTeamShort + ' ' + awayScoreString + ' **F**'
																		
									finalEmbed.add_field(name=nameString, value=valueString, inline=False)
									
								if len(scheduledGamesList) > 0:
									await message.channel.send(embed=scheduledEmbed)
								if len(inProgressGamesList) > 0:
									await message.channel.send(embed=inProgressEmbed)
								if len(finalGameList) > 0:
									await message.channel.send(embed=finalEmbed)
								
						elif 'GIBBY' in messageArray[1].upper():
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


							#https://i.imgur.com/AewHTiT.png
							
							#Create the embed object
							gibbyEmbed2 = discord.Embed()
							gibbyEmbed2.title = '**YES BRUDDA**'
							gibbyEmbed2.type = 'rich'
							#testEmbed.colour = 
							gibbyEmbed2.color = discord.Color.dark_blue()
							gibbyEmbed2.set_image(url='https://i.imgur.com/AewHTiT.png')
							gibbyEmbed2.image.width = 500
							gibbyEmbed2.image.height = 600
							
							#await message.channel.send('%s' % pewPewId)
							await message.channel.send(embed=gibbyEmbed2)
						
						elif 'NOTES' in messageArray[1].upper():
							print('DEBUG: Capturing Notes')
							print('DEBUG: game_winProbability')
							print('DEBUG: %s', statsapi.notes('game_winProbability'))
							
							print('DEBUG: game_contextMetrics')
							print('DEBUG: %s', statsapi.notes('game_contextMetrics'))
							
							
							#print('DEBUG: game_contextMetrics')
							#parameters = { 
							#			'gamePk': 55555
							#			}
							#
							#print('DEBUG: %s', statsapi.get(endpoint='game_contextMetrics', params=parameters))
						
						elif 'META' in messageArray[1].upper():
							print('DEBUG: Getting meta response for %s' % messageArray[2])
							print('DEBUG: %s' % statsapi.meta(messageArray[2]))
						
						elif 'HOCKEY' in messageArray[1].upper():
							hockeyEmbed = discord.Embed()
							hockeyEmbed.title = 'Brrr its getting cold in here...'
							hockeyEmbed.type = 'rich'
							hockeyEmbed.color = discord.Color.dark_blue()
							hockeyEmbed.set_image(url='https://i.imgur.com/yn7efui.png')
							
							#Get the NHL schedule
							scheduleResponse = await self.sendGetRequest('https://statsapi.web.nhl.com/api/v1/schedule')
							
							#Parse the JSON
							scheduleJson = json.loads(scheduleResponse.text)
							
							print('DEBUG: totalGames = %s' % scheduleJson['totalGames'])
							
							games = scheduleJson['dates'][0]['games']
							
							print('DEBUG: I found %s games' % str(len(games)))
							
							for hockeyGame in games:
								gameTimeLocal = self.get_Local_Time(hockeyGame['gameDate'])
								nameString = hockeyGame['teams']['away']['team']['name'] + ' vs ' + hockeyGame['teams']['home']['team']['name']
								valueString = gameTimeLocal.strftime('%-I:%M%p') + ' EST' + ' @ ' + hockeyGame['venue']['name']
								hockeyEmbed.add_field(name=nameString, value=valueString)
							
							contentString = 'Statsbot hipchecked ' + message.author.mention + ' into the boards! Savage! \n Anyway here are the games for ' + gameTimeLocal.strftime('%m/%d/%Y')
							await message.channel.send(content=contentString, embed=hockeyEmbed)
							
						
						#Display the help message
						elif 'HELP' in messageArray[1].upper():
							
							helpEmbed = discord.Embed()
							helpEmbed.title = 'Statsbot Help'
							helpEmbed.type = 'rich'
							helpEmbed.color = discord.Color.dark_blue()
							
							helpEmbed.add_field(name='statsbot player $PLAYERNAME', value='Lookup a players stats')
							helpEmbed.add_field(name='statsbot score $TEAMNAME', value='Lookup the latest game')
							helpEmbed.add_field(name='statsbot highlights $TEAMNAME', value='Lookup the latest highlights')
							helpEmbed.add_field(name='statsbot roster $TEAMNAME', value='Display the team\'s current roster')
							helpEmbed.add_field(name='statsbot standings', value='Show the current league standing')
							helpEmbed.add_field(name='statsbot schedule $TEAMNAME', value='Show the team\'s scheduled games')
							
							await message.channel.send(embed=helpEmbed)
							'''
							await message.channel.send('>>> use \'statsbot player $PLAYERNAME\' to lookup a players stats. \n' \
							'use \'statsbot score $TEAMNAME\' to lookup the latest game. \n' \
							'use \'statsbot highlights $TEAMNAME\' to lookup the latest highlights. \n' \
							'use \'statsbot roster $TEAMNAME\' to display the teams current roster. \n' \
							'use \'statsbot standings\' to show the current league standings. \n' \
							'use \'statsbot standings\' to show the current league standings. \n' \
							'''
						else:
							await message.channel.send('Sorry I don\'t understand, try saying \'Statsbot HELP\' for a list of available commands.')
					#Bot was called without enough arguments
					elif messageArray[0].upper() == 'STATSBOT' and len(messageArray) == 1:
						await message.channel.send('I like it when you say my name, but I need more instructions.')
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
	
	async def wait_for_response(self, message, userResponse, waitTime):
		responseFound = False
		#Set the start time
		messageTime = datetime.datetime.utcnow()
		#Give a buffer of 5 seconds back for play in the system time and discord time
		messageTime = messageTime - timedelta(seconds=5)
		
		#Wait defined time
		for wait in range(1, waitTime):
			if responseFound:
				break;
		
			time.sleep(1)
			#Get the last messages
			rawMessageList = await message.channel.history(limit=5).flatten()
			
			#Prune all messages by bots
			for messages in rawMessageList:
				if messages.author.bot == False:
					messageList.append(messages)
			
			#if the name hasn't been selected yet
			if responseFound == False:
				#loop through the past 2 messages
				for history in range (0, len(messageList)):
					#The user who requested the list responded
					if messageList[history].author == message.author:
						#check if the message was sent after the list of names
						if messageList[history].created_at > messageTime:
							#The user responded with the matching prompt
							if userResponse.upper() in messageList[history].content.upper():
								#The matching response was found
								responseFound = True
								return True
		return False
	
	async def wait_for_number(self, message, limit, waitTime):
		responseNumber = -1
		#Set the start time
		messageTime = datetime.datetime.utcnow()
		#Give a buffer of 5 seconds back for play in the system time and discord time
		messageTime = messageTime - timedelta(seconds=5)
	
		#Wait defined time
		for wait in range(1, waitTime):
			if responseNumber != -1:
				break;
			#Get the last messages
			rawMessageList = await message.channel.history(limit=5).flatten()
			
			messageList = []
			
			#Prune all messages by bots
			for messages in rawMessageList:
				if messages.author.bot == False:
					messageList.append(messages)
			
			#if the number hasn't been selected yet
			if responseNumber == -1 and len(messageList) > 0:
				#loop through the past messages
				for history in range (0, len(messageList)):
					#The user who requested the list responded
					if messageList[history].author == message.author:
						#check if the message was sent after the list of names
						if messageList[history].created_at > messageTime:
							#The user responded with a number
							if messageList[history].content.isdigit():
								#The number is valid
								if int(messageList[history].content) <= limit and int(messageList[history].content) > 0:
									responseNumber = int(messageList[history].content)
									return responseNumber
								else:
									await message.channel.send('%s is not a valid number, start over' % str(messageList[history].content))
									return
							else:
								await message.channel.send('%s is not a number, start over' % messageList[history].content)
								return
			#number has not been selected, wait
			time.sleep(1)
		#if the loop completes without a selection inform the user
		if 	responseNumber == -1:
				await message.channel.send('I\'m getting bored waiting for you, start over when you\'re ready.')
				return
	
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
		
		#Show the win %
		scoreEmbed.add_field(name=homeTeamShort + ' win %', value=game_contextMetrics['homeWinProbability'], inline=True)
		scoreEmbed.add_field(name=awayTeamShort + ' win %', value=game_contextMetrics['awayWinProbability'], inline=True)
		
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
		
	async def sendGetRequest(self, url):
		try:
			print('DEBUG: Sending HTTP request...')				
			#build the headers
			requestsHeaders = {'Content-Type': 'application/json'}
			#Send the get request
			response = requests.get(url, requestsHeaders)   
			print('DEBUG: Response HTTP Status Code: %s' % response.status_code)
			print('DEBUG: Response HTTP Response Body: %s' % response.content)
			return response
		except requests.exceptions.RequestException:
			print('DEBUG: HTTP Request failed')
		
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
	client = BaseballBot()
	token = ReadTokenFile('auth')
	
	client.run(token)
	
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('Stopping Statsbot')
		pass
