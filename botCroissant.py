import asyncio
import datetime

import discord
import pytz

class botCroissant(discord.Bot):
    def __init__(self, message_file_path):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.paris_tz = pytz.timezone("Europe/Paris")

        self.message_file_path = message_file_path
        self.load_messages_from_file()

    def restart_loop(self):
        self.need_to_restart_loop = True
        self.sleep_task.cancel()

    def load_messages_from_file(self, message_file_path=None):
        """Load messages from a file."""
        if message_file_path is None:
            message_file_path = self.message_file_path
        self.messages = []
        with open(message_file_path, "r") as file:
            for line in file:
                timecode, channel_id, message, guild_id = line.split("-SEPARATOR-")
                message = message.replace("\\n", "\n")
                self.messages.append((timecode, channel_id, message, guild_id.rstrip("\n")))
                print(line + "loaded")


    def write_messages_to_file(self, file_path=None):
        """Write messages to a file."""
        if file_path is None:
            file_path = self.message_file_path
        with open(file_path, "w") as file:
            for timecode, channel_id, message, guild_id in self.messages:
                message = message.replace("\\n", "\n")
                message = message.replace("\n", "\\n")
                file.write(
                    f"{timecode}-SEPARATOR-{channel_id}-SEPARATOR-{message}-SEPARATOR-{guild_id}\n"
                )


    async def send_messages_on_schedule(self):
        while True:
            self.need_to_restart_loop = False
            for timecode, channel_id, message, guild_id in self.messages:
                if self.need_to_restart_loop:
                    break
                if len(timecode) == 5:
                    dt = datetime.datetime.strptime(timecode, "%H:%M")
                elif len(timecode) == 8:
                    dt = datetime.datetime.strptime(timecode, "%H:%M:%S")
                else:
                    print(f"Invalid timecode: {timecode}")
                dt_now = datetime.datetime.now(self.paris_tz)
                dt = dt.replace(year=dt_now.year, month=dt_now.month, day=dt_now.day)
                dt = self.paris_tz.localize(dt)
                time_to_wait = (dt - datetime.datetime.now(self.paris_tz)).total_seconds()
                print(f"Time to wait: {time_to_wait}, dt: {dt}, now: {dt_now}")
                if time_to_wait <= 0 and time_to_wait >= -10:
                    channel = self.get_channel(int(channel_id))
                    await channel.send(message)
                elif time_to_wait > 0:
                    self.sleep_task = asyncio.create_task(asyncio.sleep(time_to_wait))
                    await asyncio.wait([self.sleep_task], return_when=asyncio.FIRST_COMPLETED)
                    channel = self.get_channel(int(channel_id))
                    await channel.send(message)
            time_until_midnight = datetime.datetime.now(self.paris_tz).replace(
                hour=23, minute=59, second=59, microsecond=999999
            ) - datetime.datetime.now(self.paris_tz)
            self.sleep_task = asyncio.create_task(asyncio.sleep(time_until_midnight.total_seconds()))
            await asyncio.wait([self.sleep_task], return_when=asyncio.FIRST_COMPLETED)
                
    def check_channel_in_guild(self, channel_id: int, guild_id: int):
        guild = self.get_guild(guild_id)
        if guild is None:
            return False
        channel = guild.get_channel(channel_id)
        return channel is not None


    async def reload_messages(self, interaction):
        if interaction.user.id != 227849368504369152:
            return
        self.load_messages_from_file()
        await interaction.response.send_message("Messages reloaded.")

    async def list_messages(self, interaction):  # Defines a new "context" (interaction) command called "list."
        embed = discord.Embed(title="Message List", color=discord.Color.blue())
        messages_temp = [message for message in self.messages if message[3] == str(interaction.guild.id)]
        i = 1
        for timecode, channel_id, message, guild_id in messages_temp:
            embed.add_field(name="Timecode", value=timecode, inline=True)
            embed.add_field(name="Message", value=message, inline=True)
            embed.add_field(name="Channel", value=f"<#{channel_id}>", inline=True)
            i += 1
        await interaction.response.send_message(embed=embed)

    async def remove_message(self, interaction, message_id: int):
        required_role = discord.utils.get(interaction.guild.roles, name="staff")
        if required_role not in interaction.user.roles:
            await interaction.response.send_message(
                "You do not have permission to use this command."
            )
            return
        try:
            messages_temp = [
                message for message in self.messages if message[3] == str(interaction.guild.id)
            ]
            index = int(message_id) - 1
            if index < 0 or index >= len(messages_temp):
                await interaction.response.send_message("Invalid message ID.")
            else:
                message_to_delete = messages_temp[index]
                self.messages.remove(message_to_delete)
                await interaction.response.send_message(f"Message with ID {message_id} removed.")
                self.restart_loop()
        except ValueError:
            await interaction.response.send_message("Invalid message ID.")

    async def add_message(self, interaction, timecode: str, channel_id: str, message: str):
        global messages
        required_role = discord.utils.get(interaction.guild.roles, name="staff")
        if required_role not in interaction.user.roles:
            await interaction.response.send_message(
                "You do not have permission to use this command."
            )
            return
        if not self.check_channel_in_guild(int(channel_id), int(interaction.guild.id)):
            await interaction.response.send_message("Invalid channel ID.")
            return
        message = message.replace("\\n", "\n")
        self.messages.append((timecode, channel_id, message, interaction.guild.id))
        await interaction.response.send_message(f"Message added to list.")
        self.messages = sorted(self.messages, key=lambda x: x[0])
        self.restart_loop()
        self.write_messages_to_file(self.message_file_path)


