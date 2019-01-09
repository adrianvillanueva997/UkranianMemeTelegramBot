from random import randint
import urllib
import re


class GoogleScrapper:
    def __init__(self, url):
        self.url = url

    def get_raw_html(self, url):
        """Connects to google emulating a web browser and downloads the raw HTML from Google
            Parameters
            ----------
            args : url with query

            Returns
            -------
            resp_data
                Raw HTML
            """
        headers = {}
        headers[
            'User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        resp_data = str(resp.read())
        return resp_data

    def get_links(self, html):
        """Returns a list of urls extracted from HTML
            Parameters
            ----------
            args : HTML data
            Returns
            -------
            List
                urls extracted with regular expression
            """
        urls = []
        url = re.findall('http[s]?:(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))*', html)
        for link in url:
            if (str(link).__contains__('encrypted') or str(link).__contains__('google') or str(link).__contains__(
                    'blogger.com') or str(link).__contains__('gstatic.com') or str(link).__contains__('youtube') or str(
                link).__contains__('schema.org') or str(link).__contains__('http://www.w3.org/2000/svg')):
                print('no')
            else:
                print(link)
                urls.append(link)
        return urls

    def get_random_picture(self, images):
        """Recives a list of urls and returns a random url
            Parameters
            ----------
            args : List
            Returns
            -------
            String
                random url

            """
        try:
            random_pic = randint(0, (len(images) - 1))
            if (images[random_pic] == None):
                self.get_random_picture(images)
            else:
                return images[random_pic]
        except Exception as e:
            print(e)
            self.find_error_pic()

    def find_error_pic(self):
        files = [r'https://i.imgur.com/NhjZ3B9.jpg', r'https://i.imgur.com/n1ne6Xf.jpg',
                 r'https://i.imgur.com/G7Vwf0z.jpg',
                 r'https://i.imgur.com/mmn8sbw.png', r'https://i.imgur.com/kVYqDWM.gif',
                 r'https://i.imgur.com/QbfsniO.jpg',
                 r'https://i.imgur.com/QHqCH2w.jpg',
                 r'https://i.imgur.com/x0e9mRu.jpg', r'https://i.imgur.com/b1izBqW.png',
                 r'https://i.redd.it/266673dajx0z.jpg',
                 r'https://cdn.dribbble.com/users/366584/screenshots/2527274/404_1.gif',
                 r'https://cdn.dribbble.com/users/469578/screenshots/2597126/404-drib23.gif']
        random = randint(0, len(files) - 1)
        random_image = files[random]
        return random_image

    def search_image(self):
        """Receives a query and searches that query on Google and returns an url related to that query
            Parameters
            ----------
            args : None

            Returns
            -------
            String
                Url
            """
        if (self.url != None):
            command_query = ' '.join(str(self.url))
            query = command_query.replace(' ', '%20').encode('utf-8')
            url = 'https://www.google.com/search?q=' + str(
                query) + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
            html = self.get_raw_html(url)
            urls = self.get_links(html)
            picture = ''
            if (len(urls) < 5):
                picture = self.find_error_pic()
            else:
                picture = self.get_random_picture(urls)
            return picture
