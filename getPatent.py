import os
import requests
import json
import random
import configure as cg
import openpyxl
from ip_pool.auto_pool import get_ip
import Recorder as rd
from Logger import get_logger
import warnings
warnings.filterwarnings("ignore")

logger = get_logger()


def spider(lock, begin, end):
    """
        begin: beggin num
        end: end num + 1
    """
    url = 'https://academic.microsoft.com/api/search/GetEntityResults'
    # provider = Pool()
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
        # 初始容错分：5分
        tolerate = 5
        for i in range(625):
            if tolerate < 1:
                if 10 >= i:
                    rd.update_set_done(lock, num, done_set=done_set, mod=1)
                elif 3 <= i < 9:
                    rd.update_set_done(lock, num, done_set=done_set, mod=2)
                else:
                    rd.update_set_done(lock, num, done_set=done_set, mod=5)
                break

            tries = 0
            rep = None
            while rep is None and tries <= 10:
                tries += 1
                try:
                    rep = requests.post(url,
                                        # proxies=provider.get_ip(),
                                        proxies=get_ip(),
                                        headers=cg.rand_header(),
                                        data=cg.data_post(subject=sub, index=i),
                                        timeout=random.choice(range(80, 180)),
                                        verify=False
                                        )
                except Exception as e:
                    rep = None
                    logger.error(
                        "No: " + str(num) + " | tries:" + str(tries) + " | Subject: " + sub + " | Page: " + str(i) + " | " + str(e))

            if rep is None:
                continue
            rep.encoding = 'utf-8'
            data = rep.text

            pos = data.find('{')
            data = data[pos:] if pos >= 0 else ""
            try:
                js = json.loads(data)
            except Exception as e:
                js = None
                tolerate -= 1
                logger.error(
                    "No: " + str(num) + " | tries:" + str(tries) + " | Subject: " + sub + " | Page: " + str(i) + " | " +str(e))

            if js is None:
                tolerate -= 1
                continue

            publications = js['publicationResults']['publications']
            idx = 0
            logger.info("No: " + str(num) + " | Subject: " + sub + " | Page: " + str(i) + " | Item: " + str(len(publications)))

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
            rd.update_set_done(lock, num, done_set=done_set, mod=1)
