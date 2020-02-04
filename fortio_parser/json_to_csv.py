import json
import math
import glob
import csv


def parse_fortio_json(file_name):
    # read file
    with open(file_name, 'r') as json_file:
        data = json_file.read()

    # parse file
    obj = json.loads(data)

    # show values
    start_time = str(obj['StartTime'])
    actual_duration = str(int((obj['ActualDuration']/1000000000)))
    labels = str(obj['Labels'])
    num_threads = str(obj['NumThreads'])
    actual_QPS = str(math.ceil(obj['ActualQPS']))
    percentiles = obj['DurationHistogram']['Percentiles']
    if "nighthawk" in file_name:
        p50 = round(percentiles[0]['Value'] * 1000, 3)  # ms
        p90 = round(percentiles[3]['Value'] * 1000, 3)
        p99 = round(percentiles[5]['Value'] * 1000, 3)
    else:
        p50 = round(percentiles[0]['Value'] * 1000, 3)  # ms
        p90 = round(percentiles[2]['Value'] * 1000, 3)
        p99 = round(percentiles[3]['Value'] * 1000, 3)
    perf_row_list = [start_time, actual_duration, labels, num_threads, actual_QPS, p50, p90, p99]
    return perf_row_list


def write_perf_number_to_csv(perf_num_list):
    with open('nighthawk.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['StartTime', 'ActualDuration', 'Labels', 'NumThreads', 'ActualQPS', 'p50', 'p90', 'p99'])
        for lst in perf_num_list:
            writer.writerow([lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7]])


def parse_perf_num():
    fortio_json_file_path = ""    # fill out the folder path of all your fortio format json files
    perf_num_list = []
    for file_name in glob.glob(fortio_json_file_path + "/*.json"):
        # print(file_name)
        perf_row_list = parse_fortio_json(file_name)
        perf_num_list.append(perf_row_list)
    # print(perf_num_list)
    write_perf_number_to_csv(perf_num_list)


parse_perf_num()
