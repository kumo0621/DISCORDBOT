import os
import socket
import discord
from discord.ext import commands
import threading

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

token = os.environ["DISCORD_TOKEN"]
HOST = '0.0.0.0'
PORT = 38244

def bot_start():
    bot.run(token)

def socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('サーバが起動しました。接続を待機しています。by nana')
        while True:
            conn, addr = s.accept()
            print('Javaクライアントが接続しました。アドレス:', addr)
            messages = [] # 新しくリストを定義する
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print('Javaからのメッセージ:', data.decode('UTF-8'))
                user_input = data.decode('UTF-8')
                send_discord_message(user_input)
            conn.close()
            print('Javaクライアントとの接続を閉じました。')

def send_discord_message(message):
    target_channel_id = 1126060676989849712
    target_channel = bot.get_channel(target_channel_id)

    if target_channel is not None:
        bot.loop.create_task(target_channel.send(message))

bot_thread = threading.Thread(target=bot_start)
socket_thread = threading.Thread(target=socket_server)

bot_thread.start()
socket_thread.start()

bot_thread.join()
socket_thread.join()
