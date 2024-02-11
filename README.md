# Jainy Bot

## Requirements
* Python 3.12+
* Discord Account
* Bot Account (see below for details on how to setup)
* Docker and Docker Compose

## How to get started
### Discord Bot Account Setup
1. Go to [discord](https://discord.com/developers/applications) and make an application for bot
2. In application page click OAuth -> URL Generator and check the box for `bot`
3. Copy the link generated and paste into web browser to invite bot to your discord server
4. Go to bot page in discord, and reset your token (make sure to copy and paste this somewhere 
or you will have to reset token again)

### Setting up your environment
1. Use virtualenv to setup a python 3.12 environment or if you want you can use native python 3.12 from system
2. Run `pip install -r requirements.txt` from this directory to install dependencies

### Setting up Python Secrets and Bot Config
1. Create a `.env` file in this directory and set the following variables
```bash
DISCORD_BOT_TOKEN=<YOUR TOKEN FROM BEFORE HERE>
LOG_LEVEL=DEBUG
```
2. Source the env file you created and run the `app.py`