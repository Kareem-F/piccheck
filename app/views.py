import requests
from flask import render_template, redirect, url_for
from config import FLICKR_KEY, GOOGLE_KEY, PIXABAY_KEY
from app import web_app
from .forms import SearchForm


def flickr_get_imgs(query):
    img_urls = []
    url = "https://api.flickr.com/services/rest/?"
    req_info = {
            "method": "flickr.photos.search",
            "api_key": FLICKR_KEY,
            "format": "json",
            "per_page": "30",
            "text": query,
            "media": "photos",
            "nojsoncallback": "1"
    }
    response = requests.get(url, params=req_info)
    if response.status_code != 200:
        print("ERROR")
        print(response.status_code)
    else:
        data = response.json()
        if data:
	        for img in data['photos']['photo']:
	            img_url = "https://farm{farmid}.staticflickr.com/{serverid}/{id}_{secret}_z.jpg".format(farmid=img['farm'], serverid=img['server'], id=img['id'], secret=img['secret'])
	            img_urls.append(img_url)
    return img_urls

def pixabay_get_imgs(query):
    img_urls = []
    url = "https://pixabay.com/api/?"
    req_info = {
        "key": PIXABAY_KEY,
        "q": query,
        "image_type": "photo",
        "safesearch": "true"
    }
    response = requests.get(url, params=req_info)
    print(response.url)
    if response.status_code != 200:
        print("ERROR")
        print(response.status_code)
    else:
        data = response.json()
        if data:
            for img in data['hits']:
                img_urls.append(img['previewURL'])
    return img_urls
@web_app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    google_places_url = "https://maps.googleapis.com/maps/api/js?key=" + GOOGLE_KEY + "&libraries=places"
    if form.validate_on_submit():
        query = form.location.data.split(',')[0]
        img_src = form.img_src.data
        if img_src == 'fk':
            img_src = 'Flicker'
        else:
            img_src = 'Pixabay'
        return redirect(url_for('search', img_src=img_src, search_query=query))
    return render_template('index.html', form=form, google_places_url=google_places_url)

@web_app.route('/<img_src>/<search_query>')
def search(img_src, search_query):
    if img_src == 'Flicker':
        imgs = flickr_get_imgs(search_query)
    else:
	    imgs = pixabay_get_imgs(search_query)
    return render_template('search.html', title=search_query, imgs_urls=imgs)
