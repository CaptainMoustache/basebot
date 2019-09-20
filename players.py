import json

class PlayerSearchInfo():
	jsonString = ''
	totalSize = ''
	position = ''
	birth_country = ''
	weight = ''
	birth_state = ''
	name_display_first_last = ''
	college = ''
	height_inches = ''
	name_display_roster = ''
	sport_code = ''
	bats = ''
	name_first = ''
	team_code = ''
	birth_city = ''
	height_feet = ''
	pro_debut_date = ''
	team_full = ''
	team_abbrev = ''
	birth_date = ''
	throws = ''
	league = ''
	name_display_last_first = ''
	position_id = ''
	high_school = ''
	name_use = ''
	player_id = ''
	name_last = ''
	team_id = ''
	service_years = ''
	active_sw = ''
	
	#Parse out json info from the API response
	def ParseJson(self, jsonData, index):
		self.jsonString = str(jsonData)
		self.totalSize = int(jsonData['search_player_all']['queryResults']['totalSize'])
		#If there is only one player in the data
		if self.totalSize == 1:
			self.position = jsonData['search_player_all']['queryResults']['row']['position']
			self.birth_country = jsonData['search_player_all']['queryResults']['row']['birth_country']
			self.weight = jsonData['search_player_all']['queryResults']['row']['weight']
			self.birth_state = jsonData['search_player_all']['queryResults']['row']['birth_state']
			self.name_display_first_last = jsonData['search_player_all']['queryResults']['row']['name_display_first_last']
			self.college = jsonData['search_player_all']['queryResults']['row']['college']
			self.height_inches = jsonData['search_player_all']['queryResults']['row']['height_inches']
			self.name_display_roster = jsonData['search_player_all']['queryResults']['row']['name_display_roster']
			self.sport_code = jsonData['search_player_all']['queryResults']['row']['sport_code']
			self.bats = jsonData['search_player_all']['queryResults']['row']['bats']
			self.name_first = jsonData['search_player_all']['queryResults']['row']['name_first']
			self.team_code = jsonData['search_player_all']['queryResults']['row']['team_code']
			self.birth_city = jsonData['search_player_all']['queryResults']['row']['birth_city']
			self.height_feet = jsonData['search_player_all']['queryResults']['row']['height_feet']
			self.pro_debut_date = jsonData['search_player_all']['queryResults']['row']['pro_debut_date']
			self.team_full = jsonData['search_player_all']['queryResults']['row']['team_full']
			self.team_abbrev = jsonData['search_player_all']['queryResults']['row']['team_abbrev']
			self.birth_date = jsonData['search_player_all']['queryResults']['row']['birth_date']
			self.throws = jsonData['search_player_all']['queryResults']['row']['throws']
			self.league = jsonData['search_player_all']['queryResults']['row']['league']
			self.name_display_last_first = jsonData['search_player_all']['queryResults']['row']['name_display_last_first']
			self.position_id = jsonData['search_player_all']['queryResults']['row']['position_id']
			self.high_school = jsonData['search_player_all']['queryResults']['row']['high_school']
			self.name_use = jsonData['search_player_all']['queryResults']['row']['name_use']
			self.player_id = jsonData['search_player_all']['queryResults']['row']['player_id']
			self.name_last = jsonData['search_player_all']['queryResults']['row']['name_last']
			self.team_id = jsonData['search_player_all']['queryResults']['row']['team_id']
			self.service_years = jsonData['search_player_all']['queryResults']['row']['service_years']
			self.active_sw = jsonData['search_player_all']['queryResults']['row']['active_sw']
		#If there are multiple players in the data then reference the correct index
		elif self.totalSize > 1:
			self.position = jsonData['search_player_all']['queryResults']['row'][int(index)]['position']
			self.birth_country = jsonData['search_player_all']['queryResults']['row'][int(index)]['birth_country']
			self.weight = jsonData['search_player_all']['queryResults']['row'][int(index)]['weight']
			self.birth_state = jsonData['search_player_all']['queryResults']['row'][int(index)]['birth_state']
			self.name_display_first_last = jsonData['search_player_all']['queryResults']['row'][int(index)]['name_display_first_last']
			self.college = jsonData['search_player_all']['queryResults']['row'][int(index)]['college']
			self.height_inches = jsonData['search_player_all']['queryResults']['row'][int(index)]['height_inches']
			self.name_display_roster = jsonData['search_player_all']['queryResults']['row'][int(index)]['name_display_roster']
			self.sport_code = jsonData['search_player_all']['queryResults']['row'][int(index)]['sport_code']
			self.bats = jsonData['search_player_all']['queryResults']['row'][int(index)]['bats']
			self.name_first = jsonData['search_player_all']['queryResults']['row'][int(index)]['name_first']
			self.team_code = jsonData['search_player_all']['queryResults']['row'][int(index)]['team_code']
			self.birth_city = jsonData['search_player_all']['queryResults']['row'][int(index)]['birth_city']
			self.height_feet = jsonData['search_player_all']['queryResults']['row'][int(index)]['height_feet']
			self.pro_debut_date = jsonData['search_player_all']['queryResults']['row'][int(index)]['pro_debut_date']
			self.team_full = jsonData['search_player_all']['queryResults']['row'][int(index)]['team_full']
			self.team_abbrev = jsonData['search_player_all']['queryResults']['row'][int(index)]['team_abbrev']
			self.birth_date = jsonData['search_player_all']['queryResults']['row'][int(index)]['birth_date']
			self.throws = jsonData['search_player_all']['queryResults']['row'][int(index)]['throws']
			self.league = jsonData['search_player_all']['queryResults']['row'][int(index)]['league']
			self.name_display_last_first = jsonData['search_player_all']['queryResults']['row'][int(index)]['name_display_last_first']
			self.position_id = jsonData['search_player_all']['queryResults']['row'][int(index)]['position_id']
			self.high_school = jsonData['search_player_all']['queryResults']['row'][int(index)]['high_school']
			self.name_use = jsonData['search_player_all']['queryResults']['row'][int(index)]['name_use']
			self.player_id = jsonData['search_player_all']['queryResults']['row'][int(index)]['player_id']
			self.name_last = jsonData['search_player_all']['queryResults']['row'][int(index)]['name_last']
			self.team_id = jsonData['search_player_all']['queryResults']['row'][int(index)]['team_id']
			self.service_years = jsonData['search_player_all']['queryResults']['row'][int(index)]['service_years']
			self.active_sw = jsonData['search_player_all']['queryResults']['row'][int(index)]['active_sw']
		#Error condition
		else:
			self.position = 'N/A'
			self.birth_country = 'N/A'
			self.weight = 'N/A'
			self.birth_state = 'N/A'
			self.name_display_first_last = 'N/A'
			self.college = 'N/A'
			self.height_inches = 'N/A'
			self.name_display_roster = 'N/A'
			self.sport_code = 'N/A'
			self.bats = 'N/A'
			self.name_first = 'N/A'
			self.team_code = 'N/A'
			self.birth_city = 'N/A'
			self.height_feet = 'N/A'
			self.pro_debut_date = 'N/A'
			self.team_full = 'N/A'
			self.team_abbrev = 'N/A'
			self.birth_date = 'N/A'
			self.throws = 'N/A'
			self.league = 'N/A'
			self.name_display_last_first = 'N/A'
			self.position_id = 'N/A'
			self.high_school = 'N/A'
			self.name_use = 'N/A'
			self.player_id = 'N/A'
			self.name_last = 'N/A'
			self.team_id = 'N/A'
			self.service_years = 'N/A'
			self.active_sw = 'N/A'
			
