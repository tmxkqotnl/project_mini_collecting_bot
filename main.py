from HRD import (
    open_api_institution_info,
    open_api_training_info,
    hrd_institution_info,
    hrd_training_info,
)
from HRD import init

import json


## 1차로 전부 다 받아오고.
##
# 1. 각 과정별 10개씩 받아오기
# 2. 나머지 정보 가져오기
# 3. DB에 데이터 확인
# 4. DB insert or update
errors = []


def get_inner_func(opt: dict[str, str]):
    global errors
    it = ""
    for info_type in ["job_hunter", "worker", "enterprise"]:
        it = info_type

        cnt = int(open_api_training_info.get_training_list_cnt(opt, info_type))
        for i in range(1, cnt // 10 + 2):
            opt["pageNum"] = str(i)
            lst = open_api_training_info.get_training_list(opt, info_type)
            for j in lst:
                inst_opt = {
                    "returnType": "XML",
                    "outType": "2",
                    "srchTrprId": j["훈련과정ID"],
                    "srchTrprDegr": j["훈련과정_순차"],
                }

                html_inst_opt = {
                    "tracseId": j["훈련과정ID"],
                    "tracseTme": j["훈련과정_순차"],
                    "crseTracseSe": j["훈련구분"],
                    "trainstCstmrId": j["훈련기관ID"],
                    "pageId": "",
                }
                inst = open_api_institution_info.get_institution_info_all(
                    inst_opt, info_type
                )
                html_inst = hrd_institution_info.get_institution_info_all(html_inst_opt)
                html_training = hrd_training_info.get_traininig_info_all(html_inst_opt)

                return {
                    "1": j,
                    "2": inst,
                    "3": html_inst,
                    "4": html_training,
                }  # for test

    errors.append({"params": opt, "type": it})


def get_all_from_2018(d: dict[str, dict[str, dict[str, int]]]):
    for i in d.keys():
        for j in d[i].keys():
            for k in range(int(d[i][j]["first"]), int(d[i][j]["last"])):
                a_day = "".join(
                    [i, j, str(k) if len(str(k)) == 2 else "".join(["0", str(k)])]
                )
                base_opt = {
                    "returnType": "XML",
                    "outType": "1",
                    "pageNum": "1",
                    "pageSize": "10",
                    "sort": "ASC",
                    "sortCol": "TR_STT_DT",
                    "srchTraStDt": a_day,
                    "srchTraEndDt": a_day,
                }
                infos = get_inner_func(base_opt)

                with open("check.json", "w+", encoding="utf-8") as f:
                    f.write(json.dumps(infos, ensure_ascii=False, allow_nan=True))
                with open("logging.txt", "a+", encoding="utf-8") as f:
                    f.write(json.dumps(errors, allow_nan=True))

                return None  # for test


with open("date_range.json", "r+") as f:
    dates = json.load(f)
get_all_from_2018(dates)
