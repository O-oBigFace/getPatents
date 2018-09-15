import os
import json

# 记录所有
path_record_all = os.path.join(os.getcwd(), "results", "record")


# 获得已经完成的文件列表
def get_set_done(lock, begin, end):
    # is_Exist()
    s = set()
    lock.acquire()
    try:
        with open(path_record_all, "r", encoding="utf-8") as all:
            table = json.loads(all.read())
            for i in range(begin, end):
                if table.get(str(i), False):
                    s.add(i)
    finally:
        lock.release()
    return s


def update_set_done(lock, num, done_set, mod=5):
    done_set.add(num)
    if num % mod is 0:
        lock.acquire()
        try:
            with open(path_record_all, "r", encoding="utf-8") as f:
                table = json.loads(f.read())
                for item in done_set:
                    table[str(item)] = True
            with open(path_record_all, "w", encoding="utf-8") as fw:
                fw.write(json.dumps(table))
        finally:
            lock.release()


def is_Exist():
    if not os.path.exists(path_record_all):
        with open(path_record_all, "w", encoding="utf-8") as all:
            all.write("{}")


#  汇总所有record
#  步骤：将左右的record文件放入record文件夹中，运行此函数
def merage_all_record():
    with open(os.path.join(os.getcwd(), 'results', "record"), 'r', encoding="utf-8") as rf:
        a_record = json.loads(rf.read())

    for record_name in os.listdir(os.path.join(os.getcwd(), "record")):
        path = os.path.join(os.getcwd(), 'record', record_name)
        print(path)
        with open(path, 'r', encoding='utf-8') as f:
            tb = json.loads(f.read())
            for key, value in tb.items():
                a_record[key] = value
    print(len(a_record))
    with open(os.path.join(os.getcwd(), 'results', "record"), 'w', encoding="utf-8") as wf:
        wf.write(json.dumps(a_record))

# 手动运行函数
def get_undone(begin, end):
    count = 0
    with open(path_record_all, "r", encoding="utf-8") as all:
        table = json.loads(all.read())
        for i in range(begin, end):
            if not table.get(str(i), False):
                count += 1
    print(count)


# 修复record文件，需要将collect文件夹移动到项目中
def recover():
    with open(path_record_all, 'r', encoding="utf-8") as f:
        all = json.loads(f.read())

    for key, value in all.items():
        if key not in os.listdir(os.path.join(os.getcwd(), "collect")):
            all[key] = False
    with open(path_record_all, 'w', encoding="utf-8") as f:
        f.write(json.dumps(all))


# 根据现有的数据备份record文件
def backup():
    with open(path_record_all, 'r', encoding="utf-8") as f:
        all = json.loads(f.read())
    for file_name in os.listdir(os.path.join(os.getcwd(), "results")):
        if file_name == "record":
            continue
        with open(os.path.join(os.getcwd(), "results", file_name)) as fruit:
            if len(fruit.read()) > 1:
                all[file_name] = True
    with open(path_record_all, 'w', encoding="utf-8") as f:
        f.write(json.dumps(all))

if __name__ == '__main__':
    backup()
