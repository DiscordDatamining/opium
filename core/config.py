from typing import Dict, List


class Authorization:
    owner_ids: list = [
        1168732514152628285,
    ]
    token: str = (
        "MTE0MzgyOTA2MDY0OTIzNDQ3Mg.G8x0sL.Inn7O4TcKAi0s8aJhuIBV6FOdnEoSR6Top5k9o"
    )
    prefix: str = "!"


class Api:
    url: str = "https://api.ermm.tech"
    key: str = ""
    headers: dict() = {
        "Authorization": "gAAAAABlQns7YfamuD0nNT6g-CXdEYJdQ8MuDghAe67WSTxqFM9EfNtQ6FrrQWb_m5vphrrHSaU8iJ4hFRDhU0SzzLAiemYnFw==",
        "X-username": "sipher",
    }


class db:
    host: str = "db.vdukveeoxwifoqdketql.supabase.co"
    user: str = "postgres"
    port: int = 5432
    database: str = "postgres"
    password: str = "101908tjmmm4"


class Color:
    regular: int = 0x2B2D31
    invis: int = 0x2B2D31
    deny: int = 0xF23F43
