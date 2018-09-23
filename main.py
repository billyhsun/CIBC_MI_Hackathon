import time, statistics
import numpy as np
import matplotlib.pyplot as plt
import pandas as pnd


def parse_data():
    time1 = time.time()
    parsed_data = []
    with open("claims_final.csv", 'r') as data:
        for line in data:
            temp = line.split(",")
            temp[0] = int(temp[0])
            temp[1] = int(temp[1])
            temp[2] = int(temp[2])
            temp[3] = int(temp[3])
            temp[4] = temp[4][1:-1]
            temp[5] = int(temp[5])
            temp[6] = int(temp[6])
            if temp[7].endswith('\n'):
                temp[7] = temp[7][:-2]
                temp[7] = temp[7][1:]
                temp[7] = float(temp[7])
            parsed_data.append(temp)

    # time2 = time.time()
    # time_taken = time2 - time1
    # print(time_taken)
    return parsed_data


# Plot any param2 over param1
def plot_params(param1_id, param2_id, parsed_data):
    data1 = []
    data2 = []

    for line in parsed_data:
        data1.append(line[param1_id])
        data2.append(line[param2_id])

    plt.plot(data1, data2, 'b.')
    plt.savefig('1.png')
    return


# Organize any two parameters into dictionary format
def organize_params(param1_id, param2_id, parsed_data):
    dictionary = {}

    for line in parsed_data:
        if line[param1_id] not in dictionary:
            dictionary[line[param1_id]] = []
            dictionary[line[param1_id]].append(line[param2_id])
        else:
            dictionary[line[param1_id]].append(line[param2_id])

    for key in dictionary:
        dictionary[key].sort()

    return dictionary


# Compile key : [no_of_items, smallest_item, largest_item, mean, median, mode, range, std_dev]
def compile_stats(dictionary, n):
    stats = {}

    for key in dictionary:
        if key not in stats and len(dictionary[key]) >= n:  # Only include keys with n or more items
            stats[key] = []
            stats[key].append(len(dictionary[key]))
            stats[key].append(min(dictionary[key]))
            stats[key].append(max(dictionary[key]))
            stats[key].append(round(statistics.mean(dictionary[key]), 1))
            stats[key].append(statistics.median(dictionary[key]))
            stats[key].append(statistics.mode(dictionary[key]))
            stats[key].append(round(max(dictionary[key]) - min(dictionary[key]), 1))
            if len(dictionary[key]) > 1:
                stats[key].append(round(statistics.stdev(dictionary[key]), 2))
            else:
                stats[key].append(-1)

    return stats


# Count frequency of operations / items in each category
def count_freq(dictionary):
    frequency = {}
    most_freq = {}

    for key in dictionary:
        if key not in frequency:
            frequency[key] = {}
            for i in dictionary[key]:
                if i not in frequency[key]:
                    frequency[key][i] = dictionary[key].count(i)

            # Get the item with maximum value
            if len(frequency[key]) > 1:
                a = max(frequency[key].values())
                for k, v in frequency[key].items():
                    if v == a:
                        most_freq[key] = k
            else:
                for k in frequency[key]:
                    most_freq[key] = k

    return frequency, most_freq


def get_doctors_freq():
    data = parse_data()
    dict1 = organize_params(6, 3, data)
    dict2 = organize_params(2, 6, data)
    dict3 = organize_params(2, 3, data)
    freq1, most_freq1 = count_freq(dict1)
    freq2, most_freq2 = count_freq(dict2)
    freq3, most_freq3 = count_freq(dict3)

    for key, value in freq2.items():
        if key in most_freq3:
            type = most_freq3[key]
            if type in most_freq1.values():
                for k, v in most_freq1.items():
                    if v == type and k in freq2[key]:
                        del freq2[key][k]

    no_of_illicit_procedures = {}
    for key, value in freq2.items():
        if len(freq2[key]) == 0:
            no_of_illicit_procedures[key] = 0
        else:
            if key not in no_of_illicit_procedures:
                no_of_illicit_procedures[key] = 0
                for v in freq2[key].values():
                    no_of_illicit_procedures[key] += v

    doctor_data = {}
    for key, value in no_of_illicit_procedures.items():
        if key not in doctor_data:
            doctor_data[key] = np.array([value])

    for key, value in doctor_data.items():
        print(key, value)

    return doctor_data

# Use numpy.insert to append to numpy array


# IDs:
# 0)     Patient Family ID
# 1)     Patient Family Member ID
# 2)     Provider ID
# 3)     Provider Type
# 4)     State Code
# 5)     Date of Service
# 6)     Medical Procedure Code
# 7)     Dollar Amount of Claim


def open_file(file_name):
    file = pnd.read_csv(file_name, header=None,
                        names=['FamID', 'FamMemID', 'ProvID', 'ProvType', 'State', 'Date', 'ProID', 'Cost'])
    return file


def get_doctors_cost():
    df = open_file("claims_final.csv")
    # numrows = len(df.index)
    # avg = []
    # sum = 0
    # count = 0
    dfdropped = df.drop(['FamID', 'FamMemID', 'ProvID', 'ProvType', 'State', 'Date'], axis=1)
    dfnewdropped = df.drop(['FamID', 'FamMemID', 'ProvType', 'State', 'Date'], axis=1)

    # thelist = df["Cost"].tolist()

    # uniqueProID = df.ProID.unique()
    # ProvIDUnique = df.ProvID.unique()

    dfmean = dfdropped.groupby(["ProID"]).mean()
    # print(dfmean.at[282, "Cost"])

    dfdoctor = dfnewdropped.groupby(["ProvID", "ProID"]).mean()
    # print(dfdoctor.keys)

    arr_doctor = dfdoctor.reset_index().values
    arr_means = dfmean.reset_index().values

    # print(dfdoctor)
    # print(dfmean)

    doctor_data = {}
    for i in range(arr_doctor.shape[0]):
        if arr_doctor[i, 0] not in doctor_data:
            doctor_data[arr_doctor[i, 0]] = []
            for k in range(1520):
                if arr_means[k, 0] < arr_doctor[i, 1]:
                    doctor_data[arr_doctor[i, 0]].append(arr_means[k, 1])
                if arr_means[k, 0] > arr_doctor[i, 1]:
                    doctor_data[arr_doctor[i, 0]].append(arr_means[k, 1])
                else:
                    doctor_data[arr_doctor[i, 0]].append(arr_doctor[i, 2])
        else:
            for k in range(1520):
                if arr_means[k, 0] == arr_doctor[i, 1]:
                    doctor_data[arr_doctor[i, 0]].append(arr_doctor[i, 2])

    return doctor_data


data = get_doctors_cost()

# for k, v in data.items():
#     print(k, v)


