import string

class Plugin:
    name = 'Chat Bridge'
    version = '1.1'
    author = 'NikZapp'
    
    def setup():
        pass
    
    async def on_discord(message, chat, api, players):
        for i in message.content:
            if i not in string.printable[:-5]:
                embed = discord.Embed(title="Invalid character!", color=0xf9330e)
                embed.set_footer(text=f'Unable to send `{i}`')
                await message.channel.send(embed=embed)
                return
        chat.send(f'[{str(message.author)[:-5]}] {message.content}')
    
    async def on_chat(username, message, channel, chat, api, players):
        await channel.send(f'{username}: {message}')
    
    async def on_join(username, ip, channel, chat, api, players):
        await channel.send(f'''
```diff
+ {username}
```''')

    async def on_leave(username, ip, channel, chat, api, players):
        await channel.send(f'''
```diff
- {username}
```''') 
    
    async def on_death(username, channel, chat, api, players):
        await channel.send(f'''
```
{username} died
```''')
