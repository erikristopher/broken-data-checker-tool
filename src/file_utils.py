import copy
import glob
import re
import csv
import os

from src import data

your_path = "D:/UPWORK/MyTools/"


def read_files(path):
    data_map = {}
    header = []
    for file_path in glob.glob(path):
        with open(file_path, 'r') as file:
            read_file = csv.reader(file)
            file_name = re.findall(r"\\([\w\-\.\,\_\s\d]+)", file_path)
            print(file_name)
            header = next(read_file)
            list_data = []
            for row in read_file:
                im_data = data.Data()
                im_data.full_name = row[0]
                im_data.first_name = row[1]
                im_data.mailing_address = row[2]
                im_data.mailing_city = row[3]
                im_data.mailing_state = row[4]
                im_data.mailing_zip = row[5]
                im_data.property_address = row[6]
                im_data.row = row
                list_data.append(im_data)
            data_map[file_name[0]] = list_data
    return data_map, header


def write_to_csv(path, dir_name, data_list, tag, header, err_count):
    file_name = "{}_{}.csv".format(tag, dir_name)
    new_header = header
    if tag == "NO_GOOD":
        new_header = copy.deepcopy(header)
        new_header.insert(0, "Errors")
        file_name = "{}_{}_{}.csv".format(tag, str(err_count), dir_name)
    csv_err_path = os.path.join(path, file_name)
    with open(csv_err_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_header)
        for data_dict in data_list:
            if tag == "NO_GOOD":
                data_dict["row"].insert(0, data_dict["error_message"])
            writer.writerow(data_dict["row"])


def create_csv(error_list, no_error_list, dir_name, header, err_count, has_error):
    new_dir_name = dir_name
    if has_error:
        new_dir_name = "{} {}".format("[ERRORS]", dir_name)
    chk_abs_path = "broken-data-checker-tool/checked_files/"
    path = os.path.join(os.path.join(your_path, chk_abs_path), new_dir_name)
    os.mkdir(path)
    write_to_csv(path, dir_name, error_list, "NO_GOOD", header, err_count)
    write_to_csv(path, dir_name, no_error_list, "GOOD", header, err_count)
