import requests
from bs4 import BeautifulSoup
import time


def check_status(response_local):
    """
    Checks the HTTP status code of a web request

    This function evaluates the code of an HTTP response. It prints "SUCCESS" if the status code is 200,
    indicating that the request was successful. If the status code is not 200, it prints "DENIED",
    and the program will exit. This function is used to ensure that the fetch operation has successfully communicated
    with the target server.
    :param response_local: The response object from a request.get() or similar request.
    :return: True if the status code is 200, otherwise the program exits
    """
    status_num = response_local.status_code
    if status_num == 200:
        print("SUCCESS")
        print(f"STATUS CODE: {status_num}")
        return True

    elif status_num != 200:
        print("DENIED ACCESS; PROGRAM PANIC")
        print(f"STATUS CODE: {status_num}")
        quit()

    else:
        print("ERROR DETECTED; PROGRAM PANIC")
        quit()


def fetch_crypto_price():
    """
    Fetches the current prices of crytocurrencies from CoinMarketCap.

    This functionality makes an HTTP GET request to the CoinMarketCap website, parses the HTML response to extract
    cryptocurrency names and their corresponding prices using BeautifulSoup, and stores this information in a dict.

    :return: A dictionary where keys are cryptocurrency names and values are their current prices
    """
    CLASS_VAR = "cmc-link"  # CSS class used to find the relevant data in the HTML
    HEADER = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0Safari/537.36"
    } # Header to mimic the browser request
    URL = "https://coinmarketcap.com/"
    r = requests.get(URL, headers=HEADER)
    https_status = check_status(r)

    if https_status:
        soup = BeautifulSoup(r.text, "html.parser")
        t_body = soup.tbody

        top_coins = {}

        for tdr in t_body:

            try:
                coin = tdr.find_all(class_=CLASS_VAR)[0].p.text
                price = float(tdr.find_all(class_=CLASS_VAR)[1].span.text.
                              replace("$", "").
                              replace(",", ""))
                top_coins[coin] = price
            except AttributeError:
                continue
        return top_coins


def main():
    while True:
        top_coins_main = fetch_crypto_price()
        print(top_coins_main)
        # adjust the sleep time as needed
        time.sleep(30)


if __name__ == "__main__":
    main()
