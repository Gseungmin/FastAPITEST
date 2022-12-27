from pathlib import Path
from fastapi import FastAPI, Request
from app.models import mongodb
from app.models.movie import MovieModel
from app.scrapper.movie_scraper import MovieScraper

#싱글톤 객체로 생성
app = FastAPI()

#Path(__file__).resolve()가 현재 파일의 경로
#즉 BASE_DIR은 현재 경로의 상위 경로, 이 경우 app 폴더
BASE_DIR = Path(__file__).resolve().parent

#Response 타입이 html, 기본적으로 json 타입
#index.html에 request와 id 변수에 값 지정
@app.get("/")
async def home(request: Request):
    return "검색어를 입력해주세요"

#검색어와 장르를 통해 검색어 받기, 데이터를 받아 MongoDB에 저장
@app.get("/search/{query}/{genre}")
async def search(request: Request, query:str, genre:int):
    #쿼리에서 검색어 추출
    keyword, genre = query, genre
    #검색어가 없다면 검색 요구 리턴
    if not keyword:
        return {"message": "검색어를 입력해주세요"}

    #해당 검색어의 데이터가 이미 DB에 존재한다면 그냥 보여줌
    # await을 통해 해당 과정 기다리게 함
    if await mongodb.engine.find_one(MovieModel, MovieModel.keyword == keyword):

        #만약 존재한다면 모든 데이터 가지고 와서 뷰 구성
        # await을 통해 해당 과정 기다리게 함
        movies = await mongodb.engine.find(MovieModel, MovieModel.keyword == keyword)
        return movies

    #Scrapper를 통해 해당 검색어에 대한 데이터 수집
    movie_scrapper = MovieScraper()

    #search가 비동기함수이므로 await 설정, 총 10개의 데이터를 가지고 옴
    #await을 통해 해당 과정 기다리게 함
    movies = await movie_scrapper.search(keyword, 10, genre)

    #각 모델 생성
    movie_models = []
    for movie in movies:
        movie_model = MovieModel(keyword = keyword,
                                 title = movie["title"],
                                 image = movie["image"],
                                 subtitle = movie["subtitle"],
                                 pubDate = movie["pubDate"])
        movie_models.append(movie_model)

    #DB에 수집된 데이터 저장
    # save_all함수는 await의 동기 패턴을 asyncio 대신 사용해 동시 실행 패턴으로 변경
    await mongodb.engine.save_all(movie_models) # save 함수가 async함수 이므로 즉 코루틴 함수 이므로 await을 붙임
    return movie_models

# DB와 연결하고 서버가 끝날때 DB와 연결 해제
# app이 시작될때 함수 실행
@app.on_event("startup")
def on_app_start():
    """before app starts"""
    mongodb.connect()

# app이 종료될때 함수 실행
@app.on_event("shutdown")
def on_app_shutdown():
    """after app shutdown"""
    mongodb.close()