from getPatent import spider, spider_none
from multiprocessing import Process, Lock
import time
import Recorder
import sys

if __name__ == '__main__':

    arglist = Recorder.cut_list(Recorder.get_num_none(), int(sys.argv[1]))

    print(len(arglist))

    for arg in arglist:
        process = Process(target=spider_none, args=[arg])
        process.start()
        time.sleep(3)
