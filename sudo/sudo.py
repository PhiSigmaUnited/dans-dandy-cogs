import os

import discord
from redbot.core import Config, checks, commands


class Sudo(commands.Cog):

    default_global_settings = {
        "sudo1": 0,
        "sudo2": 0,
        "sudoer": 0
    }

    default_guild_settings = {
        "root": "none",
        "log_channel": None
    }

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=6942001)
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
    @commands.command(name="sudo")
    async def sudo(self, ctx):
        """sudo (default: 2 hours)"""
        guild = ctx.message.guild
        channel = ctx.message.channel
        await self._post_sudo(ctx, guild, channel)