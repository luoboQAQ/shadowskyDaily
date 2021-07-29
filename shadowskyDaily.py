import os
import re
import requests
import json


def send_to_wecom(text, wecom_cid, wecom_aid, wecom_secret, wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser": wecom_touid,
            "agentid": wecom_aid,
            "msgtype": "text",
            "text": {
                "content": text
            },
            "duplicate_check_interval": 600
        }
        response = requests.post(send_msg_url, data=json.dumps(data)).content
        return response
    else:
        return False


def main():
    # 通过github的secrets输入到此
    email = os.environ["SHADOWSKY_ACCOUNT"]
    psw = os.environ["SHADOWSKY_PSW"]

    shadowsky_headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    login_data = {'email': email, 'passwd': psw, 'remember_me': 'week'}
    shadowsky_session = requests.Session()
    shadowsky_login_page = shadowsky_session.post('https://www.shadowsky.fun/auth/login', headers=shadowsky_headers,
                                                  data=login_data)

    shadowsky_headers.update({'Origin': 'https://www.shadowsky.fun', 'Referer': 'https://www.shadowsky.fun/user',
                              'Accept': 'application/json, text/javascript, */*; q=0.01',
                              'X-Requested-With': 'XMLHttpRequest'})
    shadowsky_checkin_page = shadowsky_session.post(
        'https://www.shadowsky.fun/user/checkin', headers=shadowsky_headers)
    end = shadowsky_checkin_page.json()['msg']
    print(end)

    shadowsky_remaining = shadowsky_session.get(
        'https://www.shadowsky.fun/user')
    remaining = re.search(r"剩余流量: <code>(.+?)<",
                          shadowsky_remaining.text).group(1)
    remaining = "剩余流量:"+remaining
    print(remaining)

    text = "今天的签到已经完成啦QwQ"
    if send_to_wecom(text+'\n'+end+'\n'+remaining+'\n', os.environ['CORPID'], os.environ['AGENTID'], os.environ['SECRET']):
        print("企业微信推送成功")
    else:
        print("企业微信推送失败")
        exit(1)


if __name__ == "__main__":
    main()
