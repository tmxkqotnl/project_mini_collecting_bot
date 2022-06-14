from os import getenv
from typing import Optional

from bs4 import BeautifulSoup
import requests

from src.common.const import HRD_OPEN_API_URLS
from src.common.common import error_handler

########################################################################
## HRD-net open API
# #훈련과정 목록 요청 파라미터

# opts = {
#         "authKey": "serviceKey", # required
#         "returnType": "XML",  # only XML avaliable, required
#         "outType": "1",  # 1 - list, required
#         "pageNum": "1",  # maximum 1000, required
#         "pageSize": "100",  # maximum 100, required

#         "srchTraArea1":"", # 훈련지역 대분류
#         "srchTraArea2":"", # 훈련지역 중분류

#         "srchKeco1":"", # 훈련분야 대분류
#         "srchKeco2":"", # 훈련분야 중분류
#         "srchKeco3":"", # 훈련분야 소분류

#         "crseTracseSe":"", # 훈련유형, 중장년특화 X

#         "srchTraGbn":"", # 훈련구분코드, 중장년특화 X
#         "srchTraType":"", # 훈련종류

#         "sort": "ASC", #정렬방법, required
#         "sortCol": # "TR_STT_DT",  # TOT_FXNUM - 모집인원, TR_STT_DT - 훈련시작일, TR_NM_i - 훈련과정명, required

#         "srchTraStDt": "19700101",  # 훈련 시작일 from, required
#         "srchTraEndDt": "20221231",  # 훈련 시작일 to, required

#         "srchTraProcessNm":"", # 훈련과정명
#         "srchTraOrganNm":"", # 훈련기관명
# }
########################################################################
@error_handler
def get_training_list(
    params: dict[str, Optional[str]] = {
        "authKey": getenv("HRD_API_KEY"),
        "returnType": "XML",
        "outType": "1",
        "pageNum": "1",
        "pageSize": "10",
        "sort": "ASC",
        "sortCol": "TR_STT_DT",
        "srchTraStDt": "20180101",
        "srchTraEndDt": "20180101",
    },
    info_type: str = "job_hunter",
):

    # url request
    url = "?".join(
        [
            HRD_OPEN_API_URLS["LIST"][info_type],
            "&".join(["{}={}".format(k, v) for k, v in params.items()]),
        ]
    )

    res = requests.get(url)

    # if wrong response got
    if res.status_code != 200:
        raise requests.HTTPError(
            "Bad Reponse - {status_code}, {content}, {url}".format(
                status_code=res.status_code, content=res.text
            )
        )
    xml = BeautifulSoup(res.content, "lxml-xml")

    if xml.find("error"):
        raise requests.RequestException(
            "response has a tag 'error' : {full_url}\n {error_message}".format(
                full_url=res.url, error_message=xml.find("error").contents
            )
        )

    # get target items
    scn_list = xml.find_all("scn_list")
    # no item handling
    if scn_list.__len__() == 0:
        scn_list = BeautifulSoup("<scn_list></scn_list>", "lxml-xml").find_all(
            "scn_list"
        )

    # get parsed item
    result = [parse_training_html(i) for i in scn_list]
    return list(filter(lambda x: x["inst_code"] is not None, result))


def parse_training_html(html: BeautifulSoup):
    address = html.find("address").text.split() if html.find("address") else None
    if address is not None:
        try:  # "세종" 때문
            address = {"base_adrs": address[0], "base_adrs_sub": address[1]}
        except:
            address = {"base_adrs": address, "base_adrs_sub": None}
    else:
        address = {"base_adrs": None, "base_adrs_sub": None}
    # contents = html.find("contents")
    courseMan = html.find("courseMan")

    eiEmplCnt3 = html.find("eiEmplCnt3")
    eiEmplRate3 = html.find("eiEmplRate3")
    eiEmplRate6 = html.find("eiEmplRate6")

    # grade = html.find("grade")
    # imgGubun = html.find("imgGubun")
    instCd = html.find("instCd")

    ncsCd = html.find("ncsCd")
    realMan = html.find("realMan")
    regCourseMan = html.find("regCourseMan")

    subTitle = html.find("subTitle")
    subTitleLink = html.find("subTitleLink")
    superViser = html.find("superViser")

    telNo = html.find("telNo")
    title = html.find("title")
    # titleIcon = html.find("titleIcon")
    titleLink = html.find("titleLink")

    traEndDate = html.find("traEndDate")
    traStartDate = html.find("traStartDate")

    trainTarget = html.find("trainTarget")

    trainTargetCd = html.find("trainTargetCd")
    trainstCstId = html.find("trainstCstId")

    trprDegr = html.find("trprDegr")
    trprId = html.find("trprId")

    yardMan = html.find("yardMan")

    return {
        **address,
        "fee": courseMan.text if courseMan is not None else None,
        "actual_fee": realMan.text if realMan is not None else None,
        "emp_3_month_cnt": eiEmplCnt3.text if eiEmplCnt3 is not None else None,
        "emp_rate_3": eiEmplRate3.text if eiEmplRate3 is not None else None,
        "emp_rate_6": eiEmplRate6.text if eiEmplRate6 is not None else None,
        # "컨텐츠": contents.text if contents is not None else None,
        # "등급": grade.text if grade is not None else None,
        # "제목 아이콘 구분": imgGubun.text if imgGubun is not None else None,
        "yard": yardMan.text if yardMan is not None else None,
        "registerd": regCourseMan.text if regCourseMan is not None else None,
        "inst_id": instCd.text if instCd is not None else None,
        "ncs_code": ncsCd.text if ncsCd is not None else None,
        "inst_name": subTitle.text if subTitle is not None else None,
        "inst_link": subTitleLink.text if subTitleLink is not None else None,
        "supervisor": superViser.text if superViser is not None else None,
        "tel_no": telNo.text if telNo is not None else None,
        # "제목 아이콘": titleIcon.text if titleIcon is not None else None,
        "tr_name": title.text if title is not None else None,
        "tr_link": titleLink.text if titleLink is not None else None,
        "tr_start_dt": traStartDate.text if traStartDate is not None else None,
        "tr_end_dt": traEndDate.text if traEndDate is not None else None,
        "target": trainTarget.text if trainTarget is not None else None,
        "target_category": trainTargetCd.text if trainTargetCd is not None else None,
        "inst_code": trainstCstId.text if trainstCstId is not None else None,
        "degree": trprDegr.text if trprDegr is not None else None,
        "tr_id": trprId.text if trprId is not None else None,
    }
