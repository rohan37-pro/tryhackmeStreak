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
i = 1
# for flag in subrata[:-1]:
#     print("==>",i)
#     flag = flag.replace(chr(92), r"\\")
#     print(flag,'\n')
#     ob = json.loads(flag)
#     subrata_flags[i] = ob
    
#     print(json.dumps(ob, indent=4))
#     i+=1

# with open("subrata_flags.json", 'w') as file:
#     json.dump(subrata_flags, file, indent=4)




# the parameter is json file name
# def marge(file):
#     global flags_no
#     with open(file, 'r') as file:
#         object = json.load(file)
    
#     flags_no += 1
#     for i in object:
#         if object[i] not in thm.values():
#             thm[flags_no] = object[i]
#             flags_no+=1
#     print(f"tatol flags added = {flags_no}")
#     with open("THM_flags.json", 'w') as file:
#         json.dump(thm, file, indent=4)

# marge("souman_flags.json")
# marge("subrata_flags.json")