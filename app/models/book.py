from odmantic import Model


class MovieModel(Model):
    title: str
    image: str
    subtitle: int
    pubDate: str

    class Config:
        collection = "movies"
