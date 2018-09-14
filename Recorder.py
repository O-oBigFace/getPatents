import os
import json

path_record_all = os.path.join(os.getcwd(), "results", "record")


def get_set_done(lock, begin, end):
    is_Exist()
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

