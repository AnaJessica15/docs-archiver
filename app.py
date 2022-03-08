from cgitb import text
from flask import Flask, render_template, request
import json
import requests
from newspaper import Article
from newspaper import fulltext

app = Flask(__name__)

data_list = []

urls = []

def get_json(FILE_PATH):

    with open(FILE_PATH) as f:
        data = json.load(f)

    return data

app.jinja_env.globals.update(zip=zip)

@app.route('/add',methods=["GET", "POST"])
def add():
    if request.method == "POST":
        url = request.values.get("url")

        urls.append(url)

        for list in urls:

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
             
                file_data = json.load(file)
           
                file_data['data'].append(data)
             
                file.seek(0)
         
                json.dump(file_data, file, indent = 4)

        return render_template('form.html')

    return render_template('form.html')

@app.route('/')
def index():


    links  = get_json('dataset/ai.json')

    links_list = links['data']
 
    return render_template('index.html', titles = links_list)

@app.route('/single/<title>')
def view(title):

    links  = get_json('dataset/ai.json')

    links_list = links['data']
    
    contents =[]
    images=[]

    for d in links_list:

        if title.strip(' \n') == d["title"].strip(' \n'):

            body = d["text"] 

            contents = d['summary']

            images = d['image']

    return render_template('single.html',content = contents,image = images, title=title, text= body) 
    

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port= 5000)