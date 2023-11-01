import requests

# For local streaming, the websockets are hosted without ssl - http://
HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/generate'

# For reverse-proxied streaming, the remote will likely host with ssl - https://
# URI = 'https://your-uri-here.trycloudflare.com/api/v1/generate'


def run(prompt):
    request = {
        'prompt': prompt,
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

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        print(result)
        return result


if __name__ == '__main__':
    import re
    import json
    
    def make_img_prompt(theme="阅读角落：将女性放在一个充满书籍的环境中，展现知识与智慧的魅力。"):
        prompt = '''Question: 请作为我的stable diffusion提示词大师级传奇顾问,帮我设计我所需要的男性写真的精巧、绝妙的提示词，直接告诉我生成相应写真所需的正面的提示词和反面的提示词作为输出,提示词是英文,其中正面提示词不少于20个，
        基于以上陈述，请帮我生成主题为："""{theme}"""的写真提示词，,返回格式是python的dict数据数据结构,正面提示词（positive）和反面提示词（negative）均作为dict的key，对应的value是提示词构成的数组，参考格式如下:{{
        "positive": ["Cyberpunk","Futuristic","Masculine","Neon Lights","Futuristic Fashion","Fancy","Urban Landscape","Holographic","Cybernetic Enhancements","Sleek","Dystopian","Sci-Fi Chic","Reality","Cool","Metallic","Glowing","Exotic","Urban Explorer","Engineer"],
        "negative": ["Gritty","Post-Apocalyptic","Dark Alley","Urban Decay","Grimy","Broken Technology","Pollution","Surveillance","Isolation","Desolation","Cybercrime","System Failure","Dystopian Future","Ruined Cityscape","Corruption","Hackers","Underground","Chaos","Resistance"]
        }}，严格按照示例格式仅返回format Output，不需要其他额外的输出。
        Factual answer:'''.format(theme=theme)
        result = run(prompt)
        try:
            if result:
                img_prompt_arr = re.findall("{.*?}", result, re.DOTALL)
                if img_prompt_arr:
                    img_prompt = json.loads(img_prompt_arr[0])
                    with open(f'./img-prompts/{theme}', 'w') as f:
                        f.write(json.dumps(img_prompt, indent=4, ensure_ascii=False))
        except Exception as e:
            print(e)
    
    themes = """
妖精的尾巴动漫穿越:女性主人公穿越到妖精的尾巴世界,在魔导师世界冒险。
JoJo奇妙冒险动漫穿越:女性主人公穿越JoJo奇妙冒险世界。
火忍者动漫穿越:女性主人公穿越火影忍者动漫世界。
海贼王动漫穿越:女性主人公穿越海贼王动漫世界在大航海时代冒险。
星际探险家：女性主人公穿越宇宙，探索未知星球和宇宙现象。
神秘的森林仙女：她生活在神秘的魔法森林中，与自然和野生动植物相伴。
风暴法师：操控风和天气的女性法师，引导风暴和闪电。
蒸汽朋克机械师：她是机械奇迹的创造者，穿着蒸汽朋克风格的服装。
时光旅行者：女主角在不同的历史时期中穿越，体验各种文化和时装。
美食家：她是一位烹饪大师，用魔法制作出令人垂涎欲滴的餐点。
幻想水族馆：女主人公生活在一个神奇的水族馆，与海洋生物为伴。
阴影刺客：擅长潜行和暗杀的女性刺客，隐藏在暗影中。
原始狩猎者：她是一个原始时代的狩猎女勇士，与野兽搏斗。
女性机甲驾驶员：操纵庞大机甲战斗装备的女性，捍卫未来。
希腊神话女神：化身为古希腊神话中的女神，如雅典娜或阿尔忒弥斯。
梦幻精灵王国：探索充满精灵和魔法的精美仙境。
空中航海家：在飞行船上冒险的女性船长，探索天空之上。
宇宙舞者：在太空中跳舞的女性，以星星和行星为背景。
魔法宝石猎人：她在神秘地下寻找宝石和宝藏。
星座守护者：每个星座都有一个女性守护者，代表其特质和能力。
仙境花园：女主人公生活在一个充满神奇植物和花卉的花园中。
蒸汽朋克机器人：她是一台蒸汽朋克机器人，具备人类情感。
穿越时空的恋人：两位恋人穿越不同时代，追寻彼此。
剑术大师：女性剑客在战场上展示她的剑术技巧。
飞行女巫：操控飞行魔法的女巫，在夜空中飞翔。
海底宫殿：女性王后统治的海底宫殿，与海洋生物互动。
奇幻学院学生：她是一名魔法学校的学生，学习各种魔法技能。
火焰舞者：操控火焰的女性舞者，在烈火中跳舞。
古代文明探险家：女性考古学家在古代文明遗址中探险。
机械蝴蝶：她是一个由齿轮和机械构成的蝴蝶人偶。
冰雪女皇：统治冰雪王国的女性君主，拥有冰冻魔法。
太空流行歌手：在外太空中举行音乐会的女性歌手。
幻想王国公主：在一个神奇王国中生活的女性王室成员。
魔法森林哨兵：她是森林守护者，保护树木和野生动植物。
神话中的动物伙伴：与神话中的动物伙伴一起冒险，如独角兽或凤凰。
太空奇幻小说作家：写太空冒险故事的女性作家，她的创意变为现实。
神秘的术士：女性术士掌握着神秘的魔法和咒语。
独角兽骑士：骑着独角兽的女性骑士，保护和平。
星际商人：在星际贸易中崭露头角的女性商人。
未来机器人：她是未来机器人，具有超人的技能和智慧。
魔法音乐家：演奏魔法乐器的女性音乐家，奏出魔法音符。
暗黑女巫：掌握黑暗魔法的女性，拥有神秘力量。
梦幻幽灵：她是一个神秘的幽灵，生活在梦境中。
奇幻狩猎队：一支女性冒险家队伍，追捕怪兽和恶魔。
美丽的机器人：她是一个机器人，外表美丽而高度智能。
太空海盗：女性海盗在太空中寻找宝藏和冒险。
龙骑士：骑着龙的女性骑士，保护王国免受威胁。
魔法花园仙子：她是花园中的仙子，使植物生长和开花。
未来警察：女性警察在未来城市维持法律和秩序。
古代舞者：女性舞者在古代文明的废墟中跳舞。
机械天使：她是一个由机械构成的天使，守护人们。
冰雪女孩：她生活在永恒的冰雪中，与北极生物互动。
魔法工匠：制造魔法物品的女性工匠，如魔法饰品和药水。
蒸汽朋克特工：执行机密任务的女性特工，穿着蒸汽朋克风格的装备。
恶魔女王：统治地狱的女性君主，拥有地狱之力。
星际宇航员：探索外太空的女性宇航员，与宇宙交互。
穿越历史的探险家：在不同时代的历史中探险，解开谜团。
机械花园仙子：她是一个由机械构成的花园仙子。
神秘水世界：女主人公生活在一个水下城市，与水生生物为伴。
未来医生：女性医生使用高科技医疗设备治疗病人。
魔法猎手：追捕恶魔和黑巫师的女性猎手，使用魔法武器。
天空城堡：女性君主统治的天空城堡，悬浮在云层中。
神秘的星座巫师：掌握星座魔法的女性巫师，预测未来。
奇幻童话故事：女性主人公扮演各种童话故事中的角色。
未来战士：女性战士在未来的战斗中保卫人类。
机械猎人：她是一个由机械构成的猎人，捕获机械野兽。
暗夜女巫：掌握黑夜和暗影魔法的女性，行动在夜晚。
魔法森林精灵：她是森林中的精灵，保护自然的平衡。
太空摄影师：在太空中拍摄壮观的宇宙景观的女性摄影师。
神秘探险家：女性探险家在未知地域中寻找秘密。
机械造物师：制造机械生物和装置的女性造物师。
冰雪女孩：她是冰雪之国的女孩，拥有冰雪魔法。
魔法画家：创造魔法画作的女性画家，使画中的事物栩栩如生。
蒸汽朋克飞行家：在蒸汽朋克飞行器上探索空中领域的女性。
龙之魔法师：与龙互动并掌握龙之魔法的女性巫师。
梦境游侠：在梦境中旅行的女性冒险家，解开梦境之谜。
神秘的机械园丁：她是一个由机械构成的园丁，创造机械植物。
魔法舞蹈家：演绎魔法舞蹈的女性舞者，以舞蹈表现魔法。
暗影女忍者：女性忍者在暗影中执行任务，擅长潜行。
神话中的神兽：变身为神话中的神兽，如狮子或狮鹫。
宇宙工程师：在太空站中工作的女性工程师，维护宇宙设施。
星际探险家：女性主角穿着宇航服，在外太空中探索未知星球。
奇幻仙境：进入一个充满精灵、独角兽和神秘森林的奇幻世界。
潜水冒险：女性角色穿着潜水装备，探索海底世界，与海洋生物互动。
赛博朋克反抗者：在赛博朋克城市中，女性主人公是反抗组织的领袖。
古代战士：穿着传统武士装束，展现出女性的勇气和力量。
美食冒险：女主人公在神秘的烹饪世界中探索各种美味食材。
未来机器人：以机器人女性的形象，探讨人工智能与情感的融合。
蒸汽朋克侦探：女性侦探在维多利亚时代蒸汽朋克世界中解决犯罪。
魔法学校：女主人公在一所魔法学校学习魔法，与她的魔法宠物一起。
龙之守护者：女性主角是一位勇敢的龙的护卫者，保护宝贵的龙蛋。
时间旅行者：探索不同时代，穿越历史，解开时空之谜。
太空贵族：女性角色是星际贵族，在太空城市中享受奢华生活。
魔幻雪国：在冰雪覆盖的王国中，女主人公拥有冰雪魔法。
赛车女神：以速度女神为主题，参加未来的赛车比赛。
巨人杀手：女性角色与巨人搏斗，保卫王国。
空中海盗：女性船长带领一支空中海盗团队，寻找宝藏。
漫画艺术家：女性主人公穿越漫画世界，创作自己的漫画冒险。
神秘沙漠探险：在沙漠中探索古老的宝藏和秘密。
女巫学徒：女性角色学习魔法，解锁神秘的魔法能力。
科学家探险家：在未知世界中研究新物种和科学奇迹。
音乐之旅：以音乐为主题，女性主人公追寻音乐之旅。
花仙子：女性主角是花仙子，掌控植物魔法。
火山探险家：女性冒险家勇敢地探索火山和岛屿。
动物保护者：在野生动物保护中心，女性主人公保护濒危动物。
美丽的机器人：女性机器人具有人类情感，探索自我认知。
音乐会幻想：女性主人公成为古典音乐会的明星。
古代宇航员：女性宇航员探索古代外星球。
神秘舞蹈者：以舞蹈和音乐为主题，女性角色表演神秘的舞蹈。
巨龙驯兽师：女性主人公训练巨龙，与它们一同冒险。
花园仙境：女性主人公是花园仙子，创造神奇的花园。
科幻忍者：女性忍者在未来科幻世界中执行任务。
奇幻水族馆：在一个水下王国中，女性主角与海洋生物互动。
阿拉伯夜晚：女性主人公穿越到阿拉伯夜晚的仙境。
荒野生存：在野外求生，女主人公展现生存技能。
太空探险家：女性角色探索宇宙深处，发现新星球。
音乐魔法师：以音乐为主题，女性主人公掌握音乐魔法。
奇幻图书馆：女主人公是一位图书馆管理员，掌握古老魔法。
风之精灵：女性主角掌控风之力量，探索天空王国。
亚特兰蒂斯的秘密：女性冒险家深入亚特兰蒂斯的废墟。
太空音乐家：女性音乐家在太空中演奏美妙的音乐。
古代神话英雄：女性主人公成为古代神话中的英雄。
超级力量：女性超级英雄拥有强大的超能力。
宇宙花园：女性主人公在太空中创建美丽的宇宙花园。
神秘城市：在神秘的城市中，女性角色揭示城市的秘密。
梦幻童话：重现传统童话故事，女性主人公成为童话中的角色。
音乐梦境：女性主人公在音乐的梦幻世界中冒险。
未来幻想：在未来科技世界中，女主人公探索未知的未来。
魔法图书：女性主人公通过魔法图书进入不同的世界。
天使的挑战：女性角色是一位天使，面临挑战和冒险。
钢铁女侠：女性主人公在机械世界中拯救人类。
霓虹之夜：女性主角是霓虹之夜的城市探险家。
昆虫王国：在昆虫的奇幻王国中，女性主人公探索生态。
奇幻舞蹈：女性角色以舞蹈和音乐为主题的冒险。
恐龙探险家：女性冒险家穿越时间，与恐龙互动。
糖果王国：女性主人公探索充满糖果的奇幻王国。
科学童话：女性主人公在科学童话世界中进行探险。
幻想水族馆：在奇幻水族馆中，女性主角与神奇海洋生物互动。
神秘星球：女性冒险家在未知星球上解开谜题。
惊险小说作家：女性小说家创作恐怖小说情节，然后经历它们。
花舞仙境：女性主人公在花瓣雨中跳舞，掌握花术。
美食魔法：女性角色在美食世界中使用烹饪魔法。
未来游戏玩家：女性主人公成为未来虚拟现实游戏的高手。
奇幻电影明星：女性明星穿越到电影的奇幻世界。
火之舞者：女性主角掌握火之力量，在火山中跳舞。
秘密迷宫：女性冒险家在古老迷宫中寻找宝藏。
太空生物学家：女性生物学家在外太空中研究外星生物。
神秘宇宙探险：女性主人公探索未知宇宙中的秘密。
魔法草原：女性主角在魔法草原中与神秘生物互动。
美丽的机械花园：女性主人公在机械花园中创造机械花朵。
迷失城市：女性探险家在神秘的迷失城市中寻找线索。
音乐魔法学校：女性学生在音乐魔法学校学习。
超级大侦探：女性大侦探破解复杂的谜题和犯罪。
未来格斗士：女性格斗士在未来斗技场中竞技。
奇幻绘画：女性艺术家以画笔创造出奇幻的世界。
钻石矿工：女性矿工在地下挖掘宝石和宝藏。
神秘小岛：女性冒险家在荒岛上发现宝藏和神秘生物。
深海探险家：女性潜水员深入海底，发现深海秘密。
神秘雪山：女性冒险家在雪山中探索神秘的寺庙。
魔法商店：女性主人公拥有一家魔法用品商店，帮助客户解决问题。
超级科学家：女性科学家在实验室中创造奇迹。
希腊神话：女性主人公成为古希腊神话中的神灵。
未来宇航员：女性宇航员探索未来宇宙空间站。
星际冒险家：女性角色穿越宇宙，探索外星世界。
蒸汽朋克工匠：在蒸汽朋克世界中，女性工匠修理机械。
魔法学徒：年轻女巫学徒学习魔法的日常生活。
未来战士：机械化的女性士兵在未来战场上战斗。
美食家的奇幻之旅：在美味的幻想世界中品尝各种料理。
古代神话传说：女性化身成古代神话中的女神或英雄。
动物精灵：化身成森林、海洋或天空中的动物精灵。
奇幻森林冒险：在神秘森林中寻找宝藏和冒险。
女性超级英雄：拥有超能力的女超级英雄。
精灵公主：具有精灵特征的童话公主。
奇幻海底世界：女性在海底城市中的生活和冒险。
时尚魔法师：魔法与时尚相结合的女性巫师。
机械仙境：机械与魔法交织的幻想世界。
星座守护者：不同星座的女性守护者。
外太空探险家：在外太空中探索未知星球。
古代日本传统：穿着传统和服的女性。
穿越时光：女性穿越不同历史时期的冒险。
魔法动物园：在一个充满魔法生物的奇幻动物园中。
超自然侦探：女性侦探解决超自然事件。
赛博朋克忍者：赛博朋克风格的女忍者。
幻想舞者：女性在幻想世界中跳舞。
美丽的废墟：在废弃的城市废墟中拍摄。
神秘的太空贵族：女性宇宙贵族的生活。
女性机器人：拥有人工智能的女性机器人。
女性海盗船长：领导一支女性海盗团队的船长。
甜蜜的仙境：在糖果和甜点之中的甜蜜世界。
未来都市风景：女性在未来都市的生活。
龙与骑士：女性骑士骑着龙冒险。
梦幻王国：在一个充满梦幻生物的王国中。
恶魔猎手：女性狩猎邪恶的恶魔。
奇妙的太空艺术家：创作太空主题的艺术品。
魔法学院校园生活：女性巫师在魔法学院的日常生活。
时空旅行者：在时空中穿越不同时代的冒险。
星际音乐家：女性音乐家在太空中演奏音乐。
穿越童话：女性进入不同童话世界的故事。
美丽的机械生物：机械与生物相融合的女性。
未来运动明星：女性在未来体育比赛中的表现。
赛博朋克探险家：在赛博朋克世界中探险。
神秘的仪式：女性在神秘仪式中的角色。
女性宇航员：太空站中的女性宇航员。
龙与巫师：女性巫师与她的巨龙伙伴。
奇幻歌手：女性歌手在奇幻音乐会上演唱。
天使与恶魔：女性天使与恶魔的对抗。
科学家的日常：女性科学家的实验室生活。
赛博朋克反叛者：女性反抗赛博朋克统治的反叛者。
穿越星际：在星际航行中的女性冒险家。
魔法舞者：女性在魔法舞蹈中展示技巧。
女性机械工程师：在机械工作室中创造机械奇迹。
太空花园：在太空站中的女性花园园丁。
童话公主改编：重新演绎经典童话公主故事。
赛博朋克宝石匠：女性宝石匠在赛博朋克工作室中创作。
王国守卫者：女性骑士守卫着她的王国。
奇幻彩绘：女性艺术家在幻想世界中创作壁画。
神秘的舞蹈仪式：女性参与神秘的舞蹈仪式。
未来摄影师：女性在未来都市中的摄影师生活。
飞行员的传奇：女性飞行员在太空中的传奇。
女性草原勇士：在开放的草原上的女性勇士。
魔法花园仙子：在魔法花园中的女性仙子。
赛博朋克刺客：女性刺客在赛博朋克都市中的生活。
神秘的星座仪式：女性在星座仪式中的仪式。
星际航行家：在星际航行中的女性冒险家。
女性时尚设计师：在时尚工作室中设计未来服装。
穿越神话：女性进入不同神话世界的故事。
美丽的机械舞者：机械舞与舞蹈相结合的女性。
未来宇航员：在未来宇宙飞行中的女性宇航员。
童话公主逛街：经典童话公主逛购物中心。
赛博朋克探险家团队：女性探险家团队在城市废墟中。
神秘的音乐家：女性音乐家在神秘音乐会上演奏。
未来医生：女性医生在未来医疗实践中的生活。
龙与巫师的友谊：女性巫师与她的巨龙朋友。
赛博朋克海盗：女性赛博朋克风格的海盗。
星际绘画家：女性艺术家在星际空间中的创作。
奇幻魔法森林：女性在魔法森林中的冒险。
科学家的发现：女性科学家在实验室中的发现。
赛博朋克游戏玩家：女性在赛博朋克游戏中的生活。
穿越古代：女性在不同古代文化的故事。
魔法花园守卫者：守卫魔法花园的女性。
未来机械艺术：女性机械艺术家的创作。
神秘的星座观察家：女性在星座观察中的角色。
星际旅行家：在星际旅行中的女性冒险家。
时尚设计师的奇想：时尚设计师的创意奇想。
穿越童话之旅：女性踏上不同童话之旅。
机械花园仙子：在机械花园中的女性仙子。
赛博朋克特工：女性特工在赛博朋克任务中的生活。
神秘的星际仪式：女性在星际仪式中的仪式。
星际冒险家团队：在星际冒险中的女性冒险家团队。
未来音乐家：女性音乐家在未来音乐会上演奏。
女性宇宙医生：在宇宙站中的女性医生。
龙与巫师的传奇：女性巫师与她的巨龙的传奇故事。
赛博朋克反抗者：女性领导赛博朋克反抗运动。
神秘的星际音乐家：女性在星际音乐会中的音乐表演。
未来宇航医生：在未来宇宙医疗中的女性医生。
奇幻飞行家：女性在幻想飞行中的冒险。
赛博朋克魔法师：赛博朋克世界中的女性魔法师。
神秘的星际宝石匠：女性在星际宝石匠工作室中的创作。
星际摄影家：女性在星际空间中的摄影生活。
机器人战士：女性机器人战士保卫机械世界。
""".split('\n')
    themes = list(set(themes))  # 去重复
    for theme in themes:
        make_img_prompt(theme)