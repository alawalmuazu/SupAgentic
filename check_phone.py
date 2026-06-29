import phonenumbers
from phonenumbers import carrier, geocoder, timezone

phone = "+2348163386248"
try:
    parsed = phonenumbers.parse(phone)
    print("Valid:", phonenumbers.is_valid_number(parsed))
    print("Possible:", phonenumbers.is_possible_number(parsed))
    print("Type:", phonenumbers.number_type(parsed))
    print("Carrier:", carrier.name_for_number(parsed, "en"))
    print("Region:", geocoder.description_for_number(parsed, "en"))
    print("Timezones:", timezone.time_zones_for_number(parsed))
except Exception as e:
    print(e)
