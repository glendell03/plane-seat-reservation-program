import re
import numpy as np
import pandas as pd
import numpy as np
from os.path import exists

seats_db_path = "src/db/seats.txt"
users_db_path = "src/db/users.txt"


class Seats:

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

    def __init__(self, current_user) -> None:
        self.df = Seats.df
        self.users = pd.read_csv(users_db_path, sep="\t", index_col=0)
        self.current_user = current_user
        # self.user = user

    def __str__(self) -> str:
        return self.viewAll().to_string()

    def displayUsersSeats(self, seats, mark):
        for index, values in enumerate(seats):
            self.df.at[seats[index][:2], f" {seats[index][-1]}  "] = f"[ {mark} ]"
        return self.df.to_string()

    def display_current_user_seats(self):
        current_user = self.users.loc[self.users["name"] == self.current_user]

        if pd.isna(current_user["seats"].values[0]):
            return self.df.to_string()
        seats = str(current_user["seats"].values[0]).split(",")

        self.displayUsersSeats(seats, "✔")

        return self.df

    def display_other_user_seats(self):
        other_user = self.users.loc[self.users["name"] != self.current_user]

        taken_seat_list = []
        taken_seats = other_user["seats"]
        for i in taken_seats:
            res = str(i).split(",")
            taken_seat_list += res
        self.displayUsersSeats(taken_seat_list, "✖")

        return self.df

    def viewAll(self):
        self.display_current_user_seats()
        self.display_other_user_seats()

        return self.df

    def reserve(self, input_data):
        users = pd.read_csv(users_db_path, sep="\t", index_col=0)

        seats = re.sub("\s+", ",", input_data.strip())

        current_seats = users.loc[users["name"] == self.current_user, "seats"].values[0]

        users_index = users.loc[users["name"] == self.current_user].index[0]
        users.at[users_index, "seats"] = f"{current_seats},{seats}"

        users.to_csv(users_db_path, sep="\t")

        return users

    def update(self, remove, add):
        users = pd.read_csv(users_db_path, sep="\t", index_col=0)
        user_reserved_seats = np.array(
            (users.loc[users["name"] == self.current_user, "seats"].values[0]).split(
                ","
            )
        )
        user_reserved_seats = np.delete(
            user_reserved_seats, np.where(user_reserved_seats == remove)
        )
        user_reserved_seats = np.append(user_reserved_seats, add)

        users_index = users.loc[users["name"] == self.current_user].index[0]
        users.at[users_index, "seats"] = ",".join(user_reserved_seats)

        self.df.at[remove[:-1], f" {remove[-1]}  "] = "[   ]"
        users.to_csv(users_db_path, sep="\t")
        return users

    def delete(self, remove):
        users = pd.read_csv(users_db_path, sep="\t", index_col=0)
        user_reserved_seats = np.array(
            (users.loc[users["name"] == self.current_user, "seats"].values[0]).split(
                ","
            )
        )
        user_reserved_seats = np.delete(
            user_reserved_seats, np.where(user_reserved_seats == remove)
        )

        users_index = users.loc[users["name"] == self.current_user].index[0]
        users.at[users_index, "seats"] = ",".join(user_reserved_seats)

        self.df.at[remove[:-1], f" {remove[-1]}  "] = "[   ]"
        users.to_csv(users_db_path, sep="\t")

        return users


# if __name__ == "__main__":
#     seats = Seats("Glendell")
#     # print(seats)
#     print(seats.delete("99D"))
#     print(seats.viewAll())
