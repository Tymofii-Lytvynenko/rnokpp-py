"""Python implementation of Ukrainian tax ID (RNOKPP) handling library.

Original Go library: https://github.com/fre5h/rnokpp
"""

from enum import Enum
import datetime
import random
from typing import List, Optional, Tuple, Union

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"

    def is_male(self) -> bool:
        return self == Gender.MALE

    def is_female(self) -> bool:
        return self == Gender.FEMALE

    @classmethod
    def random(cls) -> 'Gender':
        return random.choice([Gender.MALE, Gender.FEMALE])

class Details:
    def __init__(self, valid: bool, gender: Gender, birthday: datetime.date):
        self.valid = valid
        self.gender = gender
        self.birthday = birthday

    def __str__(self) -> str:
        if not self.valid:
            return "invalid"
        return f"valid, {self.gender.value}, {self.birthday.strftime('%d.%m.%Y')}"

# Constants
BASE_DATE = datetime.date(1900, 1, 1)
MALE_DIGITS = [1, 3, 5, 7, 9]
FEMALE_DIGITS = [0, 2, 4, 6, 8]

# Exceptions
class RNOKPPError(Exception):
    pass

class InvalidControlDigit(RNOKPPError):
    pass

class NumberGreaterThanZero(RNOKPPError):
    pass

class MoreThan10Digits(RNOKPPError):
    pass

class LessThan10Digits(RNOKPPError):
    pass

class StringDoesNotConsistOfDigits(RNOKPPError):
    pass

class NotAllowedDate(RNOKPPError):
    def __init__(self, date: datetime.date):
        self.date = date
        super().__init__(f"The allowed dates start from 01.01.1900, but your date {date.strftime('%d.%m.%Y')} is earlier")

class DateInFuture(RNOKPPError):
    def __init__(self, date: datetime.date):
        self.date = date
        super().__init__(f"It is allowed to use only dates in past or current date, but your date is in the future {date.strftime('%d.%m.%Y')}")

def _parse_rnokpp(rnokpp: str) -> List[int]:
    try:
        digits = [int(c) for c in rnokpp]
    except ValueError:
        raise StringDoesNotConsistOfDigits()
    
    if len(digits) > 10:
        raise MoreThan10Digits()
    if len(digits) < 10:
        raise LessThan10Digits()
    
    return digits

def _calculate_control_digit(digits: List[int]) -> int:
    checksum = digits[0] * -1
    checksum += digits[1] * 5
    checksum += digits[2] * 7
    checksum += digits[3] * 9
    checksum += digits[4] * 4
    checksum += digits[5] * 6
    checksum += digits[6] * 10
    checksum += digits[7] * 5
    checksum += digits[8] * 7
    return (checksum % 11) % 10

def get_details(rnokpp: str) -> Details:
    """Get details about RNOKPP if possible."""
    digits = _parse_rnokpp(rnokpp)
    
    gender_digit = digits[8]
    control_digit = digits[9]
    
    calculated_control = _calculate_control_digit(digits[:9])
    if control_digit != calculated_control:
        raise InvalidControlDigit()
    
    gender = Gender.MALE if gender_digit % 2 == 1 else Gender.FEMALE
    
    days_since_base = digits[0]*10000 + digits[1]*1000 + digits[2]*100 + digits[3]*10 + digits[4]
    days_since_base -= 1
    
    birthday = BASE_DATE + datetime.timedelta(days=days_since_base)
    
    return Details(True, gender, birthday)

def is_valid(rnokpp: str) -> bool:
    """Check if RNOKPP is valid."""
    try:
        details = get_details(rnokpp)
        return details.valid
    except RNOKPPError:
        return False

def is_male(rnokpp: str) -> bool:
    """Check if RNOKPP belongs to male gender."""
    details = get_details(rnokpp)
    return details.gender.is_male()

def is_female(rnokpp: str) -> bool:
    """Check if RNOKPP belongs to female gender."""
    details = get_details(rnokpp)
    return details.gender.is_female()

def get_gender(rnokpp: str) -> Gender:
    """Get gender from RNOKPP."""
    details = get_details(rnokpp)
    return details.gender

def generate_rnokpp(date: datetime.date, gender: Gender) -> str:
    """Generate valid RNOKPP by date and gender."""
    if date < BASE_DATE:
        raise NotAllowedDate(date)
    if date > datetime.date.today():
        raise DateInFuture(date)
    
    days_since_base = (date - BASE_DATE).days
    days_since_base += 1
    rnokpp = f"{days_since_base:05d}"
    
    # Add 3 random digits
    rnokpp += str(random.randint(0, 9))
    rnokpp += str(random.randint(0, 9))
    rnokpp += str(random.randint(0, 9))
    
    # Add gender digit
    if gender == Gender.MALE:
        rnokpp += str(random.choice(MALE_DIGITS))
    else:
        rnokpp += str(random.choice(FEMALE_DIGITS))
    
    # Calculate and add control digit
    digits = [int(c) for c in rnokpp]
    rnokpp += str(_calculate_control_digit(digits))
    
    return rnokpp

def generate_random_rnokpp() -> str:
    """Generate random valid RNOKPP."""
    # Generate random date between BASE_DATE and today
    days_range = (datetime.date.today() - BASE_DATE).days
    random_days = random.randint(0, days_range)
    random_date = BASE_DATE + datetime.timedelta(days=random_days)
    
    return generate_rnokpp(random_date, Gender.random())

def generate_random_rnokpp_n(count: int) -> List[str]:
    """Generate multiple random valid RNOKPPs."""
    if count <= 0:
        raise NumberGreaterThanZero()
    
    return [generate_random_rnokpp() for _ in range(count)]