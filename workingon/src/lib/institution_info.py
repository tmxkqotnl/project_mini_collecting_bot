from calendar import c
from typing import Any, Optional
from bs4 import BeautifulSoup
import requests

from src.common.const import INSTITUTION_SEARCH_DETAIL, HRD_OPEN_API_URLS
from src.common.common import error_handler


@error_handler
def get_institution_info_all(
    params: dict[str, str] = {
        "returnType": "XML",
        "outType": "2",
        "srchTrprId": "",
        "srchTrprDegr": "",
    },
    info_type: str = "job_hunter",
) -> dict[str, Any]:
    data = {}
    for i_d in INSTITUTION_SEARCH_DETAIL:
        params["srchTorgId"] = i_d

        # url request
        url = "?".join(
            [
                HRD_OPEN_API_URLS["AGENCY"][info_type],
                "&".join(["{}={}".format(k, v) for k, v in params.items()]),
            ]
        )

        res = requests.get(url)
        # if wrong response got
        if res.status_code != 200:
            raise requests.HTTPError(
                "Bad Reponse - {status_code}, {content}, {url}".format(
                    status_code=res.status_code,
                    content=res.text,
                )
            )
        xml = BeautifulSoup(res.content, "lxml-xml")

        if xml.find("error"):
            raise requests.RequestException(
                "response has a tag 'error' : {full_url}\n {error_message}".format(
                    full_url=res.url, error_message=xml.find("error").contents
                )
            )

        func = func_type(i_d)

        data[i_d] = func(xml)

    return data


def func_type(info_detail: str):
    if info_detail == "default":
        return parse_institution_info
    elif info_detail == "facility_detail":
        return parse_facility_info
    else:
        return parse_inst_eqpm_info


def parse_institution_info(xml: BeautifulSoup) -> dict[str, Optional[str]]:
    instIno = xml.find("instIno")  # 훈련기관코드
    addr1 = xml.find("addr1")  # 주소 1
    addr2 = xml.find("addr2")  # 상세주소
    # filePath = xml.find("filePath") # 파일경로
    hpAddr = xml.find("hpAddr")  # 홈페이지 주소

    inoNm = xml.find("inoNm")  # 훈련기관명

    instPerTrco = xml.find("instPerTrco")  # 실제훈련비

    ncsCd = xml.find("ncsCd")  # NCS 코드
    ncsNm = xml.find("ncsNm")  # NCS 명
    ncsYn = xml.find("ncsYn")  # NCS 여부
    nonNcsCoursePrcttqTime = xml.find("nonNcsCoursePrcttqTime")  # 비 NCS교과 실기시간
    nonNcsCourseTheoryTime = xml.find("nonNcsCourseTheoryTime")  # 비 NCS교과 이론시간

    pFileName = xml.find("pFileName")  # 로고 파일명

    perTrco = xml.find("perTrco")  # 정부지원금
    torgParGrad = xml.find("torgParGrad")  # 평가등급

    traingMthCd = xml.find("traingMthCd")  # 훈련방법코드

    trprChap = xml.find("trprChap")  # 담당자명
    trprChapEmail = xml.find("trprChapEmail")  # 담당자 이메일
    trprChapTel = xml.find("trprChapTel")  # 담당자 전화번호

    trprDegr = xml.find("trprDegr")  # 훈련과정 회차
    trprGbn = xml.find("trprGbn")  # 훈련과정 구분
    trprId = xml.find("trprId")  # 훈련과정ID
    trprNm = xml.find("trprNm")  # 훈련과정명

    trprTarget = xml.find("trprTarget")  # 주요 훈련과정 구분
    trprTargetNm = xml.find("trprTargetNm")  # 주요 훈련과정 구분명

    trtm = xml.find("trtm")  # 총 훈련시간
    trDcnt = xml.find("trDcnt")  # 총 훈련일수

    zipCd = xml.find("zipCd")  # 우편번호

    govBusiNm = xml.find("govBusiNm")  # 훈련분야명
    torgGbnCd = xml.find("torgGbnCd")  # 훈련종류
    totTraingDyct = xml.find("totTraingDyct")  # 훈련일수
    totTraingTime = xml.find("totTraingTime")  # 훈련시간
    totalCrsAt = xml.find("totalCrsAt")  # 수강료
    trprDegr = xml.find("trprDegr")  # 훈련과정 회차
    trprId = xml.find("trprId")  # 훈련과정코드
    trprNm = xml.find("trprNm")  # 훈련과정명

    return {
        "address": addr1.text if addr1 else None,
        "address_detail": addr2.text if addr2 else None,
        # "파일경로": filePath.text if filePath else None,
        "homepage": hpAddr.text if hpAddr else None,
        "inst_name": inoNm.text if inoNm else None,
        "inst_code": instIno.text if instIno else None,
        "real_fee": instPerTrco.text if instPerTrco else None,
        "ncs_code": ncsCd.text if ncsCd else None,
        "ncs_name": ncsNm.text if ncsNm else None,
        "ncs_yn": ncsYn.text if ncsYn else None,
        # "비NCS교과_실기시간": nonNcsCoursePrcttqTime.text if nonNcsCoursePrcttqTime else None,
        # "비NCS교과_이론시간": nonNcsCourseTheoryTime.text if nonNcsCourseTheoryTime else None,
        "logo": pFileName.text if pFileName else None,
        "grant": perTrco.text if perTrco else None,
        "total_days": trDcnt.text if trDcnt else None,
        "total_hours": trtm.text if trtm else None,
        "eval_grade": torgParGrad.text if torgParGrad else None,
        "tr_catecory_code": traingMthCd.text if traingMthCd else None,
        "charge": trprChap.text if trprChap else None,
        "charge_email": trprChapEmail.text if trprChapEmail else None,
        "charge_tel": trprChapTel.text if trprChapTel else None,
        # "훈련과정회차": trprDegr.text if trprDegr else None,
        "tr_class": trprGbn.text if trprGbn else None,
        "tr_id": trprId.text if trprId else None,
        "tr_name": trprNm.text if trprNm else None,
        "tr_main_class": trprTarget.text if trprTarget else None,
        "tr_main_class_name": trprTargetNm.text if trprTargetNm else None,
        "zipcode": zipCd.text if zipCd else None,
        ## detail info
        "tr_class_detail": govBusiNm.text if govBusiNm else None,
        "tr_type": torgGbnCd.text if torgGbnCd else None,
        "tr_day": totTraingDyct.text if totTraingDyct else None,
        "tr_hours": totTraingTime.text if totTraingTime else None,
        "tr_total_fee": totalCrsAt.text if totalCrsAt else None,
        "tr_degree": trprDegr.text if trprDegr else None,
        # "tr_code": trprId.text if trprId else None,
        "tr_name_another": trprNm.text if trprNm else None,
    }


