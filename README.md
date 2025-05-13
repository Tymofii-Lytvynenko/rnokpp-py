# RNOKPP (РНОКПП) - Python Version

Helper functions to work with Ukrainian registration number of the taxpayer's account card (RNOKPP).  
Допоміжні функції для роботи з реєстраційним номером облікової картки платника податків (РНОКПП).

## Requirements 🧐

* Python >= 3.8

## Features 🎁

- [x] Get details about RNOKPP
- [x] Get gender
- [x] Check gender
- [x] Check validity
- [x] Generate RNOKPP by date and gender
- [x] Generate random RNOKPP

## Usage 👨‍🎓

```python
import datetime
from rnokpp import (
    Gender, get_details, get_gender, 
    is_male, is_female, is_valid,
    generate_rnokpp, generate_random_rnokpp,
    generate_random_rnokpp_n
)

# Get details about RNOKPP
details = get_details("3652504575")
print("details:", details)  # valid, male, 2000-01-01

# Get gender from RNOKPP
gender1 = get_gender("3652504575")
print("gender1:", gender1)  # Gender.MALE
gender2 = get_gender("3068208400") 
print("gender2:", gender2)  # Gender.FEMALE

# Check gender
print("is male:", is_male("3652504575"))  # True
print("is female:", is_female("3652504575"))  # False

# Check valid RNOKPP
print("rnokpp valid:", is_valid("3652504575"), is_valid("1234567890"))  # True, False

# Generate RNOKPP by date and gender
birthday = datetime.date(2000, 1, 1)
male_rnokpp = generate_rnokpp(birthday, Gender.MALE)
print("valid RNOKPP for male:", male_rnokpp)  # e.g. 3652322032

female_rnokpp = generate_rnokpp(birthday, Gender.FEMALE) 
print("valid RNOKPP for female:", female_rnokpp)  # e.g. 3652347000

# Generate random RNOKPPs
print("random rnokpp:", generate_random_rnokpp())  # e.g. 3300507061

for i, rnokpp in enumerate(generate_random_rnokpp_n(3)):
    print(f"random rnokpp #{i}: {rnokpp}")
```
