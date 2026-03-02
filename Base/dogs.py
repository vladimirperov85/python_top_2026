import requests
URL = 'https://www.logotypes.dev/apple?version=color'


def get_url_image(url) -> str:
    try:
        """Get image from url."""
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get('message') and data.get('status') == 'success':
            link = data.get('message')
            return link
        else:
            print(data.get('status'))
            return ""
    except Exception as e:
        print(f"Вызвано исключение: {e}")
        return ""



def get_image_by_url(image_url):
    try:
        """Get image by url."""
        response = requests.get(image_url)
        response.raise_for_status()
        pass
    except Exception as e:
        print(f"Вызвано исключение: {e}")
        return None


if __name__ == '__main__':
    link = get_url_image(URL)
    if link:
        image = get_image_by_url(link)
        
    

