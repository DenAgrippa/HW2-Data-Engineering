import json
import msgpack
import os

def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)



products = read_json("./data/third_task.json")
products_stat = {}

for product in products:
    name = product['name']
    price = product['price']
    if name not in products_stat:
        products_stat[name] = {
            'name': name,
            'max_price': price,
            'min_price': price,
            'avg_price': price,
            'amount': 1,
        }
    if name in products_stat:
        products_stat[name]['amount'] += 1
        products_stat[name]['avg_price'] += price
        if price > products_stat[name]['max_price']:
            products_stat[name]['max_price'] = price
        if price < products_stat[name]['min_price']:
            products_stat[name]['min_price'] = price

for product in products_stat:
    products_stat[product]['avg_price'] /= products_stat[product]['amount']

to_save = list(products_stat.values())

with open("./results/third_task_result.json", "w", encoding="utf-8") as f:
    json.dump(to_save, f, ensure_ascii=False)

with open("./results/third_task_result.msgpack", "wb") as f:
    msgpack.dump(to_save, f)

json_size = os.path.getsize("./results/third_task_result.json")
msgpack_size = os.path.getsize("./results/third_task_result.msgpack")

print(json_size)
print(msgpack_size)
print(json_size - msgpack_size)