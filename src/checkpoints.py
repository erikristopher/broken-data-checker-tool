import re
import data


def valid_name_field(field_value):
    return re.findall(r"(^[\d\w\s\.\,\'\-\#\+\&]+$)", field_value)


def valid_city_field(field_value):
    return re.findall(r"(^[\w\s\.\,\'\-\&\#]+$)", field_value)


def valid_address_field(field_value):
    return re.findall(r"(^[\d\w\s\.\,\'\-\#]+$)", field_value)


def valid_email_address(field_value):
    return re.findall(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", field_value) != []


def are_all_numbers(field_value):
    return re.findall(r"(^[\d]+$)", field_value) != []


def has_number(field_value):
    return re.findall(r"([\d]+)", field_value) != []


def starting_with_number(field_value):
    return re.findall(r"(^[\d]+[\d\w\s\.\,\'\-\#]+$)", field_value) != []


def valid_mail_state(field_value):
    return field_value.strip().upper() in data.States


def valid_mailing_zip(field_value):
    return re.findall(r"(^\d{3,6}[\-\d{3,5}]*$)", field_value) != []


def invalid_ampersand_place(field_value):
    return re.findall(r"(^\&+[\s\w\d]+)|([\s\w\d]+\&+$)|([\w\d]+\&[\w\d]+)", field_value)


def has_seed_row(row, file_name):
    name = re.sub(r"[^A-Z\sa-z0-9]+", '', row.full_name)
    new_name = name.strip(" ").lower()
    return all(x in file_name.lower() for x in new_name)


def has_date(field_value):
    return re.findall(r"\([\d]+[-\/\\]+[\d]+[-\/\\]+[\d]+\)", field_value) != []


def has_invalid(field_value, values):
    formatted_value = field_value.strip().lower()
    flag = []
    for value in values:
        if value == "address":
            flag.append("unassigned" in formatted_value)
        elif value == "all":
            flag.append("unavailable" in formatted_value)
        elif value == "names":
            flag.append("owner" == formatted_value)
        elif value == "null":
            flag.append("null" in formatted_value)
        elif value == "zero":
            flag.append("0" == formatted_value)
        elif value == "empty":
            flag.append("" == formatted_value)
        elif value == "pobox":
            flag.append("po box box" in formatted_value)
        elif value == "xx":
            flag.append("xx" in formatted_value)
        elif value == "ampersand":
            flag.append("&" in formatted_value and invalid_ampersand_place(formatted_value))

    return any(flag)


def has_characters(field_value):
    return re.findall(r"([\w]+)", field_value)


def has_fractions(field_value):
    return re.findall(r"(\d+/\d+)", field_value)


def check_data(im_data):
    error_count = 0
    error_message = ""
    # Full name validation
    fullname_validation = are_all_numbers(im_data.full_name) or has_date(im_data.full_name) or \
                          has_invalid(im_data.full_name, ["null", "ampersand", "xx", "zero", "empty", "all"]) or \
                          not valid_name_field(im_data.full_name)
    if fullname_validation:
        error_count += 1
        error_message += "[X] Full name: {} ".format(im_data.full_name)
    # First name validation
    if has_invalid(im_data.first_name, ["ampersand", "zero", "xx", "null", "names", "all"]) or \
            (not has_invalid(im_data.first_name, ["empty"]) and
             (im_data.first_name not in im_data.full_name or
              not valid_name_field(im_data.first_name) or
              not has_characters(im_data.first_name))) or \
            (not fullname_validation and has_number(im_data.full_name)
             and (not has_invalid(im_data.first_name, ["empty"]) or im_data.first_name not in im_data.full_name)):
        error_count += 1
        error_message += "[X] First name: {} ".format(im_data.first_name)
    # Mailing address validation
    if has_invalid(im_data.mailing_address, ["zero", "pobox", "xx", "address", "all"]) or \
            not valid_address_field(im_data.mailing_address) or \
            are_all_numbers(im_data.mailing_address) or \
            has_fractions(im_data.mailing_address):
        error_count += 1
        error_message += "[X] Mailing address: {} ".format(im_data.mailing_address)
    # Mailing zip validation
    if not valid_mailing_zip(im_data.mailing_zip):
        error_count += 1
        error_message += "[X] Mailing zip: {} ".format(im_data.mailing_zip)
    # Mailing state validation
    if not valid_mail_state(im_data.mailing_state):
        error_count += 1
        error_message += "[X] Mailing state: {} ".format(im_data.mailing_state)
    # Mailing city validation
    if has_invalid(im_data.mailing_city, ["zero", "all"]) or valid_mail_state(im_data.mailing_city) or \
            not valid_city_field(im_data.mailing_city):
        error_count += 1
        error_message += "[X] Mailing city: {} ".format(im_data.mailing_city)
    # Property address validation
    if has_invalid(im_data.property_address, ["zero", "empty", "xx", "address", "all"]) or \
            not valid_address_field(im_data.property_address) or \
            has_fractions(im_data.property_address):
        error_count += 1
        error_message += "[X] Property address: {} ".format(im_data.property_address)

    return error_count, error_message
