from pricing_exceptions import PricingEngineInstrumentError

DECIMAL_PRECISION = 2


class GenericInstrument:
    """
    Generic Instrument, This must be subclassed by individual instruments
    """

    price_model = None

    def price(self) -> float:
        """Prices the contract against model provided"""
        if self.price_model:
            mid = self.price_model.calculate(self)
            return round(mid, DECIMAL_PRECISION)
        raise PricingEngineInstrumentError("Pricing model not defined!")

    @property
    def expiry(self) -> float:
        raise PricingEngineInstrumentError("Not Implemented")

    @property
    def spot(self) -> float:
        raise PricingEngineInstrumentError("Not Implemented")

    @property
    def vol(self) -> float:
        raise PricingEngineInstrumentError("Not Implemented")
