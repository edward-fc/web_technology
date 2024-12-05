import requests
from app.models import CountryCode
from app import app, db


def fetch_and_store_country_codes():
    # Fetch country names and phone codes from the given URLs
    country_names_url = "https://country.io/names.json"
    country_codes_url = "https://country.io/phone.json"

    try:
        names_response = requests.get(country_names_url)
        codes_response = requests.get(country_codes_url)
        names_response.raise_for_status()
        codes_response.raise_for_status()

        country_names = names_response.json()
        country_codes = codes_response.json()

        for country_code, country_name in country_names.items():
            phone_code = country_codes.get(country_code, "")
            if phone_code and phone_code[0] != "+":
                print(phone_code[0] != "+", phone_code[0])
                phone_code = f'+{phone_code}'
            if phone_code:
                # Check if country already exists in the database
                existing_country = CountryCode.query.filter_by(name=country_name).first()
                if not existing_country:
                    new_country = CountryCode(name=country_name, code=phone_code)
                    db.session.add(new_country)

        db.session.commit()
        print("Country codes have been successfully updated in the database.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching country data: {e}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        fetch_and_store_country_codes()
