import aiohttp
import discord
from discord.ext import commands

from deep_core.link_guard import find_first_link
from deep_core.settings_box import settings

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=settings.COMMAND_PREFIX,
    intents=intents,
)


@bot.event
async def on_ready():
    print(f"Deep_bot is online as {bot.user}")


@bot.command(name="deep")
async def deep_download(ctx: commands.Context, *, message_text: str = ""):
    video_url = find_first_link(message_text)

    if video_url is None:
        await ctx.reply("Please send a video link like this: `!deep https://example.com/video`")
        return

    status_message = await ctx.reply("Deep_bot started the download. Please wait...")

    try:
        timeout = aiohttp.ClientTimeout(total=900)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{settings.API_BASE_URL}/fetch",
                json={"url": video_url},
            ) as response:

                if response.status != 200:
                    error_text = await response.text()
                    await status_message.edit(
                        content=f"Deep_bot could not download this video.\n```{error_text[:1500]}```"
                    )
                    return

                data = await response.json()

        download_button = discord.ui.View()
        download_button.add_item(
            discord.ui.Button(
                label="View video",
                url=data["temporary_link"]
            )
        )

        await status_message.edit(
            content=(
                "**Deep_bot finished the download.**\n"
                f"**Title:** {data['title']}\n"
                f"**File:** `{data['file_name']}`\n"
                f"This link expires in {data['expires_seconds']} seconds."
            ),
            view=download_button
        )

    except Exception as error:
        await status_message.edit(
            content=f"Deep_bot had an error:\n```{str(error)[:1500]}```"
        )


if not settings.DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing in the .env file.")

bot.run(settings.DISCORD_TOKEN)