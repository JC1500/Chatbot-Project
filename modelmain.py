from langchain_redis import RedisChatMessageHistory
import os
from langchain_redis import RedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openrouter import ChatOpenRouter



class RedisModel:
    def __init__(self,session_id:str) -> None:
        self.session_id=session_id
        self.history = RedisChatMessageHistory(
            session_id=session_id,
            redis_url=os.getenv('REDIS_URL'), #type:ignore
            ttl=3600, 
        )
        self.llm=ChatOpenRouter(model="poolside/laguna-xs-2.1:free",
            temperature=0,
            max_tokens=500,
            max_retries=2,
            api_key=os.getenv('OPENROUTER_API_KEY') #type: ignore
        )
        self.prompt= ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        self.chain=self.prompt | self.llm

    def invoke(self,prompt: str):
        """
        Calls the model with streaming enabled and yields chunks as they arrive.
        """
        self.history.add_user_message(prompt)
        l=[]
        for chunk in self.chain.stream({"input": prompt,'history':self.history.messages},config={"configurable": {"session_id":self.session_id}}):
            l.append(chunk.content)
            if(chunk):
                yield chunk.content
            else:break
        resp="".join(l)
        self.history.add_ai_message(resp)

if(__name__=='__main__'):
    model=RedisModel('1')
    # while True:
    #     a=input('enter: ')
    #     if a=='exit':
    #         break
    #     res=model.invoke(a)
    #     for data in res:
    #         print(data.content,end=" ",flush=True)
    # s=model.history.session_id
    # l=model.history.messages
    # print(s)
    # print(l)
    print(model.history.messages)