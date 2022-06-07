from os import getenv
from typing import Union
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
import requests
from common.url import URL
from common.const import (
    HEADERS,
    HRD_TRAINING_INFO_BASE_URL,
    HRD_INSTITUTION_INFO_BASE_URL,
)

#################################################################################
# tracseId=AIG20210000328968 # 훈련과정ID
# tracseTme=2 # 회차
# crseTracseSe=C0061 # 훈련종류 코드
# trainstCstmrId=500020054508 # 훈련기관ID
# pageId # 훈련과정 정보 - #undefined, 훈련기관 정보 None(비어있음)
#################################################################################


def crawlinig_hrd_training_info(
    opt: dict[str, str]
) -> dict[str, Union[str, dict[str, str]]]:
    url = URL(HRD_TRAINING_INFO_BASE_URL)
    url.set_params(opt)

    opt["authKey"] = getenv("HRD_API_KEY")

    res = requests.get(url.get_full_url(), headers=HEADERS)
    html = BeautifulSoup(res.text, features="lxml")

    return process_training_info(html)
    # return html


def get_notice(html: BeautifulSoup) -> str:
    target_tag = (
        html.find("ul", {"class": "list"})
        .find_all("li")[-1]
        .find("span", {"class": "con"})
        .contents
    )
    stripped = map(lambda x: x.strip() if type(x) is NavigableString else x, target_tag)
    stringify = map(lambda x: x.__str__() if type(x) is Tag else x, stripped)
    remove_len_is_zero = "".join(filter(lambda x: x.__len__() != 0, stringify))

    return remove_len_is_zero


def get_mean_review_point(html: BeautifulSoup) -> str:
    return html.find("div", attrs={"class": "starRating"}).get("title").split()[2][2:-1]


# 훈련 종료 시점이 지난 이후에 확인 가능하기 때문에 분기처리가 필요함
def get_reviews(html: BeautifulSoup):

    pass


def get_training_introduction(html: BeautifulSoup) -> dict[str, str]:
    tbody = (
        html.find("div", {"id": "section1-1"})
        .find("table", {"class": "view"})
        .find("tbody")
    )

    # process <th>
    ths = tbody.find_all("th")
    stripped_ths = list(map(lambda x: x.text.strip(), ths))

    # process <td>
    tds = tbody.find_all("td")
    tds_contents = list(map(lambda x: x.contents, tds))

    tds_processed = []
    for i in tds_contents:
        inner_lst = []
        for j in i:
            if type(j) is Tag:
                inner_lst.append(j.__str__())
            elif type(j) is NavigableString:
                inner_lst.append(j.strip())
        tds_processed.append("".join(inner_lst))

    # to dict
    parsed = {th: td for th, td in zip(stripped_ths, tds_processed)}
    return parsed


def process_training_info(html: BeautifulSoup) -> dict[str, Union[str, dict[str, str]]]:
    notice = get_notice(html)
    mean_review_point = get_mean_review_point(html)
    traininig_introdcution = get_training_introduction(html)

    # final form
    form = {
        "point": mean_review_point,
        "notice": notice,
        "introduction": traininig_introdcution,
    }

    return form


def process_agency_info(html: BeautifulSoup):
    pass


# 훈련과정을 중심으로 크롤링 진행
# def crawling_main(url:URL,):
