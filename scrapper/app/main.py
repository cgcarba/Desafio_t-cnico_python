from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from google.cloud import bigquery
import pandas as pd
from datetime import datetime
import pytz


def get_category_from_url(url, options):
    """
    Get category from article page
    """
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        
        # Try multiple selectors in order of preference
        selectors = [
            "div.volanta_noticia.fuente_roboto_slab",
            "div.volanta.fuente_roboto_slab",
            "div.volanta_noticia",
            "div.volanta"
        ]
        
        for selector in selectors:
            try:
                element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                category = element.text.strip()
                if category:
                    return category
            except:
                continue
                
        return "N/A"
    except:
        return "N/A"
    finally:
        driver.quit()


def clean_category(category):
    """
    Clean and standardize category text
    """
    if not category or category == "None" or category.isspace():
        return "N/A"
    return category.strip().upper()


# Función de Web Scraping
def scrape_yogonet():
    """
    Scrape the latest news from Yogonet
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--start-maximized")
    options.add_argument('--log-level=3')  # Suppress most Chrome logs
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://www.yogonet.com/international/latest-news/")
        
        wait = WebDriverWait(driver, 20)
        news_container = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "contenedor_modulo"))
        )
        
        articles = driver.find_elements(By.CSS_SELECTOR, "div.contenedor_dato_modulo")
        
        article_data = []
        
        for article in articles:
            try:
                title_element = article.find_element(By.CSS_SELECTOR, "h2.titulo a")
                title = title_element.text.strip() or title_element.get_attribute("textContent").strip()
                link = title_element.get_attribute("href")
                category = get_category_from_url(link, options)
                image = article.find_element(By.CSS_SELECTOR, "img").get_attribute("src") or "N/A"
                
                if title:
                    article_data.append({
                        'title': title.strip(),
                        'category': clean_category(category),
                        'link': link,
                        'image': image,
                        'scraped_date': datetime.now(pytz.UTC)
                    })
            except:
                continue
        
        return article_data
        
    finally:
        driver.quit()


# Función de Post-Processing
def process_scraped_data(scraped_data):
    """
    Process the scraped data
    """
    if not scraped_data:
        raise ValueError("No articles were scraped successfully")
        
    df = pd.DataFrame(scraped_data)
    
    # Convert scraped_date to datetime if it isn't already
    df["scraped_date"] = pd.to_datetime(df["scraped_date"])
    
    # Add the existing processing steps
    df["word_count"] = df["title"].apply(lambda x: len(str(x).split()))
    df["char_count"] = df["title"].apply(lambda x: len(str(x)))
    df["capital_words"] = df["title"].apply(
        lambda x: ','.join([word for word in str(x).split() if word.istitle()])
    )
    
    return df


# Función para cargar datos en BigQuery
def upload_to_bigquery(processed_data, table_id):
    """
    Upload the processed data to BigQuery
    """
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        schema=[
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("category", "STRING"),
            bigquery.SchemaField("link", "STRING"),
            bigquery.SchemaField("image", "STRING"),
            bigquery.SchemaField("scraped_date", "DATETIME"),
            bigquery.SchemaField("word_count", "INTEGER"),
            bigquery.SchemaField("char_count", "INTEGER"),
            bigquery.SchemaField("capital_words", "STRING"),
        ],
    )

    job = client.load_table_from_dataframe(
        processed_data, table_id, job_config=job_config
    )
    job.result()


# Flujo principal
if __name__ == "__main__":
    # Scraping
    scraped_data = scrape_yogonet()

    # Post-Processing
    processed_data = process_scraped_data(scraped_data)

    # Upload to BigQuery
    table_id = "project.dataset.table"
    upload_to_bigquery(processed_data, table_id)
