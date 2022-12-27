import asyncio
import aiohttp
from config.config import get_secret

# 동시성을 적용해서 아주 빠른 속도로 데이터를 크롤링함
class MovieScraper:

    NAVER_API_MOVIE = "https://openapi.naver.com/v1/search/movie"
    NAVER_API_ID = get_secret("NAVER_API_ID")
    NAVER_API_SECRET = get_secret("NAVER_API_SECRET")

    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result["items"]

    #요청 URL 생성 함수
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
        async with aiohttp.ClientSession() as session:
            all_data = await asyncio.gather(
                *[MovieScraper.fetch(session, api["url"], api["headers"]) for api in apis]
            )
            result = []
            for data in all_data:
                if data is not None:
                    for book in data:
                        result.append(book)
            return result

    #비동기로 오는 결과 한번에 출력
    def run(self, keyword, total_page, genre):
        return asyncio.run(self.search(keyword, total_page, genre))


if __name__ == "__main__":
    scraper = MovieScraper()
    print(scraper.run("해리포터", 1, 1))
    print(len(scraper.run("해리포터", 3, 2)))
