import html
import json

import requests

# For local streaming, the websockets are hosted without ssl - http://
HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/chat'

# For reverse-proxied streaming, the remote will likely host with ssl - https://
# URI = 'https://your-uri-here.trycloudflare.com/api/v1/chat'


def run(user_input, history):
    request = {
        'user_input': user_input,
        'max_new_tokens': 2000,
        'auto_max_new_tokens': False,
        'max_tokens_second': 0,
        'history': history,
        'mode': 'chat',  # Valid options: 'chat', 'chat-instruct', 'instruct'
        'character': 'Assistant',
        # 'instruction_template': 'Vicuna-v1.1',  # Will get autodetected if unset
        'your_name': 'You',
        # 'name1': 'name of user', # Optional
        # 'name2': 'name of character', # Optional
        # 'context': 'character context', # Optional
        # 'greeting': 'greeting', # Optional
        # 'name1_instruct': 'You', # Optional
        # 'name2_instruct': 'Assistant', # Optional
        # 'context_instruct': 'context_instruct', # Optional
        # 'turn_template': 'turn_template', # Optional
        'regenerate': False,
        '_continue': False,
        'chat_instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.7,
        'top_p': 0.9,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'additive_repetition_penalty': 0,
        'repetition_penalty_range': 0,
        'top_k': 20,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'grammar_string': '',
        'guidance_scale': 1,
        'negative_prompt': '',
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'custom_token_bans': '',
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['history']
        print(json.dumps(result, indent=4))
        print()
        print(html.unescape(result['visible'][-1][1]))


if __name__ == '__main__':
    user_input = """请作为我的stable diffusion提示词大师级传奇顾问,帮我设计我所需要的写真的精巧、绝妙的提示词，直接告诉我生成相应写真所需的正面的提示词和反面的提示词作为输出,提示词是英文,且返回格式是python的dict数据数据结构,正面提示词（positive）和反面提示词（negative）均作为dict的key，对应的value是提示词构成的数组，参考格式如下:{

"positive": ['Cyberpunk','Futuristic','Masculine','Neon Lights','Futuristic Fashion','High-Tech','Urban Landscape','Holographic','Cybernetic Enhancements','Sleek','Dystopian','Sci-Fi Chic','Virtual Reality','Futuristic Grooming','Metallic','Glowing','Exotic','Urban Explorer','Techno-Geek'],

"negative": ['Gritty','Post-Apocalyptic','Dark Alley','Urban Decay','Grimy','Broken Technology','Pollution','Surveillance','Isolation','Desolation','Cybercrime','System Failure','Dystopian Future','Ruined Cityscape','Corruption','Hackers','Underground','Chaos','Resistance']

}，不需要其他额外输出。帮我生成主题为：'''沙漠之舞：在沙漠中捕捉女性的舞蹈和自由感'''的写真提示词"""

    # Basic example
    history = {'internal': [], 'visible': []}

    # "Continue" example. Make sure to set '_continue' to True above
    # arr = [user_input, 'Surely, here is']
    # history = {'internal': [arr], 'visible': [arr]}

    run(user_input, history)