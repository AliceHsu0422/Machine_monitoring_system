import sys
import random
import time
def test_chip(test_time):
    ## test_case_1~3
    f=open(sys.argv[1]+'.log',"a")
    f.write("start testing\n")
    f.close()
    for test_case in range(1,4):
        for test_num in range(1,101):
            f=open(sys.argv[1]+'.log',"a")
            time.sleep(test_time)
            rand=int(random.random()*600) #random 0~600
            if rand>=2 and rand<=560:
                f.write("test_case:"+str(test_case)+" WIP_number:"+str(test_num)+" -> pass\n")
            elif rand==1:
                f.write("system error\n")
                f.close()
                return
            else:
                f.write("test_case:"+str(test_case)+" WIP_number:"+str(test_num)+" -> fail\n")
            f.close()
    f=open(sys.argv[1]+'.log',"a")
    f.write("finish testing\n")
    f.close()



f=open(sys.argv[1]+'.log',"w")
f.close()
test_time = 0
if sys.argv[1] == "tester_a":
    test_time = 5
elif sys.argv[1] == "tester_b":
    test_time = 10
elif sys.argv[1] == "tester_c":
    test_time = 7

test_chip(test_time)