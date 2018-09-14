import os
import requests
import json
import random
import configure as cg
import openpyxl
from ip_pool.pool import Pool
import Recorder as rd


def spider(lock, begin, end):
    """
        begin: beggin num
        end: end num + 1
    """
    url = 'https://academic.microsoft.com/api/search/GetEntityResults'
    provider = Pool()
    wb = openpyxl.load_workbook(os.path.join(os.getcwd(), "fos.xlsx"), True)
    sheet = wb.active
    # 如果在已经爬取过，则不再爬取
    done_set = rd.get_set_done(begin, end)

    print("begin: ", begin, "| end: ", end)

    for num in range(begin, end):
        if num in done_set:
            continue
        path_res = os.path.join(os.getcwd(), 'results', str(num))
        with open(path_res, "w") as clear:
            pass
        sub = sheet["A%s" % str(num)].value.strip()

        # 错误容纳限额 -- 5分
        tolerate = 5
        for i in range(625):
            if tolerate < 1:
                lock.acquire()
                try:
                    rd.update_set_done(num, done_set=done_set, mod=2)
                finally:
                    lock.release()
                break

            rep = None
            tries = 0
            while rep is None and tries <= 10:
                tries += 1
                try:
                    rep = requests.post(url,
                                        proxies=provider.get_ip(),
                                        headers=cg.rand_header(),
                                        data=cg.data_post(subject=sub, index=i),
                                        timeout=random.choice(range(80, 180)),
                                        )
                except Exception as e:
                    print("No: ", num, " | tries:", tries, "| Subject: ", sub, " | Page: ", i, e)

            if rep is None:
                continue
            rep.encoding = 'utf-8'
            data = rep.text

            pos = data.find('{')
            data = data[pos:] if pos >= 0 else ""
            try:
                js = json.loads(data)
            # 文件为空或者错误一共减四分
            except Exception as e:
                js = None
                tolerate -= 2
                print(e)

            if js is None:
                tolerate -= 2
                continue

            publications = js['publicationResults']['publications']
            idx = 0
            print("No: ", num, "| Subject: ", sub, " | Page: ", i, " | Item: ", len(publications))
            for item in publications:
                idx = idx + 1
                tidx = i * 625 + idx
                tjson = json.dumps(item)
                restext = sub + "|" + str(i) + "|" + str(tidx)+"|" + tjson + '\n'
                with open(path_res, 'a') as f_res:
                    f_res.write(restext)

            # 数量过少， 减5分
            if len(publications) < 1:
                tolerate -= 5
            else:
                tolerate = 5
        else:
            lock.acquire()
            try:
                rd.update_set_done(num, done_set=done_set, mod=1)
            finally:
                lock.release()


# if __name__ == '__main__':
    # spider(1, 100)
