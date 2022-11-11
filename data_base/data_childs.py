import json

with open(f"./data_base/data_childs.json", "r", encoding="utf-8") as f:
    childs = json.load(f)
'''childs = [
    {},
    {
        "user_id": 1,
        "name": "Vanya",
        "nick": "@vazelinio",
        "balance": 0,
        "parent": "05-Юлия мама Вани",
        "dates": {
            "plus": [
                "2022-11-01",
            ],
            "minus": [
                "2022-11-01",
                "2022-11-02",
            ]
        }
    },
    {
        "user_id": 2,
        "name": "Muhammad",
        "nick": None,
        "balance": 0,
        "parent": "Мадина",
        "dates": {
            "plus": [],
            "minus": []
        }
    }
]'''
def get_balance(id):
    dates_plus = childs[id]["dates"]["plus"]*4 
    dates_minus = childs[id]["dates"]["minus"]
    pcs = len(dates_plus)-len(dates_minus)
    return pcs

def set_balance(id,date,count):
    if count > 0:
        childs[id]["dates"]["plus"].append(date)
    else:
        childs[id]["dates"]["minus"].append(date)
    with open(f"./data_base/data_childs.json", "w", encoding="utf-8") as f:
        json.dump(childs, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":

    a = get_balance(1)
    set_balance(1, "2022-12-1",-1)
    print(a)
