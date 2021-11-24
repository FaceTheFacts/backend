# std
from typing import List

# Third Party
import pandas
from pandas.core.frame import DataFrame


def read_csv(dir: str, header: any) -> DataFrame:
    df = pandas.read_csv(dir, encoding="utf8", header=header)
    return df


def read_poll_vote_result_df() -> DataFrame:
    return read_csv("src/cron_jobs/utils/poll_vote_results.csv", header=0)


def generate_poll_id_list() -> List:
    return read_csv("src/cron_jobs/utils/poll_id_list.csv", header=None).values.tolist()


def is_exist_vote_result(df: DataFrame, poll_id: int, vote: str) -> bool:
    if df[(df.poll_id == poll_id) & (df.vote == vote)]["count"].values.size > 0:
        return True
    else:
        return False


def get_vote_result(df: DataFrame, poll_id: int, vote: str) -> any:
    is_exist_result = is_exist_vote_result(df, poll_id, vote)
    if is_exist_result == False:
        return 0
    else:
        return df[(df.poll_id == poll_id) & (df.vote == vote)]["count"].values[0].item()


def generate_vote_results():
    data_list = []
    df = read_poll_vote_result_df()
    poll_ids = set(df.poll_id.values)
    poll_id_list = generate_poll_id_list()
    for poll_id in poll_ids:
        is_exist_poll_id = poll_id in poll_id_list
        if is_exist_poll_id:
            new_dict = {
                "yes": get_vote_result(df, poll_id, "yes"),
                "no": get_vote_result(df, poll_id, "no"),
                "abstain": get_vote_result(df, poll_id, "abstain"),
                "no_show": get_vote_result(df, poll_id, "no_show"),
                "poll_id": poll_id.item(),
            }
        data_list.append(new_dict)
    return data_list
