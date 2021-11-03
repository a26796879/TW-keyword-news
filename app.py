import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from TWnews import news

class News(BaseModel):
    #period: str=None
    keyword: str

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.post("/get_google_news")
async def get_google_news(item:News):
    return news.get_google_news(item.keyword)

@app.post("/get_udn_news")
async def get_udn_news(item:News):
    return news.get_udn_news(item.keyword)
@app.post("/get_apple_news")
async def get_apple_news(item:News):
    return news.get_apple_news(item.keyword)
@app.post("/get_setn_news")
async def get_setn_news(item:News):
    return news.get_setn_news(item.keyword)
@app.post("/get_ettoday_news")
async def get_ettoday_news(item:News):
    return news.get_ettoday_news(item.keyword)
@app.post("/get_TVBS_news")
async def get_TVBS_news(item:News):
    return news.get_TVBS_news(item.keyword)

@app.post("/get_china_news")
async def get_china_news(item:News):
    return news.get_china_news(item.keyword)
@app.post("/get_storm_news")
async def get_storm_news(item:News):
    return news.get_storm_news(item.keyword)
@app.post("/get_ttv_news")
async def get_ttv_news(item:News):
    return news.get_ttv_news(item.keyword)
@app.post("/get_ftv_news")
async def get_ftv_news(item:News):
    return news.get_ftv_news(item.keyword)
@app.post("/get_cna_news")
async def get_cna_news(item:News):
    return news.get_cna_news(item.keyword)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
