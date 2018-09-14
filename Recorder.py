import os
import json

path_record_all = os.path.join(os.getcwd(), "results", "record")


def get_set_done(begin, end):
    s = set()
    with open(path_record_all, "r", encoding="utf-8") as all:
        table = json.loads(all.read())
        for i in range(begin, end):
            if table.get(str(i), False):
                s.add(i)
    return s


def update_set_done(num, done_set, mod=5):
    done_set.add(num)
    if num % mod is 0:
        with open(path_record_all, "r", encoding="utf-8") as f:
            table = json.loads(f.read())
            for item in done_set:
                table[str(item)] = True

        with open(path_record_all, "w", encoding="utf-8") as fw:
            fw.write(json.dumps(table))


def is_Exist():
    if not os.path.exists(path_record_all):
        with open(path_record_all, "w", encoding="utf-8") as all:
            all.write("{}")

