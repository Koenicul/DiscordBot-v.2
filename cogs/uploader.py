from discord.ext import tasks, commands
import scrapetube
import db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db.engine)
session = Session()

class Uploader(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.checkforvideos.start(bot)

    @tasks.loop(seconds=30)
    async def checkforvideos(self, bot):
        await bot.wait_until_ready()
        channels = session.query(db.Channels).all()
        for youtube_channel in channels:
            videos = scrapetube.get_channel(str(youtube_channel.channel_id))
            videos_ids = []
            for video in videos:
                id = (video['videoId'])
                videos_ids.append(id)
            latest_video = "https://www.youtube.com/watch?v=" + videos_ids[0]
            if not youtube_channel.latest_video_url == latest_video:
                youtube_channel.latest_video_url = latest_video
                channel = bot.get_channel(youtube_channel.discord_channel_id)
                session.commit()
                await channel.send(f"@everyone {youtube_channel.channel_name} Just Uploaded A Video Or He is Live Go Check It Out: {youtube_channel.latest_video_url}")
    
    @commands.command(name="AddChannel", help="Add a youtube channel to the list of channels to be checked")
    async def AddChannel(self, ctx, channel_name: str, channel_id: str, discord_channel_id: int):
        exists = session.query(db.Channels).filter(db.Channels.channel_id == channel_id).first()
        if exists is None:
            channel = db.Channels(channel_name, channel_id, discord_channel_id, None)
            session.add(channel)
            session.commit()
            await ctx.send(f"Added {channel_name} to the list of channels to be checked")
        else:
            await ctx.send(f"{channel_name} is already on the list of channels to be checked")

    @commands.command(name="RemoveChannel", help="Remove a youtube channel from the list of channels to be checked")
    async def RemoveChannel(self, ctx, channel_id: str):
        exists = session.query(db.Channels).filter(db.Channels.channel_id == channel_id).first()
        if exists is not None:
            session.delete(exists)
            session.commit()
            await ctx.send(f"Removed {exists.channel_name} from the list of channels to be checked")
        else:
            await ctx.send(f"{channel_id} is not on the list of channels to be checked")

def setup(bot):
    bot.add_cog(Uploader(bot))