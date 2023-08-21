
from pymongo import MongoClient
import pandas as pd
# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]

# clear the existing collections
collections_to_clear = ["your_collection"] 

for collection_name in collections_to_clear:
    db[collection_name].drop()

print("Existing data cleared from MongoDB.")

# read data from CSV files
csv_file_paths = ["../csv/47ed05b8c52efd7b4874c11486ca6224.csv", "../csv/0e3cc9c0d06ee414e4f7000e37fe1c3c.csv", "../csv/48e47701cb3eb3d37209066d417357e8.csv","../csv/90e8fe7ad3e450efdfe9d4e50f3801b7.csv", "../csv/bfa7be10ba4d3a5bd2201d9367a31b7e.csv", "../csv/a9bea4642e94cd5f68c4537bdf1656e4.csv"]

unique_entries = set()

for csv_file_path in csv_file_paths:
    data = pd.read_csv(csv_file_path)

    # convert DataFrame to a list of dictionaries
    data_dict_list = data.to_dict(orient='records')
    if csv_file_path in [ "../csv/a9bea4642e94cd5f68c4537bdf1656e4.csv"]:
        brand = "Stussy"
    else:
        brand = "Brandy Melville"

    # brand field for each entry
    for item in data_dict_list:
        item['brand'] = brand
    # filter out duplicates
    unique_data_dict_list = []
    for item in data_dict_list:
        entry_tuple = (item['title'], item['image_url'], item['price'])
        if entry_tuple not in unique_entries:
            unique_data_dict_list.append(item)
            unique_entries.add(entry_tuple)
        else:
            print(f"Duplicate entry found: {entry_tuple}")

    # insert data into MongoDB 
    collection = db["your_collection"]
    collection.insert_many(unique_data_dict_list)

print("New data inserted into MongoDB.")
