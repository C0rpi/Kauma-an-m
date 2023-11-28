from util.kauma_util import json_parser
import json


file = "Aufgabe3/test/gcmpolypowmod.json"
with open(file) as f: inp = json.loads(f.read())['result']
out = json_parser(file)
print(out)
print(inp)
assert json.loads(out)['result'] == inp
