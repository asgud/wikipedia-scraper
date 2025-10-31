# STEP 1: Import all necessary libraries at the TOP
from bs4 import BeautifulSoup
import requests
import json
import os
import csv


# STEP 2: Define the WikipediaScraper class
class WikipediaScraper:
    def __init__(self):
        # Required attributes
        self.root_url = "https://country-leaders.onrender.com"
        self.cookie_url = f"{self.root_url}/cookie"
        self.countries_url = f"{self.root_url}/countries"
        self.leader_url = f"{self.root_url}/leaders"

        # Store scraped data and session info
        self.leaders_data = {}
        self.cookie = None
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

        # Get initial cookie
        self.refresh_cookie()

    # 2a.STEP: Refresh cookies
    def refresh_cookie(self):
        """Fetch or refresh the cookie."""
        response = self.session.get(self.cookie_url, timeout=10)
        response.raise_for_status()
        self.cookie = response.cookies
        return self.cookie

    # 2b.STEP: Get countries
    def get_countries(self):
        """Return list of supported countries."""
        response = self.session.get(self.countries_url, timeout=10)
        if response.status_code == 403:
            self.refresh_cookie()
            response = self.session.get(self.countries_url, timeout=10)
        response.raise_for_status()
        return response.json()
    
    # 2c.STEP: Get leaders per country
    def get_leaders(self, country):
        """Fetch leaders for one country and enrich them with Wikipedia data."""
        params = {"country": country}
        response = self.session.get(self.leader_url, params=params, timeout=10)
        if response.status_code == 403:
            self.refresh_cookie()
            response = self.session.get(self.leader_url, params=params, timeout=10)
        response.raise_for_status()
        leaders = response.json()

        # Enrich with Wikipedia intro paragraph
        for leader in leaders:
            if "wikipedia_url" in leader and leader["wikipedia_url"]:
                wiki_url = leader["wikipedia_url"]
                leader_intro = self.get_first_paragraph(wiki_url)
                leader["intro_paragraph"] = leader_intro
            else:
                leader["intro_paragraph"] = None

        self.leaders_data[country] = leaders

    # 2d.STEP: Get first paragraph from Wikipedia
    def get_first_paragraph(self, wikipedia_url, min_length=200):
        """Fetch the first meaningful paragraph from Wikipedia."""
        try:
            r = self.session.get(wikipedia_url, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, "html.parser")
            content = soup.find(id="mw-content-text")
            paragraphs = content.find_all("p") if content else soup.find_all("p")

            for p in paragraphs:
                text = p.get_text(" ", strip=True)
                if len(text) >= min_length and "may refer to:" not in text.lower():
                    return text
            return None
        except requests.RequestException:
            return None
        

   # 3.STEP: Save files 
   # 3a.: Save data to JSON file
    def save_json(self, leaders_per_country=None):
        """Save leaders data to JSON file"""
        if leaders_per_country is None:
            leaders_per_country = self.leaders_data

        out_path = os.path.abspath("leaders.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(leaders_per_country, f, indent=4, ensure_ascii=False)
        print(f"Data saved to: {out_path}")


    # 3b.: Save data to CSV file
    def save_csv(self, leaders_per_country=None):
        """Save leaders data to a CSV file"""
        if leaders_per_country is None:
            leaders_per_country = self.leaders_data

        out_path = os.path.abspath("leaders.csv")
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "country", "first_name", "last_name", "birth_date",
                "start_mandate", "end_mandate", "wikipedia_url", "intro_paragraph"
            ])
            for country, leaders in leaders_per_country.items():
                for leader in leaders:
                    writer.writerow([
                        country,
                        leader.get("first_name", ""),
                        leader.get("last_name", ""),
                        leader.get("birth_date", ""),
                        leader.get("start_mandate", ""),
                        leader.get("end_mandate", ""),
                        leader.get("wikipedia_url", ""),
                        leader.get("intro_paragraph", "")
                    ])
        print(f"Data saved to: {out_path}")