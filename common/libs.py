# url request
from typing import Union
from bs4 import BeautifulSoup
import requests
from common.const import (
    HEADERS,
    HRD_TRAINING_INFO_BASE_URL,
)
from common.url import URL


def request_get(
    opt: dict[str, str],
    base_url: str = HRD_TRAINING_INFO_BASE_URL,
    parse_to_html: bool = True,
) -> Union[BeautifulSoup, requests.Response]:
    url = URL(base_url)
    url.set_params(opt)

    res = requests.get(url.get_full_url(), headers=HEADERS)
    if parse_to_html:
        res = BeautifulSoup(res.text, features="lxml")

    return res
