import requests
# Proxy Pool URL, which is the address of the proxy pool server(Redis required).
PROXY_POOL_URL = 'http://localhost:5555/random'

def get_proxy():
    """
    Get a proxy from the proxy pool server. You can find more details in the Open Source Project: \
    https://github.com/Python3WebSpider/ProxyPool.git
    """
    try:
        response = requests.get(PROXY_POOL_URL)
        # If the response status code is 200, return the proxy.
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None

if __name__ == '__main__':
    print(get_proxy())