class PlayerInfo():
	jsonString = ''
	totalSize = ''
	birth_country = ''
	name_prefix = ''
	name_display_first_last = ''
	college = ''
	height_inches = ''
	death_country = ''
	age = ''
	name_display_first_last_html = ''
	gender = ''
	height_feet = ''
	pro_debut_date = ''
	death_date = ''
	primary_position = ''
	birth_date = ''
	team_abbrev = ''
	status = ''
	name_display_last_first_html = ''
	throws = ''
	death_city = ''
	primary_position_txt = ''
	high_school = ''
	name_display_roster_html = ''
	name_use = ''
	player_id = ''
	status_date = ''
	primary_stat_type = ''
	team_id = ''
	active_sw = ''
	primary_sport_code = ''
	birth_state = ''
	weight = ''
	name_middle = ''
	name_display_roster = ''
	end_date = ''
	jersey_number = ''
	death_state = ''
	name_first = ''
	bats = ''
	team_code = ''
	birth_city = ''
	name_nick = ''
	status_code = ''
	name_matrilineal = ''
	team_name = ''
	name_display_last_first = ''
	twitter_id = ''
	name_title = ''
	file_code = ''
	name_last = ''
	start_date = ''
	name_full = ''
	#Parse out json info from the API response
	def ParseJson(self, jsonData):
		self.jsonString = str(jsonData)
		self.totalSize = int(jsonData['player_info']['queryResults']['totalSize'])
		#If there is only one player in the data
		if self.totalSize == 1:
			self.birth_country = jsonData['player_info']['queryResults']['row']['birth_country']
			self.name_prefix = jsonData['player_info']['queryResults']['row']['name_prefix']
			self.name_display_first_last = jsonData['player_info']['queryResults']['row']['name_display_first_last']
			self.college = jsonData['player_info']['queryResults']['row']['college']
			self.height_inches = jsonData['player_info']['queryResults']['row']['height_inches']
			self.death_country = jsonData['player_info']['queryResults']['row']['death_country']
			self.age = jsonData['player_info']['queryResults']['row']['age']
			self.name_display_first_last_html = jsonData['player_info']['queryResults']['row']['name_display_first_last_html']
			self.gender = jsonData['player_info']['queryResults']['row']['gender']
			self.height_feet = jsonData['player_info']['queryResults']['row']['height_feet']
			self.pro_debut_date = jsonData['player_info']['queryResults']['row']['pro_debut_date']
			self.death_date = jsonData['player_info']['queryResults']['row']['death_date']
			self.primary_position = jsonData['player_info']['queryResults']['row']['primary_position']
			self.birth_date = jsonData['player_info']['queryResults']['row']['birth_date']
			self.team_abbrev = jsonData['player_info']['queryResults']['row']['team_abbrev']
			self.status = jsonData['player_info']['queryResults']['row']['status']
			self.name_display_last_first_html = jsonData['player_info']['queryResults']['row']['name_display_last_first_html']
			self.throws = jsonData['player_info']['queryResults']['row']['throws']
			self.death_city = jsonData['player_info']['queryResults']['row']['death_city']
			self.primary_position_txt = jsonData['player_info']['queryResults']['row']['primary_position_txt']
			self.high_school = jsonData['player_info']['queryResults']['row']['high_school']
			self.name_display_roster_html = jsonData['player_info']['queryResults']['row']['name_display_roster_html']
			self.name_use = jsonData['player_info']['queryResults']['row']['name_use']
			self.player_id = jsonData['player_info']['queryResults']['row']['player_id']
			self.status_date = jsonData['player_info']['queryResults']['row']['status_date']
			self.primary_stat_type = jsonData['player_info']['queryResults']['row']['primary_stat_type']
			self.team_id = jsonData['player_info']['queryResults']['row']['team_id']
			self.active_sw = jsonData['player_info']['queryResults']['row']['active_sw']
			self.primary_sport_code = jsonData['player_info']['queryResults']['row']['primary_sport_code']
			self.birth_state = jsonData['player_info']['queryResults']['row']['birth_state']
			self.weight = jsonData['player_info']['queryResults']['row']['weight']
			self.name_middle = jsonData['player_info']['queryResults']['row']['name_middle']
			self.name_display_roster = jsonData['player_info']['queryResults']['row']['name_display_roster']
			self.end_date = jsonData['player_info']['queryResults']['row']['end_date']
			self.jersey_number = jsonData['player_info']['queryResults']['row']['jersey_number']
			self.death_state = jsonData['player_info']['queryResults']['row']['death_state']
			self.name_first = jsonData['player_info']['queryResults']['row']['name_first']
			self.bats = jsonData['player_info']['queryResults']['row']['bats']
			self.team_code = jsonData['player_info']['queryResults']['row']['team_code']
			self.birth_city = jsonData['player_info']['queryResults']['row']['birth_city']
			self.name_nick = jsonData['player_info']['queryResults']['row']['name_nick']
			self.status_code = jsonData['player_info']['queryResults']['row']['status_code']
			self.name_matrilineal = jsonData['player_info']['queryResults']['row']['name_matrilineal']
			self.team_name = jsonData['player_info']['queryResults']['row']['team_name']
			self.name_display_last_first = jsonData['player_info']['queryResults']['row']['name_display_last_first']
			self.twitter_id = jsonData['player_info']['queryResults']['row']['twitter_id']
			self.name_title = jsonData['player_info']['queryResults']['row']['name_title']
			self.file_code = jsonData['player_info']['queryResults']['row']['file_code']
			self.name_last = jsonData['player_info']['queryResults']['row']['name_last']
			self.start_date = jsonData['player_info']['queryResults']['row']['start_date']
			self.name_full = jsonData['player_info']['queryResults']['row']['name_full']
		#Error condition
		else:
			self.birth_country = 'N/A'
			self.name_prefix = 'N/A'
			self.name_display_first_last = 'N/A'
			self.college = 'N/A'
			self.height_inches = 'N/A'
			self.death_country = 'N/A'
			self.age = 'N/A'
			self.name_display_first_last_html = 'N/A'
			self.gender = 'N/A'
			self.height_feet = 'N/A'
			self.pro_debut_date = 'N/A'
			self.death_date = 'N/A'
			self.primary_position = 'N/A'
			self.birth_date = 'N/A'
			self.team_abbrev = 'N/A'
			self.status = 'N/A'
			self.name_display_last_first_html = 'N/A'
			self.throws = 'N/A'
			self.death_city = 'N/A'
			self.primary_position_txt = 'N/A'
			self.high_school = 'N/A'
			self.name_display_roster_html = 'N/A'
			self.name_use = 'N/A'
			self.player_id = 'N/A'
			self.status_date = 'N/A'
			self.primary_stat_type = 'N/A'
			self.team_id = 'N/A'
			self.active_sw = 'N/A'
			self.primary_sport_code = 'N/A'
			self.birth_state = 'N/A'
			self.weight = 'N/A'
			self.name_middle = 'N/A'
			self.name_display_roster = 'N/A'
			self.end_date = 'N/A'
			self.jersey_number = 'N/A'
			self.death_state = 'N/A'
			self.name_first = 'N/A'
			self.bats = 'N/A'
			self.team_code = 'N/A'
			self.birth_city = 'N/A'
			self.name_nick = 'N/A'
			self.status_code = 'N/A'
			self.name_matrilineal = 'N/A'
			self.team_name = 'N/A'
			self.name_display_last_first = 'N/A'
			self.twitter_id = 'N/A'
			self.name_title = 'N/A'
			self.file_code = 'N/A'
			self.name_last = 'N/A'
			self.start_date = 'N/A'
			self.name_full = 'N/A'
			
