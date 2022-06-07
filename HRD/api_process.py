from requests import Response, get, HTTPError, RequestException
from bs4 import BeautifulSoup
import lxml
from common.const import HRD_OPEN_API_URLS

from common.url import URL


def request_api_response(opt: dict[str, str], request_url: str):
    dict_has_key(opt, "authKey")

    url = URL(request_url)
    url.set_params(opt)

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
    }
    res = get(url.get_full_url(), headers=HEADERS)
    if res.status_code != 200:
        raise HTTPError(
            "Bad Reponse - {status_code}, {content}".format(
                status_code=res.status_code, content=res.text
            )
        )

    return parse_api_response_to_xml(res)


def parse_api_response_to_xml(res: Response) -> BeautifulSoup:
    xml = BeautifulSoup(markup=res.content, features="lxml-xml")

    if xml.find("error"):
        raise RequestException(
            "response has a tag 'error' : {full_url}\n {error_message}".format(
                full_url=res.url, error_message=xml.find("error").contents
            )
        )

    return xml


def dict_has_key(d: dict[str, str], key: str):
    if not key in d.keys():
        raise KeyError("apiKey is not found")
    else:
        return True


def get_hrd_url(category: str, info_type: str):
    try:
        return HRD_OPEN_API_URLS[category][info_type]
    except KeyError:
        raise KeyError("No case for info_type - {}".format(info_type))
