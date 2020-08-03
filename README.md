pip install -r requirements.txt

uvicorn main:app --reload

(not secure)

Ex: ```curl -X POST "http://127.0.0.1:8000/api/uwf/scrape" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"url\":\"https://www.uwatchfree.ai/2020/08/anaconda-1997-full-movie/\"}" ```