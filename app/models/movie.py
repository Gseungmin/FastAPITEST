from odmantic import Model


class MovieModel(Model):
    keyword: str
    title: str
    image: str
    subtitle: str
    pubDate: str

    class Config:
        collection = "movies"
