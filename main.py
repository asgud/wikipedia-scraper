from src.leaders_scraper_oop import WikipediaScraper
import os

def main():
    print(f"CWD: {os.getcwd()}")
    scraper = WikipediaScraper()
    countries = scraper.get_countries()
    for c in countries:
        print(f"→ Fetching leaders for {c}...")
        scraper.get_leaders(c)
    for c, leaders in scraper.leaders_data.items():
        print(f"  - {c}: {len(leaders)} leader(s)")
    
    # Ask user how to save
    choice = input("\nSave as (J)SON or (C)SV? ").strip().lower()
    if choice == "c":
        scraper.save_csv()
    else:
        scraper.save_json()

    print("\n Done! Data saved successfully.\n")


# Run when executed directly
if __name__ == "__main__":
    main()
    

