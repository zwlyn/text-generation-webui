# coding=utf8



def baidu_fanyi(query):
    import requests 
    import hashlib
    import random
    appid = '20231101001865770'  # 你的appid
    secretKey = 'kQWTOQoNTfCIxPEUsPVW'  # 你的密钥
    salt = random.randint(1, 10)  # 随机数
    code = appid + query + str(salt) + secretKey
    sign = hashlib.md5(code.encode()).hexdigest()  # 签名
    api = "http://api.fanyi.baidu.com/api/trans/vip/translate"
    data = {
        "q": query,
        "from": "auto",
        "to": "auto",
        "appid": appid,
        "salt": salt,
        "sign": sign
    }
    response = requests.post(api, data)
    print(response.text)
    try:
        result = response.json()
        dst = result.get("trans_result")[0].get("dst")
        print(result)
    except Exception as e:
        print(e)
        dst = query
    finally:
        return dst
if __name__ == '__main__':
    query ="科学家的发现：女性科学家在实验室中的发现。"
    ret = baidu_fanyi(query)
    print(ret)
    # 苹果