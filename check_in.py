
import re
import requests
import time
import logging
import os
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_path = os.path.split(__file__)[0]
file_handler = logging.FileHandler(os.path.join(file_path, 'log.log'))
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def main():

    cookie = '''fill in your v2ex cookie'''

    base_url = 'https://www.v2ex.com'
    daily_mission_url = '/mission/daily'
    sign_rul = '/mission/daily/redeem?once={}'

    headers = {
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    }

    session = requests.session()
    r = requests.get(base_url + daily_mission_url, headers=headers)
    content = r.content.decode()

    re1 = re.match(
        r'''.*onclick="location\.href = \'/mission/daily/redeem\?once=(\d+).*''', content, re.S)
    once = re1.group(1)
    print('once: ', once)

    url = base_url + sign_rul.format(once)
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        write_log("签到成功！")
    else:
        write_log("签到失败！")


def write_log(msg):
    logger.info(msg)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        write_log(f'run failed. error: {e}')
