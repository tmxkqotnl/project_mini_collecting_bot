import traceback
import sys
from os.path import abspath, dirname, join
import json


def error_handler(func):
    def inner(*args, **kargs):
        try:
            return func(*args, **kargs)
        except Exception as e:
            file_path = dirname(dirname(dirname(abspath(__file__))))

            with open(
                join(file_path, "/crawlererror_logging.json"), "a+", encoding="utf-8"
            ) as f:
                f.write(
                    json.dumps(
                        {"traceback": traceback.format_exc(), "params": args},
                        ensure_ascii=False,
                    )
                )

            # for dev
            print(traceback, file=sys.stdout)
            print(e, file=sys.stdout)

            return None

    return inner
