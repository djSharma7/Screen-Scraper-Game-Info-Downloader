from os import path

class Game_Database():

	def __init__(self,file_name,logger):
		self.logger= logger
		if file_name:
			self.game_db_file_name = file_name
			if path.exists(file_name):
				return
			with open(file_name,'w') as d:
				d.close()
		else:
			with open('Database_File.txt','w') as d:
				d.close()
			self.game_db_file_name='Database_File.txt'


	def write_into_db(self,content):
		try:

			with open(self.game_db_file_name,'r') as rd:
				current_db_state = rd.read()
				rd.close()
			if not current_db_state :
				current_db_state = ''
			current_db_state = '{}\n{}'.format(current_db_state,content)
			with open(self.game_db_file_name,'w') as wr:
				wr.write(current_db_state)
				wr.close()
			return True
		except Exception as ee:
			self.logger.error("Exception write_into_db - {}".format(ee))
			return False

	def check_into_db(self,content):
		try:
			games_list = []
			with open(self.game_db_file_name,'r') as d:
				games_list = d.read()
				games_list = games_list.split('\n')
			d.close()
			if str(content) in games_list:
				return True
			return False
		except Exception as ee:
			self.logger.error("Exception check_into_db - {}".format(ee))
			return False
