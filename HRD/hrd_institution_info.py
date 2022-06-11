from typing import Union
from bs4 import BeautifulSoup
from common.const import HRD_INSTITUTION_INFO_BASE_URL, HRD_ROOT_URL
from common.libs import request_get

#################################################################################
# tracseId=AIG20210000328968 # 훈련과정ID
# tracseTme=2 # 회차
# crseTracseSe=C0061 # 훈련종류 코드
# trainstCstmrId=500020054508 # 훈련기관ID
# pageId # 훈련과정 정보 - #undefined, 훈련기관 정보 None(비어있음)
#################################################################################


def get_institution_info_all(
    opt: dict[str, str]
) -> dict[str, Union[str, list[str], dict[str, Union[str, list[dict[str, str]]]]]]:
    html = request_get(opt, HRD_INSTITUTION_INFO_BASE_URL, parse_to="html")

    inst_desc = get_institution_description(html)
    intro_thumb = get_thumbnail_intro(html)
    info_detail = get_info_detail(html)

    return {"description": inst_desc, "intro_thumb": intro_thumb, "detail": info_detail}


def get_institution_description(html: BeautifulSoup) -> str:
    return (
        html.find("section", {"id": "section2"})
        .find("div", {"class": "addExplainBoxArea"})
        .find("pre")
        .text
    )


def get_thumbnail_intro(html: BeautifulSoup) -> list[str]:
    thumbnail_div_list = (
        html.find("section", {"id": "section2"})
        .find("div", {"class": "thumbnailIntroListArea"})
        .find("ul", {"class": "list swiper-wrapper"})
        .find_all("div", {"class": "inner"})
    )

    return [
        "".join([HRD_ROOT_URL, i.attrs["style"].split("'")[1]])
        for i in thumbnail_div_list
    ]


def get_info_detail(html: BeautifulSoup) -> dict[str, Union[str, list[dict[str, str]]]]:
    section2_info = (
        html.find("section", {"id": "section2"})
        .find("div", {"class": "infoDetailBox"})
        .find("div", {"class": "info"})
    )

    # img src
    institution_img = (
        section2_info.find("div", {"class": "thumbnail"}).find("img").attrs["src"]
    )
    institution_thumbnail_src = "".join([HRD_ROOT_URL, institution_img])

    # info_list
    info_list = (
        section2_info.find("div", {"class": "content"})
        .find("ul", {"class": "list"})
        .find_all("li")
    )

    info_list_dict = []
    for i in info_list:
        tit = i.find("span", {"class": "tit"}).text.strip()
        con = i.find("span", {"class": "con"}).text.strip()

        info_list_dict.append({tit: con})

    return {"info_detail": info_list_dict, "thumbnail": institution_thumbnail_src}
    # infoList = filter(lambda x: type(x) is not str, infoList)
