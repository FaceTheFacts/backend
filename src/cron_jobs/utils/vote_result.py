# Third Party
import pandas
from pandas.core.frame import DataFrame


def read_poll_vote_result_df() -> DataFrame:
    df = pandas.read_csv(
        "src/cron_jobs/utils/poll_vote_results.csv", encoding="utf8", header=0
    )
    return df


def generate_vote_results():
    data_list = []
    df = read_poll_vote_result_df()
    poll_ids = df.poll_id.values
    for poll_id in poll_ids:
        if poll_id != None:
            new_dict = {
                "poll_id": poll_id,
                "yes": df[(df.poll_id == poll_id) & (df.vote == "yes")]["count"].values[
                    0
                ]
                if df[(df.poll_id == poll_id) & (df.vote == "yes")]["count"].values.size
                > 0
                else 0,
                "no": df[(df.poll_id == poll_id) & (df.vote == "no")]["count"].values[0]
                if df[(df.poll_id == poll_id) & (df.vote == "no")]["count"].values.size
                > 0
                else 0,
                "abstain": df[(df.poll_id == poll_id) & (df.vote == "abstain")][
                    "count"
                ].values[0]
                if df[(df.poll_id == poll_id) & (df.vote == "abstain")][
                    "count"
                ].values.size
                > 0
                else 0,
                "no_show": df[(df.poll_id == poll_id) & (df.vote == "no_show")][
                    "count"
                ].values[0]
                if df[(df.poll_id == poll_id) & (df.vote == "no_show")][
                    "count"
                ].values.size
                > 0
                else 0,
            }
        data_list.append(new_dict)

    return data_list


if __name__ == "__main__":
    print(generate_vote_results())
