from kafka import KafkaConsumer
import os
import pymongo
import json 

def check_overlap(list1, list2):
  # Convert lists to sets for faster intersection operation
  set1 = set(list1)
  set2 = set(list2)
  
  # Check for intersection
  if set1.intersection(set2):
    return True
  else:
    return False
  
def consume(): 
  kafka_service = os.environ.get("kafka_service")
  kafka_topic = os.environ.get("kafka_topic")
  mongo_url = os.environ.get("mongo_url")
  db_name = os.environ.get("db_name")
  collection_name = os.environ.get("collection_name")

  client = pymongo.MongoClient(mongo_url)
  db = client[db_name]
  collection = db[collection_name]
  users = list(collection.find())

  consumer = KafkaConsumer(
    bootstrap_servers=kafka_service,
    value_deserializer=json.loads,
    auto_offset_reset="latest",
  )

  consumer.subscribe(kafka_topic)

  while True:
    data = next(consumer)
    for user in users:
      if check_overlap(data["keywords"], user["notify_about"]):
        notifi = user.get("notifications", [])
        notifi.append({'id':data['id'], 'title':data["title"]})
        collection.update_one({"_id": user["_id"]}, {"$push": {"notification": notifi}})
  
  
consume()