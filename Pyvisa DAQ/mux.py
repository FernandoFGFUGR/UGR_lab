import pyfirmata
import time

board = pyfirmata.Arduino('COM9')

board.digital[6].write(0)
board.digital[8].write(1)

while True:
    
    print("Introduce num: ")
    r=input()
    temp = '{0:04b}'.format(int(r))
    print(temp[0]+temp[1]+temp[2])
    board.digital[2].write(int(temp[0]))
    board.digital[3].write(int(temp[1]))
    board.digital[4].write(int(temp[2]))
    board.digital[5].write(int(temp[3]))

    time.sleep(5)



