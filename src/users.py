import pandas as pd


users_db_path = "src/db/users.txt"


class Users:
    def __init__(self) -> None:
        pass

    def get_all_user(self):
        users = pd.read_csv(users_db_path, sep="\t", index_col=0)
        return users["name"].values

    def get_all_seats(self):
        users = pd.read_csv(users_db_path, sep="\t", index_col=0)
        return users["seats"].to_list()
