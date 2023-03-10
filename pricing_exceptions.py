class PricingEngineException(Exception):
    """
    Base exception class for Pricing Engine. This must be subclassed for the more specific error.
    """

    def __init__(self, message: str = None) -> None:
        super().__init__(message)


class PricingEngineRFQValidationFailure(PricingEngineException):
    """
    RFQ Json validation failure exception
    """


class PricingEngineInstrumentError(PricingEngineException):
    """
    Generic Instrument exception
    """


class PricingEngineSecurityError(PricingEngineException):
    """
    Generic Security failure exception
    """
