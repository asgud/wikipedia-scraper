# STEP 1: Import all necessary libraries at the TOP
from bs4 import BeautifulSoup
import requests
import json
import os
import csv

# STEP 2: Define get_first_paragraph FIRST (before get_leader, since get_leader calls it)
def get_first_paragraph(wikipedia_url, session, min_length=200):
    # Use headers to mimic a real browser
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        r = session.get(wikipedia_url, headers=headers, timeout=10)
        r.raise_for_status()
    except requests.RequestException:
        return None 
    
    soup = BeautifulSoup(r.content, "html.parser")
    
    # Prefer article body if present
    content = soup.find(id="mw-content-text")
    paragraphs = content.find_all("p") if content else soup.find_all("p")

    for p in paragraphs:
        text = p.get_text(" ", strip=True)
        # Only accept paragraphs with minimum length 
        if len(text) >= min_length and "may refer to:" not in text.lower():
            return text

    return None  # nothing suitable found

# STEP 3: Define get_leader function
def get_leader():
    # 1. define the urls 
    root_url = "https://country-leaders.onrender.com"
    cookie_url = f"{root_url}/cookie"
    countries_url = f"{root_url}/countries"
    leader_url = f"{root_url}/leaders"
    
   # single session for everything
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    # 2. get the cookies (seed session cookie)
    try:
        req = session.get(cookie_url, timeout=10)
        req.raise_for_status()
        cookies = req.cookies  # keep your variable name
    except requests.RequestException as e:
        print(f" Error while fetching cookie: {e}")
        return {}

    # 3. get the countries 
    try:
        response = session.get(countries_url, timeout=10)
        if response.status_code == 403:  # cookie might be stale → refresh once
            req = session.get(cookie_url, timeout=10)
            response = session.get(countries_url, timeout=10)
        response.raise_for_status()
        countries = response.json()
    except Exception as e:
        print(f"Error while fetching countries: {e}")
        return {}  # stop early or return empty result

    # 4. loop over countries and collect leaders
    leader_per_country = {}
    for country in countries:
        params = {"country": country}
        try:
            response = session.get(leader_url, params=params, timeout=10)
            if response.status_code == 403:
                req = session.get(cookie_url, timeout=10)
                response = session.get(leader_url, params=params, timeout=10)
            response.raise_for_status()
            leaders = response.json()
        except requests.RequestException as e:
            print(f"Error fetching leaders for {country}: {e}")
            leaders = []
        except ValueError:
            leaders = []

        # loop over each leader to add Wikipedia intro paragraph
        for leader in leaders:
            if "wikipedia_url" in leader and leader["wikipedia_url"]:
                wiki_url = leader["wikipedia_url"]
                leader_intro = get_first_paragraph(wiki_url, session)
                leader["intro_paragraph"] = leader_intro

        leader_per_country[country] = leaders

    return leader_per_country



# STEP 4: 
# 4a: Save data to Json file

def save_json(leaders_per_country):
    """Save leaders data to JSON file"""
    out_path = os.path.abspath("leaders.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(leaders_per_country, f, indent=4, ensure_ascii=False)
    print(f"Data saved to: {out_path}")


# 4b: Save data to CSV file 

def save_csv(leaders_per_country):
    """Save leaders data to a CSV file"""
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



# STEP 5: Simple CLI entry point

def main():
    print(f" CWD: {os.getcwd()}")
    data = get_leader()
    if not data:
        print("No data fetched (get_leader returned empty). Not saving.")
        return
    # quick summary so you know it worked
    for c, leaders in data.items():
        print(f"  - {c}: {len(leaders)} leader(s)")
    # Ask the user how to save
    choice = input("Save as (J)SON or (C)SV? ").strip().lower()

    if choice == "c":
        save_csv(data)
    else:
        save_json(data)


if __name__ == "__main__":
    main()
