import discord
import requests
import json
import datetime
import time
import random
import players

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged on as', self.user)
		
	async def on_message(self, message):
		# don't respond to ourselves
		#print ('Message from %s channel' % message.channel)
		
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
								index = random.randint(1, 10)
								
								if index == 1:
									await message.channel.send('%s is so bad they couldn\'t hit the ground if they fell off a ladder' % messageArray[2])
								elif index == 2:
									await message.channel.send('%s gets less hits than an Amish website' % messageArray[2])
								elif index == 3:
									await message.channel.send('%s hasn\'t reached second base since prom' % messageArray[2])
								elif index == 4:
									await message.channel.send('%s loves playing catcher...' % messageArray[2])
								elif index == 5:
									await message.channel.send('A toaster throws more heat than %s' % messageArray[2])
								elif index == 6:
									await message.channel.send('Yoko Ono has better pitch control than %s' % messageArray[2])
								elif index == 7:
									await message.channel.send('%s couldn\'t even save a word file' % messageArray[2])
								elif index == 8:
									await message.channel.send('%s couldn\'t buy a cup of coffee with their batting average' % messageArray[2])
								elif index == 9:
									await message.channel.send('I just named my new dog %s, because he gets beaten every day' % messageArray[2])
								elif index == 10:
									await message.channel.send('%s couldn\'t beat the Helen Keller School Team' % messageArray[2])
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
							discordFormattedString = '>>> I found ' + str(len(playerSearchResultsList)) + ' players matching **' + displayNameToSearch + '** in ' + str(statYear) + '\n Which one do you want? \n\n'
							
							
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
							
					#Display the help message
					elif messageArray[1].upper() == 'HELP':
						await message.channel.send('>>> use \'statsbot player PLAYERNAME\' to lookup a players stats.')
					else:
						await message.channel.send('Sorry all I support right now is player stats.')
				#Bot was called without enough arguments
				elif messageArray[0].upper() == 'STATSBOT' and len(messageArray) < 1:
					await message.channel.send('I like it when you say my name, but I need more instructions.')
				else:
					return

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