from django.shortcuts import render
from car_rental_service_app.models import News
from django.core.files import File
import requests
import logging
from tempfile import NamedTemporaryFile
import os

logger = logging.getLogger('db_logger')

def cat_facts(request):
    response = requests.get("https://catfact.ninja/facts?limit=20")
    res = response.json()
    logger.info("Cat facts showed")
    return render(request, "cat_facts.html", context={ "facts": res["data"]})



def news(request):
    # response = requests.get("https://newsapi.org/v2/everything?q=cars&apiKey=42cdc30638b24df7ba147dddf5603487")
    # res = response.json()["articles"]
    # num = 0
    # for item in res:
    #     if num > 4:
    #         break
    #     try:
    #         q = News.objects.get(title=item["title"])
    #         in_db = True
    #     except:
    #         in_db = False
    #     if not in_db:
    #         news = News()
    #         news.title = item["title"]
    #         if item["description"] is None:
    #             news.short_description = ""
    #         else:
    #             news.short_description = item["description"]
    #         news.url = item["url"]
    #         news.image_url = item["urlToImage"]
    #         news.text = item["content"]
    #         if not news.image_url is None:    
    #             response1 = requests.get(news.image_url)
    #             if response1.status_code == 200:
    #                 img_temp = NamedTemporaryFile(delete=True)
    #                 img_temp.write(response1.content)
    #                 img_temp.flush()
    #                 try:
    #                     news.image.save(os.path.basename(news.image_url), File(img_temp), save=True)
    #                     print(news.image)
    #                 except Exception as e:
    #                     print(e)
    #                     print("Failed downloading image from ", news.image_url)
    #         news.save()
    #         num += 1
    data = News.objects.all()
    logger.info("News list showed")
    return render(request, 'news.html', context={"news": data})
    