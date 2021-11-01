import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from TWnews import news

class News(BaseModel):
    period: str
    keyword: str

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/get_udn_news/")
def get_udn_news():
    return news.get_udn_news('基進')
'''
@app.post("/get_udn_news/")
async def get_udn_news(news: News):
    return round(news.weight / (news.height / 100) ** 2, 1)
'''
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=5000, reload=True)
