import asyncio
import aiohttp
from config.config import get_secret

# 동시성을 적용해서 아주 빠른 속도로 데이터를 크롤링함
class MovieScraper:

    NAVER_API_MOVIE = "https://openapi.naver.com/v1/search/movie"
    NAVER_API_ID = get_secret("NAVER_API_ID")
    NAVER_API_SECRET = get_secret("NAVER_API_SECRET")

    #비동기 함수
    @staticmethod
    async def fetch(session, url, headers):
        #세션과 연결 상태 유지
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                #await을 기점으로 다른 진입점으로 진입한 후 요청이 끝나면 다시 이지점으로 진입
                result = await response.json()
                return result["items"]

    #요청 URL 생성 함수
    #굳이 비동기 함수로 만들 필요가 없는 것들은 일반 함수로 생성
    def getRequestUrl(self, keyword, start, genre):
        return {
            "url": f"{self.NAVER_API_MOVIE}?query={keyword}&display=10&start={start}$genre={genre}",
            "headers": {
                "X-Naver-Client-Id": self.NAVER_API_ID,
                "X-Naver-Client-Secret": self.NAVER_API_SECRET,
            },
        }

    #실제 요청을 보내는 함수, 비동기 적으로 실행
    async def search(self, keyword, total_page, genre):
        #각 요청 URL을 가지고 옴
        apis = [self.getRequestUrl(keyword, 1 + i * 10, genre) for i in range(total_page)]
        #비동기 함수가 세션과 연결할떄 async with 사용
        async with aiohttp.ClientSession() as session:
            #asyncio.gather를 통해 동시 실행 설계 + asyncio 앞에는 await을 붙여 모든 결과가 리턴될때까지 기다림
            all_data = await asyncio.gather(
                *[MovieScraper.fetch(session, api["url"], api["headers"]) for api in apis]
            )
            result = []
            for data in all_data:
                if data is not None:
                    for movie in data:
                        result.append(movie)
            return result

    #비동기로 오는 결과를 동기 함수에서 출력하기 위해서는 asyncio.run이 필요
    def run(self, keyword, total_page, genre):
        return asyncio.run(self.search(keyword, total_page, genre))


if __name__ == "__main__":
    scraper = MovieScraper()
    print(scraper.run("해리포터", 1, 1))
    print(len(scraper.run("해리포터", 3, 2)))
