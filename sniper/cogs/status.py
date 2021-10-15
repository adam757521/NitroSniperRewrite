from collections import Counter, defaultdict
from typing import Dict

import discord
from discord.ext import commands

from sniper.nitro import CustomNitroResponse
from sniper.core import MainSniperBot


def format_code_list(cache: Dict[str, CustomNitroResponse], limit: int = 0) -> str:
    codes = [
        f"{code}: {response.response.server_response}"
        for code, response in cache.items()
    ]
    codes = codes[:limit] if limit else codes

    return "\n".join(reversed(codes))


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot: MainSniperBot = bot

    @commands.command()
    async def status(self, ctx, status_mode: str):
        try:
            status = discord.Status(status_mode)
        except ValueError:
            await ctx.send(f"Status '{status_mode}' is invalid.")
            return

        await self.bot.change_presence(status=status)

        await ctx.send(embed=discord.Embed(
            title=f"Status changed to '{status_mode}'",
            color=0x00ff00
        ))

    @commands.group(invoke_without_command=True)
    async def history(self, ctx, limit: int = 0):
        await ctx.send(
            embed=discord.Embed(
                title="Code History",
                description=format_code_list(self.bot.cache, limit)[:4096],
                color=0x00FF00,
            )
        )

    @history.command()
    async def user(self, ctx, user: discord.User):
        await ctx.send(
            embed=discord.Embed(
                title=f"Code History of {user}",
                description=format_code_list(
                    {
                        code: response
                        for code, response in self.bot.cache.items()
                        if response and response.message.author == user
                    }
                )[:4096],
                color=0x00FF00,
            )
        )

    @history.command()
    async def guild(self, ctx, guild: discord.Guild):
        await ctx.send(
            embed=discord.Embed(
                title=f"Code History of {guild}",
                description=format_code_list(
                    {
                        code: response
                        for code, response in self.bot.cache.items()
                        if response and response.message.guild == guild
                    }
                )[:4096],
                color=0x00FF00,
            )
        )

    @commands.command()
    async def lookup(self, ctx, code: str):
        code = code[:24]
        code_response = self.bot.cache.get(code)

        if not code_response:
            await ctx.send(f"Code {code} is not found!")
            return

        embed = discord.Embed(
            title=f"Code {code}",
            description=f"Showing code information ({code})",
            color=0x00FF00,
        )

        embed.add_field(
            name="Receiver",
            value=f"ID: {code_response.receiver.id}, Tag: {code_response.receiver}",
            inline=False,
        )

        embed.add_field(
            name="Message Information",
            value=f"Author: {code_response.message.author}, Guild: {code_response.message.guild}",
            inline=False,
        )

        embed.add_field(
            name="Ping",
            value=f"Time until API response: {round(code_response.request_time * 1000)}MS",
            inline=False,
        )

        embed.add_field(
            name="Response",
            value=f"Server Response: {code_response.response.server_response}, Nitro Type: {code_response.response.nitro_type}",
            inline=False,
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def accounts(self, ctx):
        embed = discord.Embed(
            title="Connected Accounts.",
            description=f"Shows a list of connected accounts.\nTotal guilds: {sum([len(self.bot.guilds)] + [len(alt.guilds) for alt in self.bot.alts])}",
            color=0x00FF00,
        )

        user_information = defaultdict(lambda: [])

        for response in self.bot.cache.values():
            if response:
                user_information[response.receiver].append(response)

        embed.add_field(
            name=f"Main Account {self.bot.user.id}",
            value=f"Tag: {self.bot.user}\nAPI Calls: {len(user_information[self.bot.user])}\nGuilds: {len(self.bot.guilds)}",
            inline=False,
        )

        for alt in self.bot.alts:
            embed.add_field(
                name=f"Alt Account {alt.user.id}",
                value=f"Tag: {alt.user}\nAPI Calls: {len(user_information[alt.user])}\nGuilds: {len(alt.guilds)}",
                inline=False,
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        ping_data = [
            response.request_time * 1000
            for response in self.bot.cache.values()
            if response
        ]

        if not ping_data:
            await ctx.send("No data to process!")
            return

        embed = discord.Embed(
            title="Discord API Stats.",
            color=0x00FF00,
        )

        avg = sum(ping_data) / len(ping_data)
        ping_data = f"MIN: {min(ping_data)}\nMAX: {max(ping_data)}\nAVERAGE: {avg}"
        embed.add_field(name="Ping Data", value=ping_data, inline=False)

        types = [x.response.server_response for x in self.bot.cache.values()]
        response_data = "\n".join(
            [f"{x[0]}: {x[1]}" for x in Counter(types).most_common()]
        )
        embed.add_field(name="Response Data", value=response_data, inline=False)

        embed.add_field(
            name="Total API Calls", value=str(len(self.bot.cache)), inline=False
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Status(bot))
