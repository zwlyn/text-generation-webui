import asyncio
import json
import sys

try:
    import websockets
except ImportError:
    print("Websockets package not found. Make sure it's installed.")

# For local streaming, the websockets are hosted without ssl - ws://
HOST = 'localhost:5005'
URI = f'ws://{HOST}/api/v1/stream'

# For reverse-proxied streaming, the remote will likely host with ssl - wss://
# URI = 'wss://your-uri-here.trycloudflare.com/api/v1/stream'


async def run(context):
    # Note: the selected defaults change from time to time.
    request = {
        'prompt': context,
        'character': 'Assistant',
        'max_new_tokens': 1500,
        'temperature': 0.7,
        'top_p': 0.9,
        'typical_p': 1,
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.15,
        'additive_repetition_penalty': 0,
        'repetition_penalty_range': 0,
        'top_k': 20,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        # 'penalty_alpha': 0,
        # 'length_penalty': 1,
        # 'early_stopping': False,
        # 'mirostat_mode': 0,
        # 'mirostat_tau': 5,
        # 'mirostat_eta': 0.1,
        # 'grammar_string': '',
        # 'guidance_scale': 1,
        # 'add_bos_token': True,
        'truncation_length': 2048,
        # 'ban_eos_token': False,
        # 'custom_token_bans': '',
        # 'skip_special_tokens': True,
        # 'stopping_strings': []
    }

    async with websockets.connect(URI, ping_interval=None) as websocket:
        await websocket.send(json.dumps(request))

        yield context  # Remove this if you just want to see the reply

        while True:
            incoming_data = await websocket.recv()
            incoming_data = json.loads(incoming_data)

            match incoming_data['event']:
                case 'text_stream':
                    yield incoming_data['text']
                case 'stream_end':
                    return


async def print_response_stream(prompt):
    async for response in run(prompt):
        print(response, end='')
        sys.stdout.flush()  # If we don't flush, we won't see tokens in realtime.


if __name__ == '__main__':
    prompt = '''Question: 请作为我的stable diffusion提示词大师级传奇顾问,帮我设计我所需要的写真的精巧、绝妙的提示词，直接告诉我生成相应写真所需的正面的提示词和反面的提示词作为输出,提示词是英文,其中正面提示词不少于20个，
    基于以上陈述，请帮我生成主题为："""阅读角落：将女性放在一个充满书籍的环境中，展现知识与智慧的魅力。"""的写真提示词，,返回格式是python的dict数据数据结构,正面提示词（positive）和反面提示词（negative）均作为dict的key，对应的value是提示词构成的数组，参考格式如下:{
"positive": ['Cyberpunk','Futuristic','Masculine','Neon Lights','Futuristic Fashion','High-Tech','Urban Landscape','Holographic','Cybernetic Enhancements','Sleek','Dystopian','Sci-Fi Chic','Virtual Reality','Futuristic Grooming','Metallic','Glowing','Exotic','Urban Explorer','Techno-Geek'],
"negative": ['Gritty','Post-Apocalyptic','Dark Alley','Urban Decay','Grimy','Broken Technology','Pollution','Surveillance','Isolation','Desolation','Cybercrime','System Failure','Dystopian Future','Ruined Cityscape','Corruption','Hackers','Underground','Chaos','Resistance']
}，严格按照示例格式直接返回，不需要其他额外的输出。
    Factual answer:'''
    asyncio.run(print_response_stream(prompt))
