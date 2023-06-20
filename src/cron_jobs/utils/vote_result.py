# std
from typing import List

# Third Party
import pandas
from pandas.core.frame import DataFrame
from sqlalchemy.orm import Session

from src.db.models import *


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


def get_vote_result(session: Session, poll_id: int) -> any:
    votes_per_fraction = (
        session.query(PollResultPerFraction)
        .filter(PollResultPerFraction.poll_id == poll_id)
        .first()
    )
    if votes_per_fraction:
        yes_results = (
            session.query(PollResultPerFraction.total_yes)
            .filter(PollResultPerFraction.poll_id == poll_id)
            .all()
        )
        yes_results_arr = [yes_result[0] for yes_result in yes_results]
        no_results = (
            session.query(PollResultPerFraction.total_no)
            .filter(PollResultPerFraction.poll_id == poll_id)
            .all()
        )
        no_results_arr = [no_result[0] for no_result in no_results]
        abstain_results = (
            session.query(PollResultPerFraction.total_abstain)
            .filter(PollResultPerFraction.poll_id == poll_id)
            .all()
        )
        abstain_results_arr = [abstain_result[0] for abstain_result in abstain_results]
        no_show_results = (
            session.query(PollResultPerFraction.total_no_show)
            .filter(PollResultPerFraction.poll_id == poll_id)
            .all()
        )
        no_show_results_arr = [no_show_result[0] for no_show_result in no_show_results]
        vote_results = {
            "yes": sum(yes_results_arr),
            "no": sum(no_results_arr),
            "abstain": sum(abstain_results_arr),
            "no_show": sum(no_show_results_arr),
        }
        return vote_results
    return None


def generate_vote_results(session: Session):
    data_list = []
    polls = session.query(Poll.id).order_by(Poll.id.asc()).all()
    poll_ids = [poll_id[0] for poll_id in polls]
    vote_results = session.query(VoteResult.poll_id).all()
    vote_results_poll_ids = [
        vote_results_poll_id[0] for vote_results_poll_id in vote_results
    ]
    for poll_id in poll_ids:
        if poll_id not in vote_results_poll_ids:
            new_item = get_vote_result(session, poll_id)
            if new_item:
                new_dict = {
                    "yes": new_item["yes"],
                    "no": new_item["no"],
                    "abstain": new_item["abstain"],
                    "no_show": new_item["no_show"],
                    "poll_id": poll_id,
                }
                data_list.append(new_dict)
    return data_list


def generate_appended_vote_results(session: Session, last_id: int, last_poll_id: int):
    data_list = []
    polls = (
        session.query(Poll.id)
        .where(Poll.id > last_poll_id)
        .order_by(Poll.id.asc())
        .all()
    )
    poll_ids = [poll[0] for poll in polls]
    for poll_id in poll_ids:
        last_id += 1
        new_item = get_vote_result(session, poll_id)
        if new_item:
            new_dict = {
                "id": last_id,
                "yes": new_item["yes"],
                "no": new_item["no"],
                "abstain": new_item["abstain"],
                "no_show": new_item["no_show"],
                "poll_id": poll_id,
            }
            data_list.append(new_dict)
    return data_list


def get_total_votes_of_type(
    vote_type: str, poll_id: int, fraction_id: int, session: Session
):
    return (
        session.query(Vote.id)
        .filter(Vote.poll_id == poll_id)
        .filter(Vote.vote == vote_type)
        .filter(Vote.fraction_id == fraction_id)
        .count()
    )
