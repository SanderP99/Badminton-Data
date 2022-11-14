from dataclasses import dataclass

import pandas as pd


@dataclass
class Tournament:
    name: str
    organization: str
    city: str
    country: str
    start_date: str
    end_date: str
    type: str
    link: str

    def to_data_list(self):
        print(self.organization)
        return pd.DataFrame(
            {
                "name": self.name,
                "organization": self.organization,
                "city": self.city,
                "country": self.country,
                "type": self.type,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "link": self.link,
            },
            index=[0]
        )
