# url request
from typing import Any, Union
from bs4 import BeautifulSoup
import requests
from workingon.src.common.const import (
    HEADERS,
    HRD_TRAINING_INFO_BASE_URL,
)
from common.url import URL


def request_get(
    opt: dict[str, str],
    base_url: str = HRD_TRAINING_INFO_BASE_URL,
    parse_to: str = "xml",
) -> Union[BeautifulSoup, requests.Response]:
    url = URL(base_url)
    url.set_params(opt)

    res = requests.get(url.get_full_url(), headers=HEADERS)

    if res.status_code != 200:
        raise requests.HTTPError(
            "Bad Reponse - {status_code}, {content}, {url}".format(
                status_code=res.status_code, content=res.text, url=url.get_full_url()
            )
        )

    if parse_to == "xml":
        xml = BeautifulSoup(markup=res.content, features="lxml-xml")

        if xml.find("error"):
            raise requests.RequestException(
                "response has a tag 'error' : {full_url}\n {error_message}".format(
                    full_url=res.url, error_message=xml.find("error").contents
                )
            )

        res = xml
    elif parse_to == "html":
        res = BeautifulSoup(res.text, features="lxml")

    return res


def check_type(params: Any, p_type: type):
    if type(params) is not p_type:
        raise TypeError("Arguments must be {t}".format(t=p_type))