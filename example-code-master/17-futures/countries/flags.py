"""Download flags of top 20 countries by population

Sequential version

Sample run::

    $ python3 flags.py
    BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN
    20 flags downloaded in 10.16s

"""
# BEGIN FLAGS_PY
import os
import time
import sys

import requests  # <1>

# 这里给了我一点启发，就是我之前也是想自己手打一个很长的数组，发现，数组里面的每一项都是自己手打的，但是现在
# 原来我可以先搞一个字符串，然后对字符串进行处理，生成一个数组，我之前的做法真的是。
POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()  # <2>

BASE_URL = 'http://flupy.org/data/flags'  # <3>

DEST_DIR = 'downloads'  # <4>


def save_flag(img, filename):  # <5>
    if not os.path.exists(os.path.join(os.path.dirname(__file__),DEST_DIR)):
        os.mkdir(os.path.join(os.path.dirname(__file__),DEST_DIR))
    path = os.path.join(os.path.dirname(__file__), DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc):  # <6>
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    # request库能够下载这个链接，下载的链接的内容就在content里面，而且是二进制类型的
    resp = requests.get(url)
    return resp.content


def show(text):  # <7>
    print(text, end=' ')
    sys.stdout.flush()


def download_many(cc_list):  # <8>
    for cc in sorted(cc_list):  # <9>
        image = get_flag(cc)
        # 打印国家的名称，为什么要这样做？
        show(cc)
        save_flag(image, cc.lower() + '.gif')

    return len(cc_list)


def main(download_many):  # <10>
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many)  # <11>
# END FLAGS_PY
