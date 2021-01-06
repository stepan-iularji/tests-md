import sqlite3

class SQLighter:

	def __init__(self, database):
		"""Подключаемся к БД и сохраняем курсор соединения"""
		self.connection = sqlite3.connect(database)
		self.cursor = self.connection.cursor()

	def get_file_id(self , tab , file_name):
		with self.connection:
			try:
				return  self.cursor.execute("SELECT file_id FROM {0} WHERE file_name = ?".format(tab) , ( file_name ,)).fetchall()[0][0]
			except IndexError:
				return None

	
	def get_test_file_id(self , file_name):
		return self.get_file_id('tests' , file_name)

	def get_barem_file_id(self , file_name):
		return self.get_file_id('barems' , file_name)

	def write_file_id(self , tab , file_name , file_id):
		g = self.get_file_id(tab , file_name)
		with self.connection:
			if g == None :
				return self.cursor.execute('INSERT INTO {0} (file_name , file_id ) VALUES(? , ?)'.format(tab) , (file_name , file_id))
			elif g != file_id:
				return self.cursor.execute('UPDATE {0} SET file_id = ? WHERE file_name = ?'.format(tab) , (file_id , file_name))

	def write_test_file_id(self , file_name , file_id):
		return self.write_file_id('tests' , file_name , file_id)

	def write_barem_file_id(self , file_name , file_id):
		return self.write_file_id('barems' , file_name , file_id)
        