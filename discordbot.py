import re
import textwrap
import discord
import asyncio
import random
import os

client = discord.Client()
token = os.environ['DISCORD_BOT_TOKEN']

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=',help | debug mode'))

    # or, for watching:
    activity = discord.Activity(name=',help | debug mode', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)

    channel = client.get_channel(680727914614095903)
    await channel.send('>>> **Normal Bot**が起動しました。')


@client.event
async def on_message(message):

    # Bot自身が送ったメッセージの場合は処理しない
    if message.author.bot:
        return

    # Helpコマンド
    if message.content == ',help':

        # ヘルプのメッセージを作成（ヒアドキュメントを使って視覚的に見やすくしました）
        help_msg = textwrap.dedent('''\
            **__Normal Bot__** **Help Menu**
            > `,create name`  チャンネルを作ることができます
            > `,updata`  最新のアップデータ情報を確認することができます
            > `,alldelete`実行されたチャンネルのメッセージをすべて削除します。**管理者権限必須**            
            > `,help`  このHelpMenuです。
            
        ''')

        await message.channel.send(help_msg)


    # Createコマンド
    CREATE_COMMAND = ",create "
    if message.content.startswith(CREATE_COMMAND):

        # 「,create abcdef GHI」というメッセージから「abcdef GHI」のみを取り出す
        ch_name = re.sub(CREATE_COMMAND, "", message.content)

        # Discordではチャンネル名にスペースが使えないため、ハイフンに置き換える
        ch_name = re.sub("\\s+", "-", ch_name)

        # 取り出した結果が無ければ終了
        if len(ch_name) < 1:
            return

        category = client.get_channel(605885674628841476)
        ch = await category.create_text_channel(name=ch_name)
        await message.channel.send(f"{ch.mention} を作成しました。")

    # Create単体helpコマンド
    if message.content == ',create':
        await message.channel.send('`,create name` と入力することでチャンネルを作ることができます')

    # updataコマンド
    if message.content == ',updata':
        await message.channel.send('**v1.2 Updata** \n以下のコマンドを追加しました\n>>>  `,alldel`そのチャンネルのすべてのメッセージを削除します。**管理者権限必須**')

    # alldeleteコマンド 
    if message.content == ',alldel':
        if message.author.guild_permissions.administrator:
            await message.channel.purge()
            await message.channel.send('> このチャンネルのすべてのメッセージを削除しました。')
        else:
            await message.channel.send('> あなたはこのコマンドを実行する権限がありません！')

    #運営募集コマンド
    # news
    if message.content == ',news':
        

        # bosyuのメッセージを作成（ヒアドキュメントを使って視覚的に見やすくしました）
        bosyu_msg = textwrap.dedent('''\
            **__Wakame NetWork News__** 
            
            >>>公式Wikiサイトを作りました！
            こちらからアクセスできます！

            ``http://bid.do/wikinet``

            <@&605725636241129482>
            
        ''')
        if message.author.guild_permissions.administrator:
            await message.channel.send(bosyu_msg)
        else:
            await message.channel.send('> あなたはこのコマンドを実行する権限がありません！')


    
    if message.content == ',kudel':
        if message.author.guild_permissions.administrator:
            await message.channel.send('> <@514349162519592963> のメッセージを削除しました。>')
        else:
            await message.channel.send('> あなたはこのコマンドを実行する権限がありません！')

client.run(token)
