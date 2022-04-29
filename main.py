import os
import sys
import chat
import asyncio

chat_discord_channel_id = 0  # Put your channel id or it will not work
bot_token = 'your token here'
path_to_plugins = './plugins'
version = '1'
server_motd = 'Pi-SMP S1'  # needed for correct chat handling
bot_motd = 'on Pi SMP'  # in discord: Playing <bot_motd>


def list_plugins():
    global plugins
    print(f'{Fore.MAGENTA}{Style.NORMAL}Plugins:{Fore.BLUE}{Style.BRIGHT}')
    for plugin in plugins:
        print(plugin.name)
    print()


def list_commands():
    global commands
    print(f'{Fore.MAGENTA}{Style.NORMAL}Commands:{Fore.BLUE}{Style.BRIGHT}')
    for command in commands:
        print(command)
    print()


try:
    from mcpi import minecraft
except ImportError:
    print('Discord library not found. Installing.')
    os.system('sudo pip3 install mcpi')
    from mcpi import minecraft


try:
    import discord
    from discord.ext import tasks
except ImportError:
    print('Discord library not found. Installing.')
    os.system('sudo pip3 install discord')
    import discord
    from discord.ext import tasks

try:
    import colorama
    from colorama import Fore, Back, Style
except ImportError:
    print('Colorama library not found. Installing.')
    os.system('pip install colorama')
    import colorama
    from colorama import Fore, Back, Style

files = os.listdir(path_to_plugins)
plugins = []
commands = {}
player_permissions = {}
player_ips = {}

bot_online = False
permission_coloring = [f'{Fore.BLACK}{Back.YELLOW}{Style.BRIGHT}', f'{Fore.BLACK}{Back.GREEN}{Style.BRIGHT}',
                       f'{Fore.BLACK}{Back.CYAN}{Style.BRIGHT}', f'{Fore.BLACK}{Back.BLUE}{Style.NORMAL}',
                       f'{Fore.BLACK}{Back.RED}{Style.BRIGHT}']

client = discord.Client(activity=discord.Game(name=bot_motd))
os.system('clear')
log_path = input(f'{Fore.BLUE}{Style.BRIGHT}Path to latest log file:{Fore.YELLOW}')
os.system('clear')

print(f'{Style.NORMAL}{Fore.MAGENTA}Running {Style.BRIGHT}Amethyst{Style.NORMAL} backend.')
print(f'Version {Style.BRIGHT}{version}')
print(f'{Fore.YELLOW}Made by NikZapp (NikZapp#6774 on discord){Fore.RESET}{Style.NORMAL}')
print()

sys.path.insert(1, path_to_plugins)
for f in files:
    if not f.startswith('-'):
        plugin = __import__(f).Plugin
        plugins.append(plugin)
        try:
            getattr(plugin, 'setup')()
        except Exception as e:
            print(f'{Fore.RED}{Style.NORMAL}{Back.BLACK}Error in plugin {plugin.name} '
                  f'while handling setup: {e}{Fore.RESET}')
        if hasattr(plugin, 'commands'):
            import_commands = getattr(plugin, 'commands')
            for command in import_commands:
                commands[command] = import_commands[command]

list_plugins()
list_commands()

print(f'{Fore.RED}{Style.NORMAL}Connecting the {Style.BRIGHT}MCPI API', end='\r')
while True:
    try:
        mcpi_api = minecraft.Minecraft.create()
        break
    except Exception as e:
        print(e)
print(f'{Fore.GREEN}{Style.NORMAL}Connecting the {Style.BRIGHT}MCPI API')


@client.event
async def on_ready():
    print(f'{Fore.GREEN}{Style.NORMAL}Bot online as')
    print(f'{client.user.name}')
    print(f'{client.user.id}{Fore.RESET}')
    global bot_online
    bot_online = True


@client.event
async def on_message(discord_message):
    global plugins, mcpi_chat, mcpi_api
    if discord_message.channel.id == chat_discord_channel_id and discord_message.author != client.user:
        for plugin in plugins:
            if hasattr(plugin, 'on_discord'):
                await getattr(plugin, 'on_discord')(discord_message, mcpi_chat, mcpi_api, player_permissions)


# Start chat
print(f'{Fore.RED}{Style.NORMAL}Starting chat listener', end='\r')
mcpi_chat = chat.Chat(log_path)


