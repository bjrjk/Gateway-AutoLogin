from config import *
import xencode, b64
import requests, json, hmac, hashlib

session = requests.session()

challenge_param = {
    "callback": "j",
    "username": USERNAME,
    "ip": IP
}
response = session.get("https://gw.ict.ac.cn/cgi-bin/get_challenge", params=challenge_param)
response_json = json.loads(response.text[2:-1])
token = response_json['challenge']

login_info_json = {
    "username": USERNAME,
    "password": PASSWORD,
    "ip": IP,
    "acid": "1",
    "enc_ver": "srun_bx1"
}
login_hmd5 = hmac.new(token.encode(), b"", digestmod='md5').hexdigest()
login_info = '{SRBX1}' + b64.base64(xencode.xencode(json.dumps(login_info_json).replace(" ", ""), token))
login_data = {
    "callback": "j",
    "action": "login",
    "username": USERNAME,
    "password": '{MD5}' + login_hmd5,
    "ac_id": 1,
    "ip": IP,
    "info": login_info,
    "chksum": hashlib.sha1((token + USERNAME + token + login_hmd5 + token + "1" + token + IP + token + "200" + token + "1" + token + login_info).encode()).hexdigest(),
    "n": 200,
    "type": 1
}
response = session.get("https://gw.ict.ac.cn/cgi-bin/srun_portal", params=login_data)
response_json = json.loads(response.text[2:-1])
print(response_json)