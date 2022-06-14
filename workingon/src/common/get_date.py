import calendar
from datetime import datetime

dates = {}
for i in range(2018, 2025):
    dates[i] = {}
    for j in range(1, 13):
        month_range = calendar.monthrange(i, j)
        if len(str(j)) == 1:
            j = "".join(["0", str(j)])
        else:
            j = str(j)
        dates[i][j] = {"first": "01", "last": str(month_range[1])}

with open("date_range.json", "w+") as f:
    import json

    f.write(json.dumps(dates))
