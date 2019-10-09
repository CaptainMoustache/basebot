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
		#Give a buffer of 2 seconds back for play in the system time and discord time
		messageTime = messageTime - timedelta(seconds=2)
		
		#Wait defined time
		for wait in range(1, waitTime):
			if responseFound:
				break;
		
			time.sleep(1)
			#Get the last messages
			rawMessageList = await message.channel.history(limit=5).flatten()
			
			messageList = []
			
			#Prune all messages by bots and the original message
			for messages in rawMessageList:
				if messages.author.bot == False and messages != message:
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
		#Give a buffer of 2 seconds back for play in the system time and discord time
		messageTime = messageTime - timedelta(seconds=2)
	
		#Wait defined time
		for wait in range(1, waitTime):
			if responseNumber != -1:
				break;
			#Get the last messages
			rawMessageList = await message.channel.history(limit=5).flatten()
			
			messageList = []
			
			#Prune all messages by bots and the original message
			for messages in rawMessageList:
				if messages.author.bot == False and messages != message:
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
	
	async def sendGetRequest(self, url):
		try:
			#print('DEBUG: Sending HTTP request...')				
			#build the headers
			requestsHeaders = {'Content-Type': 'application/json'}
			#Send the get request
			response = requests.get(url, requestsHeaders)   
			#print('DEBUG: Response HTTP Status Code: %s' % response.status_code)
			#print('DEBUG: Response HTTP Response Body: %s' % response.content)
			return response
		except requests.exceptions.RequestException:
			print('DEBUG: HTTP Request failed')