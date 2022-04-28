from discord.ext import tasks
import json
import scrapetube

@tasks.loop(seconds=30)
async def checkforvideos(ctx):
    with open("channels.json", "r") as f:
        data=json.load(f)
    for youtube_channel in data:
        videos = scrapetube.get_channel(youtube_channel)
        videos_ids = []
        for video in videos:
            id = (video['videoId'])
            videos_ids.append(id)
        latest_video = "https://www.youtube.com/watch?v=" + videos_ids[0]
        if not str(data[youtube_channel]["latest_video_url"]) == latest_video:
            data[str(youtube_channel)]['latest_video_url'] = latest_video
            discord_channel_id = data[str(youtube_channel)]['notifying_discord_channel']
            discord_channel = ctx.get_channel(int(discord_channel_id))
            with open("channels.json", "w") as f:
                json.dump(data, f)
            await discord_channel.send(f"@everyone {data[str(youtube_channel)]['channel_name']} Just Uploaded A Video Or He is Live Go Check It Out: {data[str(youtube_channel)]['latest_video_url']}")

def setup(bot):
    checkforvideos.start(bot)