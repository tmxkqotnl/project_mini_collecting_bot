from typing import Union
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from common.const import REVIEW_BASE_URL
from common.libs import request_get
import json
import re

#################################################################################
# tracseId=AIG20210000328968 # 훈련과정ID
# tracseTme=2 # 회차
# crseTracseSe=C0061 # 훈련종류 코드
# trainstCstmrId=500020054508 # 훈련기관ID
# pageId # 훈련과정 정보 - #undefined, 훈련기관 정보 None(비어있음)
#################################################################################

# 모집여부
def get_training_is_recruiting(html: BeautifulSoup) -> bool:
    statusTag = (
        html.find("section", {"id": "section1"})
        .find("div", {"class": "info"})
        .find("div", {"class": "title"})
        .find("h4")
        .find("span", {"class": "statusTag"})
    )

    status = statusTag.get_attribute_list("class")[1]
    if status == "orange":
        return True
    else:
        return False


# 훈련과정 정보 첫 번째 박스
def get_info_list(html: BeautifulSoup) -> str:
    infoList = (
        html.find("section", {"id": "section1"})
        .find("div", {"class": "infoList"})
        .find("ul", {"class": "list"})
        .find_all("li")
    )

    # 안내사항 - 리스트 맨 마지막
    notice_contents = infoList[-1].find("span", {"class": "con"}).contents

    stripped = map(
        lambda x: x.strip() if type(x) is NavigableString else x, notice_contents
    )
    stringify = map(lambda x: x.__str__() if type(x) is Tag else x, stripped)
    remove_len_is_zero = "".join(filter(lambda x: x.__len__() != 0, stringify))

    # NCS 수준 - 리스트 네 번째
    NCS_contents = infoList[3].find("span", {"class": "con"}).contents[0]
    NCS_num = NCS_contents.strip()[0]

    return {"notice": remove_len_is_zero, "ncs_degree": NCS_num}


# 수강생 평균 만족도
def get_mean_review_point(html: BeautifulSoup) -> str:
    return html.find("div", attrs={"class": "starRating"}).get("title").split()[2][2:-1]


# 상세 리뷰
# 리뷰가 없으면 길이가 0인 reviews가 반환된다.
def get_reviews(html: BeautifulSoup) -> dict[str, Union[str, list[str]]]:
    # 최대 회차 구하기
    max_degree = (
        html.find("select", {"id": "srchTracseTme"}).find_all("option").__len__()
    )

    # 리뷰 목록을 받아오기 위해 훈련과정 ID가 필요함
    training_id = re.findall(
        re.compile("AIG\d*"),
        html.find("form", {"id": "ogcrLoginScrinForm"}).attrs["action"],
    )[0]

    # 리뷰 목록을 받아오기 위한 쿼리 파라미터
    opt = {"tracseId": training_id}

    rvs = {"training_id": training_id, "reviews": []}
    for i in range(1, max_degree + 1):
        opt["srchTracseTme"] = i
        review_json = json.loads(
            request_get(opt, REVIEW_BASE_URL, parse_to_html=False).text
        )

        a_review = {
            "degree": review_json["commandMap"]["srchTracseTme"],
            "reviews": [i["pstcptCn"] for i in review_json["epilogueList"]],
        }
        rvs["reviews"].append(a_review)

    return rvs


# 훈련과정안내 - 훈련과정 개요
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


# fix - 함수 통합, 함수명 변경
def get_traininig_info_all(
    html: BeautifulSoup,
) -> dict[str, Union[str, dict[str, str]]]:
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
