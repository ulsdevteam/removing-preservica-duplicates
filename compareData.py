import csv
import sys


def read_data(file_name):

    data = set()
    with open(file_name, 'r', newline='', encoding='utf-8') as file:
        for line in file:
            split = line.strip().split('|')
            if len(split) == 2:
                title, ref_id = split
                data.add((title,ref_id))

    return data


def compare_datasets(file1, file2, file3):

    data1 = read_data(file1)
    data2 = read_data(file2)
    data3 = read_data(file3)

    print(f"total in actual content connected to islandora: {len(data1)}")
    print(f"total in new collection 145 opex: {len(data2)}")
    print(f"total in older collection 145 opex: {len(data3)}")

    common = data1 & data2 & data3
    file1_only = data1 - data2 - data3
    file1_and_file2 = data2 & data2
    file1_and_file3 = data1 & data3

    return common, file1_only, file1_and_file2, file1_and_file3

file1 = "important-ids.csv"
file2 = "145-islandora-preservica.csv"
file3 = "145_older_refs.csv"

# common, file1_only, file1_and_file2, file1_and_file3 = compare_datasets(file1, file2, file3)


# print("common entries: " )
# for entry in common:
#     print(entry)

# print("unique to actual islandora content: ")
# for entry in file1_only:
#     print(entry)

# print(f"common: {len(common)}")
# print(f"common between actual content and new opex: {len(file1_and_file2)}")
# print(f"common between actual content and older opex: {len(file1_and_file3)}")