@tasks.loop(seconds=0.5)
async def chat_updater():
    global mcpi_chat, plugins, commands, client, chat_discord_channel_id
    global player_ips, mcpi_api, bot_online, permission_coloring
    await client.wait_until_ready()

    channel = client.get_channel(chat_discord_channel_id)
    mcpi_chat.get_messages()
    while not mcpi_chat.messages.empty():
        message = mcpi_chat.messages.get()

        for plugin in plugins:
            if hasattr(plugin, 'on_raw'):
                try:
                    await getattr(plugin, 'on_raw')(message[22:], channel, mcpi_chat, mcpi_api, player_permissions)
                except Exception as e:
                    print(f'{Fore.RED}{Style.NORMAL}{Back.BLACK}Error in plugin {plugin.name} while handling on_raw: '
                          f'{e}{Fore.RESET}')

        try:
            if message[22] != '[':
                pass
            else:
                message_type = message[23:27]
                if message_type == 'INFO':
                    if ''.join(message.split()[-4:-2]) == 'HasJoined':
                        username = ' '.join(message.split()[3:-4])
                        ip = message.split()[-1][:-1]

                        player_ips[username] = ip
                        player_permissions[username] = -1  # Plugins are responsible for changing that

                        for plugin in plugins:
                            if hasattr(plugin, 'on_join'):
                                try:
                                    await getattr(plugin, 'on_join')(username, ip, channel, mcpi_chat, mcpi_api,
                                                                     player_permissions)
                                except Exception as e:
                                    print(f'{Fore.RED}{Style.NORMAL}{Back.BLACK}Error in plugin {plugin.name} while '
                                          f'handling on_join: {e}{Fore.RESET}')
                        print(f'{permission_coloring[player_permissions[username]]}+ {username}'
                              f'{Fore.RESET}{Back.RESET}'f'{Style.NORMAL}')
                elif message_type == 'CHAT':
                    # Check if it is from the bot
                    if message[30:].startswith(f'<{server_motd}> '):
                        pass
                    else:
                        is_user_message = not message.endswith('joined the game')
                        try:
                            if ''.join(message.split()[4:]) == 'disconnectedfromthegame':
                                username = ' '.join(message.split()[3:-4])
                                # !!! LOGOFF EVENT
                                for plugin in plugins:
                                    if hasattr(plugin, 'on_leave'):
                                        try:
                                            await getattr(plugin, 'on_leave')(username, player_ips[username], channel,
                                                                              mcpi_chat, mcpi_api, player_permissions)
                                        except Exception as e:
                                            print(f'{Fore.RED}{Style.NORMAL}{Back.BLACK}Error in plugin {plugin.name} '
                                                  f'while handling on_leave: {e}{Fore.RESET}')
                                print(
                                    f'{permission_coloring[player_permissions[username]]}- {username}'
                                    f'{Fore.RESET}{Back.RESET}{Style.NORMAL}')
                                player_permissions.pop(username)
                                is_user_message = False
                        except:
                            pass
                        if ''.join(message.split()[-2:]) == 'hasdied':
                            username = ' '.join(message.split()[3:-2])
                            for plugin in plugins:
                                if hasattr(plugin, 'on_death'):
                                    try:
                                        await getattr(plugin, 'on_death')(username, channel, mcpi_chat, mcpi_api,
                                                                          player_permissions)
                                    except Exception as e:
                                        print(f'{Fore.RED}{Style.NORMAL}{Back.BLACK}Error in plugin {plugin.name} '
                                              f'while handling on_death: {e}{Fore.RESET}')
                            is_user_message = False

                        if is_user_message:
                            try:
                                username = message.split()[3][1:-1]
                                user_message = message.split()[4:]
                                if user_message[0] in commands or user_message[0] == '/help':
                                    # Check permissions
                                    command = user_message[0]
                                    arguments = user_message[1:]
                                    if command == '/help':
                                        if len(arguments) == 0:
                                            for i in commands:
                                                if commands[i][1] <= player_permissions[username]:
                                                    mcpi_chat.send(f'{i} - {commands[i][2]}')
                                            mcpi_chat.send('Use /help <command> for more info.')
                                        else:
                                            for i in arguments:
                                                try:
                                                    if commands[i][1] <= player_permissions[username]:
                                                        mcpi_chat.send(f'{i} - {commands[i][2]}')
                                                    else:
                                                        mcpi_chat.send('Not enough permissions.')
                                                except:
                                                    mcpi_chat.send('Command does not exist')
                                    else:
                                        print(commands[command][1], player_permissions[username])
                                        if commands[command][1] <= player_permissions[username]:
                                            try:
                                                await commands[command][0](arguments, channel, mcpi_chat, mcpi_api,
                                                                           player_permissions)
                                            except Exception as e:
                                                mcpi_chat.send(f'Error: {e}')
                                        else:
                                            mcpi_chat.send('Not enough permissions.')
                                else:
                                    for plugin in plugins:
                                        if hasattr(plugin, 'on_chat'):
                                            try:
                                                await getattr(plugin, 'on_chat')(username, ' '.join(user_message),
                                                                                 channel,mcpi_chat, mcpi_api,
                                                                                 player_permissions)
                                            except Exception as e:
                                                print(
                                                    f'{Fore.RED}{Style.NORMAL}{Back.BLACK}Error in plugin '
                                                    f'{plugin.name} while handling on_death: {e}{Fore.RESET}')
                            except:
                                pass
        except Exception as e:
            pass  # System message/error


print(f'{Fore.GREEN}{Style.NORMAL}Starting chat listener')

print(f'{Fore.WHITE}Initialising plugin clocks:{Style.BRIGHT}')
plugin_clocks = {}
for plugin in plugins:
    if hasattr(plugin, 'process'):
        if plugin.process_interval != 0:
            print(f'{Fore.BLUE}{plugin.name} {Fore.YELLOW}{1 / plugin.process_interval}Hz')
        else:
            print(f'{Fore.BLUE}{plugin.name} {Fore.YELLOW}Always')


        async def plugin_clock(plugin, interval, client, chat, api):
            global chat_discord_channel_id, bot_online, player_permissions

            while not bot_online:
                await asyncio.sleep(1)
            channel = client.get_channel(chat_discord_channel_id)

            while interval >= 0 and hasattr(plugin, 'process'):
                await asyncio.sleep(interval)
                await plugin.process(channel, chat, api, player_permissions)


        client.loop.create_task(plugin_clock(plugin, plugin.process_interval, client, mcpi_chat, mcpi_api))
    else:
        print(f'{Fore.BLUE}{plugin.name} {Fore.YELLOW}Never')

print(f'{Fore.WHITE}{Style.NORMAL}Starting discord bot{Fore.RESET}')
chat_updater.start()
client.run(bot_token)
