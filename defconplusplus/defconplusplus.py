import os

import discord
from redbot.core import Config, checks, commands


class DefconPlusPlus(commands.Cog):

    """Server DEFCON Levels"""

    default_global_settings = {
        # Yes this is weird, but lower defcon == higher threat
        # NO ITS NOT THIS IS AMERICA USA USA USA USA USA USA USA USA USA USA USA USA USA USA USA USA USA USA USA USA USA
        "max_defcon": 5,
        "min_defcon": 1
    }

    default_guild_settings = {
        "defcon": 5,
        "authority": "none",
        "channel": None
    }

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=6942000)
        self.conf.register_global(
            **self.default_global_settings
        )
        self.conf.register_guild(
            **self.default_guild_settings
        )

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.guild_only()
    @commands.command(name="defcon")
    async def checkdefcon(self, ctx):
        """Check on Phi Discord Sigma's current Academic DEFCON level."""
        guild = ctx.message.guild
        # channel = ctx.message.channel
        level = await self.conf.guild(guild).defcon()
        await ctx.send("The current Summer 2022 DEFCON level is:\n\n**DEFCON __{}__**.".format(level))

    @commands.guild_only()
    @commands.command(name="postdefconstatus")
    async def postdefcon(self, ctx):
        """Announce Phi Discord Sigma's current Academic DEFCON level."""
        guild = ctx.message.guild
        channel = ctx.message.channel
        await self._post_defcon(ctx, guild, channel)

    @commands.guild_only()
    @commands.command(name="defcon+")
    async def defconplus(self, ctx):
        """Elevate & Announce Phi Discord Sigma's Academic DEFCON level."""
        guild = ctx.message.guild
        channel = ctx.message.channel
        member = ctx.message.author
        level = await self.conf.guild(guild).defcon()
        if level == await self.conf.max_defcon():
            await ctx.send("chilllll we are at DEFCON 5 bro lolol")
            return
        else:
            await self.conf.guild(guild).defcon.set(level + 1)
        await self.conf.guild(guild).authority.set(member.display_name)
        await self._post_defcon(ctx, guild, channel)

    @commands.guild_only()
    @commands.command(name="defcon-")
    async def defconminus(self, ctx):
        """Lower & Announce Phi Discord Sigma's Academic DEFCON level."""
        guild = ctx.message.guild
        channel = ctx.message.channel
        member = ctx.message.author
        level = await self.conf.guild(guild).defcon()
        if level == await self.conf.min_defcon():
            await ctx.send("We are already at minimum DEFCON lmao")
            return
        else:
            await self.conf.guild(guild).defcon.set(level - 1)
        await self.conf.guild(guild).authority.set(member.display_name)
        await self._post_defcon(ctx, guild, channel)

    @commands.guild_only()
    @commands.command(name="setdefcon")
    async def setdefcon(self, ctx, level: int):
        """Manually Set & Announce Phi Discord Sigma's Academic DEFCON level - in case of emergencies."""
        guild = ctx.message.guild
        channel = ctx.message.channel
        member = ctx.message.author
        if await self.conf.min_defcon() <= level <= await self.conf.max_defcon():
            await self.conf.guild(guild).defcon.set(level)
            await self.conf.guild(guild).authority.set(member.display_name)
            await self._post_defcon(ctx, guild, channel)
        else:
            await ctx.send("Not a valid DEFCON level bruh")

    @commands.guild_only()
    @commands.command(name="defconchan")
    @checks.mod()
    async def defconchan(self, ctx, channel: discord.TextChannel = None):
        """Set the Channel for the Academic DEFCON alerts to a specific channel.
        Omit the channel argument to clear the setting."""
        me = ctx.me
        author = ctx.author
        guild = ctx.guild
        if channel is None:
            await self.conf.guild(guild).channel.set(None)
            await ctx.send("Phi Discord Sigma's Academic channel setting cleared.")
            return

        if not channel.permissions_for(author).send_messages:
            await ctx.send("You're not allowed to send messages in that channel.")
            return
        elif not channel.permissions_for(me).send_messages:
            await ctx.send("I'm not allowed to send messaages in that channel.")
            return

        await self.conf.guild(guild).channel.set(channel.id)
        await ctx.send("Phi Discord Sigma's Academic DEFCON channel set to **{}**.".format(channel.name))

    async def _post_defcon(self, ctx, guild, channel):

        level = await self.conf.guild(guild).defcon()
        nick = await self.conf.guild(guild).authority()

        icon_url = 'https://i.imgur.com/MfDcOEU.gif'

        if level == 5:
            color = 0x0080ff
            thumbnail_url = 'https://i.imgur.com/ynitQlf.gif'
            author = "Summer 2022 Term is at DEFCON LEVEL {}.".format(level)
            subtitle = ("No known threats to your GPA or PSU grades "
                        "exist at this time.")
            instructions = ("- Relaxing & Enjoying the peace before the exams is encouraged.\n"
                            "- Remain vigilant of sneaky Canvas guerrilla assignment-warfare.\n"
                            "- Report all sussy behavior.")
        elif level == 4:
            color = 0x00ff00
            thumbnail_url = 'https://i.imgur.com/sRhQekI.gif'
            author = "Summer 2022 Term is at DEFCON LEVEL {}.".format(level)
            subtitle = 'Academic threats have been detected to be near or soon.'
            instructions = ("! Follow Your 'G.N.C.':\n"
                            "-> G - Your PSU Google Calendar.\n"
                            "-> N - Your Notifications.\n"
                            "-> C - Your Canvas Calendar.")
        elif level == 3:
            color = 0xffff00
            thumbnail_url = 'https://i.imgur.com/xY9SkkA.gif'
            author = "Summer 2022 Term is at DEFCON LEVEL {}.".format(level)
            subtitle = 'Academic threats have been detected to be imminent.'
            instructions = ("! Use extreme caution if procrastinating at this time.\n"
                            "! Check your PSU Email,"
                            " Canvas & Google Calendars regularly.\n"
                            "! Avoid sleep deprivation or"
                            " excessive recreational activities.\n"
                            "! Maintain self-esteem & your willpower"
                            " for maximum academic success.")
        elif level == 2:
            color = 0xff0000
            thumbnail_url = 'https://i.imgur.com/cSzezRE.gif'
            author = "Summer 2022 Term is at DEFCON LEVEL {}.".format(level)
            subtitle = 'Prepare for War. Brace For Academic Self-Esteem Impact.'
            instructions = ("!! Immediately start pre-planning"
                            " for upcoming projects & exams.\n"
                            "!! Ready your stress-relief methods"
                            " for self-esteem recovery & motivational energy crashes.\n"
                            "!! Maximize study-collaborations"
                            " with your fellow classmates ASAP as appropriate.")
        elif level == 1:
            color = 0xffffff
            thumbnail_url = 'https://i.imgur.com/NVB1AFA.gif'
            author = "Summer 2022 Term is at DEFCON LEVEL {}.".format(level)
            subtitle = 'Finals Week. Let\'s get this fucking bread.'
            instructions = ("!!! Good luck, fellow students.\n"
                            "!!! Remember: If you give it your all...\n"
                            "...that's all that matters.")
        else:
            # Better error handling?
            return

        embed = discord.Embed(title="\u2063", color=color)
        embed.set_author(name=author, icon_url=icon_url)
        embed.set_thumbnail(url=thumbnail_url)
        embed.add_field(name=subtitle, value=instructions, inline=False)
        embed.set_footer(text="Authority: {}".format(nick))

        set_channel = self.bot.get_channel(await self.conf.guild(guild).channel())
        if set_channel is None:
            await channel.send(embed=embed)
        else:
            if channel != set_channel:
                # catvibe = "<:cat_foh_da_clout:936976381181579295>"
                # salute = "<:salute:936976381205865984>"
                await ctx.send("👍 its done chief. 😉")
            await set_channel.send(embed=embed)
