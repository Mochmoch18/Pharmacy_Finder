import requests
from bs4 import BeautifulSoup
import csv
import time

# Base URL for cities and individual pharmacies
base_city_url = "https://annuaire-gratuit.ma/pharmacie-garde-{}.html"

# List of cities to scrape
cities = ["marrakech"]  # Start with one city for testing "casablanca","kenitra","rabat","sale"

# CSV file path
csv_file_path = "on_call_pharmacies.csv"

# Create the CSV file
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["City", "District", "Name", "Address", "Phone", "Garde_Status"])

    for city in cities:
        print(f"Processing city: {city}")

        # Step 1: Access the city page and extract district links
        city_url = base_city_url.format(city)
        city_response = requests.get(city_url)

        if city_response.status_code == 200:
            city_soup = BeautifulSoup(city_response.text, "html.parser")

            # Find district links
            district_links = [
                f"https://annuaire-gratuit.ma{a['href']}"
                for a in city_soup.find_all("a", href=True)
                if f"/pharmacie-garde-{city}/quartier-" in a['href']
            ]
            print("Found District Links:", district_links)

            # Step 2: Scrape data from each district page
            for district_url in district_links:
                # Extract district name from URL
                district_name = district_url.split("/quartier-")[1].split(".")[0].replace("-", " ").capitalize()
                print(f"Processing district: {district_name}")

                district_response = requests.get(district_url)

                if district_response.status_code == 200:
                    district_soup = BeautifulSoup(district_response.text, "html.parser")

                    # Find the pharmacy list in the <ul id="agItemList">
                    pharmacy_list = district_soup.find("ul", id="agItemList")
                    if pharmacy_list:
                        pharmacy_items = pharmacy_list.find_all("li", class_="ag_listing_item")
                        for item in pharmacy_items:
                            name = item.find("h3", itemprop="name").get_text(strip=True) if item.find("h3", itemprop="name") else "N/A"
                            address = item.find("p", itemprop="streetAddress").get_text(strip=True) if item.find("p", itemprop="streetAddress") else "N/A"
                            garde_status = item.find("span", class_="garde_status").get_text(strip=True) if item.find("span", class_="garde_status") else "N/A"
                            pharmacy_link = item.find("a", href=True)["href"] if item.find("a", href=True) else None

                            # Visit individual pharmacy page to get the full phone number
                            if pharmacy_link:
                                pharmacy_url = f"https://annuaire-gratuit.ma{pharmacy_link}"
                                pharmacy_response = requests.get(pharmacy_url)

                                if pharmacy_response.status_code == 200:
                                    pharmacy_soup = BeautifulSoup(pharmacy_response.text, "html.parser")
                                    phone = pharmacy_soup.find("a", itemprop="telephone").get_text(strip=True) if pharmacy_soup.find("a", itemprop="telephone") else "N/A"
                                else:
                                    phone = "N/A"
                                print(f"Retrieved phone: {phone}")

                            # Check if any field contains 'N/A'
                            if name != "N/A" and address != "N/A" and phone != "N/A" and garde_status != "N/A":
                                # Write data to CSV, including district name
                                writer.writerow([city.capitalize(), district_name, name, address , phone, garde_status])
                                print(f"Added pharmacy: {name}")

                    else:
                        print("No pharmacy items found in this district.")

                    # Adding delay to avoid server overload
                    time.sleep(1)

                else:
                    print(f"Failed to retrieve district page: {district_url}")

print(f"Data scraping completed. Results saved to {csv_file_path}")
