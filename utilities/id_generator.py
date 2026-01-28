import hashlib


def generate_employee_id(first_name: str, last_name: str) -> str:
    """
    Generate unique employee ID from name using MD5 hash.

    :param first_name: Employee first name
    :type first_name: str
    :param last_name: Employee last name
    :type last_name: str
    :return: MD5 hash of the combined name
    :rtype: str
    """
    data = first_name + last_name
    return hashlib.md5(data.encode("utf-8")).hexdigest()
