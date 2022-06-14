from os import getenv
from sys import path
import sys
from dotenv import load_dotenv
from os.path import abspath, join, dirname
import json

project_path = dirname(abspath(__file__))
env_file_path = join(project_path, ".env")
load_dotenv(env_file_path)
path.append(project_path)

from src.db.db import engine, Base
from src.models import training, institution, facility, equipment

from src.lib.training_list import get_training_list
from src.lib.institution_info import get_institution_info_all
from src.db.training_crud import insert_training
from src.db.institution_crud import insert_institution
from src.db.facility_crud import insert_facility
from src.db.equipment_crud import insert_equipment

Base.metadata.create_all(engine)


params = {
    "authKey": getenv("HRD_API_KEY"),
    "returnType": "XML",
    "outType": "1",
    "pageNum": "1",
    "pageSize": "10",
    "sort": "ASC",
    "sortCol": "TR_STT_DT",
    "srchTraStDt": "20180101",
    "srchTraEndDt": "20180101",
}


def get_date_range():
    with open(join(dirname(abspath(__file__)), "date_range.json"), "r+") as f:
        return json.load(f)


def get_all_from_2018(info_type: str):
    d = get_date_range()
    api_key = getenv("HRD_API_KEY")

    params = {
        "authKey": api_key,
        "returnType": "XML",
        "outType": "1",
        "pageSize": "10",
        "sort": "ASC",
        "sortCol": "TR_STT_DT",
    }

    inst_opt = {
        "authKey": api_key,
        "returnType": "XML",
        "outType": "2",
    }

    for i in d.keys():
        for j in d[i].keys():
            for k in range(int(d[i][j]["first"]), int(d[i][j]["last"])):
                a_day = "".join(
                    [i, j, str(k) if len(str(k)) == 2 else "".join(["0", str(k)])]
                )

                params["srchTraStDt"] = a_day
                params["srchTraEndDt"] = a_day

                idx = 1
                while True:
                    params["pageNum"] = idx

                    lst = get_training_list(params, info_type)
                    if len(lst) == 0:
                        break

                    for x in lst:
                        insert_training(x)

                        inst_opt["srchTrprId"] = x["tr_id"]
                        inst_opt["srchTrprDegr"] = x["degree"]

                        infos = get_institution_info_all(inst_opt, info_type)
                        
                        # 기관 정보 insert
                        insert_institution(infos["default"])
                        
                        # 시설물 정보 insert
                        for f in infos["facility_detail"]:
                            f["inst_code"] = infos["default"]["inst_code"]
                            f["tr_id"] = infos["default"]["tr_id"]
                            f['degree'] = infos['default']['tr_degree']
                            insert_facility(f)

                        # 장비 정보 insert
                        for e in infos["eqnm_detail"]:
                            e["inst_code"] = infos["default"]["inst_code"]
                            e["tr_id"] = infos["default"]["tr_id"]
                            e['degree'] = infos['default']['tr_degree']
                            insert_equipment(e)
                    idx = idx + 1


get_all_from_2018(info_type="job_hunter")
get_all_from_2018(info_type="worker")
get_all_from_2018(info_type="enterprise")
