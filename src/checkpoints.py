import re
import data


def valid_name_field(field_value):
    return re.findall(r"(^[\d\w\s\|\.\,\'\(\)\-\&\/\\\#]+$)", field_value)


def valid_address_field(field_value):
    return re.findall(r"(^[\d\w\s\|\.\,\'\(\)\-\#\/\\\&]+$)", field_value)


def valid_email_address(field_value):
    return re.findall(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", field_value) != []


def is_empty_field(field_value):
    return field_value.strip().lower() == ""


def are_all_numbers(field_value):
    return re.findall(r"(^[\d]+$)", field_value) != []


def has_number(field_value):
    return re.findall(r"([\d]+)", field_value) != []


def starting_with_number(field_value):
    return re.findall(r"(^[\d]+[\d\w\s\|\.\,\'\(\)\-\#]+$)", field_value) != []


def valid_mail_state(field_value):
    return field_value.strip().upper() in data.States


def valid_mailing_zip(field_value):
    return re.findall(r"(^[\d\-]+$)", field_value) != []


def check_data(im_data):
    error_count = 0
    error_message = ""
    # Full name validation
    fullname_validation = not valid_name_field(im_data.full_name) or is_empty_field(im_data.full_name)
    if fullname_validation:
        error_count += 1
        error_message += "[X] Full name: {}".format(im_data.full_name)
    # First name validation
    if (im_data.first_name != "" and
        (im_data.first_name not in im_data.first_name or not valid_name_field(im_data.first_name))) or \
            (not fullname_validation and starting_with_number(im_data.full_name)
             and im_data.full_name != im_data.first_name):
        error_count += 1
        error_message += "[X] First name: {}".format(im_data.first_name)
    # Mailing address validation
    if not valid_address_field(im_data.mailing_address) or \
            are_all_numbers(im_data.mailing_address):
        error_count += 1
        error_message += "[X] Mailing address: {}".format(im_data.mailing_address)
    # Mailing zip validation
    if not valid_mailing_zip(im_data.mailing_zip):
        error_count += 1
        error_message += "[X] Mailing zip: {}".format(im_data.mailing_zip)
    # Mailing state validation
    if not valid_mail_state(im_data.mailing_state):
        error_count += 1
        error_message += "[X] Mailing state: {}".format(im_data.mailing_state)
    # Mailing city validation
    if valid_mail_state(im_data.mailing_city) or \
            not valid_name_field(im_data.mailing_city):
        error_count += 1
        error_message += "[X] Mailing city: {}".format(im_data.mailing_city)
    # Mailing city validation
    if is_empty_field(im_data.property_address) or \
            not valid_address_field(im_data.property_address):
        error_count += 1
        error_message += "[X] Property address: {}".format(im_data.property_address)

    return error_count, error_message
