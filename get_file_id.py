import os
import config
import asyncio
import logging
from aiogram import Bot

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN) 


