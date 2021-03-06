import glob
import os
import pathlib
import pkgutil
import re
import random
import string
import unicodedata


def get_modules_list(package_path, glob_expression):
    paths = glob.glob(os.path.join(package_path, glob_expression), recursive=True)
    modules = []
    for file_handler, module, _ in pkgutil.walk_packages(path=paths):
        packages = ".".join(filter(None, file_handler.path.replace(package_path, '').split(os.sep)))
        modules.append(".".join(element for element in [pathlib.Path(package_path).name, packages, module] if element))
    return modules


def get_string(length=8, char='lower'):
    chars = {'lower': string.ascii_lowercase,
             'upper': string.ascii_uppercase,
             'digits': string.digits,
             'mix': string.ascii_letters + string.digits}
    string_ = chars[char] if char in chars.keys() else string.ascii_letters
    return ''.join(random.choice(string_) for _ in range(length))


def slugify(value, allow_unicode=False):
    """Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w[]\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)
