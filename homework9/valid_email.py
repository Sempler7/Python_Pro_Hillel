"""Перевірка валідності email-адреси за допомогою регулярних виразів"""

import re


def is_valid_email(email: str) -> bool:
    """Перевіряє, чи є email-адреса валідною"""

    pattern = re.compile(
        r'^[A-Za-z0-9](?:[A-Za-z0-9.]*[A-Za-z0-9])?@'  # локальна частина
        r'(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9]))+\.'  # домен (з тире)
        r'[A-Za-z]{2,7}$'  # TLD
    )
    return bool(pattern.match(email))


emails = [
    "user@my-domain.com",  # валідний
    "user@domain.com",  # валідний
    "user@do-main.net",  # валідний
    "user@-domain.com",  # невалідний (починається з тире)
    "user@domain-.org",  # невалідний (закінчується тире)
    "user@domain.companys",  # невалідний (TLD занадто довгий)
]

for e in emails:
    print(f"{e}: {is_valid_email(e)}")
