from os import getenv
from typing import Any, Optional
from bs4 import BeautifulSoup

import pandas as pd
from HRD.api_process import (
    check_info_detail_type,
    check_info_type,
    get_hrd_url,
    request_api_response,
)
from common.const import INSTITUTION_SEARCH_DETAIL
from common.libs import check_type

########################################################################
## 과정/기관정보 요청 파라미터
# 모든 옵션은 필수 사항입니다.
# api 반환값은 srchTorgId가 default 옵션일 때의 반환값을 모두 포함합니다.

# opt = {
#         'authKey':API_KEY, # API Auth key
#         'returnType':'XML', # only XML available
#         'outType':'2', # detail - 고정
#         'srchTrprId':None, # 훈련과정 ID
#         'srchTrprDegr':None, # 훈련과정 회차 # 없으면 함수가 제대로 돌아가지 않음..
# }

#         'srchTorgId':'default', # default - 기본 정보 + 세부 정보 , facility_detail - 시설 정보, eqnm_detail - 장비 정보
########################################################################


def get_institution_info_all(opt: dict[str, str], info_type: str) -> dict[str, Any]:
    check_type(opt, dict)
    check_info_type(info_type)

    data = {}
    for i_d in INSTITUTION_SEARCH_DETAIL:
        opt["srchTorgId"] = i_d
        url = get_hrd_url("AGENCY", info_type)

        res = request_api_response(opt, url)
        func = func_type(i_d)

        data[i_d] = func(res)

    return data


def func_type(info_detail: str):
    if info_detail == "default":
        return parse_institution_info
    elif info_detail == "facility_detail":
        return parse_facility_info
    else:
        return parse_inst_eqpm_info


def get_institution_info(
    opt: dict[str, str], info_type: str = "job_hunter", info_detail: str = "default"
):
    check_type(opt, dict)
    check_info_type(info_type)
    check_info_detail_type(info_detail)

    opt["srchTorgId"] = info_detail

    url = get_hrd_url("AGENCY", info_type)
    xml_res = request_api_response(opt, url)

    func = func_type(info_detail)

    return func(xml_res)


