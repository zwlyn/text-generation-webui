import json
import requests
import io
import os
import base64
import hashlib
from PIL import Image, PngImagePlugin
os.environ.pop('all_proxy', None)
os.environ.pop('ALL_PROXY', None)


def calculate_hash(input_string, hash_algorithm="sha256"):
    hash_obj = hashlib.new(hash_algorithm)
    hash_obj.update(input_string.encode("utf-8"))
    hash_value = hash_obj.hexdigest()
    return hash_value

def get_file_base64(file_path):
    with open(file_path, 'rb') as image_file:
        # 将图片文件编码为 Base64 字符串
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        return base64_image

url = "http://127.0.0.1:7860"
# url = "http://sd.symsu.com"
def make_payload(prompt, negative_prompt):
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": 30,
        "sampler_index": "DPM++ 2M SDE Karras",
        "seed": -1,
        "batch_size": 1,
        "n_iter": 1,  # batch_count
        "cfg_scale": 7,
        "width": 512,
        "height": 768,
        "alwayson_scripts": {
            "ADetailer":{
                "args": [
                    {
                    "ad_model": "person_yolov8n-seg.pt",
                    "ad_prompt": "",
                    "ad_negative_prompt": "",
                    },
                    {
                    "ad_model": "hand_yolov8n.pt",
                    "ad_prompt": "",
                    "ad_negative_prompt": "",
                    "ad_denoising_strength": 0.3,
                    },
                    {
                    "ad_model": "face_yolov8n.pt",
                    "ad_prompt": "",
                    "ad_negative_prompt": "",
                    },
                ]
            },
        }
    }
    return payload


def save_img_with_info(imgBase64, filename=None, folder='folder', basepath='results'):
    image = Image.open(io.BytesIO(base64.b64decode(imgBase64.split(",", 1)[0])))
    png_payload = {
        "image": "data:image/png;base64," + imgBase64
    }
    response = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
    pnginfo = PngImagePlugin.PngInfo()
    imginfo = response.json().get("info")
    pnginfo.add_text("parameters", imginfo)
    if not filename:
        filename = calculate_hash(imginfo) + '.png'
    if not os.path.exists(f"./{basepath}"):
        os.mkdir(basepath)
    if not os.path.exists(f"./{basepath}/{folder}"):
        os.mkdir(f"./{basepath}/{folder}")
    image.save(f'{basepath}/{folder}/{filename}', pnginfo=pnginfo)

