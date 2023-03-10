from math import exp, log, sqrt

from scipy.stats import norm

from instruments.generic_instrument import GenericInstrument


class BlackScholes:
    """
    Black Scholes Pricing model

    This class implements the formula to price a single European vanilla option
    with the following assumption
        - Works only for European options
        - With no dividend pay off
        - With no markups charges included
        - with each contract of 100 units
        - With a constant interest rate
        - With a constant volatility
    """

    def __init__(self, rate: float) -> None:
        self.rate = rate

    def d1(self, inst: GenericInstrument) -> float:
        delta = log(inst.spot / inst.strike) + (self.rate + inst.vol**2 / 2.0) * inst.expiry
        return delta / (inst.vol * sqrt(inst.expiry))

    def d2(self, inst: GenericInstrument) -> float:
        return self.d1(inst) - (inst.vol * sqrt(inst.expiry))

    def calculate_call(self, inst: GenericInstrument) -> float:
        d1 = self.d1(inst)
        d2 = self.d2(inst)
        return inst.spot * norm.cdf(d1) - inst.strike * exp(-self.rate * inst.expiry) * norm.cdf(d2)

    def calculate_put(self, inst: GenericInstrument) -> float:
        d1 = self.d1(inst)
        d2 = self.d2(inst)
        return inst.strike * exp(-self.rate * inst.expiry) * norm.cdf(-d2) - inst.spot * norm.cdf(-d1)

    def calculate(self, inst: GenericInstrument) -> float:
        if inst.putcall == "CALL":
            price = self.calculate_call(inst)

        if inst.putcall == "PUT":
            price = self.calculate_put(inst)

        return price * 100
