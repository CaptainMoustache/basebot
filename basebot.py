import discord
import json
from datetime import timedelta
from datetime import datetime
import players
import time
import random
import statsapi
import re
import dateutil.parser
import requests
import commonfunctions
import embedfunctions
import os
import collections
import threading
import sys
import portalocker
import logging
import dateparser


class BaseballBot(discord.Client):
	commonFunctions = commonfunctions.CommonFunctions()
	embedFunctions = embedfunctions.EmbedFunctions()
	guild_data_list = []
	dataFilePath = "DataFiles/"
	testFile = None

	async def refresh_datafiles(self):
		temp_list = []
		for file in os.listdir(self.dataFilePath):
			# Possibly check for valid json here
			saved_guild_data = self.read_data_file(file, self.dataFilePath)
			temp_list.append(saved_guild_data)
		self.guild_data_list = temp_list

	def guild_data_exists(self, guildId):
		for guilds in self.guild_data_list:
			if str(guildId) == guilds['guildid']:
				return True
		return False

	# Compare text channels in the guild to the stored channels and correct any differences
	async def refresh_channel_names(self, guild, guild_data):
		# Flag to indicate the channel data needs to be updated
		update_required = False

		# Loop through all subscribed channels
		for channel_index in range(0, len(guild_data['subscribedChannels'])):

			# Flag to indicate a channel no longer exists
			remove_channel = True

			# loop through all the servers current text channels
			for guild_channel in guild.text_channels:
				# If the stored id matches the guild channel
				if guild_data['subscribedChannels'][channel_index]['id'] == str(guild_channel.id):
					# Clear the flag to remove the stored channel
					remove_channel = False

					# Check the name value
					if guild_data['subscribedChannels'][channel_index]['name'] != guild_channel.name:
						# Update the channel name
						update_required = True
						print('DEBUG: Updating channel name for id ' + guild_data['subscribedChannels'][channel_index][
							'id'])
						# Figure out how to store the new name
						guild_data['subscribedChannels'][channel_index]['name'] = guild_channel.name
						break
					else:
						break
			if remove_channel:
				update_required = True
				# Remove a channel that is no longer on the server
				guild_data['subscribedChannels'].pop(channel_index)

		if update_required:
			self.write_data_file(self.dataFilePath + str(guild.id), guild_data)
		return guild_data

	@staticmethod
	def read_data_file(filename, filepath):
		with open(filepath + filename) as json_file:
			try:
				return json.load(json_file)
			except ValueError as e:
				print('DEBUG: ValueError loading datafile ' + filename)
			except:
				print('DEBUG Exception loading datafile ' + filename)

	@staticmethod
	def write_data_file(filename, jsonpayload):
		with portalocker.Lock(filename, 'w', timeout=1) as outfile:
			json.dump(jsonpayload, outfile)
			outfile.flush()
			os.fsync(outfile.fileno())

	async def on_ready(self):
		print('Logged on as', self.user)
		status_file = open("status.txt", "r")
		status_text = status_file.read()
		status_file.close()
		await self.change_presence(activity=discord.Game(name=status_text))
		await self.refresh_datafiles()

	async def on_message(self, message):
		try:
			# don't respond to ourselves or other bots
			if (message.author == self.user) or message.author.bot:
				return
			else:
				# Check if the guild has data
				if self.guild_data_exists(message.guild.id):
					# Need to clean this up :(
					for guilds in self.guild_data_list:
						if str(message.guild.id) == guilds['guildid']:
							saved_guild_data = guilds

					# saved_guild_data = self.guild_data_list[0]['guildid'][str(message.guild.id)]
					# Check if the channel should be listened to
					if IdExists(message.channel.id, saved_guild_data['subscribedChannels']):
						# Split the message at whitespace
						messageArray = message.content.split()
						if len(messageArray) > 0:
							# Bot was called with enough arguments
							if ('BASEBOT' in messageArray[0].upper() and len(messageArray) > 1) or (
									str(self.user.id) in messageArray[0].upper()):
								# if the first message part is 'player' lookup the players stats
								if 'PLAYER' in messageArray[1].upper():
									try:
										# Set the year to lookup to the current year
										now = datetime.now()
										statYear = now.year
										# check if the input is empty
										if len(messageArray) < 2:
											await message.channel.send('I need at least a name to search yah dingus.')
											return
										# There is a search string
										else:
											# search for the playerid
											# create a list of mention strings
											# mentionList = []
											# for users in message.channel.members: #self.guilds[0].members:
											#	if users.bot == False:
											#		mentionList.append(users.mention)

											notBotList = []
											for users in message.channel.members:  # self.guilds[0].members:
												if users.bot == False:
													notBotList.append(users)

											# if someone is being a smartass
											if messageArray[2].upper() == 'PENIS':
												await message.channel.send(
													'My penis is currently batting 1000 with your mom')
												return
											elif messageArray[2].upper() == 'KAPPA':
												await message.channel.send(
													u'\u0028 \u0361 \u00B0 \u035C \u0296 \u0361 \u00B0 \u0029')
												return
											# if trying to use a channel member
											elif len(message.mentions) > 0:

												# this is an unsorted list so we don't know who is the intended target
												for memberToInsult in message.mentions:

													# Target is not a bot
													if memberToInsult.bot == False:
														insultList = []
														insultList.append(
															'%s is so bad they couldn\'t hit the ground if they fell off a ladder')
														insultList.append('%s gets less hits than an Amish website')
														insultList.append('%s hasn\'t reached second base since prom')
														insultList.append('%s loves playing catcher...')
														insultList.append('A toaster throws more heat than %s')
														insultList.append('Yoko Ono has better pitch control than %s')
														insultList.append('%s couldn\'t even save a word file')
														insultList.append('%s is a jerk')
														insultList.append(
															'I just named my new dog %s, because they get beaten every day')
														insultList.append(
															'%s couldn\'t beat the Helen Keller School Team')
														insultList.append('%s is a Butterface Cock Box')
														insultList.append(
															'%s is a triple bagger, one for me, one for them, and one for anyone who happens to be walking by')
														insultList.append(
															'%s is so ugly their mother breast fed them through a straw')
														insultList.append(
															'%s looks like they were drawn with my left hand')
														insultList.append(
															'I would call %s\'s aim cancer, but cancer kills people')
														insultList.append('%s smells like an old jizz rag')
														insultList.append(
															'%s is so ugly if they laid down on the beach not even the tide would take them')
														insultList.append(
															'%s is so ugly, when their mom dropped them off at school she got a fine for littering')

														# await message.channel.send(insultList[random.randint(0, len(insultList) - 1)] % messageArray[2])
														await message.channel.send(insultList[random.randint(0, len(
															insultList) - 1)] % memberToInsult.mention)
														return
													# Target is a bot
													'''
													else:
														#The bot is not self
														if memberToInsult != self.user:
															binaryString = " 01101000 01100001 01110011 00100000 01101101 01101111 01110010 01100101 00100000 01101111 01100110 00100000 01100001 00100000 01110011 01101111 01100011 01101001 01100001 01101100 00100000 01101100 01101001 01100110 01100101 00100000 01110100 01101000 01100001 01101110 00100000 01111001 01101111 01110101 00100000 01101110 01100101 01110010 01100100 00100001"
															await message.channel.send(memberToInsult.mention + binaryString)
															break
														else:
															break
													'''

											# We might have an actual name to search
											else:
												# Parse year if supplied after a name or names
												if messageArray[len(messageArray) - 1].isdigit() and len(
														messageArray) > 3:
													# The last part of the message is a year
													if int(messageArray[len(messageArray) - 1]) > now.year:
														await message.channel.send(
															'I wish I could predict the future, for now try sticking to %s and earlier' % now.year, tts=False)
														return
													elif int(messageArray[len(messageArray) - 1]) < 1900:
														await message.channel.send(
															'Right now I don\'t work with dates pre 1900. Sorry')
														return
													else:
														statYear = messageArray[len(messageArray) - 1]

												name_to_search = ""
												display_name_to_search = ""

												# Get the name and ignore the year
												if messageArray[len(messageArray) - 1].isdigit():
													# Get all the name parts between player and the year

													for index in range(2, len(messageArray) - 1):
														name_to_search = name_to_search + messageArray[index] + ' '
														display_name_to_search = display_name_to_search + messageArray[
															index] + ' '
													# Remove trailing whitespace, otherwise the MLB api returns nothing
													name_to_search = name_to_search.strip()
													display_name_to_search = display_name_to_search.strip()
													# Append %25 to the end of the search term
													name_to_search = name_to_search + '%25'

												# Get the name, no year supplied
												else:
													for index in range(2, len(messageArray)):
														name_to_search = name_to_search + messageArray[index] + ' '
														display_name_to_search = display_name_to_search + messageArray[
															index] + ' '
													# Remove trailing whitespace, otherwise the MLB api returns nothing
													name_to_search = name_to_search.strip()
													display_name_to_search = display_name_to_search.strip()
													# Append %25 to the end of the search term
													name_to_search = name_to_search + '%25'

										# Check that we have a valid name to search
										if name_to_search is None or name_to_search == '':
											await message.channel.send(
												'I didn\'t get a name to search. Something went wrong, Sorry')
											return

										# build the playerSearchURL
										activePlayerSearchURL = 'http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=\'mlb\'&active_sw=\'Y\'&name_part=\'' + name_to_search + '\''

										# Send the GET
										playerSearch = await self.commonFunctions.sendGetRequest(activePlayerSearchURL)

										# parse the json response
										playerSearchJson = json.loads(playerSearch.text)

										# get the number of players found
										playersFoundCount = playerSearchJson['search_player_all']['queryResults'][
											'totalSize']

										# If no players are returned, try again looking for inactive players
										if playersFoundCount == "0":
											# build the playerSearchURL
											inactivePlayerSearchURL = 'http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=\'mlb\'&active_sw=\'N\'&name_part=\'' + name_to_search + '\''

											# Send the GET
											playerSearch = await self.commonFunctions.sendGetRequest(
												inactivePlayerSearchURL)

											# parse the json response
											playerSearchJson = json.loads(playerSearch.text)

											# get the number of players found
											playersFoundCount = playerSearchJson['search_player_all']['queryResults'][
												'totalSize']

										# Create a list of PlayerSearchInfo objects
										playerSearchResultsList = []

										# Populate the list of PlayerSearchInfo objects with all players returned
										for searchIndex in range(int(playersFoundCount)):
											foundPlayer = players.PlayerSearchInfo()
											foundPlayer.ParseJson(playerSearchJson, searchIndex)
											playerSearchResultsList.append(foundPlayer)

										# We have multiple matches, list them and prompt for number
										if len(playerSearchResultsList) > 1:
											# Make sure the list isn't too big
											if len(playerSearchResultsList) > 50:
												await message.channel.send(
													'I found over 50 matches for ' + display_name_to_search + '. \n Try being a little more specific')
												return

											# TODO make this dynamically list the team and position based on year
											playerGenInfoList = []

											for player in playerSearchResultsList:
												playerGenInfo = players.PlayerInfo()
												# Send GET to download player info
												# http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id='493316'

												playerInfoURL = 'http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code=\'mlb\'&player_id=\'' + player.player_id + '\''
												# Send the GET
												playerInfoRequest = await self.commonFunctions.sendGetRequest(
													playerInfoURL)
												playerInfoJson = json.loads(playerInfoRequest.text)
												playerGenInfo.ParseJson(playerInfoJson)
												# Append the playerInfo to the list
												playerGenInfoList.append(playerGenInfo)

											# Build the display string
											discordFormattedString = '>>> I found ' + str(len(
												playerSearchResultsList)) + ' players matching **' + display_name_to_search + '** in ' + str(
												statYear) + '\n Enter the number for the player you want \n\n'

											# Build the string to display the found players
											for index in range(len(playerSearchResultsList)):
												# Add a newline for the next list item
												if index < len(playerSearchResultsList):
													appendString = ' ' + str(index + 1) + ': ' + playerGenInfoList[
														index].name_display_first_last + ' - ' + playerGenInfoList[
																	   index].team_name + ' (' + playerGenInfoList[
																	   index].primary_position_txt + ')' + '\n'
												else:
													appendString = ' ' + str(index + 1) + ': ' + playerGenInfoList[
														index].name_display_first_last + ' - ' + playerGenInfoList[
																	   index].team_name + ' (' + playerGenInfoList[
																	   index].primary_position_txt + ')'
												discordFormattedString = discordFormattedString + appendString

											# Send the message to the channel
											await message.channel.send(discordFormattedString)
											messageTime = datetime.utcnow()
											time.sleep(2)

											# Initialize a new PlayerInfo object
											playerGenInfo = players.PlayerInfo()


											playerSelectedIndex = await self.commonFunctions.wait_for_number(message,
																											 len(
																												 playerSearchResultsList),
																											 30)

											if playerSelectedIndex:
												playerGenInfo = playerGenInfoList[playerSelectedIndex - 1]
											else:
												return


										# Only one player was returned from the search
										elif len(playerSearchResultsList) == 1:
											# Initialize a new PlayerSearchInfo object
											playerGenInfo = players.PlayerInfo()

											playerInfoURL = 'http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code=\'mlb\'&player_id=\'' + \
															playerSearchResultsList[0].player_id + '\''
											playerInfoHeader = {'Content-Type': 'application/json'}
											playerInfoRequest = requests.get(playerInfoURL, playerInfoHeader)
											playerInfoJson = json.loads(playerInfoRequest.text)

											# Parse the json info and populate all the properties
											playerGenInfo.ParseJson(playerInfoJson)

										elif len(playerSearchResultsList) == 0:
											await message.channel.send(
												'I couldn\'t find any players with the name %s in the year %s' % (display_name_to_search, statYear))
											return

										# print('DEBUG: PlayerID = %s' % playerGenInfo.player_id)

										# player is NOT a pitcher
										if playerGenInfo.primary_position_txt != 'P':
											# Get their stats
											# Right now this is hardcoded for the regular season
											playerStatsURL = 'http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id=\'mlb\'&game_type=\'R\'&season=\'' + str(
												statYear) + '\'&player_id=\'' + playerGenInfo.player_id + '\''
											playerStatsHeader = {'Content-Type': 'application/json'}
											playerStatsRequest = requests.get(playerStatsURL, playerStatsHeader)
											playerStatsJson = json.loads(playerStatsRequest.text)

											if int(playerStatsJson['sport_hitting_tm']['queryResults'][
													   'totalSize']) == 0:
												await message.channel.send(
													'%s doesn\'t appear to have any stats for %s' % (
														playerGenInfo.name_display_first_last, statYear))
												return

											# Create a new SeasonBattingStats object
											seasonBattingInfo = players.SeasonBattingStats()
											# Parse the season batting stats
											seasonBattingInfo.ParseJson(playerStatsJson)

											# Create the embed object
											playerEmbed = discord.Embed()
											playerEmbed.title = '**' + playerGenInfo.name_display_first_last + '\'s** Stats for **' + str(
												statYear) + '**'
											playerEmbed.type = 'rich'
											# testEmbed.colour =
											playerEmbed.color = discord.Color.dark_blue()

											for index in range(0, seasonBattingInfo.totalSize):
												valueString = ' Batting Avg: %s\n' \
															  ' HomeRuns: %s\n' \
															  ' Slugging: %s\n' \
															  ' OPS: %s\n' \
															  ' RBI: %s' % (
																  seasonBattingInfo.avg[index],
																  seasonBattingInfo.hr[index],
																  seasonBattingInfo.slg[index],
																  seasonBattingInfo.ops[index],
																  seasonBattingInfo.rbi[index])
												playerEmbed.add_field(name=seasonBattingInfo.team_abbrev[index],
																	  value=valueString)

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
											# Get their stats
											# Right now this is hardcoded for the regular season
											playerStatsURL = 'http://lookup-service-prod.mlb.com/json/named.sport_pitching_tm.bam?league_list_id=\'mlb\'&game_type=\'R\'&season=\'' + str(
												statYear) + '\'&player_id=\'' + playerGenInfo.player_id + '\''
											playerStatsHeader = {'Content-Type': 'application/json'}
											playerStatsRequest = requests.get(playerStatsURL, playerStatsHeader)
											playerStatsJson = json.loads(playerStatsRequest.text)

											if int(playerStatsJson['sport_pitching_tm']['queryResults'][
													   'totalSize']) == 0:
												await message.channel.send(
													'%s doesn\'t appear to have any stats for %s' % (
														playerGenInfo.name_display_first_last, statYear))
												return

											# Create a new SeasonBattingStats object
											seasonPitchingInfo = players.SeasonPitchingStats()
											# Parse the season batting stats
											seasonPitchingInfo.ParseJson(playerStatsJson)

											# Create the embed object
											pitcherEmbed = discord.Embed()
											pitcherEmbed.title = '**' + playerGenInfo.name_display_first_last + '\'s** Stats for **' + str(
												statYear) + '**'
											pitcherEmbed.type = 'rich'
											# testEmbed.colour =
											pitcherEmbed.color = discord.Color.dark_blue()

											for index in range(0, seasonPitchingInfo.totalSize):
												valueString = ' ERA: %s\n' \
															  ' Wins/Losses: %s/%s\n' \
															  ' Games: %s\n' \
															  ' WHIP: %s' % (
																  seasonPitchingInfo.era[index],
																  seasonPitchingInfo.w[index],
																  seasonPitchingInfo.l[index],
																  seasonPitchingInfo.gs[index],
																  seasonPitchingInfo.whip[index])
												pitcherEmbed.add_field(name=seasonPitchingInfo.team_abbrev[index],
																	   value=valueString)

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
									except Exception as e:
										print('DEBUG: Exception in PLAYER. Input was %s' % message.content)
										print('DEBUG: Exception is %s' % e)

								elif 'SCORE' in messageArray[1].upper():
									try:

										# If no team was provided, exit the call
										if len(messageArray) < 3:
											# TODO return all current live games
											await message.channel.send(
												"I need a team to check the score for, try again")
											return

										# Check if there was a date provided, if not use the current date
										if len(messageArray) > 3:
											targetDateTime = dateparser.parse(messageArray[3])
											if targetDateTime is not None:
												await message.channel.send('DEBUG: Getting scores for %s' % targetDateTime.strftime('%Y%m%d'))
											else:
												await message.channel.send("Sorry, I could not figure out the date ""\"%s\"" % messageArray[3])
												return
										else:
											# Set the target day as today
											targetDateTime = datetime.now()

										# Get the team
										teamSelected = await self.commonFunctions.get_team(messageArray[2], message)

										# Make sure a team was returned
										if teamSelected is None:
											await message.channel.send('I couldn\'t find a team with the name %s. Please try again.' % messageArray[2])
											print('DEBUG: Failed to get the team in time in SCORE function')
											print('DEBUG: Input was: ' + messageArray[2])
											print('DEBUG: Message content was: ' + message.content)
											return

										# Get the schedule for the selected date
										queriedSchedule = statsapi.schedule(date=targetDateTime.strftime('%Y-%m-%d'),
																			team=int(teamSelected['id']))

										# Get a list of games a week in the past
										pastDay = datetime.today() - timedelta(1)
										pastWeek = datetime.today() - timedelta(7)
										pastGames = statsapi.schedule(start_date=pastWeek.strftime('%m/%d/%Y'),
																	end_date=pastDay.strftime('%m/%d/%Y'),
																	team=teamSelected['id'])

										# Get a list of games a week in the future
										nextDay = datetime.today() + timedelta(1)
										NextWeek = datetime.today() + timedelta(7)
										nextGames = statsapi.schedule(start_date=nextDay.strftime('%m/%d/%Y'),
																	  end_date=NextWeek.strftime('%m/%d/%Y'),
																	  team=teamSelected['id'])

										# Check for games played in the past week
										if len(pastGames) > 0:
											prev_game = pastGames[len(pastGames) - 1]
										else:
											prev_game = None

										# Double check if a list is returned
										if type(queriedSchedule) is list:

											final_status_list = ["Final", "Game Over", "Completed Early"]
											scheduled_status_list = ["Scheduled", "Pre-Game"]
											live_status_list = ["In Progress", "Delayed"]
											other_status_list = ["Postponed"]

											# Check if the previous game is still 'In Progress' and if so set that as the target game
											# Apparently the MLB api returns the next game sometimes
											if prev_game is not None:
												if prev_game['status'] == 'In Progress' and queriedSchedule[0][
													'status'] == 'Scheduled':
													queriedSchedule[0] = prev_game

											# More than 2 games returned a 2020 special!
											if len(queriedSchedule) > 2:

												# Loop through and spit out each game
												for game in queriedSchedule:
													# Game is over
													if any(game_status in game['status'] for game_status in
														   final_status_list):
														await self.embedFunctions.final_Game_Embed(game, message)

													# Game is scheduled
													elif any(game_status in game['status'] for game_status in
															 scheduled_status_list):
														await self.embedFunctions.scheduled_Game_Embed(game,
																									   message)

													# Game is live
													elif any(game_status in game['status'] for game_status in
															 live_status_list):
														await self.embedFunctions.live_Game_Embed(game, message)

													# Game is other status
													elif any(game_status in game['status'] for game_status in
															 other_status_list):
														await self.embedFunctions.generic_Game_Embed(game, message)

											# There is a doubleheader
											elif len(queriedSchedule) == 2:

												'''GAME 1'''

												# Game 1 is over
												if any(game_status in queriedSchedule[0]['status'] for game_status in final_status_list):
													await self.embedFunctions.final_Game_Embed(queriedSchedule[0], message)

												# Game 1 is scheduled
												elif any(game_status in queriedSchedule[0]['status'] for game_status in scheduled_status_list):
													await self.embedFunctions.scheduled_Game_Embed(queriedSchedule[0], message)
													if prev_game is not None:
														await self.embedFunctions.final_Game_Embed(prev_game, message)

												# Game 1 is live
												elif any(game_status in queriedSchedule[0]['status'] for game_status in live_status_list):
													await self.embedFunctions.live_Game_Embed(queriedSchedule[0], message)
													return

												# Game 1 is other state
												elif any(game_status in queriedSchedule[0]['status'] for game_status in other_status_list):
													await self.embedFunctions.generic_Game_Embed(queriedSchedule[0], message)

												'''GAME 2'''

												# Game 2 is over
												if any(game_status in queriedSchedule[1]['status'] for game_status in final_status_list):
													await self.embedFunctions.final_Game_Embed(queriedSchedule[1], message)
													# If there is a game in the next week, return it
													if len(nextGames) > 0:
														await self.embedFunctions.scheduled_Game_Embed(nextGames[0], message)

												# Game 2 is scheduled
												elif any(game_status in queriedSchedule[1]['status'] for game_status in scheduled_status_list):
													await self.embedFunctions.scheduled_Game_Embed(queriedSchedule[1], message)
													if prev_game is not None:
														await self.embedFunctions.final_Game_Embed(prev_game, message)

												# Game 2 is live
												elif any(game_status in queriedSchedule[1]['status'] for game_status in live_status_list):
													await self.embedFunctions.live_Game_Embed(queriedSchedule[1], message)
													return

												# Game 2 is other state
												elif any(game_status in queriedSchedule[1]['status'] for game_status in other_status_list):
													await self.embedFunctions.generic_Game_Embed(queriedSchedule[0],  message)
												# If there is a game in the next week, return it
												if len(nextGames) > 0:
													await self.embedFunctions.scheduled_Game_Embed(nextGames[0], message)

											# One game was returned
											elif len(queriedSchedule) == 1:

												# Game is over
												if any(game_status in queriedSchedule[0]['status'] for game_status in final_status_list):
													await self.embedFunctions.final_Game_Embed(queriedSchedule[0],  message)
													# If there is a game in the next week, return it
													if len(nextGames) > 0:
														await self.embedFunctions.scheduled_Game_Embed(nextGames[0], message)

												# Game is scheduled
												elif any(game_status in queriedSchedule[0]['status'] for game_status in scheduled_status_list):
													await self.embedFunctions.scheduled_Game_Embed(queriedSchedule[0],  message)
													if prev_game is not None:
														await self.embedFunctions.final_Game_Embed(prev_game, message)

												# Game is live
												elif any(game_status in queriedSchedule[0]['status'] for game_status in live_status_list):
													await self.embedFunctions.live_Game_Embed(queriedSchedule[0], message)

												# Game is other status
												elif any(game_status in queriedSchedule[0]['status'] for game_status in  other_status_list):
													await self.embedFunctions.generic_Game_Embed(queriedSchedule[0], message)
													# If there is a game in the next week, return it
													if len(nextGames) > 0:
														await self.embedFunctions.scheduled_Game_Embed(nextGames[0],  message)

											# No games were returned for the day
											elif len(queriedSchedule) <= 0:
												if len(pastGames) > 0:
													# Return the most recent game
													prev_game = pastGames[len(pastGames) - 1]
												else:
													# No games were returned
													await message.channel.send(
														'Sorry, there are no current or recent games')
													return
												# Check if the previous game is still 'In Progress' and if so set that as the target game
												# Apparently the MLB api returns the next game sometimes
												if prev_game['status'] == 'In Progress':
													print('DEBUG: Previous game still in progress!')
													await self.embedFunctions.live_Game_Embed(prev_game, message)

												# List of status that indicate the game is over
												final_status_list = ["Final", "Game Over", "Completed Early"]
												# Game is over
												if any(game_status in prev_game['status'] for game_status in
													   final_status_list):

													# Game is over
													await self.embedFunctions.final_Game_Embed(prev_game, message)
													# If there is a game in the next week, return it
													if len(nextGames) > 0:
														await self.embedFunctions.scheduled_Game_Embed(nextGames[0],
																									   message)


									except Exception as e:
										print('DEBUG: Exception in SCORE. Input was %s' % message.content)
										print('DEBUG: Exception was %s' % e)
										await message.channel.send('Sorry, something went wrong :( %s', e)

								elif 'HIGHLIGHTS' in messageArray[1].upper():
									try:
										# Set the target day
										targetDateTime = datetime.now()

										# Get the team
										teamSelected = await self.commonFunctions.get_team(messageArray[2], message)

										# Get a list of games a week in the past
										# Remove the lookback by one day for now
										# pastDay = datetime.today()
										# pastWeek = datetime.today() - timedelta(7)
										# pastGames = statsapi.schedule(start_date=pastWeek.strftime('%m/%d/%Y'),
										#							  end_date=pastDay.strftime('%m/%d/%Y'),
										#							  team=teamSelected['id'])

										# Get the last game
										lastGameInfo = statsapi.last_game(teamSelected['id'])
										# lastGameInfo = pastGames[0]

										last_game_pk = statsapi.schedule(game_id=lastGameInfo)

										last_game_datetime = datetime.strptime(last_game_pk[0]['game_date'], "%Y-%m-%d")


										# Get the highlights for the last game
										highlights = statsapi.game_highlights(lastGameInfo)
										highlights_list = statsapi.game_highlight_data(lastGameInfo)
										print(highlights_list)


										# If no highlights are returned then check the previous dates for a game
										if len(highlights) == 0:

											# Look back one week for highlights
											for day in range(0, 7):
												pastDay = datetime.today() - timedelta(day)
												schedule = statsapi.schedule(date=pastDay.strftime('%m/%d/%Y'),
																			 team=teamSelected['id'])
												# TODO check for a double header
												nextToLastGameInfo = schedule[0]['game_id']
												highlights = statsapi.game_highlights(nextToLastGameInfo)
												if len(highlights) > 0:
													break

											# Attempt to get the next to last game highlights
											# = datetime.datetime.today() - timedelta(1)
											# schedule = statsapi.schedule(date=yesterday.strftime('%m/%d/%Y'), team=teamSelected['id'])

											# TODO support double headers
											# nextToLastGameInfo = schedule[0]['game_id']

											# Get the highlights for the last game
											highlights = statsapi.game_highlights(nextToLastGameInfo)

										if len(highlights) > 0:

											# split the highlights on the line breaks of the video links returned
											highlightsList = highlights.split('\n\n')
											# split each highlight on the newline to get 0. Short description 1. Long description 2. Video Link
											splitHighlightsList = []
											for listItem in highlightsList:
												splitHighlightsList.append(listItem.split('\n'))

											# Create the embed object
											highlightEmbed = discord.Embed()
											highlightEmbed.title = '**' + teamSelected[
												'name'] + '** highlights from ' + last_game_datetime.strftime('%A %-m/%-d/%Y')
											highlightEmbed.type = 'rich'
											# testEmbed.colour =
											highlightEmbed.color = discord.Color.dark_blue()

											# Loop through all the returned highlights and format the strings
											for index in range(0, len(highlightsList) - 1):
												# Replace https with <https
												# splitHighlightsList[index][2] = splitHighlightsList[index][2].replace('https', '<https')
												# Replace .mp4 with .mp4>
												# splitHighlightsList[index][2] = splitHighlightsList[index][2].replace('.mp4', '.mp4>')

												# If we haven't hit the character limit yet, add the next highlight
												if len(highlightEmbed) < 6000:
													highlightEmbed.add_field(name=splitHighlightsList[index][0],
																			 value='[' + splitHighlightsList[index][2][
																						 :27] + '...]' + '(' +
																				   splitHighlightsList[index][2] + ')',
																			 inline=False)

											await message.channel.send(embed=highlightEmbed)
										else:
											await message.channel.send(
												'Sorry, I couldn\'t find any highlights for the past week')
									except Exception as e:
										print('DEBUG: Exception in HIGHLIGHTS. Input was %s' % message.content)
										print('DEBUG: Exception was %s' % e)

								elif 'ROSTER' in messageArray[1].upper():
									try:
										teamSelected = await self.commonFunctions.get_team(messageArray[2], message)

										# Create the embed object
										rosterEmbed = discord.Embed()
										rosterEmbed.type = 'rich'
										rosterEmbed.color = discord.Color.dark_blue()

										rosterEmbed.add_field(
											name='Current Roster for the **' + teamSelected['name'] + '**',
											value='```' + statsapi.roster(int(teamSelected['id'])) + '```')
										await message.channel.send(embed=rosterEmbed)
									except Exception as e:
										print('DEBUG: Exception in ROSTER. Input was %s' % message.content)
										print('DEBUG: Exception was %s' % e)

								elif 'STANDINGS' in messageArray[1].upper():
									try:
										# league IDs

										# 103 = American
										# 104 = National

										# Division IDs

										# AL East - 201
										# AL Central = 202
										# AL West = 200

										# NL East - 204
										# NL Central - 205
										# NL West - 203

										# alEastStandingsString = statsapi.standings(leagueId='103', division='201', standingsTypes='byDivision')
										# alCentralStandingsString = statsapi.standings(leagueId='103', division='202', standingsTypes='byDivision')
										# alWestStandingsString = statsapi.standings(leagueId='103', division='200', standingsTypes='byDivision')

										# nlEastStandingsString = statsapi.standings(leagueId=104, division='204')
										# nlCentralStandingsString = statsapi.standings(leagueId='104', division='205', standingsTypes='byDivision')
										# nlWestStandingsString = statsapi.standings(leagueId='104', division='203', standingsTypes='byDivision')

										alStandingsString = statsapi.standings(leagueId='103',
																			   standingsTypes='byDivision',
																			   include_wildcard=False)

										alStandingsArray = alStandingsString.split('\n\n')

										nlStandingsString = statsapi.standings(leagueId='104',
																			   standingsTypes='byDivision',
																			   include_wildcard=False)

										nlStandingsArray = nlStandingsString.split('\n\n')

										# Create the embed object
										standingsEmbed = discord.Embed()
										standingsEmbed.type = 'rich'
										# testEmbed.colour =
										standingsEmbed.color = discord.Color.dark_blue()
										standingsEmbed.add_field(name='**AL East**',
																 value='```' + alStandingsArray[1] + '```',
																 inline=True)
										standingsEmbed.add_field(name='**AL Central**',
																 value='```' + alStandingsArray[2] + '```',
																 inline=False)
										standingsEmbed.add_field(name='**AL West**',
																 value='```' + alStandingsArray[0] + '```',
																 inline=False)

										standingsEmbed.add_field(name='**NL East**',
																 value='```' + nlStandingsArray[2] + '```',
																 inline=False)
										standingsEmbed.add_field(name='**NL Central**',
																 value='```' + nlStandingsArray[0] + '```',
																 inline=False)
										standingsEmbed.add_field(name='**NL West**',
																 value='```' + nlStandingsArray[1] + '```',
																 inline=False)

										await message.channel.send(embed=standingsEmbed)
									except Exception as e:
										print('DEBUG: Exception in STANDINGS. Input was %s' % message.content)
										print('DEBUG: Exception was %s' % e)

								elif 'SCHEDULE' in messageArray[1].upper():
									try:
										# Set the target day
										# targetDateTime = datetime.datetime.now()
										targetDateTime = datetime.now()

										# TODO analyze messageArray[2] and check if its a date
										# targetDateTime = datetime.datetime.strptime(messageArray[2], '%Y-%m-%d')

										# If there is a team supplied
										if len(messageArray) > 2:

											# Get the team
											teamSelected = await self.commonFunctions.get_team(messageArray[2], message)

											# Get the schedule for the selected date
											queriedSchedule = statsapi.schedule(
												date=targetDateTime.strftime('%Y-%m-%d'),
												team=int(teamSelected['id']))

											# Get a list of games a week in the past
											pastDay = datetime.today() - timedelta(1)
											pastWeek = datetime.today() - timedelta(7)
											pastGames = statsapi.schedule(start_date=pastWeek.strftime('%m/%d/%Y'),
																		  end_date=pastDay.strftime('%m/%d/%Y'),
																		  team=teamSelected['id'])

											# Get a list of games a week in the future
											nextDay = datetime.today() + timedelta(1)
											NextWeek = datetime.today() + timedelta(7)
											nextGames = statsapi.schedule(start_date=nextDay.strftime('%m/%d/%Y'),
																		  end_date=NextWeek.strftime('%m/%d/%Y'),
																		  team=teamSelected['id'])

											# Create the schedule embed
											scheduleEmbed = discord.Embed()
											scheduleEmbed.title = '**' + teamSelected[
												'name'] + '**\'s games for the next week'
											scheduleEmbed.type = 'rich'
											# testEmbed.colour =
											scheduleEmbed.color = discord.Color.dark_blue()

											# scoreEmbed.add_field(name='NAME', value='VALUE', inline=False)
											# scheduleEmbed.add_field(name=gameTimeLocal.strftime('%m/%d/%Y'), value= + ' EST', inline=False)

											if len(pastGames) > 0:
												prev_game = pastGames[len(pastGames) - 1]

											print(queriedSchedule)
											# Check for a double header
											if len(queriedSchedule) == 2:

												# TODO Handle games past midnight

												# Game is scheduled
												if queriedSchedule[0]['status'] == 'Scheduled' or queriedSchedule[0][
													'status'] == 'Pre-Game':
													# Add the game to the list
													nextGames.insert(0, queriedSchedule[0])

												# Game is scheduled
												if queriedSchedule[1]['status'] == 'Scheduled' or queriedSchedule[1][
													'status'] == 'Pre-Game':
													# Add the game to the list
													nextGames.insert(0, queriedSchedule[1])
											# A single game was returned
											elif len(queriedSchedule) == 1:
												if len(pastGames) > 0:
													prev_game = pastGames[len(pastGames) - 1]

												# Check if the previous game is still 'In Progress' and if so set that as the target game
												# Apparently the MLB api returns the next game sometimes
												if prev_game['status'] == 'In Progress' and queriedSchedule[0][
													'status'] == 'Scheduled':
													queriedSchedule = prev_game

												# Game is scheduled
												if queriedSchedule[0]['status'] == 'Scheduled' or queriedSchedule[0][
													'status'] == 'Pre-Game':
													# Add the game to the list
													nextGames.insert(0, queriedSchedule[0])
											# No games were returned for the day
											elif len(queriedSchedule) <= 0:
												if len(pastGames) > 0:
													prev_game = pastGames[len(pastGames) - 1]

													# Game is still scheduled
													if prev_game['status'] == 'Scheduled' or prev_game[
														'status'] == 'Pre-Game':
														# Add the game to the list
														nextGames.insert(0, queriedSchedule[0])

											# Uhh more than 2 games in a day?
											else:
												print('DEBUG: statsapi.schedule(date=' + targetDateTime.strftime(
													'%Y-%m-%d') + ',team=' +
													  str(team=int(
														  teamSelected['id'])) + ')) returned more than 2 games')

											# Add each game from the nextGames list to the embed
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
												print('DEBUG: game_datetime' + str(games['game_datetime']))

												gameTimeLocal = self.commonFunctions.get_Local_Time(
													games['game_datetime'])
												print('DEBUG: localtime' + str(gameTimeLocal))
												scheduleEmbed.add_field(
													name=gameTimeLocal.strftime(
														'%m/%d/%Y') + ' @ ' + gameTimeLocal.strftime(
														'%-I:%M%p') + ' EST',
													value=homeTeamShort + ' vs ' + awayTeamShort,
													inline=False)

											await message.channel.send(embed=scheduleEmbed)
										# List all games found for the target date
										else:
											# For now assume the target date is today

											# Get the schedule for the selected date
											queriedSchedule = statsapi.schedule(
												date=targetDateTime.strftime('%Y-%m-%d'))

											scheduledGamesList = []
											inProgressGamesList = []
											finalGameList = []

											# More than one game was returned
											if len(queriedSchedule) >= 1:

												# Loop through all the games and add them to the list
												for index in range(0, len(queriedSchedule)):
													# If the game isn't in progress add it
													if queriedSchedule[index]['status'] == 'Scheduled' or \
															queriedSchedule[index]['status'] == 'Pre-Game':
														scheduledGamesList.insert(0, queriedSchedule[index])
													elif queriedSchedule[index]['status'] == 'In Progress':
														inProgressGamesList.insert(0, queriedSchedule[index])
													elif queriedSchedule[index]['status'] == 'Final' or \
															queriedSchedule[index][
																'status'] == 'Game Over':
														finalGameList.insert(0, queriedSchedule[index])

											# A single game was returned
											elif len(queriedSchedule) == 1:
												# Game is scheduled
												if queriedSchedule['status'] == 'Scheduled' or queriedSchedule[
													'status'] == 'Pre-Game':
													scheduledGamesList.insert(0, queriedSchedule)
												elif queriedSchedule['status'] == 'In Progress':
													inProgressGamesList.insert(0, queriedSchedule)
												elif queriedSchedule['status'] == 'Final' or queriedSchedule[
													'status'] == 'Game Over':
													finalGameList.insert(0, queriedSchedule)

											# No games were returned for the day
											elif len(queriedSchedule) <= 0:
												await message.channel.send(
													'Sorry, I didn\'t find any games on %s' % targetDateTime.strftime(
														'%Y-%m-%d'))
												return

											# Create the schedule embed
											scheduledEmbed = discord.Embed()
											scheduledEmbed.title = '**Scheduled Games on ' + targetDateTime.strftime(
												'%Y-%-m-%-d') + '**'
											scheduledEmbed.type = 'rich'
											# testEmbed.colour =
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
												gameTimeLocal = self.commonFunctions.get_Local_Time(
													games['game_datetime'])
												scheduledEmbed.add_field(
													name=gameTimeLocal.strftime(
														'%m/%d/%Y') + ' @ ' + gameTimeLocal.strftime(
														'%-I:%M%p' + ' ET'),
													value=homeTeamShort + ' vs ' + awayTeamShort,
													inline=False)

											# Create the live embed
											inProgressEmbed = discord.Embed()
											inProgressEmbed.title = '**Live Games on ' + targetDateTime.strftime(
												'%Y-%-m-%-d') + '**'
											inProgressEmbed.type = 'rich'
											# testEmbed.colour =
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

												nameString = '**' + games['home_name'] + '** vs **' + games[
													'away_name'] + '**'
												# Add the scores
												valueString = homeTeamShort + ' ' + homeScoreString + ' - ' + awayTeamShort + ' ' + awayScoreString + '\n'
												valueString = valueString + games['inning_state'] + ' ' + str(
													games['current_inning'])

												inProgressEmbed.add_field(name=nameString, value=valueString,
																		  inline=False)

											# Create the final embed
											finalEmbed = discord.Embed()
											finalEmbed.title = '**Final Games on ' + targetDateTime.strftime(
												'%Y-%-m-%-d') + '**'
											finalEmbed.type = 'rich'
											# testEmbed.colour =
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

												nameString = '**' + games['home_name'] + '** vs **' + games[
													'away_name'] + '**'
												# Add the scores
												valueString = homeTeamShort + ' ' + homeScoreString + ' - ' + awayTeamShort + ' ' + awayScoreString + ' **F**'

												finalEmbed.add_field(name=nameString, value=valueString, inline=False)

											if len(scheduledGamesList) > 0:
												await message.channel.send(embed=scheduledEmbed)
											if len(inProgressGamesList) > 0:
												await message.channel.send(embed=inProgressEmbed)
											if len(finalGameList) > 0:
												await message.channel.send(embed=finalEmbed)
									except Exception as e:
										print('DEBUG: Exception in SCHEDULE. Input was %s' % message.content)
										print('DEBUG: Exception was %s' % e)

								elif 'GIBBY' in messageArray[1].upper():
									# Create the embed object
									gibbyEmbed = discord.Embed()
									gibbyEmbed.title = '**BRUDDA**'
									gibbyEmbed.type = 'rich'
									# testEmbed.colour =
									gibbyEmbed.color = discord.Color.dark_blue()

									pewPewId = '<@&607777470208540710>'

									gibbyEmbed.set_image(url='https://i.imgur.com/kqGHmdi.jpg')
									gibbyEmbed.image.width = 500
									gibbyEmbed.image.height = 600

									# await message.channel.send('%s' % pewPewId)
									await message.channel.send(content=pewPewId, embed=gibbyEmbed)

									# https://i.imgur.com/AewHTiT.png

									index = random.randint(1, 20)

									if index < 10:
										# Create the embed object
										gibbyEmbed2 = discord.Embed()
										gibbyEmbed2.title = '**BRUDDA!!**'
										gibbyEmbed2.type = 'rich'
										# testEmbed.colour =
										gibbyEmbed2.color = discord.Color.dark_blue()
										gibbyEmbed2.set_image(url='https://i.redd.it/w5zopr127us31.jpg')
										gibbyEmbed2.image.width = 500
										gibbyEmbed2.image.height = 600
									else:
										# Create the embed object
										gibbyEmbed2 = discord.Embed()
										gibbyEmbed2.title = '**BRUDDA!!**'
										gibbyEmbed2.type = 'rich'
										# testEmbed.colour =
										gibbyEmbed2.color = discord.Color.dark_blue()
										gibbyEmbed2.set_image(url='https://i.redd.it/ekjqwa98qin21.jpg')
										gibbyEmbed2.image.width = 500
										gibbyEmbed2.image.height = 600

									# await message.channel.send('%s' % pewPewId)
									await message.channel.send(embed=gibbyEmbed2)

								elif 'LISTEN' in messageArray[1].upper():
									try:
										saved_guild_data = await self.refresh_channel_names(message.guild,
																							saved_guild_data)
										# Listen to all channels
										if messageArray[2].upper() != "ALL":
											newChannelName = messageArray[2]
											newChannel = None
											# get the channel id
											for guildTextChannels in message.guild.text_channels:
												if newChannelName == guildTextChannels.name:
													newChannel = guildTextChannels

											# If the channel name is a match then add it to the subscribed channels
											if newChannel is not None:
												# Check that it doesn't already exist
												if IdExists(newChannel.id, saved_guild_data['subscribedChannels']):
													await message.channel.send(
														'I\'m already listening to ' + newChannelName)
												else:
													saved_guild_data['subscribedChannels'].append({
														'id': str(newChannel.id),
														'name': newChannel.name})
													self.write_data_file(self.dataFilePath + str(message.guild.id),
																		 saved_guild_data)
													await message.channel.send('I will now listen to ' + newChannelName)
											else:
												await message.channel.send(
													'Sorry I couldn\'t find the channel ' + newChannelName)
										elif messageArray[2].upper() == 'ALL':
											# Check for a channel named 'ALL'
											found_all_channel = False
											for guildTextChannels in message.guild.text_channels:
												if 'ALL' == guildTextChannels.name.upper():
													found_all_channel = True
													newChannel = guildTextChannels

													if newChannel is not None:
														# Check that it doesn't already exist
														if IdExists(newChannel.id,
																	saved_guild_data['subscribedChannels']):
															await message.channel.send(
																'I\'m already listening to ' + newChannel.name)
														else:
															saved_guild_data['subscribedChannels'].append({
																'id': str(newChannel.id),
																'name': newChannel.name})
															self.write_data_file(
																self.dataFilePath + str(message.guild.id),
																saved_guild_data)
															await message.channel.send(
																'I will now listen to ' + newChannel.name)

											if found_all_channel is False:
												# Subscribe to all channels
												newChannel = None

												for guildTextChannels in message.guild.text_channels:
													# Check that it doesn't already exist
													if IdExists(guildTextChannels.id, saved_guild_data['subscribedChannels']):
														continue
													else:
														saved_guild_data['subscribedChannels'].append({
															'id': str(guildTextChannels.id),
															'name': guildTextChannels.name})
														self.write_data_file(self.dataFilePath + str(message.guild.id),
																			 saved_guild_data)
												await message.channel.send(
													'I will now listen to all channels that I can')



									except Exception as e:
										print('DEBUG: Exception in LISTEN. Input was %s' % message.content)
										print('DEBUG: Exception was %s' % e)

								elif 'IGNORE' in messageArray[1].upper():
									try:
										saved_guild_data = await self.refresh_channel_names(message.guild,
																							saved_guild_data)
										channelToRemoveName = messageArray[2]
										remChannel = None
										# get the channel id
										for guildTextChannels in message.guild.text_channels:
											if channelToRemoveName == guildTextChannels.name:
												remChannel = guildTextChannels

										# If the channel name is a match then remove it from the subscribed channels
										if remChannel is not None:
											# Check that it exist
											if IdExists(remChannel.id, saved_guild_data['subscribedChannels']):
												# Iterate through the objects in the JSON and pop (remove)
												# the obj once we find it.
												for i in range(len(saved_guild_data['subscribedChannels'])):
													if saved_guild_data['subscribedChannels'][i]["id"] == str(
															remChannel.id):
														saved_guild_data['subscribedChannels'].pop(i)
														break
												self.write_data_file(self.dataFilePath + str(message.guild.id),
																	 saved_guild_data)
												await message.channel.send(
													'I will not listen to ' + channelToRemoveName + ' anymore')
											else:
												await message.channel.send(
													'I\'m not listening to ' + channelToRemoveName)

										else:
											await message.channel.send(
												'Sorry I couldn\'t find the channel ' + channelToRemoveName)
									except Exception as e:
										print('DEBUG: Exception in IGNORE. Input was %s' % message.content)
										print('DEBUG: Exception was %s' % e)

								elif 'LISTCHANNELS' in messageArray[1].upper():
									try:
										saved_guild_data = await self.refresh_channel_names(message.guild,
																							saved_guild_data)
										subbedEmbed = discord.Embed()
										# subbedEmbed.title = 'Subscribed Channels'
										subbedEmbed.type = 'rich'
										subbedEmbed.color = discord.Color.dark_blue()
										subbed_channel_string = ""
										for index, channel in enumerate(saved_guild_data['subscribedChannels']):
											subbed_channel_string = subbed_channel_string + str(index + 1) + '. ' + \
																	channel[
																		'name'] + '\n'
										# subbedEmbed.add_field(name=str(index + 1), value=channel['name'], inline=False)

										subbedEmbed.add_field(name='Subscribed Channels', value=subbed_channel_string,
															  inline=False)
										await message.channel.send(embed=subbedEmbed)
									except Exception as e:
										print('DEBUG: Exception in LISTCHANNELS. Input was %s' % message.content)
										print('DEBUG: Exception was %s' % e)

								elif 'NOTES' in messageArray[1].upper():
									# print('DEBUG: Capturing Notes')
									# print('DEBUG: game_winProbability')
									# print('DEBUG: %s', statsapi.notes('game_winProbability'))

									print('DEBUG: game_contextMetrics')
									print('DEBUG: %s', statsapi.notes('game_contextMetrics'))
									#logging.info('%s called NOTES' % message.author.display_name)
									#print('DEBUG: Capturing Notes')
									#print('DEBUG: standings')
									#print('DEBUG: %s', statsapi.notes('status'))

								# print('DEBUG: game_contextMetrics')
								# parameters = {
								#			'gamePk': 55555
								#			}
								#
								# print('DEBUG: %s', statsapi.get(endpoint='game_contextMetrics', params=parameters))

								elif 'META' in messageArray[1].upper():
									print('DEBUG: Getting meta response for %s' % messageArray[2])
									print('DEBUG: %s' % statsapi.meta(messageArray[2]))

								# elif 'TEST' in messageArray[1].upper():
								#	commonFunctions = commonfunctions.CommonFunctions()
								#	teamSelected = await commonFunctions.get_team('phi', message)
								#	print('DEBUG: teamSelected = %s' % teamSelected)

								elif 'PLAYOFFS' in messageArray[1].upper():
									try:
										# await message.channel.send('The playoffs command is currently being updated for the new playoff format of all the teams.')
										# required parameter but it doesn't seem to matter which league is specified
										parameters = {'leagueId': '103'}
										seriesStandingsDict = statsapi.get(endpoint='schedule_postseason_series',
																		   params=parameters)
										#print('DEBUG: seriesStandingsDict:')
										#print(seriesStandingsDict)

										print('DEBUG: Got the playoff series')
										'''
										[{'name': 'regularSeason', 'description': 'Regular Season Standings'}, {'name': 'wildCard', 'description': 'Wild card standings'}, {'name': 'divisionLeaders', 'description': 'Division Leader standings'}, {'name': 'wildCardWithLeaders', 'description': 'Wild card standings with Division Leaders'}, {'name': 'firstHalf', 'description': 'First half standings.  Only valid for leagues with a split season.'}, {'name': 'secondHalf', 'description': 'Second half standings. Only valid for leagues with a split season.'}, {'name': 'springTraining', 'description': 'Spring Training Standings'}, {'name': 'postseason', 'description': 'Postseason Standings'}, {'name': 'byDivision', 'description': 'Standings by Division'}, {'name': 'byConference', 'description': 'Standings by Conference'}, {'name': 'byLeague', 'description': 'Standings by League'}, {'name': 'byOrganization', 'description': 'Standing by Organization'}]
		
										'''
										# This throws an 500 error
										# parameters = {'leagueId':'103', 'standingsTypes':'postSeason'}
										# playoffStandings = statsapi.get(endpoint='standings', params=parameters)
										# print(playoffStandings)

										alwildCard = None
										alwildCardA = None
										alwildCardB = None
										alwildCardC = None
										alwildCardD = None
										aldsA = None
										aldsB = None
										alcs = None

										nlwildCard = None
										nlwildCardA = None
										nlwildCardB = None
										nlwildCardC = None
										nlwildCardD = None
										nldsA = None
										nldsB = None
										nlcs = None

										worldSeries = None

										for seriesFound in seriesStandingsDict['series']:
											# print('DEBUG: Series ID = %s' % seriesFound['series']['id'])
											if seriesFound['series']['id'] == 'ALDS \'A\'':
												aldsA = seriesFound
											elif seriesFound['series']['id'] == 'ALDS \'B\'':
												aldsB = seriesFound
											elif seriesFound['series']['id'] == 'NLDS \'A\'':
												nldsA = seriesFound
											elif seriesFound['series']['id'] == 'NLDS \'B\'':
												nldsB = seriesFound
											elif seriesFound['series']['id'] == 'ALCS':
												alcs = seriesFound
											elif seriesFound['series']['id'] == 'NLCS':
												nlcs = seriesFound
											elif seriesFound['series']['id'] == 'WS':
												worldSeries = seriesFound
											# Leaving these in for now if we return to this format in 2021
											elif seriesFound['series']['id'] == 'ALWC':
												alwildCard = seriesFound
											elif seriesFound['series']['id'] == 'NLWC':
												nlwildCard = seriesFound
											# 16 teams in the playoffs for 2020!
											elif seriesFound['series']['id'] == 'ALWC \'A\'':
												alwildCardA = seriesFound
											elif seriesFound['series']['id'] == 'ALWC \'B\'':
												alwildCardB = seriesFound
											elif seriesFound['series']['id'] == 'ALWC \'C\'':
												alwildCardC = seriesFound
											elif seriesFound['series']['id'] == 'ALWC \'D\'':
												alwildCardD = seriesFound
											elif seriesFound['series']['id'] == 'NLWC \'A\'':
												nlwildCardA = seriesFound
											elif seriesFound['series']['id'] == 'NLWC \'B\'':
												nlwildCardB = seriesFound
											elif seriesFound['series']['id'] == 'NLWC \'C\'':
												nlwildCardC = seriesFound
											elif seriesFound['series']['id'] == 'NLWC \'D\'':
												nlwildCardD = seriesFound

										# print('DEBUG: Completed series eval')
										# print('DEBUG aldsA = {}'.format(aldsA))
										# print('DEBUG aldsB = {}'.format(aldsB))
										# print('DEBUG nldsA = {}'.format(nldsA))
										# print('DEBUG nldsB = {}'.format(nldsB))
										# print('DEBUG alcs = {}'.format(alcs))
										# print('DEBUG nlcs = {}'.format(nlcs))
										# print('DEBUG worldSeries = {}'.format(worldSeries))
										# print('DEBUG alwildCardA = {}'.format(alwildCardA))
										# print('DEBUG alwildCardB = {}'.format(alwildCardB))
										# print('DEBUG alwildCardC = {}'.format(alwildCardC))
										# print('DEBUG alwildCardD = {}'.format(alwildCardD))
										# print('DEBUG nlwildCardA = {}'.format(nlwildCardA))
										# print('DEBUG nlwildCardB = {}'.format(nlwildCardB))
										# print('DEBUG nlwildCardC = {}'.format(nlwildCardC))
										# print('DEBUG nlwildCardD = {}'.format(nlwildCardD))

										'''
										#Series Lists
										aldsA = seriesStandingsDict['series'][0]
										#await self.embedFunctions.playoff_Series_Embed(aldsA, message)
										nldsB = seriesStandingsDict['series'][1]
										#await self.embedFunctions.playoff_Series_Embed(nsldB, message)
										nldsA = seriesStandingsDict['series'][2]
										#await self.embedFunctions.playoff_Series_Embed(nsldA, message)
										aldsB = seriesStandingsDict['series'][3]
										#await self.embedFunctions.playoff_Series_Embed(aldsB, message)
										nlcs = seriesStandingsDict['series'][4]
										#await self.embedFunctions.playoff_Series_Embed(nlcs, message)
										alcs = seriesStandingsDict['series'][5]
										#await self.embedFunctions.playoff_Series_Embed(alcs, message)
										worldSeries = seriesStandingsDict['series'][6]
										#await self.embedFunctions.playoff_Series_Embed(worldSeries, message)
										alwildCard = seriesStandingsDict['series'][7]
										#await self.embedFunctions.playoff_Series_Embed(alwildCard, message)
										nlwildCard = seriesStandingsDict['series'][8]
										#await self.embedFunctions.playoff_Series_Embed(nlwildCard, message)
										'''

										# Get the state of all AL series
										if alwildCard is not None:
											alwildCardComplete = await self.commonFunctions.playoffSeriesOver(alwildCard)
										if alwildCardA is not None:

											alwildCard_A_Complete = await self.commonFunctions.playoffSeriesOver(
												alwildCardA)
										if alwildCardB is not None:
											alwildCard_B_Complete = await self.commonFunctions.playoffSeriesOver(
												alwildCardB)
										if alwildCardC is not None:
											alwildCard_C_Complete = await self.commonFunctions.playoffSeriesOver(
												alwildCardC)
										if alwildCardD is not None:
											alwildCard_D_Complete = await self.commonFunctions.playoffSeriesOver(
												alwildCardD)
										if aldsA is not None:
											aldsAComplete = await self.commonFunctions.playoffSeriesOver(aldsA)
										if aldsB is not None:
											aldsBComplete = await self.commonFunctions.playoffSeriesOver(aldsB)
										if alcs is not None:
											alcsComplete = await self.commonFunctions.playoffSeriesOver(alcs)

										# Get the state of all NL series
										if nlwildCard is not None:
											nlwildCardComplete = await self.commonFunctions.playoffSeriesOver(nlwildCard)
										if nlwildCardA is not None:
											nlwildCard_A_Complete = await self.commonFunctions.playoffSeriesOver(
												nlwildCardA)
										if nlwildCardB is not None:
											nlwildCard_B_Complete = await self.commonFunctions.playoffSeriesOver(
												nlwildCardB)
										if nlwildCardC is not None:
											nlwildCard_C_Complete = await self.commonFunctions.playoffSeriesOver(
												nlwildCardC)
										if nlwildCardD is not None:
											nlwildCard_D_Complete = await self.commonFunctions.playoffSeriesOver(
												nlwildCardD)
										if nldsA is not None:
											nldsAComplete = await self.commonFunctions.playoffSeriesOver(nldsA)
										if nldsB is not None:
											nldsBComplete = await self.commonFunctions.playoffSeriesOver(nldsB)
										if nlcs is not None:
											nlcsComplete = await self.commonFunctions.playoffSeriesOver(nlcs)


										if alcsComplete and nlcsComplete:
											await self.embedFunctions.playoff_Series_Embed(worldSeries, message)
										else:
											# If the division series are over, display the championship series
											if aldsAComplete and aldsBComplete:
												await self.embedFunctions.playoff_Series_Embed(alcs, message)
											else:
												await self.embedFunctions.playoff_Series_Embed(aldsA, message)
												await self.embedFunctions.playoff_Series_Embed(aldsB, message)

											# If the division series are over, display the championship series
											if nldsAComplete and nldsBComplete:
												await self.embedFunctions.playoff_Series_Embed(nlcs, message)
											else:
												await self.embedFunctions.playoff_Series_Embed(nldsA, message)
												await self.embedFunctions.playoff_Series_Embed(nldsB, message)

										# If the wild card game exists and is over, don't display it
										if alwildCard is not None and not alwildCardComplete:
											await self.embedFunctions.playoff_Series_Embed(alwildCard, message)

										# If the wild card game exists and is over, don't display it
										if alwildCardA is not None and not alwildCard_A_Complete:
											await self.embedFunctions.playoff_Series_Embed(alwildCardA, message)

										# If the wild card game exists and is over, don't display it
										if alwildCardB is not None and not alwildCard_B_Complete:
											await self.embedFunctions.playoff_Series_Embed(alwildCardB, message)

										# If the wild card game exists and is over, don't display it
										if alwildCardC is not None and not alwildCard_C_Complete:
											await self.embedFunctions.playoff_Series_Embed(alwildCardC,
																						   message)

										# If the wild card game exists and is over, don't display it
										if alwildCardD is not None and not alwildCard_D_Complete:
											await self.embedFunctions.playoff_Series_Embed(alwildCardD,
																						   message)

										# If the wild card game is over, don't display it
										if nlwildCard is not None and not nlwildCardComplete:
											await self.embedFunctions.playoff_Series_Embed(nlwildCard, message)

										# If the wild card game exists and is over, don't display it
										if nlwildCardA is not None and not nlwildCard_A_Complete:
											await self.embedFunctions.playoff_Series_Embed(nlwildCardA, message)

										# If the wild card game exists and is over, don't display it
										if nlwildCardB is not None and not nlwildCard_B_Complete:
											await self.embedFunctions.playoff_Series_Embed(nlwildCardB, message)

										# If the wild card game exists and is over, don't display it
										if nlwildCardC is not None and not nlwildCard_C_Complete:
											await self.embedFunctions.playoff_Series_Embed(nlwildCardC,
																						   message)

										# If the wild card game exists and is over, don't display it
										if nlwildCardD is not None and not nlwildCard_D_Complete:
											await self.embedFunctions.playoff_Series_Embed(nlwildCardD,
																						   message)

										# print(statsapi.get('standings',{'leagueId':'103','sportId':1,'hydrate':'hydrations','fields':'hydrations'}))

										# (leagueId='103', standingsTypes='byDivision', include_wildcard=False)
										# playoffEmbed.add_field(name='Current Standings', value=playoffStandingsString)
										# await message.channel.send(embed=playoffEmbed)

										'''
										DEBUG: Getting meta response for standingsTypes
										DEBUG: [{'name': 'regularSeason', 'description': 'Regular Season Standings'}, {'name': 'wildCard', 'description': 'Wild card standings'}, {'name': 'divisionLeaders', 'description': 'Division Leader standings'}, {'name': 'wildCardWithLeaders', 'description': 'Wild card standings with Division Leaders'}, {'name': 'firstHalf', 'description': 'First half standings.  Only valid for leagues with a split season.'}, {'name': 'secondHalf', 'description': 'Second half standings. Only valid for leagues with a split season.'}, {'name': 'springTraining', 'description': 'Spring Training Standings'}, {'name': 'postseason', 'description': 'Postseason Standings'}, {'name': 'byDivision', 'description': 'Standings by Division'}, {'name': 'byConference', 'description': 'Standings by Conference'}, {'name': 'byLeague', 'description': 'Standings by League'}, {'name': 'byOrganization', 'description': 'Standing by Organization'}]
		
										DEBUG: standings
										DEBUG: %s Endpoint: standings
										All path parameters: ['ver'].
										Required path parameters (note: ver will be included by default): ['ver'].
										All query parameters: ['leagueId', 'season', 'standingsTypes', 'date', 'hydrate', 'fields'].
										Required query parameters: [['leagueId']].
										The hydrate function is supported by this endpoint. Call the endpoint with {'hydrate':'hydrations'} in the parameters to return a list of available hydrations. For example, statsapi.get('schedule',{'sportId':1,'hydrate':'hydrations','fields':'hydrations'})
										'''
									except Exception as e:
										print('DEBUG: Exception in PLAYOFFS. Input was %s' % message.content)
										print('DEBUG: Exception was %s' % e)


								elif 'HOCKEY' in messageArray[1].upper():
									hockeyEmbed = discord.Embed()
									hockeyEmbed.title = 'Brrr its getting cold in here...'
									hockeyEmbed.type = 'rich'
									hockeyEmbed.color = discord.Color.dark_blue()
									hockeyEmbed.set_image(url='https://i.imgur.com/yn7efui.png')

									# Get the NHL schedule
									scheduleResponse = await self.commonFunctions.sendGetRequest(
										'https://statsapi.web.nhl.com/api/v1/schedule')

									# Parse the JSON
									scheduleJson = json.loads(scheduleResponse.text)

									if scheduleJson['totalGames'] != 0:

										games = scheduleJson['dates'][0]['games']

										for hockeyGame in games:
											gameTimeLocal = self.commonFunctions.get_Local_Time(hockeyGame['gameDate'])
											nameString = hockeyGame['teams']['away']['team']['name'] + ' vs ' + \
														 hockeyGame['teams']['home']['team']['name']
											valueString = gameTimeLocal.strftime('%I:%M%p' + ' ET') + ' @ ' + \
														  hockeyGame['venue']['name']
											hockeyEmbed.add_field(name=nameString, value=valueString)

										contentString = 'BaseBot hipchecked ' + message.author.mention + ' into the boards! Savage! \n Anyway here are the games for ' + gameTimeLocal.strftime(
											'%m/%d/%Y')
										await message.channel.send(content=contentString, embed=hockeyEmbed)
										return
									else:
										await message.channel.send("I didn't find any upcoming hockey games")
										return


								# Display the help message
								elif 'HELP' in messageArray[1].upper():
									await self.embedFunctions.helpEmbed(message)

								else:
									await message.channel.send(
										'Sorry I don\'t understand, try saying \'BaseBot HELP\' for a list of available commands.')
							# Bot was called without enough arguments
							elif messageArray[0].upper() == 'BASEBOT' and len(messageArray) == 1:
								await message.channel.send(
									'I like it when you say my name, but I need more instructions.')
								return

					else:
						return
				# The guild has no data, create it
				else:
					found_channel = False
					# Try to send the welcome message to text channels until successful
					for channel_index in range(0, len(message.guild.text_channels)):
						try:
							# Send a welcome message to the first channel with help and instructions
							await message.guild.text_channels[channel_index].send(
								'Hi! I\'m ' + self.user.mention + '! I\'m a bot for Major League Baseball stats, '
																  'schedules, scores, standings and more. '
																  '\nRight now I will only listen to this channel. '
																  '\nFor a list of commands, type <basebot help>')
							found_channel = True

							# Write a new guid data file and populate the meta data
							jsonData = {}
							jsonData['guildname'] = message.guild.name
							jsonData['guildid'] = str(message.guild.id)
							jsonData['dateCreated'] = datetime.now().strftime('%m/%d/%Y')
							jsonData['lastModified'] = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
							jsonData['subscribedChannels'] = []
							# get the info for the first text channel in the guild
							jsonData['subscribedChannels'].append({
								'id': str(message.guild.text_channels[channel_index].id),
								'name': message.guild.text_channels[channel_index].name
							})
							self.write_data_file(self.dataFilePath + str(message.guild.id), jsonData)
							await self.refresh_datafiles()
							break
						except discord.Forbidden:
							# Unable to send message in channel, try the next one
							pass

					# If the loop exits without finding a channel ignore everything I guess :/
					if not found_channel:
						print('DEBUG: Guild %s | %s has no channels basebot can send to' % str(message.guild.id, message.guild.name))
						# Write a new guid data file and populate the meta data
						jsonData = {}
						jsonData['guildname'] = message.guild.name
						jsonData['guildid'] = str(message.guild.id)
						jsonData['dateCreated'] = datetime.now().strftime('%m/%d/%Y')
						jsonData['lastModified'] = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
						jsonData['subscribedChannels'] = []
						# get the info for the first text channel in the guild
						jsonData['subscribedChannels'].append({
							'id': '0',
							'name': 'unknown'
						})
						self.write_data_file(self.dataFilePath + str(message.guild.id), jsonData)
						await self.refresh_datafiles()
		except Exception as e:
			print('DEBUG: Error in on_message. Input was \'{}\''.format(message.content))
			print('DEBUG: Message was from guild: {} | \'{}\' '.format(str(message.guild.id), message.guild.name))


def IdExists(channel_id, channel_list):
	for channel in channel_list:
		if str(channel_id) == channel['id']:
			return True
	return False


def FileExists(filename, filepath):
	# read the datafile directory
	with os.scandir(filepath) as datafiles:
		# Check if the guild has a datafile
		for entry in datafiles:
			if (entry.name == str(filename)) and entry.is_file():
				return True
		return False


def ReadTokenFile(filename):
	# Read the token from a file
	try:
		key_file = open(filename, "r")
		token = key_file.read()
		key_file.close()
		return token
	except FileNotFoundError:
		print("No %s file found!" % filename)
		sys.exit(1)


# finally:
#	print("Error reading auth token")
#	sys.exit(1)


def main():
	# logging.basicConfig(filename='basebot.log', level=logging.ERROR)
	# logging.error('Starting Basebot')
	client = BaseballBot()
	token = ReadTokenFile('auth')

	client.run(token)


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('Stopping BaseBot')
		pass
