from speedtest import Speedtest
import logging
from ..functions.Human_Format import human_readable_bytes

torlog = logging.getLogger(__name__)

async def get_speed(message):
    imspd = await message.reply("`Running speedtest...`")
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result['share'])
    string_speed = f'''
⚡𝗦𝗽𝗲𝗲𝗱𝘁𝗲𝘀𝘁 𝗥𝗲𝘀𝘂𝗹𝘁𝘀:-
• 𝗦𝗲𝗿𝘃𝗲𝗿 𝗡𝗮𝗺𝗲: `{result["server"]["name"]}`
• 𝗖𝗼𝘂𝗻𝘁𝗿𝘆: `{result["server"]["country"]}, {result["server"]["cc"]}`
• 𝗦𝗽𝗼𝗻𝘀𝗼𝗿: `{result["server"]["sponsor"]}`
• 𝗨𝗽𝗹𝗼𝗮𝗱: `{human_readable_bytes(result["upload"] / 8)}/s`
• 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱: `{human_readable_bytes(result["download"] / 8)}/s`
• 𝗣𝗶𝗻𝗴: `{result["ping"]} ms`
• 𝗜𝗦𝗣: `{result["client"]["isp"]}`
'''
    await imspd.delete()
    await message.reply(string_speed, parse_mode="markdown")
    torlog.info(f'Server Speed result:-\nDL: {human_readable_bytes(result["download"] / 8)}/s UL: {human_readable_bytes(result["upload"] / 8)}/s')
