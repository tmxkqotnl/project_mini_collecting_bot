from os import getenv
from sys import path
import sys
from dotenv import load_dotenv
from os.path import abspath, join, dirname


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


def get_all_from_2018(info_type: str):
    with open("/crawler/date_range.json", "r+") as f:
        import json

        d = json.load(f)
    for i in d.keys():
        for j in d[i].keys():
            for k in range(int(d[i][j]["first"]), int(d[i][j]["last"])):
                a_day = "".join(
                    [i, j, str(k) if len(str(k)) == 2 else "".join(["0", str(k)])]
                )

                params = {
                    "authKey": getenv("HRD_API_KEY"),
                    "returnType": "XML",
                    "outType": "1",
                    "pageSize": "10",
                    "sort": "ASC",
                    "sortCol": "TR_STT_DT",
                    "srchTraStDt": a_day,
                    "srchTraEndDt": a_day,
                }

                idx = 1
                while True:
                    params["pageNum"] = idx
                    lst = get_training_list(params, info_type)
                    if len(lst) == 0:
                        break

                    for x in lst:
                        if x["inst_code"] == "" or x["inst_code"] is None:
                            continue

                        insert_training(x)

                        inst_opt = {
                            "authKey": getenv("HRD_API_KEY"),
                            "returnType": "XML",
                            "outType": "2",
                            "srchTrprId": x["tr_id"],
                            "srchTrprDegr": x["degree"],
                        }

                        infos = get_institution_info_all(inst_opt, info_type)

                        insert_institution(infos["default"])
                        for f in infos["facility_detail"]:
                            f["inst_code"] = infos["default"]["inst_code"]
                            f["tr_id"] = infos["default"]["tr_id"]
                            insert_facility(f)

                        for e in infos["eqnm_detail"]:
                            e["inst_code"] = infos["default"]["inst_code"]
                            e["tr_id"] = infos["default"]["tr_id"]
                            insert_equipment(e)
                    idx = idx + 1


get_all_from_2018(info_type="job_hunter")
get_all_from_2018(info_type="worker")
get_all_from_2018(info_type="enterprise")
