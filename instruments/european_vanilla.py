import calendar
from datetime import datetime

from dateutil.relativedelta import relativedelta

from instruments.generic_instrument import GenericInstrument
from models.blackscholes import BlackScholes
from pricing_exceptions import PricingEngineInstrumentError
from securities import get_security_object


def last_day_of_month(day: datetime) -> datetime:
    _, last_day = calendar.monthrange(day.year, day.month)
    return day.replace(day=last_day)


class EuropeanVanilla(GenericInstrument):
    """
    European Vanilla Instrument
    """

    price_model = BlackScholes(rate=0.1)

    # pylint: disable=unused-argument
    def __init__(self, commodity=None, strike=None, putcall=None, delivery=None, **kwargs) -> None:
        self.delivery = delivery
        self.strike = strike
        self.putcall = putcall
        self.underlying = get_security_object(commodity)

    @property
    def expiry(self) -> float:
        expiry = datetime.strptime(self.delivery, "%b-%y")
        today = datetime.today()

        if expiry < today:
            raise PricingEngineInstrumentError(f"Delivery date {self.delivery} is in the past")

        expiry = last_day_of_month(expiry - relativedelta(months=2))

        if expiry < today:
            raise PricingEngineInstrumentError(f"Expiry date {expiry:%b-%y} is in the past")

        return (expiry - today).days / 365

    @property
    def spot(self) -> float:
        return self.underlying.spot()

    @property
    def vol(self) -> float:
        return self.underlying.vol()
