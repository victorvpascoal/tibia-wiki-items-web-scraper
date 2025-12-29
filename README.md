# Tibia Wiki Items Scraper

A **Python-based web scraper** that collects data about **pickupable items** from the **Tibia Fandom Wiki** and generates a CSV file containing the extracted information.

The generated output file is:

```
tibia_wiki_items.csv
```

The project includes a **GitHub Actions workflow** that runs automatically to keep the dataset up to date.

---

## 📦 Features

- Scrapes pickupable item pages from the Tibia Fandom Wiki  
- Extracts structured data from each page’s **infobox**  
- Exports item data to `tibia_wiki_items.csv`  
- Automated updates via GitHub Actions  
- Simple local execution using Python  

---

## ⏱️ Automation (GitHub Actions)

A GitHub Action is configured to run automatically on:

- **The 1st day of every month**
- **The 15th day of every month**

On each run, the scraper checks for new items and updates `tibia_wiki_items.csv` if new data is found.

---

## 🧠 How It Works

- Each Tibia Wiki item page contains an **infobox** with structured metadata.
- The scraper parses this infobox by searching for **specific HTML tags**.
- These tags are explicitly handled in `main.py`.

⚠️ **Important:**  
If new tags are added or the infobox structure changes on the Tibia Wiki, **`main.py` must be updated** to include and parse the new tags correctly.

---

## 🛠️ Running Locally

### Requirements

- Python 3.x
- `pip`
- `requests`
- `pandas`

### Installation

Install the project dependencies:

```bash
pip install -r requirements.txt
```

### Run the Scraper

```bash
python main.py
```

After execution, the file `tibia_wiki_items.csv` will be created or updated in the project directory.

---

## 📜 License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.
