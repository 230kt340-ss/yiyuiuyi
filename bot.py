import discord
from discord.ext import commands

TOKEN = "MTQ1OTY5NDU0NTM4NTE2NDkzNQ.GtcFjk.Un5rV3pHOKs8tUoXaEjEsGHOUaxC14ZHNwNkaw"

VERIFY_ROLE_ID = 1166394284723937280   # Zweryfikowany
REMOVE_ROLE_ID = 1459263454362996820    # Niezweryfikowany

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="✅ Zweryfikuj się",
        style=discord.ButtonStyle.success,
        custom_id="verify_button"
    )
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            guild = interaction.guild
            member = interaction.user

            verify_role = guild.get_role(VERIFY_ROLE_ID)
            remove_role = guild.get_role(REMOVE_ROLE_ID)

            if verify_role is None:
                await interaction.response.send_message(
                    "❌ Nie znaleziono roli weryfikacyjnej.",
                    ephemeral=True
                )
                return

            if verify_role in member.roles:
                await interaction.response.send_message(
                    "ℹ️ Jesteś już zweryfikowany.",
                    ephemeral=True
                )
                return

            await member.add_roles(verify_role, reason="Weryfikacja")

            if remove_role and remove_role in member.roles:
                await member.remove_roles(remove_role, reason="Weryfikacja")

            await interaction.response.send_message(
                "✅ Weryfikacja zakończona pomyślnie!",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Bot nie ma uprawnień do zarządzania rolami.",
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                "❌ Wystąpił błąd podczas weryfikacji.",
                ephemeral=True
            )
            print(e)


@bot.event
async def on_ready():
    bot.add_view(VerifyView())
    print(f"Zalogowano jako {bot.user}")


@bot.command()
@commands.has_permissions(administrator=True)
async def weryfikacja(ctx):
    embed = discord.Embed(
        title="Weryfikacja",
        description="Kliknij przycisk poniżej, aby się zweryfikować.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, view=VerifyView())


bot.run(TOKEN)