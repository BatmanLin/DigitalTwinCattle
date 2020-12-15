# Script contains functions for converting cattle behaviour state data contained in excel files
# to summary data which represents the average 24 hour cycle of the herd for given behaviour types.
# see average_day function for details of inputs.

import pandas as pd

def average_day(data, state):
    """
    takes the raw excel data and converts it to the average 24 hours cycle of the herd for the
    selected state.

    :param data: a dictionary containing dates as keys and the corresponding excel data stored in
    a dataframe as the values.
    :param state: a number of range 1-9 or 15 denoting the animal state of interest.
    :return:
    """

    average_day = []
    # loop through the raw data from each day
    for key, value in data.items():
        if not len(value.index) == 1440:
            continue
        # calculate minute spent in given state per hour for each animal
        per_hour_df = create_mins_per_hour(value, state)
        # average mins per hour for a given day across all animals
        average_mins_day = average_cows(per_hour_df)
        # create a list of the distributions for each day
        for i in range(0,len(average_mins_day)):
            if not len(average_day)==24:
                average_day.append([average_mins_day[i]])
            else:
                average_day[i].append(average_mins_day[i])
    # find average of distribution
    for i in range(0, len(average_day)):
        average_day[i] = sum(average_day[i])/len(average_day[i])
    return average_day

def create_mins_per_hour(df, state):
    """
    takes the dataframe of single day with per minute cow state recorded for every day. This function
    converts this to a dataframe where each row corresponds to a cow and each column corresponds to an
    hour of the day. The time per hour spent in the input state is calculated and stored in each element.

    :param df:
    :param state:
    :return:
    """
    per_hour_list = []
    # iterate through each cow (columns)
    for cow in df.columns:
        # ignore first column as this is the time.
        if cow == 'Cow':
            continue
        # extract the cow df
        cow_df = df[cow]
        new_cow_data = [cow]
        # iterate through the column of each cow and count the time spent in the given state each hour.
        state_count = 0
        for index, value in cow_df.items():
            if value == state:
                state_count+=1
            if not (index+1)%60:
                new_cow_data.append(state_count)
                state_count=0
        # add this to the list
        per_hour_list.append(new_cow_data)

    # create new columns headings, the cow ID and the hour of the day.
    columns = ["Cow"] + list(range(0,24))
    # convert data to dataframe.
    per_hour_df = pd.DataFrame(per_hour_list, columns = columns)
    return per_hour_df


def average_cows(per_hour_df):
    """
    recieves the dataframe summarising time spent in the given state each hour for each animal across a
    given day and finds the average for each hour across all animals.

    :param per_hour_df:
    :return:
    """
    # iterate through each time, calculate the average time spent in each state and add to list.
    daily_average_mins = []
    for time in per_hour_df.columns:
        if time == 'Cow':
            continue
        average_mins = per_hour_df[time].mean()
        daily_average_mins.append(average_mins)

    return daily_average_mins
