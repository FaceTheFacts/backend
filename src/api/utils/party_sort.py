import itertools


def party_sort(politicians):
    highest_popularity = []
    medium_popularity = []
    low_popularity = []
    lowest_popularity = []
    sorted_politicians = [None] * 4

    for politician in politicians:
        party_id = politician.party.id
        if party_id == 1 or party_id == 2:
            highest_popularity.append(politician)
        elif party_id == 3 or party_id == 4 or party_id == 5:
            medium_popularity.append(politician)
        elif party_id == 8 or party_id == 9:
            low_popularity.append(politician)
        else:
            lowest_popularity.append(politician)
    sorted_politicians[0] = highest_popularity
    sorted_politicians[1] = medium_popularity
    sorted_politicians[2] = low_popularity
    sorted_politicians[3] = lowest_popularity
    return list(itertools.chain(*sorted_politicians))
