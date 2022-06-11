import pandas as pd

from bs4 import BeautifulSoup
import lxml

from HRD.api_libs import get_hrd_url, request_api_response

########################################################################
## API 훈련과정 목록 요청 파라미터

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


def get_training_list(opt: dict[str, str], info_type: str = "job_hunter"):
    if type(opt) is not dict:
        raise TypeError("opt must be dict][str,str]")

    url = get_hrd_url("LIST", info_type)
    xml_res = request_api_response(opt, url)

    return parse_training_list(xml_res)


# 구직자 과정을 제외한 나머지 두 개 과정은
# eiEmplCnt3, eiEmplCnt3Gt10, eiEmplRate3, eiEmplRate6
# 총 4개 컬럼이 존재하지 않습니다. => None
def parse_training_list(xml: BeautifulSoup) -> pd.DataFrame:
    scn_list = xml.find_all("scn_list")

    if scn_list.__len__() == 0:
        scn_list = BeautifulSoup("<scn_list></scn_list>", "lxml-xml").find_all(
            "scn_list"
        )

    n_lst = []
    for i in scn_list:
        address = i.find("address")
        contents = i.find("contents")
        courseMan = i.find("courseMan")

        eiEmplCnt3 = i.find("eiEmplCnt3")
        eiEmplRate3 = i.find("eiEmplRate3")
        eiEmplRate6 = i.find("eiEmplRate6")

        grade = i.find("grade")
        imgGubun = i.find("imgGubun")
        instCd = i.find("instCd")

        ncsCd = i.find("ncsCd")
        realMan = i.find("realMan")
        regCourseMan = i.find("regCourseMan")

        subTitle = i.find("subTitle")
        subTitleLink = i.find("subTitleLink")
        superViser = i.find("superViser")

        telNo = i.find("telNo")
        title = i.find("title")
        titleIcon = i.find("titleIcon")
        titleLink = i.find("titleLink")

        traEndDate = i.find("traEndDate")
        traStartDate = i.find("traStartDate")

        trainTarget = i.find("trainTarget")

        trainTargetCd = i.find("trainTargetCd")
        trainstCstId = i.find("trainstCstId")

        trprDegr = i.find("trprDegr")
        trprId = i.find("trprId")

        yardMan = i.find("yardMan")

        n_lst.append(
            {
                "주소": address.text if address is not None else None,
                "컨텐츠": contents.text if contents is not None else None,
                "수강비": courseMan.text if courseMan is not None else None,
                "고용보험3개월 취업인원 수": eiEmplCnt3.text if eiEmplCnt3 is not None else None,
                "고용보험3개월 취업률": eiEmplRate3.text if eiEmplRate3 is not None else None,
                "고용보험6개월 취업률": eiEmplRate6.text if eiEmplRate6 is not None else None,
                "등급": grade.text if grade is not None else None,
                "제목 아이콘 구분": imgGubun.text if imgGubun is not None else None,
                "훈련기관_코드": instCd.text if instCd is not None else None,
                "NCS_코드": ncsCd.text if ncsCd is not None else None,
                "실제_훈련비": realMan.text if realMan is not None else None,
                "수강신청_인원": regCourseMan.text if regCourseMan is not None else None,
                "부제목": subTitle.text if subTitle is not None else None,
                "부제목 링크": subTitleLink.text if subTitleLink is not None else None,
                "주관부처": superViser.text if superViser is not None else None,
                "전화번호": telNo.text if telNo is not None else None,
                "제목": title.text if title is not None else None,
                "제목 아이콘": titleIcon.text if titleIcon is not None else None,
                "제목 링크": titleLink.text if titleLink is not None else None,
                "훈련시작시작일자": traStartDate.text if traStartDate is not None else None,
                "훈련시작종료일자": traEndDate.text if traEndDate is not None else None,
                "훈련대상": trainTarget.text if trainTarget is not None else None,
                "훈련구분": trainTargetCd.text if trainTargetCd is not None else None,
                "훈련기관ID": trainstCstId.text if trainstCstId is not None else None,
                "훈련과정_순차": trprDegr.text if trprDegr is not None else None,
                "훈련과정ID": trprId.text if trprId is not None else None,
                "정원": yardMan.text if yardMan is not None else None,
            }
        )

    return pd.DataFrame(n_lst)
