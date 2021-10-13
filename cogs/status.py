from collections import Counter, defaultdict

import discord
from discord.ext import commands


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            description="Shows a list of connected accounts.",
            color=0x00FF00,
        )

        user_information = defaultdict(lambda: [])

        for response in self.bot.cache.values():
            if response:
                user_information[response.receiver].append(response)

        embed.add_field(
            name=f"Main Account {self.bot.user.id}",
            value=f"Tag: {self.bot.user}\nAPI Calls: {len(user_information[self.bot.user])}",
            inline=False,
        )

        for alt in self.bot.alts:
            embed.add_field(
                name=f"Alt Account {alt.user.id}",
                value=f"Tag: {alt.user}\nAPI Calls: {len(user_information[alt.user])}",
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
