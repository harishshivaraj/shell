from instruments.european_vanilla import EuropeanVanilla
from instruments.generic_instrument import GenericInstrument

INSTRUMENT_MAP = {"VANILLA": EuropeanVanilla}


def create_instrument(rfq: dict) -> GenericInstrument:
    """Factory class returns an instrument given an RFQ"""
    instrument = INSTRUMENT_MAP[rfq["type"]]
    return instrument(**rfq)
