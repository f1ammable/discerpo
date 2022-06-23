import aiohttp
import aiofiles
from pathlib import Path


__all__ = (
    "getSession",
    "download"
)


async def getSession(bot):  # Don't create new aiohttp.Clientsession() everytime
    if bot.session is None:
        bot.session = aiohttp.ClientSession()
    return bot.session


async def download(url, filename, bot):  # Downloading files
    async with await getSession(bot) as s:
        async with s.get(url) as r:
            if r.status == 200:
                f = await aiofiles.open(f'{filename}', mode='wb')
                await f.write(await r.read())
                await f.close()
                return Path(str(filename)).absolute()
            else:
                return "Invalid url provided"
