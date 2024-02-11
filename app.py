from config import DISCORD_BOT_TOKEN
from jainy_bot import JainyBot

if __name__ == '__main__':
    bot = JainyBot()
    bot.run(DISCORD_BOT_TOKEN)

