import discord
from discord import app_commands
import random
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def load_config():
    """Loads configuration from config.json."""
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            return json.load(f)
    else:

        default_config = {"channel_id": None, "cooldown_duration": 3600}
        with open('config.json', 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config

def save_config(data):
    """Saves configuration to config.json."""
    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)

config = load_config()
user_cooldowns = {}

# --- Credit ---
GITHUB_PROFILE = "https://github.com/AdityaLF"
SUPPORT_ME_KOFI = "https://ko-fi.com/adityaf"

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class CooldownModal(discord.ui.Modal, title="Set Message Cooldown"):
    """A Modal for setting the cooldown duration."""
    duration = discord.ui.TextInput(
        label="Cooldown Duration (in minutes)",
        placeholder="e.g., 60 for 1 hour",
        required=True,
        style=discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):
        global config
        try:
            minutes = int(self.duration.value)
            if minutes < 0:
                await interaction.response.send_message("❌ Duration cannot be negative.", ephemeral=True)
                return
            
            config['cooldown_duration'] = minutes * 60
            save_config(config)
            await interaction.response.send_message(f"✅ Cooldown has been set to **{minutes} minutes**.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Please enter a valid number for minutes.", ephemeral=True)

class ChannelSelectView(discord.ui.View):
    """A View with a channel selector dropdown."""
    def __init__(self):
        super().__init__(timeout=180)

        self.select_menu = discord.ui.ChannelSelect(
            placeholder="Select a channel to send messages to...",
            channel_types=[discord.ChannelType.text]
        )

        self.select_menu.callback = self.select_callback

        self.add_item(self.select_menu)

    async def select_callback(self, interaction: discord.Interaction):
        """This function is called when a user selects a channel."""
        global config
        # Get the selected channel from the values attribute
        selected_channel = self.select_menu.values[0]
        
        config['channel_id'] = selected_channel.id
        save_config(config)
        await interaction.response.send_message(f"✅ Secret messages will now be sent to {selected_channel.mention}.", ephemeral=True)
        self.stop() 

class SetupView(discord.ui.View):
    """The main view for the /setup command with three buttons."""
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Set Channel", style=discord.ButtonStyle.success, emoji="🔧")
    async def set_channel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(view=ChannelSelectView(), ephemeral=True)

    @discord.ui.button(label="Set Cooldown", style=discord.ButtonStyle.danger, emoji="⏱️")
    async def set_cooldown_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CooldownModal())

    @discord.ui.button(label="Info & Help", style=discord.ButtonStyle.primary, emoji="📜")
    async def info_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Information & Help",
            description="Here's some important information and useful links for you",
            color=discord.Color.blue()
        )
        embed.add_field(name="GitHub Profile", value=f"[AdityaLF]({GITHUB_PROFILE})", inline=False)
        embed.add_field(name="Support Me", value=f"[Buy Me a Coffee]({SUPPORT_ME_KOFI})", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

# --- SLASH COMMAND DEFINITION ---

@tree.command(name="setup", description="Configure the secret message bot.")
@app_commands.checks.has_permissions(administrator=True)
async def setup_command(interaction: discord.Interaction):
    """Displays the setup panel for the bot."""
    embed = discord.Embed(
        title="⚙️ Secret Message Bot Setup",
        description="Use the buttons below to configure the bot for this server.",
        color=0x2F3136
    )
    channel_id = config.get('channel_id')
    cooldown = config.get('cooldown_duration', 3600) // 60

    channel_text = f"<#{channel_id}>" if channel_id else "Not set"
    cooldown_text = f"{cooldown} minutes"

    embed.add_field(name="Current Channel", value=channel_text, inline=False)
    embed.add_field(name="Current Cooldown", value=cooldown_text, inline=False)

    await interaction.response.send_message(embed=embed, view=SetupView(), ephemeral=True)

@setup_command.error
async def on_setup_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Error handler for the /setup command."""
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ You must be an administrator to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"An unexpected error occurred: {error}", ephemeral=True)

@client.event
async def on_ready():
    """Event that runs when the bot is ready."""
    await tree.sync()
    print(f'Bot has logged in as {client.user}')
    print(f'Successfully synced {len(await tree.fetch_commands())} application commands.')
    print('------------------------------------')
    await client.change_presence(activity=discord.Game(name="Receiving Secret Messages | DM me!"))

@client.event
async def on_message(message: discord.Message):
    """Event that runs on every message."""
    if message.author.bot or not isinstance(message.channel, discord.DMChannel):
        return

    # Check if a channel has been set up
    target_channel_id = config.get('channel_id')
    if not target_channel_id:
        await message.author.send("Sorry, the bot has not been configured by a server administrator yet.")
        return

    # Cooldown Check
    cooldown_duration = config.get('cooldown_duration', 3600)
    current_time = time.time()
    if message.author.id in user_cooldowns:
        end_time = user_cooldowns[message.author.id]
        if current_time < end_time:
            remaining = round(end_time - current_time)
            minutes, seconds = divmod(remaining, 60)
            await message.author.send(f"❌ You are on cooldown. Please wait **{minutes}m {seconds}s**.")
            return

    # Attachment/Link Check
    if message.attachments or "http://" in message.content or "https://" in message.content:
        rejection_embed = discord.Embed(
            title="❌ Message Rejected",
            description="Your message was not sent because it contains a link or an attachment. Please send **text only**.",
            color=discord.Color.red()
        )
        await message.author.send(embed=rejection_embed)
        return

    # Process and send the message
    target_channel = client.get_channel(target_channel_id)
    if target_channel:
        try:
            server_embed = discord.Embed(description=message.content, color=random.randint(0, 0xFFFFFF))
            server_embed.set_author(name="Secret Message")
            await target_channel.send(embed=server_embed)

            confirmation_embed = discord.Embed(title="✅ Message Sent Successfully!", color=discord.Color.green())
            confirmation_embed.set_footer(text="~No one will ever know it was you.")
            await message.author.send(embed=confirmation_embed)

            # Set cooldown after successful send
            user_cooldowns[message.author.id] = time.time() + cooldown_duration
        except discord.Forbidden:
            print(f"Error: Bot lacks permissions for channel {target_channel_id}.")
        except Exception as e:
            print(f"An unexpected error occurred in on_message: {e}")

client.run(BOT_TOKEN)