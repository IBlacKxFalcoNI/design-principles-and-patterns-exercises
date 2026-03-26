# TODO: `Product` violates the SRP principle.
#       Identify where the violations occur and discuss/implement
#       a better solution. See exercise_1_hints.py if you need help
from __future__ import annotations
from decimal import Decimal



class Money:
    def __init__(self, amount: str | Decimal) -> None:
        if isinstance(amount, str):
            self._amount = Decimal(self._format_amount(amount))
        else:
            assert amount.same_quantum(self._get_representative_decimal())
            self._amount = amount

    def apply_discount(self, percentage: int) -> Money:
        assert percentage >= 0 and percentage <= 100
        discounted = self._amount * (1 - Decimal(percentage) / Decimal(100))
        discounted = discounted.quantize(self._get_representative_decimal())
        return Money(discounted)
    
    def _format_amount(self, money_str: str) -> str:
        if "." not in money_str:
            return f"{money_str}.00"
        elif len(money_str.split(".")[1]) != 2:
            raise IOError("Too many decimal digits")
        return money_str
    
    def _get_representative_decimal(self) -> Decimal:
        return Decimal("1.00")
    
    def __repr__(self) -> str:
        return str(self._amount)
    

class Product:
    def __init__(self, name: str, price: Money, has_discount: bool = False) -> None:
        self._name = name
        self._price = price
        self._has_discount = has_discount

    def __repr__(self) -> str:
        return f"Product: {self._name}, price: {self._price}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> Money:
        return self._price

    def reduced(self, percentage: int) -> Product:
        assert percentage >= 0 and percentage <= 100
        assert not self._has_discount
        return Product(
            name=f"{self._name} (reduced)",
            price=self._price.apply_discount(percentage)
        )

if __name__ == "__main__":
    print(Product("Laptop", Money("999.00")))
    print(Product("Laptop", Money("999.00")).reduced(30))
