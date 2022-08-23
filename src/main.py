import file_utils
import checkpoints
import os
import sys

#your_path = "D:/Erik/UPWORK/Tool/"
your_path = sys.argv[1]

if __name__ == '__main__':
    abs_path = "broken-data-checker-tool/unchecked_files/*.csv"
    im_data_list = {}
    im_data_list_checked = []
    im_data_list, header = file_utils.read_files(os.path.join(your_path, abs_path))
    for im_file_name, im_data in im_data_list.items():
        each_file_data_list_errors = []
        each_file_data_list_no_errors = []
        row_list_errors = []
        row_list_no_errors = []
        each_file_dict = {}
        seed_dict = {}
        all_errors_count = 0
        seed_row_err = 0
        seed_row = im_data[0]
        has_error = False
        # if not checkpoints.has_seed_row(seed_row, im_file_name):
        #     err_count, err_message = checkpoints.check_data(seed_row)
        #     seed_row_err = 1
        #     err_count += seed_row_err
        #     err_message += "[X] No seed row found for {}".format(im_file_name)
        #     seed_dict["error_count"] = err_count
        #     seed_dict["error_message"] = err_message
        #     seed_dict["row"] = seed_row.row
        count = 0
        for data in im_data:
            check_dict = {}
            error_count = 0
            error_message = ""
            if count == 0:
                count += 1
            else:
                error_count, error_message = checkpoints.check_data(data)
            check_dict["error_count"] = error_count
            check_dict["error_message"] = error_message
            check_dict["row"] = data.row
            if error_count == 0:
                each_file_data_list_no_errors.append(check_dict)
                row_list_no_errors.append(data.row)
            else:
                each_file_data_list_errors.append(check_dict)
                row_list_errors.append(data.row)
            all_errors_count += error_count
            each_file_dict["file_name"] = im_file_name
            each_file_dict["no_error_list"] = each_file_data_list_no_errors
            each_file_dict["error_list"] = each_file_data_list_errors
        # if seed_row_err == 1:
        #     if err_count > 0:
        #         each_file_data_list_errors.append(seed_dict)
        #         all_errors_count += err_count
        #     else:
        #         each_file_data_list_no_errors.append(seed_dict)
        if len(row_list_errors) != 0:
            has_error = True
        file_utils.create_csv(each_file_data_list_errors, each_file_data_list_no_errors,
                              im_file_name.replace(".csv", ""), header, all_errors_count, has_error)
        im_data_list_checked.append(each_file_dict)
    print("Done processing files")