class SeasonBattingStats():
	jsonString = ''
	totalSize = ''
	gidp = ''
	sac = ''
	np = ''
	sport_code = ''
	hgnd = ''
	tb = ''
	gidp_opp = ''
	sport_id = ''
	bb = ''
	avg = ''
	slg = ''
	team_full = ''
	ops = ''
	hbp = ''
	league_full = ''
	team_abbrev = ''
	so = ''
	hfly = ''
	wo = ''
	league_id = ''
	sf = ''
	team_seq = ''
	league = ''
	hpop = ''
	cs = ''
	season = ''
	sb = ''
	go_ao = ''
	ppa = ''
	player_id = ''
	ibb = ''
	team_id = ''
	go = ''
	hr = ''
	rbi = ''
	babip = ''
	lob = ''
	end_date = ''
	xbh = ''
	league_short = ''
	g = ''
	d = ''
	sport = ''
	team_short = ''
	tpa = ''
	h = ''
	obp = ''
	hldr = ''
	t = ''
	ao = ''
	r = ''
	ab = ''
	#Parse out json info from the API response
	def ParseJson(self, jsonData):
		self.jsonString = str(jsonData)
		self.totalSize = int(jsonData['sport_hitting_tm']['queryResults']['totalSize'])
		#If there is only one player in the data
		if self.totalSize == 1:
			self.gidp = jsonData['sport_hitting_tm']['queryResults']['row']['gidp']
			self.sac = jsonData['sport_hitting_tm']['queryResults']['row']['sac']
			self.np = jsonData['sport_hitting_tm']['queryResults']['row']['np']
			self.sport_code = jsonData['sport_hitting_tm']['queryResults']['row']['sport_code']
			self.hgnd = jsonData['sport_hitting_tm']['queryResults']['row']['hgnd']
			self.tb = jsonData['sport_hitting_tm']['queryResults']['row']['tb']
			self.gidp_opp = jsonData['sport_hitting_tm']['queryResults']['row']['gidp_opp']
			self.sport_id = jsonData['sport_hitting_tm']['queryResults']['row']['sport_id']
			self.bb = jsonData['sport_hitting_tm']['queryResults']['row']['bb']
			self.avg = jsonData['sport_hitting_tm']['queryResults']['row']['avg']
			self.slg = jsonData['sport_hitting_tm']['queryResults']['row']['slg']
			self.team_full = jsonData['sport_hitting_tm']['queryResults']['row']['team_full']
			self.ops = jsonData['sport_hitting_tm']['queryResults']['row']['ops']
			self.hbp = jsonData['sport_hitting_tm']['queryResults']['row']['hbp']
			self.league_full = jsonData['sport_hitting_tm']['queryResults']['row']['league_full']
			self.team_abbrev = jsonData['sport_hitting_tm']['queryResults']['row']['team_abbrev']
			self.so = jsonData['sport_hitting_tm']['queryResults']['row']['so']
			self.hfly = jsonData['sport_hitting_tm']['queryResults']['row']['hfly']
			self.wo = jsonData['sport_hitting_tm']['queryResults']['row']['wo']
			self.league_id = jsonData['sport_hitting_tm']['queryResults']['row']['league_id']
			self.sf = jsonData['sport_hitting_tm']['queryResults']['row']['sf']
			self.team_seq = jsonData['sport_hitting_tm']['queryResults']['row']['team_seq']
			self.league = jsonData['sport_hitting_tm']['queryResults']['row']['league']
			self.hpop = jsonData['sport_hitting_tm']['queryResults']['row']['hpop']
			self.cs = jsonData['sport_hitting_tm']['queryResults']['row']['cs']
			self.season = jsonData['sport_hitting_tm']['queryResults']['row']['season']
			self.sb = jsonData['sport_hitting_tm']['queryResults']['row']['sb']
			self.go_ao = jsonData['sport_hitting_tm']['queryResults']['row']['go_ao']
			self.ppa = jsonData['sport_hitting_tm']['queryResults']['row']['ppa']
			self.player_id = jsonData['sport_hitting_tm']['queryResults']['row']['player_id']
			self.ibb = jsonData['sport_hitting_tm']['queryResults']['row']['ibb']
			self.team_id = jsonData['sport_hitting_tm']['queryResults']['row']['team_id']
			self.go = jsonData['sport_hitting_tm']['queryResults']['row']['go']
			self.hr = jsonData['sport_hitting_tm']['queryResults']['row']['hr']
			self.rbi = jsonData['sport_hitting_tm']['queryResults']['row']['rbi']
			self.babip = jsonData['sport_hitting_tm']['queryResults']['row']['babip']
			self.lob = jsonData['sport_hitting_tm']['queryResults']['row']['lob']
			self.end_date = jsonData['sport_hitting_tm']['queryResults']['row']['end_date']
			self.xbh = jsonData['sport_hitting_tm']['queryResults']['row']['xbh']
			self.league_short = jsonData['sport_hitting_tm']['queryResults']['row']['league_short']
			self.g = jsonData['sport_hitting_tm']['queryResults']['row']['g']
			self.d = jsonData['sport_hitting_tm']['queryResults']['row']['d']
			self.sport = jsonData['sport_hitting_tm']['queryResults']['row']['sport']
			self.team_short = jsonData['sport_hitting_tm']['queryResults']['row']['team_short']
			self.tpa = jsonData['sport_hitting_tm']['queryResults']['row']['tpa']
			self.h = jsonData['sport_hitting_tm']['queryResults']['row']['h']
			self.obp = jsonData['sport_hitting_tm']['queryResults']['row']['obp']
			self.hldr = jsonData['sport_hitting_tm']['queryResults']['row']['hldr']
			self.t = jsonData['sport_hitting_tm']['queryResults']['row']['t']
			self.ao = jsonData['sport_hitting_tm']['queryResults']['row']['ao']
			self.r = jsonData['sport_hitting_tm']['queryResults']['row']['r']
			self.ab = jsonData['sport_hitting_tm']['queryResults']['row']['ab']
		#Error condition
		else:
			self.gidp = 'N/A'
			self.sac = 'N/A'
			self.np = 'N/A'
			self.sport_code = 'N/A'
			self.hgnd = 'N/A'
			self.tb = 'N/A'
			self.gidp_opp = 'N/A'
			self.sport_id = 'N/A'
			self.bb = 'N/A'
			self.avg = 'N/A'
			self.slg = 'N/A'
			self.team_full = 'N/A'
			self.ops = 'N/A'
			self.hbp = 'N/A'
			self.league_full = 'N/A'
			self.team_abbrev = 'N/A'
			self.so = 'N/A'
			self.hfly = 'N/A'
			self.wo = 'N/A'
			self.league_id = 'N/A'
			self.sf = 'N/A'
			self.team_seq = 'N/A'
			self.league = 'N/A'
			self.hpop = 'N/A'
			self.cs = 'N/A'
			self.season = 'N/A'
			self.sb = 'N/A'
			self.go_ao = 'N/A'
			self.ppa = 'N/A'
			self.player_id = 'N/A'
			self.ibb = 'N/A'
			self.team_id = 'N/A'
			self.go = 'N/A'
			self.hr = 'N/A'
			self.rbi = 'N/A'
			self.babip = 'N/A'
			self.lob = 'N/A'
			self.end_date = 'N/A'
			self.xbh = 'N/A'
			self.league_short = 'N/A'
			self.g = 'N/A'
			self.d = 'N/A'
			self.sport = 'N/A'
			self.team_short = 'N/A'
			self.tpa = 'N/A'
			self.h = 'N/A'
			self.obp = 'N/A'
			self.hldr = 'N/A'
			self.t = 'N/A'
			self.ao = 'N/A'
			self.r = 'N/A'
			self.ab = 'N/A'

