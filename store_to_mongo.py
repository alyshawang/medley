# import pandas as pd
# from pymongo import MongoClient

# # Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["your_database"]

# # Read data from CSV file
# csv_file_path = "./47ed05b8c52efd7b4874c11486ca6224.csv"
# data = pd.read_csv(csv_file_path)
# csv_file_path = "./0e3cc9c0d06ee414e4f7000e37fe1c3c.csv"
# data = pd.read_csv(csv_file_path)
# # Convert the DataFrame to a list of dictionaries
# data_dict_list = data.to_dict(orient='records')

# # Insert data into a MongoDB collection
# collection = db["your_collection"]
# collection.insert_many(data_dict_list)

# print("Data inserted into MongoDB.")

# import pandas as pd
# from pymongo import MongoClient

# # Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["your_database"]

# # Read data from CSV files
# csv_file_paths = ["./47ed05b8c52efd7b4874c11486ca6224.csv", "./0e3cc9c0d06ee414e4f7000e37fe1c3c.csv"]

# # Prepare a set to store unique image URLs
# unique_image_urls = set()

# # Loop through each CSV file
# for csv_file_path in csv_file_paths:
#     data = pd.read_csv(csv_file_path)
    
#     # Convert the DataFrame to a list of dictionaries
#     data_dict_list = data.to_dict(orient='records')
    
#     # Filter out entries with duplicate image URLs before inserting
#     unique_data_dict_list = [item for item in data_dict_list if item['image_url'] not in unique_image_urls]
#     unique_image_urls.update(item['image_url'] for item in unique_data_dict_list)
    
#     # Insert data into the MongoDB collection
#     collection = db["your_collection"]
#     collection.insert_many(unique_data_dict_list)

# print("Data inserted into MongoDB.")

from pymongo import MongoClient
import pandas as pd
# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]

# Clear the existing collections
collections_to_clear = ["your_collection"]  # Add more collection names if needed

for collection_name in collections_to_clear:
    db[collection_name].drop()

print("Existing data cleared from MongoDB.")

# Read data from CSV files
csv_file_paths = ["./47ed05b8c52efd7b4874c11486ca6224.csv", "./0e3cc9c0d06ee414e4f7000e37fe1c3c.csv", "./48e47701cb3eb3d37209066d417357e8.csv","./90e8fe7ad3e450efdfe9d4e50f3801b7.csv", "./bfa7be10ba4d3a5bd2201d9367a31b7e.csv", "./a9bea4642e94cd5f68c4537bdf1656e4.csv"]

# Prepare a set to store unique image URLs
# unique_image_urls = set()

# # Loop through each CSV file
# for csv_file_path in csv_file_paths:
#     data = pd.read_csv(csv_file_path)
    
#     # Convert the DataFrame to a list of dictionaries
#     data_dict_list = data.to_dict(orient='records')
    
#     # Filter out entries with duplicate image URLs before inserting
#     unique_data_dict_list = []
#     for item in data_dict_list:
#         if item['image_url'] not in unique_image_urls:
#             unique_data_dict_list.append(item)
#             unique_image_urls.add(item['image_url'])

#     # Insert data into the MongoDB collection
#     collection = db["your_collection"]
#     collection.insert_many(unique_data_dict_list)

# print("New data inserted into MongoDB.")
unique_entries = set()

for csv_file_path in csv_file_paths:
    data = pd.read_csv(csv_file_path)

    # Convert the DataFrame to a list of dictionaries
    data_dict_list = data.to_dict(orient='records')

    # Filter out entries with duplicate combinations before inserting
    unique_data_dict_list = []
    for item in data_dict_list:
        entry_tuple = (item['title'], item['image_url'], item['price'])
        if entry_tuple not in unique_entries:
            unique_data_dict_list.append(item)
            unique_entries.add(entry_tuple)
        else:
            print(f"Duplicate entry found: {entry_tuple}")

    # Insert data into the MongoDB collection
    collection = db["your_collection"]
    collection.insert_many(unique_data_dict_list)

print("New data inserted into MongoDB.")
