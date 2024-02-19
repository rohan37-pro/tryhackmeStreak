import json

## open souman.txt
with open("souman.txt", 'r') as file:
    souman = file.read()

## open subrata.txt
with open("subrata.txt", 'r') as file:
    subrata = file.read()

## open THM_flags.json
with open("THM_flags.json", 'r') as file:
    thm = json.load(file)

souman = souman.split("@#$")
subrata = subrata.split("@#$")
souman_flags = {}
subrata_flags = {}
souman_flags_len = len(souman)

flags_no = len(thm)
print(flags_no)
for i in range(18):
    s = json.loads(souman[i])
    print(json.dumps(s, indent=4))
    print(type(s))