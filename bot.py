import discord
from discord.ext import commands
from discord import app_commands
import os
TOKEN = "MTUxNTgwNjk3NzkyMDMzNTg3Mg.GSe027.hmEpNPmYEcF9rp_JFnrr2oXP-902kTr52TUoj0"
WEBHOOK_NAME = "Gaultier"
WEBHOOK_AVATAR = "https://cdn.discordapp.com/attachments/1513659487343476928/1515814998969155705/EA1CA7CE-2E38-42AC-A2D8-E41F309D09AD.png?ex=6a30603a&is=6a2f0eba&hm=6a1d916d14bb012266725a13857145a3e27d59ad3dc3f64ca1d601dbaf2e4558"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


class EmbedModal(discord.ui.Modal, title="Create Embed"):
    title_input = discord.ui.TextInput(label="Title", required=False, max_length=256)
    desc_input = discord.ui.TextInput(label="Description", style=discord.TextStyle.paragraph, required=True, max_length=4000)
    color_input = discord.ui.TextInput(label="Color Hex", placeholder="#ff0000", required=False, max_length=7)
    image_input = discord.ui.TextInput(label="Image URL", placeholder="https://image.png", required=False)
    footer_input = discord.ui.TextInput(label="Footer", required=False, max_length=2048)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            color = discord.Color(int((self.color_input.value or "#ff0000").replace("#", ""), 16))
        except:
            color = discord.Color.red()

        embed = discord.Embed(
            title=self.title_input.value,
            description=self.desc_input.value,
            color=color
        )

        if self.image_input.value:
            embed.set_image(url=self.image_input.value)

        if self.footer_input.value:
            embed.set_footer(text=self.footer_input.value)

        await interaction.response.send_message(
            content="Embed Preview",
            embed=embed,
            view=EmbedView(embed),
            ephemeral=True
        )


class EditModal(discord.ui.Modal, title="Edit Embed"):
    title_input = discord.ui.TextInput(label="New Title", required=False)
    desc_input = discord.ui.TextInput(label="New Description", style=discord.TextStyle.paragraph, required=False)

    def __init__(self, embed):
        super().__init__()
        self.embed = embed

    async def on_submit(self, interaction: discord.Interaction):
        if self.title_input.value:
            self.embed.title = self.title_input.value

        if self.desc_input.value:
            self.embed.description = self.desc_input.value

        await interaction.response.edit_message(
            content="Embed Preview",
            embed=self.embed,
            view=EmbedView(self.embed)
        )


class EmbedView(discord.ui.View):
    def __init__(self, embed):
        super().__init__(timeout=None)
        self.embed = embed

    @discord.ui.button(label="Send", style=discord.ButtonStyle.green)
    async def send_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            webhook = await interaction.channel.create_webhook(name=WEBHOOK_NAME)

            await webhook.send(
                embed=self.embed,
                username=WEBHOOK_NAME,
                avatar_url=WEBHOOK_AVATAR
            )

            await webhook.delete()

            await interaction.response.edit_message(
                content="Embed sent.",
                embed=None,
                view=None
            )

        except Exception as e:
            await interaction.response.send_message(f"Error: `{e}`", ephemeral=True)

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.blurple)
    async def edit_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EditModal(self.embed))

    @discord.ui.button(label="Delete Preview", style=discord.ButtonStyle.red)
    async def delete_preview(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content="Preview deleted.",
            embed=None,
            view=None
        )


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@app_commands.default_permissions(administrator=True)
@bot.tree.command(name="embed", description="Create a webhook embed")
async def embed(interaction: discord.Interaction):
    await interaction.response.send_modal(EmbedModal())

bot.run(TOKEN)
