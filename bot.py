import os

from dotenv import load_dotenv

from botCroissant import botCroissant

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
MESSAGE_FILE = "messages.txt"

if TOKEN is None:
    raise ValueError("Token is not set in the environment variables.")

bot = botCroissant(MESSAGE_FILE)
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.send_messages_on_schedule()

@bot.command(
    name="list",
    description="List programmed messages",
)
async def list(ctx):
    await bot.list_messages(ctx)

@bot.command(
    name="reload_messages",
    description="Reload messages from file",
)
async def reload_messages(ctx):
    await bot.reload_messages(ctx)

@bot.command(
    name="remove",
    description="Remove a message",
)
async def remove_message(ctx, message_id: int):
    await bot.remove_message(ctx, message_id)

@bot.command(
    name="add",
    description="Add a message",
)
async def add_message(ctx, timecode: str, channel_id: str, message: str):
    await bot.add_message(ctx, timecode, channel_id, message)

bot.run(TOKEN)
