import os
import csv
import json
import msgpack
import pickle
import math

def read_csv(path):
    data = []

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['reviews_per_month'] == '':
                row['reviews_per_month'] = '0'
            data.append({
                'id': int(row['id']),
                'name': row['name'],
#                'host_id': int(row['host_id']),
                'host_name': row['host_name'],
#                'neighbourhood_group': row['neighbourhood_group'],
#                'neighbourhood': row['neighbourhood'],
#                'latitude': float(row['latitude']),
#                'longitude': float(row['longitude']),
                'room_type': row['room_type'],
                'price': int(row['price']),
                'minimum_nights': int(row['minimum_nights']),
                'number_of_reviews': int(row['number_of_reviews']),
#                'last_review': row['last_review'],
                'reviews_per_month': float(row['reviews_per_month']),
#                'calculated_host_listings_count': int(row['calculated_host_listings_count']),
                'availability_365': int(row['availability_365']),
#                'number_of_reviews_ltm': int(row['number_of_reviews_ltm']),
                'city': row['city'],
            })
    
    return data

def write_report(path, report):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f)

def save_to_files(path, data):
    with open(f"{path}.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    
    dictionary = {}
    for item in data:
        key = item['id']
        value = item.copy()
        del value['id']
        dictionary[key] = value
    with open(f"{path}.json", "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False)

    with open(f"{path}.msgpack", "wb") as f:
        msgpack.dump(dictionary, f)

    with open(f"{path}.pkl", "wb") as f:
        pickle.dump(dictionary, f)


data = read_csv("./data/AB_US_2023.csv")

size = len(data)

sums = {
    'price': 0,
    'minimum_nights': 0,
    'number_of_reviews': 0,
    'reviews_per_month': 0,
    'availability_365': 0,
}

maxs = {
    'price': data[0]['price'],
    'minimum_nights': data[0]['minimum_nights'],
    'number_of_reviews': data[0]['number_of_reviews'],
    'reviews_per_month': data[0]['reviews_per_month'],
    'availability_365': data[0]['availability_365'],
}

mins = {
    'price': data[0]['price'],
    'minimum_nights': data[0]['minimum_nights'],
    'number_of_reviews': data[0]['number_of_reviews'],
    'reviews_per_month': data[0]['reviews_per_month'],
    'availability_365': data[0]['availability_365'],
}

avgs = {
    'price': 0,
    'minimum_nights': 0,
    'number_of_reviews': 0,
    'reviews_per_month': 0,
    'availability_365': 0,
}

stdevs = {
    'price': 0,
    'minimum_nights': 0,
    'number_of_reviews': 0,
    'reviews_per_month': 0,
    'availability_365': 0,
}

freqs = {
    'host_name': {},
    'room_type': {},
    'city': {},
}

for item in data:
    for key, value in item.items():
        if key in sums:
            sums[key] += value
        
        if key in maxs:
            if value > maxs[key]:
                maxs[key] = value
        
        if key in mins:
            if value < mins[key]:
                mins[key] = value
        
        if key in freqs:
            if value not in freqs[key]:
                freqs[key][value] = 1
            if value in freqs[key]:
                freqs[key][value] += 1

for key, value in avgs.items():
    avgs[key] = sums[key] / size

for item in data:
    for key, value in item.items():
        if key in stdevs:
            stdevs[key] += pow((value - avgs[key]), 2)

for key, value in stdevs.items():
    stdevs[key] = math.sqrt(value / size)

for item in freqs.values():
    for key, value in item.items():
        item[key] = value / size


""" print(sums)
print(maxs)
print(mins)
print(freqs)
print(stdevs) """

report = {
    'sums': sums,
    'maximums': maxs,
    'minimums': mins,
    'averages': avgs,
    'standart_deviations': stdevs,
    'frequencies': freqs
}

write_report("./results/fifth_task_result_report.json", report)
save_to_files("./results/fifth_task_result_dataset", data)

json_size = os.path.getsize("./results/fifth_task_result_dataset.json")
msgpack_size = os.path.getsize("./results/fifth_task_result_dataset.msgpack")
csv_size = os.path.getsize("./results/fifth_task_result_dataset.csv")
pickle_size = os.path.getsize("./results/fifth_task_result_dataset.pkl")

print(f"json: {json_size},\ncsv: {csv_size},\nmsgpack: {msgpack_size},\npickle: {pickle_size}")