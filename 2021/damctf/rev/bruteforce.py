#!/usr/bin/env python3
import sys
import time
import random
import hashlib

def seed():
    return round(time.time())

def hash(text):
    return hashlib.sha256(str(text).encode()).hexdigest()

def main():
    s = 1636167332 # start at contest begin
    
    seen_before = 0.1448081453121044
    while True:
        random.seed(s, version=2)

        x = random.random()
        if(x == seen_before):
            print(s)
            break
        else:
            s -= 1


if __name__ == "__main__":
   sys.exit(main())
