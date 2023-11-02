from typing import Dict, List


class Authorization:
    owner_ids: list = [
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
        "Authorization": "gAAAAABlQns7YfamuD0nNT6g-CXdEYJdQ8MuDghAe67WSTxqFM9EfNtQ6FrrQWb_m5vphrrHSaU8iJ4hFRDhU0SzzLAiemYnFw==",
        "X-username": "sipher",
    }


class db:
    host: str = ""
    user: str = ""
    port: str = ""
    database: str = ""
    password: str = ""


class Color:
    regular: int = 0x2B2D31
    invis: int = 0x2B2D31
    deny: int = 0xF23F43