# ideas = ['宇航员之梦：在太空舱中捕捉女性宇航员的梦想。', '艺术装置：在艺术装置中捕捉女性的实验和创新。', '自然之和：捕捉女性与自然的和谐与平静。', '时光隧道：以时光穿越为主题，捕捉女性的历史之美。', '现代冒险家：在探险中捕捉女性的现代冒险精神。', '雨中之美：在雨天捕捉女性的雨中浪漫。', '历史名人：女性扮演历史上的名人，重现历史场景。', '失落的城市：在废弃建筑中捕捉女性的探险精神。', 'Enchanted Garden: Dress a woman in flowy, whimsical attire and photograph her amidst a lush, magical garden setting.', '荒野之美：在荒野和戈壁中捕捉女性的坚韧与自然之美。', '小世界：捕捉女性微缩模型世界中的创意。', '马戏团表演：在马戏团表演中捕捉女性的表演和灵活性。', '露天音乐会：在音乐会现场捕捉女性的音乐狂欢。', '母性之爱：捕捉女性在母性和家庭中的爱与关怀。', '飞翔之美：捕捉女性在飞翔或滑翔中的自由感。', '色彩对比：在鲜明的对比色背景下，强调女性的特点。', '美丽的城市：在城市街头捕捉女性的城市生活。', '电影幕后：捕捉女性在电影制作幕后的工作和创意。', '惊险摩托骑手：捕捉女性摩托骑手的冒险精神。', '冰雪之美：在冰雪世界中捕捉女性的冰雪仙子形象。', '彩虹色彩：创造一个多彩的环境，强调各种色彩的美感。', '印度宫殿：在印度宫殿中捕捉女性的宫廷风范。', '城市文化：在城市文化和街头艺术中捕捉女性的表现。', '古典芭蕾：捕捉女性在芭蕾舞蹈中的优雅和舞蹈之美。', '骑马女性：在马场上捕捉女性的马术技能。', '摇滚明星：捕捉女性的摇滚明星形象和音乐魅力。', '科学家之美：突出女性在科学领域的工作和创造力。', '露天音乐：在露天音乐会中捕捉女性的音乐狂欢。', '美丽山谷：在山谷中捕捉女性的自然之美。', '星座宇宙：以不同星座为主题，捕捉女性的星座特质。', '漫画风格：以漫画和卡通为灵感，创造出色彩丰富的视觉效果。', '纽约时尚：在纽约城市中捕捉女性的时尚之美。', '高科技城市：在未来高科技城市中捕捉女性的现代感。', '城市光影：在城市街头捕捉女性的光影和魅力。', '花园舞者：在花园中捕捉女性的芭蕾舞蹈。', '太空探险：在外太空探险中捕捉女性的太空之美。', '红色风情：在红色场景中捕捉女性的激情和火热。', '花园仙境：在花园或公园中捕捉女性在花朵和自然美景中的画面。', '机械工程：捕捉女性在机械工程领域的科技魅力。', '暗黑精灵：捕捉女性的神秘和幽暗魅力，以精灵为主题。', '画家工作室：在画家工作室中捕捉女性的创作与艺术。', '奇幻童话：在童话故事场景中捕捉女性的童话之美。', 'Fitness Fantasy: Capture women engaging in various fitness activities or sports, highlighting their strength and determination.', '经典电影：以经典电影为主题，捕捉女性的电影明星魅力。', '魔法幻境：在魔法世界场景中捕捉女性的仙境之美。', '欧洲古城：在古老的欧洲城市中捕捉女性的风情。', '梦境花园：在梦幻花园中捕捉女性的仙境之美。', '恶魔的诱惑：突出女性的神秘和恶魔形象。', '未来城市：创造未来城市场景，捕捉女性的未来之美。', '魅力宇宙：捕捉女性在宇宙中的星际魅力。', '大都市女性：强调女性的职业和城市生活方式。', '自然之声：在自然环境中捕捉女性的与自然的联系。', '阴暗幻想：在阴暗幻想场景中捕捉女性的神秘之美。', '印度风情：在印度风格场景中捕捉女性的风情和服饰。', '女性掌控：捕捉女性在领导和支配的角色中的自信。', '魔法童话：在仙境中捕捉女性的童话之美。', 'Circus Chic: Create a glamorous, whimsical circus-inspired shoot with acrobats, jugglers, or clowns.', '钢琴艺术家：捕捉女性钢琴家的音乐才华和优雅。', '儿童乐园：在儿童乐园中捕捉女性的童真之美。', '足球狂热：在足球场上捕捉女性的足球热情。', '自然灵感：捕捉女性在自然中获得的创意和启发。', '民族风情：在不同文化的民族风情中捕捉女性的多元魅力。', '乐队女性：在音乐乐队中捕捉女性的音乐才华。', '黑暗精灵：捕捉女性的幽暗神秘，强调幻想元素。', '极地探险：在极地地区中捕捉女性的冰雪冒险。', '森林之韵：在森林中捕捉女性的大自然之美。', '高山探险：在高山和攀登中捕捉女性的冒险家精神。', '游戏玩家：在电子游戏场景中捕捉女性的游戏激情。', '复古冒险：重现20世纪探险家的风格和精神。', '工业风格：在工业风格的场景中捕捉女性的坚韧和力量。', '运动女性：捕捉女性在各种运动中的精彩瞬间。', '摄影大师：捕捉女性在摄影领域的创造性。', '农村之美：在农村风光中捕捉女性的自然之美。', '冰雪之吻：在雪地中捕捉女性与冰雪的和谐。', '自然音乐家：在自然环境中捕捉女性与自然的音乐和和谐。', '海底宝藏：在沉船场景中捕捉女性与宝藏的幻想。', '异国之旅：在异国旅行场景中捕捉女性的冒险精神。', '未来太空城：捕捉女性在未来太空城市中的生活。', '高山冒险：在高山探险中捕捉女性的勇气和坚韧。', 'Urban Goddess: Capture a woman dressed in chic city attire, contrasted against a gritty urban backdrop.', '灵感工作室：突出女性在创意工作室中的艺术创造力。', 'Goddess of Wind and Waves: Capture a woman dressed as a god', '时尚采访：将女性摄影成时尚杂志封面人物。', '未来宇宙：创造一个未来宇宙场景，捕捉女性的科技魅力。', '舞台之美：在剧院舞台上捕捉女性的表演艺术。', '魔法学校：捕捉女性在魔法学校中的奇幻冒险。', '草原之舞：在草原中捕捉女性的舞蹈和草原之美。', '水中舞蹈：在游泳池中捕捉女性的水下舞蹈。', 'Architectural Accents: Use architectural elements as backgrounds to create visually striking portraits of women.', '雪地之美：在雪地中捕捉女性的雪景和冒险。', '钢铁女性：捕捉女性在制造业和机械领域的坚强。', '空中飞行：在滑翔伞或热气球中捕捉女性的空中飞行。', '科学幻想：创造科学幻想场景，捕捉女性的未来科技。', '未来科技：捕捉女性在未来科技领域的未来之美。', 'Time-Travel Fashion: Dress models in attire inspired by different historical periods and photograph them in corresponding settings.', '雕塑之美：在雕塑工作室中捕捉女性的艺术创造力。', '忍者女性：在忍者场景中捕捉女性的武术技巧。', '韩国时尚：在韩国风格场景中捕捉女性的时尚之美。', '互联网女性：突出女性在科技和互联网领域的影响。', '梦幻花嫁：捕捉女性的婚礼梦想和浪漫之美。', '美食探险：在世界各地美食之旅中捕捉女性的探险精神。', 'Femme Fatale: Create alluring, mysterious portraits of women dressed in seductive attire, using dramatic lighting and bold colors.', '蒸汽朋克：在蒸汽朋克风格场景中捕捉女性的古典与未来的结合。', '雪后童话：在雪后的童话般世界中捕捉女性的美丽。', 'Whimsical Wonderland: Create a fantastical world inspired by Alice in Wonderland or other magical tales, with women dressed as peculiar characters.', '女性艺术家：捕捉女性在绘画、雕塑等艺术领域的创意。', '科学家的时刻：捕捉女性在实验室中的科学家魅力。', '太空征程：以太空和星际旅行为主题，探索宇宙的未知。', '赫尔墨斯：以希腊神话为主题，捕捉女性的神话之美。', '文学之美：突出女性在文学和创作领域的才能。', '幸福家庭：捕捉女性在家庭生活中的幸福和温馨。', '野外探险：将女性放在大自然中，探索山林、沙滩或森林，呈现出自然之美。', '高山风情：在山脉中捕捉女性的登山冒险与壮丽景色。', '空中冒险：在热气球或滑翔伞中捕捉女性的空中冒险。', '海底宝藏：在海底寻宝中捕捉女性的冒险与宝藏。', '贵族女性：在贵族府邸中捕捉女性的贵族风范。', '军事冒险：在军事场景中捕捉女性的勇气和坚韧。', '音乐之旅：捕捉女性在各种音乐场景中的音乐之旅。', '舞蹈之美：在舞蹈表演中捕捉女性的舞蹈魅力。', '天空探险：在滑翔伞或热气球中捕捉女性的空中冒险。', '都市时尚：在大城市中捕捉女性的时尚和现代魅力。', '奢华时刻：在豪华和奢华的场景中捕捉女性的精致。', '书店之美：在独立书店中捕捉女性的文学魅力。', '魔法之城：在魔法城市中捕捉女性的神秘之美。', '舞蹈剧场：捕捉女性在舞蹈剧场中的舞蹈之美。', '音乐创作：捕捉女性在音乐创作中的创意天赋。', '大自然之声：在自然环境中捕捉女性的与自然的联系。', '印第安传统：突出女性的印第安文化和传统。', '城市风情：在城市街头捕捉女性的时尚和个性。', '音乐会表演：在音乐会现场捕捉女性的音乐狂欢。', '冬日仙境：在冬季雪景中捕捉女性的仙境之美。', '高山探险：在高山和峡谷中捕捉女性的探险精神。', '乡村冒险：在乡村探险中捕捉女性的自然之美。', '旅行梦想：捕捉女性对世界各地旅行的渴望。', '忧郁之美：捕捉女性的忧郁和情感深度。', '贵族生活：在贵族府邸中捕捉女性的贵族风范。', '童话故事：以童话故事为灵感，重现童话中的场景和角色。', '印度舞蹈：在印度舞蹈场景中捕捉女性的优雅舞姿。', '时光旅行：穿越不同历史时期，捕捉女性的不同造型。', '足球女将：在足球场上捕捉女性的足球技巧。', '时尚运动：在时尚和运动的场景中捕捉女性的活力。', '自然之美：捕捉女性与自然的和谐与平静。', '音乐节：在音乐节现场捕捉女性的音乐狂欢。', '美食诱惑：在美食摄影中捕捉女性的食欲与诱惑。', '亚洲之美：突出女性在亚洲文化中的风情和美丽。', '王室风采：在皇宫中捕捉女性的皇室风范。', '女性力量：捕捉女性在各种运动中的力量和自信。', '银河之美：在银河系场景中捕捉女性的宇宙之美。', '海底奇遇：在海底冒险中捕捉女性的奇幻之美。', '天使与恶魔：捕捉女性两面性，既有天使的善良，又有恶魔的诱惑。', '霓虹之光：在夜晚的城市中捕捉霓虹灯光下的女性形象。', '仙境之旅：在仙境般的场景中捕捉女性的奇妙之美。', '极简之美：将女性融入极简主义和现代设计中。', '黑白经典：创造经典的黑白照片，突出光影和纹理。', '海盗传说：突出女性的海盗冒险者形象。', '梦幻森林：在童话般的森林中捕捉女性的仙境之美。', '机械之美：在工业场景中捕捉女性的机械工程和科技魅力。', '贝尔法斯特风情：在北爱尔兰贝尔法斯特捕捉女性的风情。', '迷幻色彩：使用强烈的色彩和抽象元素，创造视觉效果。', '异国庭院：在异国庭院中捕捉女性的异域之美。', '东方之美：在东方风格场景中捕捉女性的风情和服饰。', '恶魔与天使：捕捉女性的两面性，同时展现恶魔与天使的形象。', '沉船幻想：在沉船场景中捕捉女性与宝藏的幻想。', '城市冒险：在城市探险中捕捉女性的勇气和决心。', '西部牛仔：在西部风格的场景中捕捉女性的牛仔形象。', '极简主义：在简洁的背景下，突出女性的线条和轮廓。', '音乐盛典：在音乐节现场捕捉女性的音乐狂欢。', '电影幕后：捕捉女性在电影制作幕后的创意。', '航空飞行：在航空场景中捕捉女性的飞行之美。', '乡村生活：捕捉女性在乡村生活中的宁静和和谐。', '光与影：捕捉女性在光影下的戏剧效果。', '童话世界：以经典童话故事为主题，捕捉女性的童话之美。', '神秘故事：在神秘场景中捕捉女性的故事之美。', '时尚模特：突出女性在时尚界的职业形象。', '秘境之美：捕捉女性在未知探险中的神秘之美。', '夏日海滩：在夏季海滩中捕捉女性的夏日时光。', '欧洲风景：在欧洲名胜中捕捉女性的风景之美。', '舞台剧演员：捕捉女性在戏剧表演中的戏剧魅力。', '复古电影：以老式电影为主题，捕捉女性的复古风情。', '艺术家之眼：捕捉女性在艺术创作和创新中的表现。', '空中宫殿：在云端城堡中捕捉女性的宫殿风范。', '美食创意：在美食创意场景中捕捉女性的烹饪艺术。', '巴黎时尚：在巴黎街头捕捉女性的时尚之美。', '雪地仙子：在雪地中捕捉女性的冰雪仙子形象。', '奇幻冒险：创造一个奇幻冒险场景，捕捉女性的探险精神。', '手工艺品：突出女性在手工艺品制作中的创意才华。', '高山探险：在雪山和高山中捕捉女性的探险和坚韧。', '波西米亚自由：在波西米亚文化中捕捉女性的自由精神。', '魔法森林：在神秘的森林中捕捉女性的仙灵之美。', '狂欢音乐：在音乐节中捕捉女性的音乐狂欢。', '森林仙女：在森林中捕捉女性的仙女形象。', "Nature's Muse: Capture women interacting with nature, like dancing in a field of flowers or sitting atop a tree trunk.", '荒漠之美：在沙漠中捕捉女性的坚韧与大自然之美。', '舞台剧表演：捕捉女性在舞台剧演出中的戏剧魅力。', '明信片之美：将女性摄影成精美的明信片风格。', '茶道之美：在日本茶道场景中捕捉女性的优雅。', '惊险刺激：在极限运动中捕捉女性的勇敢和刺激。', '水下梦幻：在水下世界中捕捉女性的梦幻之美。', '文学之美：在图书馆或书店中捕捉女性的文学魅力。', 'Futuristic Fantasies: Experiment with futuristic clothing, hair, and makeup to create innovative, forward-looking portraits of women.', '表情包之美：以表情包为主题，捕捉不同表情的多样性。', '秘密花园：在私密花园中捕捉女性的隐秘之美。', '女性艺术家：捕捉女性在各种艺术形式中的创作。', '浪漫童话：在童话般的场景中捕捉女性的浪漫之美。', '夏日花园：在花园中捕捉女性的夏日和鲜花。', '黑暗童话：以黑暗童话为主题，捕捉女性的神秘之美。', '红色热情：在红色场景中捕捉女性的激情和火热。', '舞台之上：在音乐会或剧院舞台上捕捉女性的表演魅力。', '魔法森林：在神秘的森林中，捕捉女性的神秘和仙女感。', '冰雪童话：在冰雪世界中捕捉女性的冰雪仙子形象。', '艺术学院：在艺术学院场景中捕捉女性的创作过程。', '数字艺术：将女性融入数字艺术和绘画中。', '现代冒险：在都市冒险中捕捉女性的现代探险。', '赛车手：捕捉女性赛车手的速度和激情。', '飞行员之美：在飞机场和飞行中捕捉女性的飞行之美。', '亚洲花园：在亚洲花园中捕捉女性的和谐与宁静。', '未来机器人：在机器人世界中捕捉女性的未来科技感。', '魔法之美：在奇幻魔法场景中捕捉女性的仙境之美。', '美丽骑行：在自行车骑行中捕捉女性的自由和活力。', '音乐盛宴：在音乐节现场捕捉女性的音乐狂欢。', '城市美食家：捕捉女性的美食品味和烹饪技能。', '精灵之韵：捕捉女性在精灵世界中的仙灵之美。', '迷失在大都市：捕捉女性在繁忙城市中的独立魅力。', '阴暗童话：突出女性的神秘和暗黑童话形象。', '童真童趣：捕捉女童心中的美丽和快乐。', 'Tea Time Tales: Dress women in elegant attire and photograph them enjoying tea in a charming, vintage setting.', '都市风格：拍摄都市女性的街头时尚和个性。', '沙漠驼队：在沙漠中捕捉女性与驼队的沙漠之旅。', '小人国：创造一个微缩世界场景，捕捉女性的小巧之美。', '珍稀动物：与野生动物一同拍摄，捕捉女性与自然的亲近。', '机械之美：将女性融入复古机械或机械工程中。', '鲁冰花之美：在寒冷的环境中捕捉女性的坚韧和美丽。', '夜光之美：在黑暗中捕捉女性的夜光魅力。', '魔法梦境：捕捉女性在魔法梦境中的幻想之美。', '美丽农田：在农田中捕捉女性与大自然的和谐。', '科学实验室：捕捉女性在科学和研究中的聪明和创造力。', '时光穿越：重现不同历史时期的女性风采和生活。', '爵士音乐：在爵士音乐现场捕捉女性的音乐风采。', '未来太空：捕捉女性在未来太空城市中的生活。', '都市风情：在城市街头捕捉女性的时尚和个性。', '城市画廊：在城市画廊中捕捉女性的文化与艺术。', '梦幻之美：捕捉女性在梦境中的神秘之美。', '水中幻境：在水下场景中捕捉女性与水的互动。', '沙漠之舞：在沙漠中捕捉女性的舞蹈和自由感。', '星际宇航员：在太空舱中捕捉女性宇航员的科幻之美。', '复古摩登：捕捉女性的复古摩登时尚风格。', '赛车女性：在赛车场上捕捉女性的速度和激情。', '海滩度假：在热带海滩中捕捉女性的度假时光。', '梦幻森林：在神秘的森林中捕捉女性的仙灵之美。', '赛车手：捕捉女性赛车手的速度和竞技能力。', '机车文化：捕捉女性在机车骑行和机车文化中的魅力。', '未来航海家：捕捉女性在未来海洋探险中的冒险精神。', '美食厨艺：突出女性在烹饪和美食创意方面的技能。', '舞蹈之美：以各种舞蹈为主题，捕捉女性的舞蹈动感。', '旧时摩登：以复古时尚为主题，捕捉女性的摩登魅力。', '梦幻仙境：在仙境场景中捕捉女性的神秘之美。', '自然韵律：在大自然环境中捕捉女性的和谐与平和。', '东方神秘：在东方文化场景中捕捉女性的神秘之美。', '美食博主：突出女性在美食博客和烹饪方面的才华。', '家居时尚：在家中捕捉女性的时尚魅力。', '未来城市：捕捉女性在未来城市中的现代感。', '幻想城堡：在城堡和宫殿中捕捉女性的皇室风范。', 'Architectural Angles: Use architecturally interesting buildings as backdrops to create dynamic compositions with female subjects.', '美丽林荫：在森林中捕捉女性的自然之美。', '神话传说：以不同神话传说为主题，捕捉女性的神话之美。', '旅行探险：在全球旅行中捕捉女性的探险和冒险。', '高端时尚：捕捉女性的高端时尚和奢华魅力。', '时尚摄影：捕捉女性时尚摄影的创新和创意。', '拼图之美：以拼图为主题，捕捉女性的创意思维。', '梦幻画廊：在画廊中捕捉女性的文化与艺术。', '未来战士：在未来战场中捕捉女性的军事风格。', '极限自由：在极限运动中捕捉女性的勇气和刺激。', '舞蹈之魅：在舞蹈表演中捕捉女性的舞蹈魅力。', '自然芭蕾：在自然环境中捕捉女性的舞蹈和自然之美。', '霓虹夜景：在城市的霓虹夜景中捕捉女性的光影之美。', '自然之吻：在大自然中捕捉女性与自然的亲近。', '阴阳平衡：突出女性的平衡和和谐之美。', '魔法童话：在童话般的场景中捕捉女性的仙境之美。', '超自然力量：以超自然元素为主题，捕捉女性的神秘感。', '超级模特：捕捉女性的时尚模特职业形象。', '精灵花园：在花园中捕捉女性的精灵之美。', '海底幻境：在水下场景中捕捉女性与海洋生物的互动。', 'Time-Traveler: Dress a model in clothing inspired by different historical periods and photograph her in corresponding settings.', '影视明星：将女性摄影成影视明星的风采。', '仙境花园：在花园中捕捉女性的仙境之美。', '舞台之美：在舞台背景中捕捉女性的舞台表演。', '浪漫庄园：在乡村庄园中捕捉女性的浪漫之美。', '音乐之梦：捕捉女性在音乐场景中的表现，演奏乐器或欣赏音乐。', '霓虹都市：在城市夜晚中捕捉霓虹灯下的女性形象。', '赛马女骑手：在赛马场上捕捉女性的马术技能。', '夏日冰淇淋：在夏日冰淇淋摊中捕捉女性的快乐和童真。', '美食之美：女性与美味食物互动，突出食物的诱人之美。', '神话传说：以古代神话为主题，捕捉女性的神话之美。', '水下冒险：在水下世界中捕捉女性的水下冒险。', '星座神话：以星座和神话为主题，突出女性的神话之美。', '魔法学院：在魔法学院中捕捉女性的魔法之美。', '车库摇滚：在车库音乐会中捕捉女性的摇滚精神。', '珠宝之美：将女性与精美珠宝相结合。', '漫画世界：在漫画风格场景中捕捉女性的卡通形象。', '迷失城市：在废弃的城市场景中捕捉女性的冒险之美。', '街头文化：在街头涂鸦场景中捕捉女性的涂鸦艺术。', '地下音乐会：在地下音乐场景中捕捉女性的摇滚精神。', '街头风格：拍摄都市女性的街头时尚和个性。', '未来科技：在未来科幻场景中捕捉女性的科技时代魅力。', '惊险特工：捕捉女性的特工风范，强调智慧和勇敢。', 'Literary Ladies Revisited: Continue exploring iconic female characters from literature, capturing their stories in a modern or unique way.', 'Music Makes the World Go Round: Photograph female musicians playing various instruments or singing in diverse settings.', '自然韵律：在自然环境中捕捉女性与大自然的和谐。', '高山探险：在高山中捕捉女性的探险精神。', '海滩情感：在沙滩上捕捉女性的情感与自然和谐。', '帆船冒险：在帆船冒险中捕捉女性的海洋之美。', '美术馆之美：在美术馆中捕捉女性与艺术品的互动。', '金色时刻：在日落时分捕捉女性与金色光线的瞬间。', '玛丽莲梦露风格：重现玛丽莲梦露的经典造型和风格。', '星座宇宙：以星座和宇宙为主题，突出女性的宇宙之美。', '童年梦想：捕捉女性对童年梦想的追求。', '冰雪女神：在冰雪中捕捉女性的神秘和仙灵之美。', 'Celestial Beauty: Create a dreamy, ethereal atmosphere with celestial motifs, like stars or galaxies, in the background.', '时尚雕塑：在现代雕塑园中捕捉女性的时尚与艺术。', '高尔夫女将：在高尔夫球场上捕捉女性的高尔夫技能。', '古代女王：以古代女性君主为主题，突出女性的皇家风采。', '异国风情：将女性融入异国风情和文化中。', '舞台魅力：在剧院舞台上捕捉女性的表演魅力。', 'Creative Cuisine: Dress models as chefs or food enthusiasts, showcasing their culinary creations in a visually appealing manner.', '建筑师之美：捕捉女性在建筑设计中的创意才华。', 'Literary Legends: Dress models as iconic female characters from literature, such as Jane Eyre or Elizabeth Bennet, and recreate scenes from their stories.', 'Vintage Traveler: Capture a woman dressed in vintage travel attire, with luggage and props that evoke the spirit of adventure.', '玛雅文明：在古玛雅文明遗址中捕捉女性的神秘之美。', '爱情小故事：记录女性的浪漫故事和关系时刻。', '雪地仙境：在雪地中捕捉女性的冰雪仙子形象。', '异国风情：在异国文化场景中捕捉女性的异域之美。', '种植者之美：在农田和花园中捕捉女性的农业之美。', 'Glass Slipper Story: Reimagine the Cinderella story with a modern twist, showcasing the glass slipper and other iconic elements.', '原始部落：在原始文化和部落场景中捕捉女性的自然美。', '街头涂鸦：在涂鸦艺术墙前捕捉女性的时尚。', '远东神秘：以远东文化为灵感，突出东方之美。']
ideas = os.listdir('./img-prompts')
for idea in ideas:
    try:
        # if os.path.exists(f'./{idea}'):
        #     continue
        # print(idea)
        with open(f'./img-prompts/{idea}') as f:
            content = json.load(f)
        prompt = """
        ((1woman)),((cartoon)),dynamic composition,rich colors,natural blurry,((masterpiece)),((bestquality)),8k,high detailed,ultra-detailed,Appropriate Dress,Respectable Appearance,Moderate Dressing,
        """
        negative_prompt = """
        more than 1person,man,AS-YoungV2-neg,BadDream,(badhandv4),BadNegAnatomyV1-neg,EasyNegative,FastNegativeV2,NSFW,watermark,signature,word,logo,text,blurry,low quality,bad anatomy,sketches,lowres,normal quality,monochrome,grayscale,worstquality,username,out of focus,bad proportions,cropped,watermark,signature,wrong hand,bad hand,bad feet,bhands-neg,Fixhand,negative_hand-neg,
        """
        prompt += ','.join(content['positive'])
        negative_prompt += ','.join(content['negative'])
        payload = make_payload(prompt, negative_prompt)
        for _ in range(25):
            response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
            r = response.json()
            print(r)
            save_img_with_info(r['images'][0], filename=None, folder=idea)
    except Exception as e:
        print(e)
        print(idea)
        raise Exception('error')
