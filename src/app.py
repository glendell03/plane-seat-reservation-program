import numpy as np
import pandas as pd
import numpy as np
from os.path import exists

seats_db_path = "src/db/seats.txt"
seats = {
    " A  ": np.array(["[   ]" for i in range(1, 100)]),
    " B  ": np.array(["[   ]" for i in range(1, 100)]),
    " C  ": np.array(["[   ]" for i in range(1, 100)]),
    "    ": np.array(["     " for i in range(1, 100)]),
    " D  ": np.array(["[   ]" for i in range(1, 100)]),
    " E  ": np.array(["[   ]" for i in range(1, 100)]),
    " F  ": np.array(["[   ]" for i in range(1, 100)]),
}

df = pd.DataFrame(
    pd.read_csv(seats_db_path, sep="\t", index_col=0)
    if exists(seats_db_path)
    else seats
)
df.index = np.array(["{:02}".format(num) for num in range(1, 100)])


def getCell(index, col):
    return df.at[index, f" {col}  "]


def updateCell(index, col):
    df.at[index, f" {col}  "] = "[ x ]"
    df.to_csv(seats_db_path, sep="\t")


updateCell("01", "B")
print(df)
# print(getCell("01", "A"))
