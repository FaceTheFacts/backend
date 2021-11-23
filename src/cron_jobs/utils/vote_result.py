# Third Party
import pandas
from pandas.core.frame import DataFrame


def read_poll_vote_result_df() -> DataFrame:
    df = pandas.read_csv(
        "src/cron_jobs/utils/poll_vote_results.csv", encoding="utf8", header=0
    )
    return df


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
        return df[(df.poll_id == poll_id) & (df.vote == vote)]["count"].values[0]


def generate_vote_results():
    data_list = []
    df = read_poll_vote_result_df()
    poll_ids = df.poll_id.values
    for poll_id in poll_ids:
        if poll_id != None:
            new_dict = {
                "poll_id": poll_id,
                "yes": get_vote_result(df, poll_id, "yes"),
                "no": get_vote_result(df, poll_id, "no"),
                "abstain": get_vote_result(df, poll_id, "abstain"),
                "no_show": get_vote_result(df, poll_id, "no_show"),
            }
        data_list.append(new_dict)

    return data_list

