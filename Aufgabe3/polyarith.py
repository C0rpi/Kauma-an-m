import base64
from poly import Poly
from aes import AES128GCM
from math import ceil

b = base64.b64decode("OkfFRfHYf/t/PILSC706Qg==")
p = Poly(b)
assert p.p == [2, 3, 4, 6, 9, 13, 14, 15, 16, 17, 21, 23, 25, 29, 31, 32, 33, 34, 35, 39, 40, 41, 43, 44, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 62, 63, 65, 66, 67, 68, 69, 70, 71, 74, 75, 76, 77, 80, 86, 88, 89, 91, 94, 100, 102, 103, 104, 106, 107, 108, 109, 111, 114, 115, 116, 118, 121, 126] 

l = [ 4, 8, 15, 16, 23, 42 ]
p = Poly(l)
res = str(base64.b64encode(p.poly2block()),'ascii')
#assert res == 'CIGBAAAgAAAAAAAAAAAAAA==' #TODO padding
a = base64.b64decode("jjYoD6kfN+/Y/g4Hl991Cw==")
b = base64.b64decode("tQsToM4bzOQtot/1w4x8PA==")
p1 = Poly(a)
p2 = Poly(b)
p3 = p1*p2
res = base64.b64encode(bytearray(p3.poly2block()))
assert res == b"khnvYitpTW8Sv3ZUmFqasw=="

key =  Poly(base64.b64decode("/v/pkoZlcxxtao+UZzCDCA=="))
nonce=  Poly(base64.b64decode("yv66vvrO263eyviI"))
associated_data =  Poly(base64.b64decode(""))
ptb = (base64.b64decode("2TEyJfiEBuWlWQnFr/UmmoanqVMVNPfaLkwwPYoxinIcPAyVlWgJUy/PDiRJprUl"))
pt = list()
for i in range(0,len(ptb),16):
    pt.append(Poly(ptb[i:i+16]))
#cipher = AES128GCM(key,nonce,associated_data,pt)
#cts,at,y0,h = cipher.encrypt()
#print(f"cts: {cts}\nat: {at}\ny0:{y0}\nh: {h}")
#ct_out = base64.b64encode(b''.join([i.poly2block() for i in cts]))
#at_out = base64.b64encode(at.poly2block())
#y0_out = base64.b64encode(y0.poly2block()) #b'yv66vvrO263eyviIAAAAAA=='
#h_out = base64.b64encode(h.poly2block())
print()




out = {
  "ciphertext": "QoMewiF3dCRLciG3hNDUnOOqIS8sAqTgNcF+IymsoS4h1RSyVGaTHH2PalqshKoFG6MLOWoKrJc9WOCR",
  "auth_tag": "W8lPvDIhpduU+ula5xIaRw==",
  "Y0": "yv66vvrO263eyviIAAAAAQ==",
  "H": "uDtTNwi/U10KpuUpgNU7eA=="
}
inp = {
    "action": "gcm-encrypt",
    "key": "/v/pkoZlcxxtao+UZzCDCA==",
    "nonce": "yv66vvrO263eyviI",
    "associated_data": "",
    "plaintext": "2TEyJfiEBuWlWQnFr/UmmoanqVMVNPfaLkwwPYoxinIcPAyVlWgJUy/PDiRJprUl"
}

key =  Poly(base64.b64decode(inp['key']))
nonce =  Poly(base64.b64decode(inp['nonce']))
associated_data =  base64.b64decode(inp['associated_data'])
ptb = (base64.b64decode(inp['plaintext']))



print(len(ptb))

adt = list()
if not associated_data == "" or not associated_data == []:
    for i in range(0,len(associated_data),16):
        adt.append(Poly(associated_data[i:i+16]))
else:
    adt.append(Poly([]))
pt = list()
if not ptb == []:
    for i in range(0,len(ptb),16):
        pt.append(Poly(ptb[i:i+16])) 
else:
    pt.append(Poly(adt))


cipher = AES128GCM(Poly(base64.b64decode(inp['key'])),Poly(base64.b64decode(inp['nonce'])),adt,pt)
cts,at,y0,h = cipher.encrypt()
out_ct = base64.b64encode(b''.join([i.poly2block() for i in cts]))
out_at = base64.b64encode(at.poly2block())
out_y0 = base64.b64encode(y0.poly2block())
out_h = base64.b64encode(h.poly2block())
print()