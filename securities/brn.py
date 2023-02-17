from pathlib import Path

from securities import GenericSecurity


class BRN(GenericSecurity):
    """
    Brent Crude Oil security
    """

    market_data_src = f"{Path(__file__).parent}/../market-data/BRN.csv"

    def __init__(self):

        print(Path(__file__).parent)

    def vol(self) -> float:
        return 1.5
