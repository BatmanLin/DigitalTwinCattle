import matplotlib.pyplot as plt
from datetime import datetime
from average_24hr import *

def create_category_dict(category_header, cow_ID_header, details_df):
    categories = set(cow_details_df[category_header])
    category_dict = {key: [] for key in categories}
    for category in categories:
        category_dict[category] = details_df[cow_ID_header][details_df[category_header] == category].tolist()
    #print(category_dict)
    return category_dict

# directary of animal state data and anaimal information
data_dir = 'HeatData/csvs_brisbane_18_10_18__2_1_19_tags/'
file_name = 'DailyCowStates_Brisbane Valley Feedlot_'
animal_info_name = 'Cow_ID.csv'

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

# store cow info in dataframe
cow_details_df = pd.read_csv(data_dir + animal_info_name)
# sort cow IDs into categories using dictionaries
breed_dict = create_category_dict("Breed", "Tag#", cow_details_df)
coat_dict = create_category_dict("Coat colour", "Tag#", cow_details_df)
docility_dict = create_category_dict("Docility score", "Tag#", cow_details_df)
# select cows to be plotted, cow_category is the descriptor for the plot title.
cow_category = "Red"
plot_cows = [str(x) for x in coat_dict["Red"]]

# create date range for extracting data from excel
total_date_list = pd.date_range(datetime(2018, 10, 19), periods=76).tolist()
# dates of heat taken from paper
hot_date_set = set(total_date_list[16:20] + total_date_list[42:46] + total_date_list[62:65])

# split into hot data and other data
heat_data = {}
other_data = {}


for date in total_date_list:
    # upload daily data
    date_str = date.strftime("%d-%b-%Y")
    date_df = pd.read_csv(data_dir + file_name + date_str + '.csv')
    new_columns = ["Cow"] + [x for x in plot_cows if x in date_df.columns]

    date_df = date_df[new_columns]

    if date in hot_date_set:
        heat_data[date_str] = date_df
    else:
        other_data[date_str] = date_df


# define states to run and default x_axis
# state_indeces = [1, 2, 3, 4, 5, 6, 7, 8, 9, 15]
state_indeces = [1, 5, 8]
x_axis = list(range(1,25))

# create plots for each state
for state_index in state_indeces:
    print("Plotting for " + str(state_data[state_index]))
    # calculate the average day for each dataset
    ave_day_other = average_day(other_data, state_index)
    # rotate list to transfer times to GMT+10
    ave_day_other = ave_day_other[-10:] + ave_day_other[:-10]
    print("First dataset complete")
    ave_day_heat = average_day(heat_data, state_index)
    # again adjust timing
    ave_day_heat = ave_day_heat[-10:] + ave_day_heat[:-10]
    print("Second dataset complete")

    # plot the two data sets
    plt.figure(state_index)
    plt.plot(x_axis,ave_day_other, label="other")
    plt.plot(x_axis,ave_day_heat, label="heat")
    plt.legend(loc="upper right")
    plt.title("Average time spent " + str(state_data[state_index]) + " (" + cow_category + " Cattle 19-Oct-18 to 1-Jan-19)")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Average minutes " + str(state_data[state_index]) + " per hour")

# show plots
plt.show()