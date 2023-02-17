import importlib

import pandas as pd

from pricing_exceptions import PricingEngineSecurityError


class GenericSecurity:
    """
    Generic Security, This must be subclassed by individual security class
    """

    market_data_src = None

    def spot(self) -> float:
        """
        Returns spot price for the security

        Spot price is the last closing price from the market data
        """
        if self.market_data_src:
            mkt_data = pd.read_csv(self.market_data_src, index_col=0)
            mkt_data = mkt_data.sort_values(by='Date', ascending=False)
            return mkt_data['Close'][0]

        raise PricingEngineSecurityError("Market Data path not set")

    def vol(self) -> float:
        raise PricingEngineSecurityError("Not Implemented!")


def get_security_object(security: str) -> GenericSecurity:
    """ Factory class returns a security object given the security name """
    module = importlib.import_module(f"securities.{security.lower()}")
    return getattr(module, security)()
