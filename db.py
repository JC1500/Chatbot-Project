from pymongo import MongoClient,ASCENDING
from pymongo.server_api import ServerApi
import os
from typing import List,Dict
from langchain_core.messages import BaseMessage,HumanMessage,AIMessage
from bson import Binary
import uuid

client=MongoClient(os.getenv("MONGO_URI"),server_api=ServerApi('1',strict=True))
database=client['FIRSTdb']['ModelStore']


def push_to_store(session_id: str, chat_id: int, chat: List[Dict[str, str]], user_email: str):
   try:
      database.insert_one({
          "user_email": user_email,
          "chat_id": chat_id,
          "session_id": session_id,
          "chat": chat
      })
   except Exception as e:
      print(e)
   
def get_from_store(session_id: str, user_email: str) -> List[Dict[str, str]]:
   # Ensure users can only query their own data
   l = database.find({'session_id': session_id, 'user_email': user_email}, sort={"name": ASCENDING})
   ret = []
   for obj in l:
      ret.extend(obj['chat'])
   return ret

def get_user_sessions(user_email: str) -> List[str]:
   # Optional: Fetch all unique session IDs belonging to this specific user
   with database.find({"user_email": user_email}) as  cus:
      s=set()
      for doc in cus:
         s.add(doc['session_id'])
      return list(s)
   
if(__name__=='__main__'):
   l=[{
      'human':'hi',
      'ai':'hello'
   }]
   try:
      client.admin.command("ping")
      print("Connected successfully")
      # other application code
      # push_to_store(chat_id=44,session_id='987660-346378',chat=l)
      l=get_from_store('987660-346378','689')
      print(l)
      for r in l:
         print(type(r))
         print(r)
      # print(l['chat'])
      client.close()
   except Exception as e:
      raise Exception(
         "The following error occurred: ", e)