# Amethyst
MCPI plugin system for servers  
CURRENTLY UNDER A MAJOR REWORK.  

# Setup
1. Logging  
- For Amethyst to work you must pipe the server output into a logging command like `tee`.  
- You should also add a timestamp to the logs, using a command like `ts`.  
- The formatting for `ts` MUST be this:  
```ts '[%Y-%m-%d %H:%M:%S]'```  
- While a chat message should look like this:  
```[2022-02-02 12:34:56] [CHAT]: <Player> Example message```  
- The server should not have colored output.  
2. Discord bot  
- Every Amethyst instance must have a Discord bot. (Will be optional in later releases)  
- To set up a bot, make one on the Discord developer portal, copy the token and paste it into the beginning of `main.py`  
- Then, enable developer mode in Discord, right click the channel you want to use with Amethyst, copy the ID and paste it in the beginning of `main.py`  
- You will also need to choose a status for the bot. It will show up as **Playing** <insert status here> in Discord.
3. MCPI  
- The server MOTD must be specified in the beginning of `main.py`.  
- If this is not done, a feedback loop of messages will appear.  
- The server MOTD **can** have spaces in it.  
- Any player joining **cannot** have spaces in their username.
4. Plugin directory
- While the defaut one is `./plugins`, you can specify a different one.  
5. Dependencies  
- Amethyst automatically installs the needed libraries: `colorama`, `discord` and of course `mcpi`
  
# Launching
After you have completed the setup, you can launch Amethyst by going in its directory and, while using the terminal, type `python3 main.py`.  
You will need to specify the path to the latest log file.


# TODO
> Make the Discord bot optional  
> Add a separate configuration file  
> Add a CLI for setting up the configuration file  
> Add proxy support for low-level plugins  
> Add plugin development documentation  
> Upload the actual code.  
> Explain reasoning behind banning spaces in usernames.  