def parse_facility_info(
    xml: BeautifulSoup,
) -> list[dict[str, Optional[str]]]:
    inst_facility_info_list = xml.find_all("inst_facility_info_list")

    if inst_facility_info_list.__len__() == 0:
        inst_facility_info_list = BeautifulSoup(
            "<inst_facility_info_list></inst_facility_info_list>",
            "lxml-xml",
        ).find_all("inst_facility_info_list")

    lst = []
    for k in inst_facility_info_list:
        fcltyArCn = k.find("fcltyArCn")
        ocuAcptnNmprCn = k.find("ocuAcptnNmprCn")
        trafcltyNm = k.find("trafcltyNm")
        holdQy = k.find("holdQy")

        lst.append(
            {
                "area": fcltyArCn.text if fcltyArCn else None,
                "occupation": ocuAcptnNmprCn.text if ocuAcptnNmprCn else None,  # 수용인원
                "name": trafcltyNm.text if trafcltyNm else None,
                "quantity": holdQy.text if holdQy else None,
            }
        )

    return lst


def parse_inst_eqpm_info(
    xml: BeautifulSoup,
) -> list[dict[str, Optional[str]]]:
    lst = []

    inst_eqnm_info_list = xml.find_all("inst_eqnm_info_list")
    if inst_eqnm_info_list.__len__() == 0:
        inst_eqnm_info_list = BeautifulSoup(
            "<inst_eqnm_info_list></inst_eqnm_info_list>", "lxml-xml"
        ).find_all("inst_eqnm_info_list")

    for k in inst_eqnm_info_list:
        eqpmnNm = k.find("eqpmnNm")
        holdQy = k.find("holdQy")

        lst.append(
            {
                "name": eqpmnNm.text if eqpmnNm else None,
                "quantity": holdQy.text if holdQy else None,
            }
        )

    return lst
