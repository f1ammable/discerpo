import aiohttp
import aiofiles
from pathlib import Path

async def download(url, filename):
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            if r.status == 200:
                f = await aiofiles.open(f'{filename}', mode='wb')
                await f.write(await r.read())
                await f.close()
    return Path(str(filename)).absolute() 


