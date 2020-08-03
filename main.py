from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from time import time

class UWatchFreeModel(BaseModel):
    url: str
    host_url: Optional[str] = None
    id: Optional[str] = None
    manifest_url: Optional[str] = None
    poster_url: Optional[str] = None

class UWatchFreeScrapper:
    def __init__(self, model_data: UWatchFreeModel):
        self.model = model_data

    def scrape(self):
        source = requests.get(self.model.url).content
        soup = BeautifulSoup(source, 'html.parser')

        media_elem =  soup.select(".p2p2 > iframe")[0]
        scraped_url = media_elem['src']

        parsed_url = urlparse(scraped_url)
        self.model.host_url = "{url.scheme}://{url.netloc}".format(url=parsed_url)

        parsed_query = parse_qs(parsed_url.query)
        self.model.id = parsed_query['id'][0]

        self.__get_manifest_url()
        self.__get_poster_url()

        return self.model

    def __get_manifest_url(self):
        self.model.manifest_url = "{host_url}/playlist/{id}/{time}.m3u8".format(
                    host_url=self.model.host_url,
                    id=self.model.id,
                    time=int(time()*1000))

        return self.model.manifest_url

    def __get_poster_url(self):
        poster_redirect = "{host_url}/thumbnailRedirect/{id}".format(
                            host_url=self.model.host_url,
                            id=self.model.id)
        self.model.poster_url = requests.get(poster_redirect).url
        
        return self.model.poster_url


app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/uwf/scrape")
def scrape(model_data: UWatchFreeModel):
    try:
        result = UWatchFreeScrapper(model_data).scrape()
    except:
        return model_data
    else:
        return result