from data_base.data_childs import childs, get_balance, set_balance
import json

with open(f"./data_base/data_groups.json", "r", encoding="utf-8") as f:
    groups = json.load(f)
'''
groups = {
    1: {
        "group": "ОГЭ математика",
        "zoom": "https://us05web.zoom.us/j/78289857291?pwd=K2lVaHlDK0I2b3Bzdllxa2xEVXo4UT09",
        "tm_gr": "N/a",
        "participants": [
            childs[1],
        ]
    },
    2: {
        "group": "ОГЭ информатика",
        "zoom": "https://us05web.zoom.us/j/74787987569?pwd=ekVZK2N3c2F4MmFwQVBPeXNUN0p2Zz09",
        "tm_gr": "N/a",
        "participants": [
            childs[1],
            childs[2],
        ]
    },
}
'''

#get_balance(groups["1"]["participants"])

if __name__ == "__main__":
    a = groups[2]["participants"]
    print(a)