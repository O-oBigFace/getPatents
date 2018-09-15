from getPatent import spider
from multiprocessing import Process, Lock
import sys
import time

if __name__ == '__main__':
    lock = Lock()
    begin = int(sys.argv[1])
    end = int(sys.argv[2])
    num_of_ps = int(sys.argv[3])

    count = end - begin
    quarter = count // num_of_ps

    arglist = [(lock, begin + i * quarter, begin + (i + 1) * quarter) for i in range(num_of_ps)]
    print(arglist)

    for arg in arglist:
        process = Process(target=spider, args=arg)
        process.start()
        time.sleep(3)
