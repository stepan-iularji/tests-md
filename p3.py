import os

l = os.listdir('buf/')

for i in l:
	if 'test' in i:
		os.rename("buf/" + i , "tests/" + i)
	elif 'barem' in i:
		os.rename("buf/" + i , "barems/" + i)