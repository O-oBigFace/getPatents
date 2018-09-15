import os
import requests
import json
import random
import configure as cg
import openpyxl
from ip_pool.auto_pool import get_ip
import Recorder as rd
from Logger import get_logger
import time
import warnings
warnings.filterwarnings("ignore")
import logging
logger = get_logger()


def spider(lock, begin, end):
    """
        begin: beggin num
        end: end num + 1
    """
    url = 'https://academic.microsoft.com/api/search/GetEntityResults'
    wb = openpyxl.load_workbook(os.path.join(os.getcwd(), "fos.xlsx"), True)
    sheet = wb.active
    done_set = rd.get_set_done(lock, begin, end)

    logger.info("begin: " + str(begin) + " | end: " + str(end))

    for num in range(begin, end):
        if num in done_set:
            continue
        path_res = os.path.join(os.getcwd(), 'results', str(num))
        with open(path_res, "w") as clear:
            pass
        sub = sheet["A%s" % str(num)].value.strip()
        # 给予每个页面初始容错分：5分
        tolerate = 5

        # i 表示页码
        for i in range(625):

            # 结束条件之一：该页面容错分被扣完
            if tolerate < 1:
                if 10 >= i:
                    rd.update_set_done(lock, num, done_set=done_set, mod=1)
                elif 3 <= i < 9:
                    rd.update_set_done(lock, num, done_set=done_set, mod=2)
                else:
                    rd.update_set_done(lock, num, done_set=done_set, mod=10)
                break

            """
            接收不到页面一般为网络故障,这里给予其十次容故障机会
            有两种情况被认为是网络故障：
            1. 网络连接失败，此时rep为初始值None
            2. rep收到空数据包
            """
            tries = 0
            rep = None
            while rep is None and tries <= 10:
                tries += 1
                try:
                    # rep 为post对象
                    rep = requests.post(url,
                                        proxies=get_ip(),
                                        headers=cg.rand_header(),
                                        data=cg.data_post(subject=sub, index=i),
                                        timeout=random.choice(range(80, 180)),
                                        verify=False
                                        )
                    rep.encoding = 'utf-8'
                    if rep.status_code in [200, 503]:
                        break
                    elif rep.status_code == 429:
                        time.sleep(3)
                        continue
                except Exception as e:
                    logger.error("No: %d | tries: %d | Subject: %s | Page: %d | %s | Net Error" %
                                 (num, tries, sub, i, str(e)))

            # 若重试10次以后仍有故障, 换主题
            if rep is None:
                tolerate -= 100
                logger.error("No: %d | tries: %d | Subject: %s | Page: %d | MAX_TRY" %
                             (num, tries, sub, i))
                continue

            data = rep.text
            pos = data.find('{')
            data = data[pos:] if pos >= 0 else ""
            try:
                js = json.loads(data)
            except Exception as e:
                js = None
                tolerate -= 2
                logger.error(
                    "No: %d | Subject: %s | Page: %d | %s | JSONParse Error" %
                    (num, sub, i, str(e)))

            if js is None:
                tolerate -= 4
                continue

            publications = js['publicationResults']['publications']
            idx = 0
            logger.info("No: %d | Subject: %s | Page: %d | Item: %d" % (num, sub, i, len(publications)))

            for item in publications:
                idx = idx + 1
                tidx = i * 625 + idx
                tjson = json.dumps(item)
                restext = sub + "|" + str(i) + "|" + str(tidx)+"|" + tjson + '\n'
                with open(path_res, 'a') as f_res:
                    f_res.write(restext)

            if len(publications) < 1:
                tolerate -= 5
            else:
                tolerate = 5

        else:
            # 切换主题条件之二：主题页面数目超过阈值
            rd.update_set_done(lock, num, done_set=done_set, mod=1)

# if __name__ == '__main__':
