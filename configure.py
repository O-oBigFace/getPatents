import random
from ip_pool.agents import agents


def rand_header():
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': random.choice(agents),
        'Cookie': 'A=I&I=AxUFAAAAAADcBgAAppxkMXdDMh8WbdW6REgxYA!!&V=4; MC1=GUID=b696858225fe44c09863f86e57fa4c09' + str(random.randint(100, 200)) + '&HASH=b696&LV=201802&V=4&LU=1519437260089; MUID=04435427E0D767D039295F68E4D76468; msacademic=143996b2-ae82-4969-b7ce-6130b0cf5bab; ai_user=lXzhe|2018-07-12T02:39:50.922Z; _ga=GA1.2.1293331498.1532580770; optimizelyEndUserId=oeu1533104931073r0.32495626027565705; _gid=GA1.2.656390118.1536651064; MS-CV=hOV9oOG+lEq5qhM7.1; ARRAffinity=9a0da02f1d53d0f9874c7a700758edc589bffa9ac51b6216b0d6687ec58ee90f; ai_session=GG8NK|1536709208620|1536709262678',
    }


def data_post(subject, index):
    return {
        'Query':  "Composite(F.FN == '%s')" % subject.strip(),
        'Filters': "Pt = '2'",
        'Limit': 8,
        'Offset': index * 8,
        'OrderBy': '',
        'SortAscending': 'false'
    }


if __name__ == '__main__':
    print(data_post("cs", 1))
