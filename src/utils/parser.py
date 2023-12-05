# DEPRECATED!!!

import random
import time

import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW32; rv:20.0) Gecko/20100101 Firefox/20.0"}
result = set()

main_page = requests.get(  # noqa: S113
    "https://spb.cian.ru/snyat-pomeshenie-pod-obshepit/",
    headers=headers,
)
time.sleep(random.randint(2, 10))

for i in range(1, 14):
    print(f"-------------{i}------------")

    page = requests.get(  # noqa: S113
        f"https://spb.cian.ru/ \
        cat.php?deal_type=rent&engine_version=2&offer_type=offices&office_type%5B0%5D=4&p={i}&region=2",
        headers=headers,
    )
    time.sleep(random.randint(2, 10))

    soup = BeautifulSoup(page.text, "lxml")
    all_publications = soup.find_all("div", {"class": "_8c559fa4c7--card-wrapper--hR8ns"})

    for publication in all_publications:
        """space_h2 = publication.find("h2").contents[0]
        if "м²" not in space_h2:
            continue
        space = space_h2.split(" ")[-2]"""

        card_price_block = publication.find("div", {"data-name": "CardPriceBlock"})
        cost = card_price_block.find("span", {"style": "letter-spacing:-0.5px"})
        cost = cost.contents[0].replace("\xa0", "").replace("₽/мес.", "")
        pure_cost = int("".join(filter(str.isdigit, cost)))

        car_address_block = publication.find("div", {"data-name": "CardAddressBlock"})
        address_elements = car_address_block.find_all("a", {"data-name": "InteractiveTextFactory"})
        street = address_elements[-2].contents[0][:-2]
        full_address = "".join([a_e.contents[0] for a_e in address_elements])

        print(pure_cost, full_address, street)
        result.add(full_address)

print(len(result))
