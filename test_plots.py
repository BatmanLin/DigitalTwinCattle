import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

def average_day(data, state):
    average_day = []
    # loop through the raw data from each day
    for key, value in data.items():
        if not len(value.index) == 1440:
            continue
        # calculate minute spent in given state per hour for each animal
        per_hour_df = create_mins_per_hour(value, state)
        # average mins per hour for a given day across all animals
        average_mins_day = average_cows(per_hour_df)
        print(average_mins_day)
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

def average_cows(per_hour_df):
    daily_average_mins = []
    for time in per_hour_df.columns:
        if time=='Cow':
            continue
        average_mins = per_hour_df[time].mean()
        daily_average_mins.append(average_mins)
    return daily_average_mins

def create_mins_per_hour(df, state):

    per_hour_list = []

    for cow in df.columns:
        if cow == 'Cow':
            continue
        cow_df = df[cow]
        new_cow_data = [cow]

        state_count = 0
        for index, value in cow_df.items():
            if value == state:
                state_count+=1
            if not (index+1)%60:
                new_cow_data.append(state_count)
                state_count=0

        per_hour_list.append(new_cow_data)

    columns = ["Cow"] + list(range(0,24))
    per_hour_df = pd.DataFrame(per_hour_list, columns = columns)
    return per_hour_df


data_dir = 'HeatData/csvs_brisbane_18_10_18__2_1_19_tags/'
file_name = 'DailyCowStates_Brisbane Valley Feedlot_'

# create date range for extracting data from excel
total_date_list = pd.date_range(datetime(2018, 10, 19), periods=76).tolist()
# dates of heat taken from paper
hot_date_set = set(total_date_list[16:20] + total_date_list[42:46] + total_date_list[62:65])

# split into hot data and other data
heat_data = {}
other_data = {}
for date in total_date_list:
    date_str = date.strftime("%d-%b-%Y")
    date_df = pd.read_csv(data_dir + file_name + date_str + '.csv')
    #print(date_df)
    if date in hot_date_set:
        heat_data[date_str] = date_df
    else:
        other_data[date_str] = date_df

# calculate the average day for a given dataset and state
ave_day_other = average_day(other_data, 1)
ave_day_heat = average_day(heat_data, 1)
#ave_day = ave_day[7:] + ave_day[0:7]

x_axis = list(range(1,25))
# x_axis = list(range(7,25))+list(range(1,7))
# x_axis = [str(x) for x in x_axis]
plt.plot(x_axis,ave_day_other, label="other")
plt.plot(x_axis,ave_day_heat, label="heat")
plt.legend(loc="upper right")
plt.title("resting")
plt.show()

