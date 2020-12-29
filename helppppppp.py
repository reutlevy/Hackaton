# !/usr/bin/env python3
from readchar import readchar


def getchar():
    print("heloooooo")
    ch = readchar()
    if ord(ch) == 3 or ord(ch) == 4:
        return False
    print("heloooooo1")
    return ch

ch = getchar()
print('You pressed', ch)

while not ch is False:
    ch = getchar()
    print('You pressed', ch)