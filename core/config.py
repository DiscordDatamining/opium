from typing import Dict, List


class Authorization:
    owner_ids: list[int, int] = [
        1168732514152628285,
    ]
    token: str = (
        "MTE2ODkwOTcyMTYyNTk2NDYwNQ.GXCjT5.PsUkz8v_BI7VnYbMCCnaw80yzxXdVKK6NrFswc"
    )
    prefix: str = ","


class Api:
    url: str = "https://api.ermm.tech"
    key: str = ""
    headers: dict() = {
        "Authorization": "ownership",
        "X-username": "wise",
    }


class db:
    host: str = ""
    user: str = ""
    port: str = ""
    database: str = ""
    password: str = ""