class SeasonPitchingStats():
	jsonString = ''
	totalSize = ''
	gidp = []
	h9 = []
	np = []
	tr = []
	gf = []
	sport_code = []
	bqs = []
	hgnd = []
	sho = []
	bq = []
	gidp_opp = []
	bk = []
	kbb = []
	sport_id = []
	hr9 = []
	sv = []
	slg = []
	bb = []
	whip = []
	avg = []
	ops = []
	team_full = []
	db = []
	league_full = []
	team_abbrev = []
	hfly = []
	so = []
	tbf = []
	bb9 = []
	league_id = []
	wp = []
	team_seq = []
	hpop = []
	league = []
	hb = []
	cs = []
	pgs = []
	season = []
	sb = []
	go_ao = []
	ppa = []
	cg = []
	player_id = []
	gs = []
	ibb = []
	team_id = []
	pk = []
	go = []
	hr = []
	irs = []
	wpct = []
	era = []
	babip = []
	end_date = []
	rs9 = []
	qs = []
	league_short = []
	g = []
	ir = []
	hld = []
	k9 = []
	sport = []
	team_short = []
	l = []
	svo = []
	h = []
	ip = []
	obp = []
	w = []
	hldr = []
	ao = []
	s = []
	r = []
	spct = []
	pip = []
	ab = []
	er = []
	#Parse out json info from the API response
	def ParseJson(self, jsonData):
		self.jsonString = str(jsonData)
		self.totalSize = int(jsonData['sport_pitching_tm']['queryResults']['totalSize'])
		print('DEBUG: totalSize = %s' % str(self.totalSize))
		#Loop through all returned stats
		for index in range(0, self.totalSize - 1):
			print('DEBUG: Adding index %s to pitching stats' % str(index))
			self.gidp.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['gidp'])
			self.h9.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['h9'])
			self.np.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['np'])
			self.tr.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['tr'])
			self.gf.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['gf'])
			self.sport_code.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['sport_code'])
			self.bqs.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['bqs'])
			self.hgnd.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['hgnd'])
			self.sho.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['sho'])
			self.bq.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['bq'])
			self.gidp_opp.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['gidp_opp'])
			self.bk.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['bk'])
			self.kbb.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['kbb'])
			self.sport_id.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['sport_id'])
			self.hr9.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['hr9'])
			self.sv.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['sv'])
			self.slg.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['slg'])
			self.bb.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['bb'])
			self.whip.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['whip'])
			self.avg.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['avg'])
			self.ops.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['ops'])
			self.team_full.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['team_full'])
			self.db.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['db'])
			self.league_full.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['league_full'])
			self.team_abbrev.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['team_abbrev'])
			self.hfly.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['hfly'])
			self.so.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['so'])
			self.tbf.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['tbf'])
			self.bb9.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['bb9'])
			self.league_id.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['league_id'])
			self.wp.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['wp'])
			self.team_seq.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['team_seq'])
			self.hpop.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['hpop'])
			self.league.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['league'])
			self.hb.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['hb'])
			self.cs.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['cs'])
			self.pgs.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['pgs'])
			self.season.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['season'])
			self.sb.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['sb'])
			self.go_ao.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['go_ao'])
			self.ppa.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['ppa'])
			self.cg.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['cg'])
			self.player_id.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['player_id'])
			self.gs.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['gs'])
			self.ibb.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['ibb'])
			self.team_id.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['team_id'])
			self.pk.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['pk'])
			self.go.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['go'])
			self.hr.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['hr'])
			self.irs.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['irs'])
			self.wpct.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['wpct'])
			self.era.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['era'])
			self.babip.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['babip'])
			self.end_date.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['end_date'])
			self.rs9.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['rs9'])
			self.qs.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['qs'])
			self.league_short.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['league_short'])
			self.g.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['g'])
			self.ir.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['ir'])
			self.hld.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['hld'])
			self.k9.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['k9'])
			self.sport.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['sport'])
			self.team_short.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['team_short'])
			self.l.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['l'])
			self.svo.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['svo'])
			self.h.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['h'])
			self.ip.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['ip'])
			self.obp.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['obp'])
			self.w.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['w'])
			self.hldr.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['hldr'])
			self.ao.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['ao'])
			self.s.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['s'])
			self.r.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['r'])
			self.spct.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['spct'])
			self.pip.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['pip'])
			self.ab.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['ab'])
			self.er.append(jsonData['sport_pitching_tm']['queryResults']['row'][index]['er'])
		'''
		#If there is only one player in the data
		if self.totalSize == 1:
			self.gidp = jsonData['sport_pitching_tm']['queryResults']['row']['gidp']
			self.h9 = jsonData['sport_pitching_tm']['queryResults']['row']['h9']
			self.np = jsonData['sport_pitching_tm']['queryResults']['row']['np']
			self.tr = jsonData['sport_pitching_tm']['queryResults']['row']['tr']
			self.gf = jsonData['sport_pitching_tm']['queryResults']['row']['gf']
			self.sport_code = jsonData['sport_pitching_tm']['queryResults']['row']['sport_code']
			self.bqs = jsonData['sport_pitching_tm']['queryResults']['row']['bqs']
			self.hgnd = jsonData['sport_pitching_tm']['queryResults']['row']['hgnd']
			self.sho = jsonData['sport_pitching_tm']['queryResults']['row']['sho']
			self.bq = jsonData['sport_pitching_tm']['queryResults']['row']['bq']
			self.gidp_opp = jsonData['sport_pitching_tm']['queryResults']['row']['gidp_opp']
			self.bk = jsonData['sport_pitching_tm']['queryResults']['row']['bk']
			self.kbb = jsonData['sport_pitching_tm']['queryResults']['row']['kbb']
			self.sport_id = jsonData['sport_pitching_tm']['queryResults']['row']['sport_id']
			self.hr9 = jsonData['sport_pitching_tm']['queryResults']['row']['hr9']
			self.sv = jsonData['sport_pitching_tm']['queryResults']['row']['sv']
			self.slg = jsonData['sport_pitching_tm']['queryResults']['row']['slg']
			self.bb = jsonData['sport_pitching_tm']['queryResults']['row']['bb']
			self.whip = jsonData['sport_pitching_tm']['queryResults']['row']['whip']
			self.avg = jsonData['sport_pitching_tm']['queryResults']['row']['avg']
			self.ops = jsonData['sport_pitching_tm']['queryResults']['row']['ops']
			self.team_full = jsonData['sport_pitching_tm']['queryResults']['row']['team_full']
			self.db = jsonData['sport_pitching_tm']['queryResults']['row']['db']
			self.league_full = jsonData['sport_pitching_tm']['queryResults']['row']['league_full']
			self.team_abbrev = jsonData['sport_pitching_tm']['queryResults']['row']['team_abbrev']
			self.hfly = jsonData['sport_pitching_tm']['queryResults']['row']['hfly']
			self.so = jsonData['sport_pitching_tm']['queryResults']['row']['so']
			self.tbf = jsonData['sport_pitching_tm']['queryResults']['row']['tbf']
			self.bb9 = jsonData['sport_pitching_tm']['queryResults']['row']['bb9']
			self.league_id = jsonData['sport_pitching_tm']['queryResults']['row']['league_id']
			self.wp = jsonData['sport_pitching_tm']['queryResults']['row']['wp']
			self.team_seq = jsonData['sport_pitching_tm']['queryResults']['row']['team_seq']
			self.hpop = jsonData['sport_pitching_tm']['queryResults']['row']['hpop']
			self.league = jsonData['sport_pitching_tm']['queryResults']['row']['league']
			self.hb = jsonData['sport_pitching_tm']['queryResults']['row']['hb']
			self.cs = jsonData['sport_pitching_tm']['queryResults']['row']['cs']
			self.pgs = jsonData['sport_pitching_tm']['queryResults']['row']['pgs']
			self.season = jsonData['sport_pitching_tm']['queryResults']['row']['season']
			self.sb = jsonData['sport_pitching_tm']['queryResults']['row']['sb']
			self.go_ao = jsonData['sport_pitching_tm']['queryResults']['row']['go_ao']
			self.ppa = jsonData['sport_pitching_tm']['queryResults']['row']['ppa']
			self.cg = jsonData['sport_pitching_tm']['queryResults']['row']['cg']
			self.player_id = jsonData['sport_pitching_tm']['queryResults']['row']['player_id']
			self.gs = jsonData['sport_pitching_tm']['queryResults']['row']['gs']
			self.ibb = jsonData['sport_pitching_tm']['queryResults']['row']['ibb']
			self.team_id = jsonData['sport_pitching_tm']['queryResults']['row']['team_id']
			self.pk = jsonData['sport_pitching_tm']['queryResults']['row']['pk']
			self.go = jsonData['sport_pitching_tm']['queryResults']['row']['go']
			self.hr = jsonData['sport_pitching_tm']['queryResults']['row']['hr']
			self.irs = jsonData['sport_pitching_tm']['queryResults']['row']['irs']
			self.wpct = jsonData['sport_pitching_tm']['queryResults']['row']['wpct']
			self.era = jsonData['sport_pitching_tm']['queryResults']['row']['era']
			self.babip = jsonData['sport_pitching_tm']['queryResults']['row']['babip']
			self.end_date = jsonData['sport_pitching_tm']['queryResults']['row']['end_date']
			self.rs9 = jsonData['sport_pitching_tm']['queryResults']['row']['rs9']
			self.qs = jsonData['sport_pitching_tm']['queryResults']['row']['qs']
			self.league_short = jsonData['sport_pitching_tm']['queryResults']['row']['league_short']
			self.g = jsonData['sport_pitching_tm']['queryResults']['row']['g']
			self.ir = jsonData['sport_pitching_tm']['queryResults']['row']['ir']
			self.hld = jsonData['sport_pitching_tm']['queryResults']['row']['hld']
			self.k9 = jsonData['sport_pitching_tm']['queryResults']['row']['k9']
			self.sport = jsonData['sport_pitching_tm']['queryResults']['row']['sport']
			self.team_short = jsonData['sport_pitching_tm']['queryResults']['row']['team_short']
			self.l = jsonData['sport_pitching_tm']['queryResults']['row']['l']
			self.svo = jsonData['sport_pitching_tm']['queryResults']['row']['svo']
			self.h = jsonData['sport_pitching_tm']['queryResults']['row']['h']
			self.ip = jsonData['sport_pitching_tm']['queryResults']['row']['ip']
			self.obp = jsonData['sport_pitching_tm']['queryResults']['row']['obp']
			self.w = jsonData['sport_pitching_tm']['queryResults']['row']['w']
			self.hldr = jsonData['sport_pitching_tm']['queryResults']['row']['hldr']
			self.ao = jsonData['sport_pitching_tm']['queryResults']['row']['ao']
			self.s = jsonData['sport_pitching_tm']['queryResults']['row']['s']
			self.r = jsonData['sport_pitching_tm']['queryResults']['row']['r']
			self.spct = jsonData['sport_pitching_tm']['queryResults']['row']['spct']
			self.pip = jsonData['sport_pitching_tm']['queryResults']['row']['pip']
			self.ab = jsonData['sport_pitching_tm']['queryResults']['row']['ab']
			self.er = jsonData['sport_pitching_tm']['queryResults']['row']['er']
		#Error condition
		else:
			self.gidp = 'N/A'
			self.h9 = 'N/A'
			self.np = 'N/A'
			self.tr = 'N/A'
			self.gf = 'N/A'
			self.sport_code = 'N/A'
			self.bqs = 'N/A'
			self.hgnd = 'N/A'
			self.sho = 'N/A'
			self.bq = 'N/A'
			self.gidp_opp = 'N/A'
			self.bk = 'N/A'
			self.kbb = 'N/A'
			self.sport_id = 'N/A'
			self.hr9 = 'N/A'
			self.sv = 'N/A'
			self.slg = 'N/A'
			self.bb = 'N/A'
			self.whip = 'N/A'
			self.avg = 'N/A'
			self.ops = 'N/A'
			self.team_full = 'N/A'
			self.db = 'N/A'
			self.league_full = 'N/A'
			self.team_abbrev = 'N/A'
			self.hfly = 'N/A'
			self.so = 'N/A'
			self.tbf = 'N/A'
			self.bb9 = 'N/A'
			self.league_id = 'N/A'
			self.wp = 'N/A'
			self.team_seq = 'N/A'
			self.hpop = 'N/A'
			self.league = 'N/A'
			self.hb = 'N/A'
			self.cs = 'N/A'
			self.pgs = 'N/A'
			self.season = 'N/A'
			self.sb = 'N/A'
			self.go_ao = 'N/A'
			self.ppa = 'N/A'
			self.cg = 'N/A'
			self.player_id = 'N/A'
			self.gs = 'N/A'
			self.ibb = 'N/A'
			self.team_id = 'N/A'
			self.pk = 'N/A'
			self.go = 'N/A'
			self.hr = 'N/A'
			self.irs = 'N/A'
			self.wpct = 'N/A'
			self.era = 'N/A'
			self.babip = 'N/A'
			self.end_date = 'N/A'
			self.rs9 = 'N/A'
			self.qs = 'N/A'
			self.league_short = 'N/A'
			self.g = 'N/A'
			self.ir = 'N/A'
			self.hld = 'N/A'
			self.k9 = 'N/A'
			self.sport = 'N/A'
			self.team_short = 'N/A'
			self.l = 'N/A'
			self.svo = 'N/A'
			self.h = 'N/A'
			self.ip = 'N/A'
			self.obp = 'N/A'
			self.w = 'N/A'
			self.hldr = 'N/A'
			self.ao = 'N/A'
			self.s = 'N/A'
			self.r = 'N/A'
			self.spct = 'N/A'
			self.pip = 'N/A'
			self.ab = 'N/A'
			self.er = 'N/A'
		'''
#class CareerBattingStats():
#
#class CareerPitchingStats():

