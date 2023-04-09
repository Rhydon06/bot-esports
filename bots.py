import discord
import asyncio
import re

from Members import Members

# Discord Botのクライアント
client = discord.Client(intents=discord.Intents.all())

# 学籍番号の正規表現
pattern = r'\d{2}[a-z]{2}\d{3}'

# 学籍番号保存
file_path = "members.json"
members = Members(file_path)


@client.event
async def on_ready():
    print('Logged on as', client.user.name)


@client.event
async def on_message(message):
    # メッセージがbotからなら無視
    if message.author.bot:
        return

    # メッセージに[check]ときたら処理開始
    if message.content == 'check':
        await message.channel.send('番号を入力してください 例:21ec999')
        try:
            # ユーザーの入力を30秒以内に待機
            msg = await client.wait_for(
                'message', timeout=30.0,
                check=lambda m: m.author == message.author and m.channel == message.channel
            )
            number = msg.content  # 入力を取得
            if re.match(pattern, number):  # 入力が正しい番号の形式かチェック
                if number in members.read_members():
                    await message.channel.send('あなたはe-sports同好会に参加しています。こちらのURLから同好会のdiscordに参加してください \nhttps://discord.gg/r8tCaWcWTG ')
                else:
                    await message.channel.send('あなたはe-sports同好会に参加していません。参加する場合は役員に一言声をかけてください。')
            else:
                await message.channel.send('正しい番号の形式で入力してください。例:学科番号が小文字でない')

        except asyncio.TimeoutError:
            await message.channel.send('タイムアウトしました。もう一度コマンドを入力してください。')

    if message.content == 'register':  # メッセージに[register]ときたら処理開始
        await message.channel.send('番号を入力してください 例:21ec999')
        try:
            # ユーザーの入力を30秒以内に待機
            msg = await client.wait_for(
                'message', timeout=30.0,
                check=lambda m: m.author == message.author and m.channel == message.channel
            )
            number = msg.content  # 入力を取得
            
            if re.match(pattern, number):  # 入力が正しい番号の形式かチェック
                if number in members.read_members():  # 入力された番号がリストに存在するかチェック
                    if members.read_members()[number] == "":     # すでにIDが登録されていないかチェック
                        new_id = {number: message.author.id}            # ユーザー情報を辞書に追加
                        members.add_member(new_id)
                        await message.channel.send('discordのユーザーIDを登録しました。別アカウントを使ってオンライン活動に参加する場合は役員にお問い合わせください。')
                    else:
                        await message.channel.send('既に登録されています\ndiscordのアカウントを変更する場合は運営にお声掛け下さい。')
                else:
                    # ユーザー情報を辞書に追加
                    new_id = {number: message.author.id}
                    members.add_member(new_id)
            else:
                await message.channel.send('正しい番号の形式で入力してください。')
        except asyncio.TimeoutError:
            await message.channel.send('タイムアウトしました。もう一度コマンドを入力してください。')


@client.event
async def on_member_remove(member):  # メンバーがサーバーから退出した場合に辞書から削除
    if member.id in member.read_members:
        del member.read_members[member.id]

client.run(
    'DISCORD_TOKEN')
