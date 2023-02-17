class PricingEngineException(Exception):
    """
    Base exception class for Pricing Engine. This must be subclassed for more specific error.
    """

    def __init__(self, message=None):
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
