import unittest
import random
import datetime
from rnokpp import (
    Gender, Details, 
    InvalidControlDigit, NumberGreaterThanZero, MoreThan10Digits, LessThan10Digits,
    StringDoesNotConsistOfDigits, NotAllowedDate, DateInFuture,
    get_details, is_valid, is_male, is_female, get_gender,
    generate_rnokpp, generate_random_rnokpp, generate_random_rnokpp_n
)

class TestRNOKPP(unittest.TestCase):
    def test_get_details(self):
        # Test known valid RNOKPP
        details = get_details("3652504575")
        self.assertTrue(details.valid)
        self.assertEqual(details.gender, Gender.MALE)
        self.assertEqual(details.birthday, datetime.date(2000, 1, 1))
        
        # Test female RNOKPP
        details = get_details("3068208400")
        self.assertTrue(details.valid)
        self.assertEqual(details.gender, Gender.FEMALE)
        
        # Test invalid control digit
        with self.assertRaises(InvalidControlDigit):
            get_details("3652504576")  # Changed last digit

    def test_get_details_with_errors(self):
        with self.assertRaises(StringDoesNotConsistOfDigits):
            get_details("1234567890+")
        
        with self.assertRaises(LessThan10Digits):
            get_details("123456789")
        
        invalid_numbers = ["123456789X", "          ", "ABCDEFGHIJ", " 234567890", "123456789 "]
        for num in invalid_numbers:
            with self.assertRaises(StringDoesNotConsistOfDigits):
                get_details(num)

    def test_is_male(self):
        self.assertTrue(is_male("3652504575"))  # male
        self.assertFalse(is_male("3068208400"))  # female
        with self.assertRaises(StringDoesNotConsistOfDigits):
            is_male("invalid")

    def test_is_female(self):
        self.assertFalse(is_female("3652504575"))  # male
        self.assertTrue(is_female("3068208400"))  # female
        with self.assertRaises(StringDoesNotConsistOfDigits):
            is_female("invalid")

    def test_get_gender(self):
        self.assertEqual(get_gender("3652504575"), Gender.MALE)
        self.assertEqual(get_gender("3068208400"), Gender.FEMALE)
        with self.assertRaises(StringDoesNotConsistOfDigits):
            get_gender("invalid")

    def test_generate_rnokpp(self):
        # Test date boundaries
        with self.assertRaises(NotAllowedDate):
            generate_rnokpp(datetime.date(1899, 12, 31), Gender.MALE)
        
        with self.assertRaises(DateInFuture):
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            generate_rnokpp(tomorrow, Gender.MALE)
        
        # Test minimum allowed date
        rnokpp = generate_rnokpp(datetime.date(1900, 1, 1), Gender.FEMALE)
        self.assertTrue(is_valid(rnokpp))
        
        # Test current date
        rnokpp = generate_rnokpp(datetime.date.today(), Gender.MALE)
        self.assertTrue(is_valid(rnokpp))
        
        # Test random dates
        for _ in range(100):
            birthday = datetime.date.today() - datetime.timedelta(days=random.randint(0, 365*100))
            rnokpp = generate_rnokpp(birthday, Gender.MALE)
            self.assertTrue(is_valid(rnokpp))

    def test_generate_random_rnokpp(self):
        # Test gender distribution in random generation
        male_count = 0
        female_count = 0
        for _ in range(1000):
            rnokpp = generate_random_rnokpp()
            self.assertTrue(is_valid(rnokpp))
            if is_male(rnokpp):
                male_count += 1
            else:
                female_count += 1
        # Should be roughly 50/50 distribution
        self.assertGreater(male_count, 400)
        self.assertGreater(female_count, 400)

    def test_generate_random_rnokpp_n(self):
        rnokpps = generate_random_rnokpp_n(100)
        for rnokpp in rnokpps:
            self.assertTrue(is_valid(rnokpp))
        
        with self.assertRaises(NumberGreaterThanZero):
            generate_random_rnokpp_n(0)

if __name__ == '__main__':
    unittest.main()