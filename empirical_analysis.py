import matplotlib.pyplot as plot
from base64 import b64decode
import Tools.benchmark as b
import json 
from hashlib import sha256
import random

#creates a plot from the output of our b'\0'*2*20
def show_bar():
    with open("tests/test1.json") as file: input = json.loads(file.read())
    rotors = input['rotors']
    out = b.bytenigma(list(b'\0'*2**20), rotors)
    assert sha256(out).hexdigest() == '306a58f1d0589ec1ff4af1637e76774957389aa6152b6e04d6b389b1980efa8c'
    out = list(out)
    plot.hist(out,255)
    plot.show()


show_bar()