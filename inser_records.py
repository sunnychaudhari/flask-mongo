from pymongo import MongoClient

try:
	conn = MongoClient()
	print("Connected successfully!!!")
except:
	print("Could not connect to MongoDB")

db = conn.ecom_db
collection = db.products

prod1 = {"name":"Monte Carlo","color":"green","price":1100}
prod2 = {"name":"Arrow","color":"yellow","price":800}
prod3 = {"name":"GAP","color":"white","price":1200}
prod4 = {"name":"Tantra","color":"yellow","price":1400}
prod5 = {"name":"Tommy Hilfiger","color":"green","price":2000}

collection.insert_one(prod1)
collection.insert_one(prod2)
collection.insert_one(prod3)
collection.insert_one(prod4)
collection.insert_one(prod5)

print("Data inserted Successfully")

# Printing the data inserted
cursor = collection.find()
for record in cursor:
	print(record)
