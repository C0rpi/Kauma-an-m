import matplotlib.pyplot as plot
from base64 import b64decode
import Tools.benchmark as b
import json 
from hashlib import sha256
import random
from base64 import b64decode

#creates a plot from the output of our b'\0'*2*20
#diagrams were generated seperately
def show_bar():
    rotor = [i for i in range(0,256)]
    
    #test 1 rotor
    out = b.bytenigma(list(b'\0'*2**20), [random.sample(rotor,256)] )
    out = list(out)
    plot.hist(out,255)
    plot.show()

    #test 2 rotors
    out = b.bytenigma(list(b'\0'*2**20), [random.sample(rotor,256),random.sample(rotor,256)])
    out = list(out)
    plot.hist(out,255)
    plot.show()

    #test 3 rotors
    out = b.bytenigma(list(b'\0'*2**20), [random.sample(rotor,256) for i in range(0,2)])
    out = list(out)
    plot.hist(out,255)
    plot.show()

    #test 10 rotors
    out = b.bytenigma(list(b'\0'*2**20), [random.sample(rotor,256) for i in range(0,9)])
    out = list(out)
    plot.hist(out,255)
    plot.show()

    #10rotors but everything is 0..255
    out = b.bytenigma(list(b'\0'*2**20), [rotor for i in range(0,10)])
    out = list(out)
    plot.hist(out,255)
    plot.show()

    #10rotors but the first is 0..255 with the remaining random
    out = b.bytenigma(list(b'\0'*2**20), [rotor] + [random.sample(rotor,256) for i in range(0,9)])
    out = list(out)
    plot.hist(out,255)
    plot.show()

    #10rotors with small input
    test = bytes("abcdefghij",'ascii')
    out = b.bytenigma(list(test), [random.sample(rotor,256) for i in range(0,10)])
    out = list(out)
    plot.hist(out,255)
    plot.show()
    
    #10rotors with b'\0'*
    out = b.bytenigma(list(b'\0'*100), [random.sample(rotor,256) for i in range(0,10)])
    out = list(out)
    plot.hist(out,255)
    plot.show()

    #10rotors with 100 word input
    test = b64decode("TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNldGV0dXIgc2FkaXBzY2luZyBlbGl0ciwgc2VkIGRpYW0gbm9udW15IGVpcm1vZCB0ZW1wb3IgaW52aWR1bnQgdXQgbGFib3JlIGV0IGRvbG9yZSBtYWduYSBhbGlxdXlhbSBlcmF0LCBzZWQgZGlhbSB2b2x1cHR1YS4gQXQgdmVybyBlb3MgZXQgYWNjdXNhbSBldCBqdXN0byBkdW8gZG9sb3JlcyBldCBlYSByZWJ1bS4gU3RldCBjbGl0YSBrYXNkIGd1YmVyZ3Jlbiwgbm8gc2VhIHRha2ltYXRhIHNhbmN0dXMgZXN0IExvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0LiBMb3JlbSBpcHN1bSBkb2xvciBzaXQgYW1ldCwgY29uc2V0ZXR1ciBzYWRpcHNjaW5nIGVsaXRyLCBzZWQgZGlhbSBub251bXkgZWlybW9kIHRlbXBvciBpbnZpZHVudCB1dCBsYWJvcmUgZXQgZG9sb3JlIG1hZ25hIGFsaXF1eWFtIGVyYXQsIHNlZCBkaWFtIHZvbHVwdHVhLiBBdCB2ZXJvIGVvcyBldCBhY2N1c2FtIGV0IGp1c3RvIGR1byBkb2xvcmVzIGV0IGVhIHJlYnVtLiBTdGV0IGNsaXRhIGthc2QgZ3ViZXJncmVuLCBubyBzZWEgdGFraW1hdGEgc2FuY3R1cyBlc3QgTG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQu")
    out = b.bytenigma(list(test), [random.sample(rotor,256) for i in range(0,10)])
    out = list(out)
    plot.hist(out,255)
    plot.show()

    #10rotors but everyone is identical and random 
    r = random.sample(rotor,256)
    out = b.bytenigma(list(b'\0'*2**20), [r for i in range(0,10)])
    out = list(out)
    plot.hist(out,255)
    plot.show() 
    print()

show_bar()