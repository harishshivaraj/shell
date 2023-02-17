from pathlib import Path

from securities import GenericSecurity


class HH(GenericSecurity):
    """
    Henry Hub Gas security
    """

    market_data_src = f"{Path(__file__).parent}/../market-data/HH.csv"

    def vol(self) -> float:
        return 0.5
