'''
Created on 

Course work: 

@author: Ana

Source: 
https://newspaper.readthedocs.io/en/latest/
https://www.tutorialspoint.com/python-module-newspaper-for-article-scraping-and-curation
http://theautomatic.net/2020/08/05/how-to-scrape-news-articles-with-python/
https://stackoverflow.com/questions/27962458/downloading-articles-from-multiple-urls-with-newspaper
https://stackoverflow.com/questions/65659787/get-web-article-information-content-title-from-multiple-web-pages-pytho
    
'''

from newspaper import Article
# import nltk
# nltk.download('punkt')
from newspaper import fulltext
import requests
import json

data_list = []


# url = "https://medium.com/featurepreneur/creating-a-kubernetes-cluster-using-kind-35e0e17d2e44"

lists = ['https://medium.com/featurepreneur/run-minio-as-daemon-6120174f9f2','https://medium.com/featurepreneur/upload-files-in-minio-using-python-4f987f902076']


for list in lists:

    article = Article(url="%s" % list, language='de')

    # article = Article(url)
    article.download()
    article.parse()
    title     = article.title 
    content = article.text
    image    = article.top_image
    article.nlp()
    summary   = article.summary

    data = {
                "title": title, 
                'text' : content,
                'image': image,
                'summary': summary
    }

    data_list.append(data)

    details = {
            'data' :data_list
        }
    with open("dataset/ai.json",'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data['data'].append(data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

# with open('dataset/ai.json', 'w') as f:
#     json.dump(details, f) 


# print(article.authors)
# print("Article Publication Date:")
# print(article.publish_date)
# print("Major Image in the article:")
# print(article.top_image)
# article.nlp()
# print ("Keywords in the article")
# print(article.keywords)
# print("Article Summary")
# print(article.summary)