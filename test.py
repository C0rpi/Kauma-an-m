from util.kauma_util import json_parser
import json
from Aufgabe3.CZPoly import CZPoly

file = "Aufgabe3/test/gcmrecover.json"
with open(file) as f: inp = json.loads(f.read())['result']
out = json_parser(file)
print(out)
print(inp)
assert json.loads(out)['result'] == inp
