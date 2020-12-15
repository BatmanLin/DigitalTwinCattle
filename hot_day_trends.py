import matplotlib.pyplot as plt
from datetime import datetime
from average_24hr import *

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
#ave_day_other = average_day(other_data, 1)
ave_day_heat = average_day(heat_data, 1)
#ave_day = ave_day[7:] + ave_day[0:7]

x_axis = list(range(1,25))
# x_axis = list(range(7,25))+list(range(1,7))
# x_axis = [str(x) for x in x_axis]
#plt.plot(x_axis,ave_day_other, label="other")
plt.plot(x_axis,ave_day_heat, label="heat")
plt.legend(loc="upper right")
plt.title("resting")
plt.show()