
import os
import time
import sqlighter
import config
import asyncio
import logging
import aiogram
from aiogram import Bot, Dispatcher, executor, types

sql = sqlighter.SQLighter('db.db') #init dataBase

logging.basicConfig(level=logging.INFO)

#init BOT annd Dispatcher
bot = Bot(token=config.API_TOKEN) 
dp = Dispatcher(bot)


def S_rep(s):
	s = s.replace(' ' , '')
	s = s.replace(chr(10) , '')
	s = s.replace(chr(13) , '')
	s = s.lower()
	return s
	

def g_answ(fil):
	r = ''
	if '_llru_' in fil :
		r += 'Русский язык '

	if '12_' in fil :
		r += 'БАК'

	r += ' 20' + fil[-6 : -4] + ' ('

	
	if '_es' in fil :
		r += 'Teste pentru exersare'
	elif '_pr' in fil :
		r += 'Pretestare'
	elif '_sb' in fil :
		r += 'Sesiunea de baza'
	elif '_ss' in fil :
		r += 'Sesiunea suplimentara'

	r += ' , '

	if ('_r_' in fil) or ('_real_' in fil):
		r += 'real'
	elif ('_u_' in fil) or ('_uman_' in fil):
		r += 'uman'

	if '_test1_' in fil :
		r += ' , n1'
	elif '_test2_' in fil :
		r += ' , n2'
	r += ')'
	return r

def g_test(fil):
	r = 'тест : ' + fil[:-4].replace('-' , '/').replace('+' , ':')
	return r

def g_barem(t):
	r = 'барем : '
	return r + t[7:].replace('test' , 'barem')


	

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

	await message.answer(config.welc_t)
	await message.answer(config.welc_t_1)




@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):

	await message.answer(config.help_t , parse_mode = 'HTML')



@dp.message_handler()
async def m_func(message: types.Message):
	t = message.text

	if (t.strip()[0] == '*') and (t.strip()[-1] == '*') :
		await message.answer(config.r_t)
		await bot.send_message(chat_id = config.id_chat_admin , text = message.text + ' --- ' + str(message.from_user.mention))
	else:
		t = S_rep(t)
		
		b = True

		for file in os.listdir(config.folder_txts):

			with open(config.folder_txts + '/' + file , encoding='utf-8') as f:
				s = f.read()
				s = S_rep(s)
			
				if t in s:
		
					await message.answer(g_answ(file))

					#sending test
					test = file.replace('.txt' , '.pdf')
					if sql.get_test_file_id(test) == None:
						d = open('tests/' + test , 'rb')
						msg = await message.answer_document(d , caption = 'тест')
						sql.write_test_file_id(test , msg.document.file_id)
					else:
						try:
							await message.answer_document(sql.get_test_file_id(test) , caption = 'тест')
						except Exception: 
							d = open('tests/' + test , 'rb')
							msg = await message.answer_document(d , caption = 'тест')
							sql.write_test_file_id(test , msg.document.file_id)

					#sending barem
					barem = test.replace('test' , 'barem')
					if sql.get_barem_file_id(barem) == None:
						d = open('barems/' + barem , 'rb')
						msg = await message.answer_document(d , caption = 'барем')
						sql.write_barem_file_id(barem , msg.document.file_id)
					else:
						try:
							await message.answer_document(sql.get_test_file_id(barem) , caption = 'барем')
						except Exception: 
							d = open('barems/' + barem , 'rb')
							msg = await message.answer_document(d , caption = 'барем')
							sql.write_barem_file_id(barem , msg.document.file_id)

					b = False
					time.sleep(1)


		if b :
			await message.answer(config.no_result_t)

	





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
