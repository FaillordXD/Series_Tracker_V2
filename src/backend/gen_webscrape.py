import requests

def extract_image(path,url='https://bs.to/public/images/default-cover.jpg'):
    try:
        page = requests.get(url, stream=True)
    except TypeError as e:
        print (e)
        page = requests.get('https://bs.to/public/images/default-cover.jpg', stream=True)
    if page.status_code == 200:
        with open(path, 'wb') as f:
            f.write(page.content)