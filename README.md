# Amethyst
MCPI plugin system for servers

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
- You must have the MCPI library installed, and the server MOTD must be specified in the beginning of `main.py`.  
- If this is not done, a feedback loop of messages will appear.

# TODO
> Finish this README  
> Make the Discord bot optional  
> Add a separate configuration file  
> Add a CLI for setting up the configuration file  
> Upload the actual code.