def parse_institution_info(xml: BeautifulSoup) -> list[dict[str, Optional[str]]]:
    instIno = xml.find("instIno")
    addr1 = xml.find("addr1")
    addr2 = xml.find("addr2")
    filePath = xml.find("filePath")
    hpAddr = xml.find("hpAddr")

    inoNm = xml.find("inoNm")

    instPerTrco = xml.find("instPerTrco")

    ncsCd = xml.find("ncsCd")
    ncsNm = xml.find("ncsNm")
    ncsYn = xml.find("ncsYn")
    nonNcsCoursePrcttqTime = xml.find("nonNcsCoursePrcttqTime")
    nonNcsCourseTheoryTime = xml.find("nonNcsCourseTheoryTime")

    pFileName = xml.find("pFileName")

    perTrco = xml.find("perTrco")
    torgParGrad = xml.find("torgParGrad")

    traingMthCd = xml.find("traingMthCd")

    trprChap = xml.find("trprChap")
    trprChapEmail = xml.find("trprChapEmail")
    trprChapTel = xml.find("trprChapTel")

    trprDegr = xml.find("trprDegr")
    trprGbn = xml.find("trprGbn")
    trprId = xml.find("trprId")
    trprNm = xml.find("trprNm")

    trprTarget = xml.find("trprTarget")
    trprTargetNm = xml.find("trprTargetNm")

    trtm = xml.find("trtm")
    trDcnt = xml.find("trDcnt")

    zipCd = xml.find("zipCd")

    govBusiNm = xml.find("govBusiNm")
    torgGbnCd = xml.find("torgGbnCd")
    totTraingDyct = xml.find("totTraingDyct")
    totTraingTime = xml.find("totTraingTime")
    totalCrsAt = xml.find("totalCrsAt")
    trprDegr = xml.find("trprDegr")
    trprId = xml.find("trprId")
    trprNm = xml.find("trprNm")

    return [
        {
            "주소지": addr1.text if addr1 else None,
            "상세주소": addr2.text if addr2 else None,
            "파일경로": filePath.text if filePath else None,
            "홈페이지_주소": hpAddr.text if hpAddr else None,
            "훈련기관명": inoNm.text if inoNm else None,
            "훈련기관_코드": instIno.text if instIno else None,
            "실제_훈련비": instPerTrco.text if instPerTrco else None,
            "NCS코드": ncsCd.text if ncsCd else None,
            "NCS명": ncsNm.text if ncsNm else None,
            "NCS여부": ncsYn.text if ncsYn else None,
            "비NCS교과_실기시간": nonNcsCoursePrcttqTime.text
            if nonNcsCoursePrcttqTime
            else None,
            "비NCS교과_이론시간": nonNcsCourseTheoryTime.text
            if nonNcsCourseTheoryTime
            else None,
            "로고파일명": pFileName.text if pFileName else None,
            "정부지원금": perTrco.text if perTrco else None,
            "평가등급": torgParGrad.text if torgParGrad else None,
            "총_훈련일수": trDcnt.text if trDcnt else None,
            "훈련방법코드": traingMthCd.text if traingMthCd else None,
            "담당자명": trprChap.text if trprChap else None,
            "담당자_이메일": trprChapEmail.text if trprChapEmail else None,
            "담당자_전화번호": trprChapTel.text if trprChapTel else None,
            "훈련과정회차": trprDegr.text if trprDegr else None,
            "훈련과정구분": trprGbn.text if trprGbn else None,
            "훈련과정ID": trprId.text if trprId else None,
            "훈련과정명": trprNm.text if trprNm else None,
            "주요_훈련과정_구분": trprTarget.text if trprTarget else None,
            "주요_훈련과정_구분명": trprTargetNm.text if trprTargetNm else None,
            "총_훈련시간": trtm.text if trtm else None,
            "우편번호": zipCd.text if zipCd else None,
            ## detail info
            "훈련분야명": govBusiNm.text if govBusiNm else None,
            "훈련종류": torgGbnCd.text if torgGbnCd else None,
            "훈련일수": totTraingDyct.text if totTraingDyct else None,
            "훈련시간": totTraingTime.text if totTraingTime else None,
            "수강료": totalCrsAt.text if totalCrsAt else None,
            "훈련과정회차": trprDegr.text if trprDegr else None,
            "훈련과정코드": trprId.text if trprId else None,
            "훈련과정명": trprNm.text if trprNm else None,
        }
    ]


def parse_facility_info(
    xml: BeautifulSoup,
) -> list[dict[str, Optional[str]]]:
    inst_facility_info_list = xml.find_all("inst_facility_info_list")

    if inst_facility_info_list.__len__() == 0:
        inst_facility_info_list = BeautifulSoup(
            "<inst_facility_info_list></inst_facility_info_list>",
            "lxml-xml",
        ).find_all("inst_facility_info_list")

    instIno = xml.find("instIno")

    lst = []
    for k in inst_facility_info_list:
        cstmrNm = k.find("cstmrNm")
        fcltyArCn = k.find("fcltyArCn")
        ocuAcptnNmprCn = k.find("ocuAcptnNmprCn")
        trafcltyNm = k.find("trafcltyNm")
        holdQy = k.find("holdQy")

        lst.append(
            {
                "훈련기관_코드": instIno.text if instIno else None,
                "등록훈련기관": cstmrNm.text if cstmrNm else None,
                "시설면적(m*m)": fcltyArCn.text if fcltyArCn else None,
                "인원(명)": ocuAcptnNmprCn.text if ocuAcptnNmprCn else None,  # 수용인원
                "시설명": trafcltyNm.text if trafcltyNm else None,
                "시설 수": holdQy.text if holdQy else None,
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

    instIno = xml.find("instIno")
    for k in inst_eqnm_info_list:
        cstmrNm = k.find("cstmrNm")
        eqpmnNm = k.find("eqpmnNm")
        holdQy = k.find("holdQy")

        lst.append(
            {
                "훈련기관_코드": instIno.text if instIno else None,
                "등록훈련기관": cstmrNm.text if cstmrNm else None,
                "장비명": eqpmnNm.text if eqpmnNm else None,
                "보유 수량": holdQy.text if holdQy else None,
            }
        )

    return lst
