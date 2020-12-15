import matplotlib.pyplot as plt
from datetime import datetime
from average_24hr import *

# directary of data
data_dir = 'HeatData/csvs_brisbane_18_10_18__2_1_19_tags/'
file_name = 'DailyCowStates_Brisbane Valley Feedlot_'

# definitions of state
state_data = {0: "side lying",
              1: "resting",
              2: "medium activity",
              3: "high activity",
              4: "rumination",
              5: "eating",
              6: "walking",
              7: "grazing",
              8: "panting",
              9: "unsure",
              15: "invalid data"}

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

# define states to run and default x_axis
#state_indeces = [1, 4, 7, 8, 15]
state_indeces = [0, 2, 3, 5, 6, 9]
x_axis = list(range(1,25))

# create plots for each state
for state_index in state_indeces:
    print("Plotting for " + str(state_data[state_index]))
    # calculate the average day for each dataset
    ave_day_other = average_day(other_data, state_index)
    print("First dataset complete")
    ave_day_heat = average_day(heat_data, state_index)
    print("Second dataset complete")

    # plot the two data sets
    plt.figure(state_index)
    plt.plot(x_axis,ave_day_other, label="other")
    plt.plot(x_axis,ave_day_heat, label="heat")
    plt.legend(loc="upper right")
    plt.title("Average time spent " + str(state_data[state_index]) + " (all Cattle 19-Oct-18 to 1-Jan-19)")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Average minutes " + str(state_data[state_index]) + " per hour")

# show plots
plt.show()