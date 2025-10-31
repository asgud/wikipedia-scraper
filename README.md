# 🌍 Wikipedia Scraper 



## 🧭 Project Overview

This project is part of my data science learning journey — focused on **data collection and web scraping**.  
The goal was to build a **complete scraper** that:
1. Retrieves political leaders’ data from an API,  
2. Scrapes their Wikipedia introduction paragraphs, and  
3. Saves everything as structured **JSON** or **CSV** files.

Scraping and data retrieval are common first steps in any data project.

---

## 🎯 Mission Objectives

 ✅ Work inside a **self-contained environment** (`venv`)\
 ✅ Retrieve data from an external **REST API**\
 ✅ **Scrape** data from HTML pages using BeautifulSoup\
 ✅ Handle cookies, exceptions, and files properly\
 ✅ Save and reuse data in **JSON** and **CSV** formats\
 ✅ Build both **functional** and **object-oriented** versions

---

## 🧠 Learning Outcomes

This project helped me practice and strengthen the following Python skills:

| Area | Description |
|-------|--------------|
| 🧰 **Python Libraries** | `os`, `requests`, `json`, `csv`, `beautifulsoup4` |
| 🌐 **Requests & Sessions** | Calling APIs, reusing sessions for efficiency |
| 🍪 **Cookies Handling** | Refreshing expired cookies  |
| 📜 **BeautifulSoup** | Extracting first paragraphs from Wikipedia pages |
| ⚙️ **Exception Handling** | Managing connection errors, invalid data, retries |
| 💾 **File Handling** | Writing output to `leaders.json` and `leaders.csv` |
| 🧱 **OOP Concepts** | Refactoring procedural code into class-based structure |

---

## 🚀 The Mission

The main task was to collect and combine data from two sources:
- The **Country Leaders API** 👉 [https://country-leaders.onrender.com/docs](https://country-leaders.onrender.com/docs)  
- The leaders’ **Wikipedia pages**

### Steps:
1. Fetch the list of countries from the API.  
2. Retrieve all political leaders for each country.  
3. Visit each leader’s Wikipedia page and scrape the first `<p>` paragraph.  
4. Save all results in `leaders.json` or `leaders.csv`.

---

## 🧩 Project Structure

```
wikipedia-scraper/
│
├── src/
│ ├── leaders_scraper.py            # Functional version (non-OOP)
│ ├── leaders_scraper_oop.py        # OOP version (WikipediaScraper class)
│ └── pycache/                      # Compiled cache
│
├── wikipedia_scraper_env/          # Virtual environment folder
├── main.py                         # Entry point (runs OOP scraper)
├── leaders.json                    # Saved output (JSON)
├── leaders.csv                     # Saved output (CSV)
├── wikipedia_scraper.ipynb         # Jupyter notebook version
└── README.md                       # Project documentation

```

---

## ⚙️ How to Run

1️⃣ Clone the repository** to your local machine: 

2️⃣ Activate the virtual environment (make sure wikipedia_scraper_env exists):

```
source wikipedia_scraper_env/bin/activate       # macOS/Linux
# OR
wikipedia_scraper_env\Scripts\activate          # Windows
```

3️⃣ Run the program — execute main.py from the command line:
```
python3 main.py
```

4️⃣ View the result


## 🧱 Code Versions
📜 Functional Version (src/leaders_scraper.py)

A step-by-step implementation using functions like:
- get_first_paragraph()
-  get_leader()
-  save_json()
-  save_csv()

🧭 OOP Version (src/leaders_scraper_oop.py)

An improved, object-oriented version with cleaner structure:

1. Attributes:  
             root_url, cookie_url, countries_url, leader_url, leaders_data, cookie, session
   
2. Methods:
- refresh_cookie()
- get_countries()
- get_leaders(country)
- get_first_paragraph(wikipedia_url)
- save() and save_csv()

## ⏱️ Timeline

This project took 3 days for completion.


## 🧑‍💻 Author

Astha Gudgilla\
🌱 This project was done as part of the AI Bootcamp at BeCode.org.\
📫 Connect with me on [LinkedIn](https://www.linkedin.com/in/asthagudgilla/).

