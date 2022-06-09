from os import getenv
from requests import Response, get, HTTPError, RequestException
from bs4 import BeautifulSoup
import lxml
from common.const import (
    HEADERS,
    HRD_OPEN_API_URLS,
    INSTITUTION_SEARCH_DETAIL,
    TRAINING_TYPE,
)
from common.libs import request_get

from common.url import URL


def request_api_response(opt: dict[str, str], base_url: str):
    opt["authKey"] = getenv("HRD_API_KEY")

    return request_get(opt,base_url,parse_to='xml')


def dict_has_key(d: dict[str, str], key: str):
    if not key in d.keys():
        raise KeyError("apiKey is not found")
    else:
        return True


def get_hrd_url(category: str, info_type: str):
    try:
        return HRD_OPEN_API_URLS[category][info_type]
    except KeyError:
        raise KeyError(
            "No case for category or info_type - {c}, {i}".format(
                c=category, i=info_type
            )
        )


def check_info_detail_type(info_detail: str):
    if info_detail is None or info_detail not in INSTITUTION_SEARCH_DETAIL:
        raise ValueError("info_detail must be one of {type}".format(type=info_detail))


def check_info_type(info_type: str):
    if info_type is None or info_type not in TRAINING_TYPE:
        raise ValueError("info_detail must be one of {type}".format(type=info_type))
