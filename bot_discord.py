import discord
import os
from discord import Intents
import psycopg2

# PostgreSQLに接続するための情報
host = 'localhost'
port = 38244
database = 'postgres'
user = 'test'
password = "test"

token = os.environ["DISCORD_TOKEN"]

intents = Intents.default()
intents.typing = False  # タイピングイベントを無効にする
intents.presences = False  # プレゼンスイベントを無効にする
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

#データベースに接続
def postgresql_handler(host, port, database, user, password, name, member_value):
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    cur = conn.cursor()

    def execute_query(query, *args):
        cur.execute(query, args)
        conn.commit()

    def close_connection():
        cur.close()
        conn.close()
        
    #データベース削除
    #query = "DROP TABLE IF EXISTS achievement_table"
    #execute_query(query)

    # PostgreSQLに接続して処理を実行する例
    execute_query('''
        CREATE TABLE IF NOT EXISTS achievement_table (
            number SERIAL PRIMARY KEY,
            id BIGINT,
            name VARCHAR(255),
            set VARCHAR(255)
        )
    ''')
#データベースに入力する値
    query = "INSERT INTO achievement_table (id, name, set) VALUES (%s, %s, %s)"
    set = "初めて一週間"
    args = (member_value, name, set)
    execute_query(query, *args)
    conn.commit()
    execute_query("SELECT * FROM achievement_table")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    close_connection()


#起動メッセージ
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    # メッセージを送信するチャンネルを指定する
    target_channel = await client.fetch_channel("1126060676989849712")  # 特定のチャンネルのID（CHANNEL_ID）を指定する

    if target_channel is not None:
        await target_channel.send('ボットが起動しました！')  # メッセージを送信する

#リアクションの反応に対してロールを付与する
@client.event
async def on_raw_reaction_add(payload):
    #if payload.message_id == "1126141547776311326":
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        member = await guild.fetch_member(payload.user_id)
        role = discord.utils.get(guild.roles, id=1126173114800279613)
        if member is not None:
            await member.add_roles(role)
            name = "初心者"
            member_value = payload.user_id
            postgresql_handler(host, port, database, user, password, name, member_value)
        else: print("error")
    #else: print("erro2r")

#サーバーに参加したときの初めての実績付与
@client.event
async def on_member_join(member):
    print("join")
    guild_id = member.guild.id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    role = discord.utils.get(guild.roles, id=1126453426931388447)
    if role is not None:
        #await member.add_roles(role)
        name = "初めまして"
        member_value = member.id
        postgresql_handler(host, port, database, user, password, name, member_value)
    else:
        print("Error: Role not found")
#else: print("erro2r")
client.run(token)