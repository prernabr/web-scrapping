import requests
import csv
from bs4 import BeautifulSoup

# Define the URL
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

# Number of pages to scrape
num_pages = 20

# Create a CSV file and write headers
with open("product_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews", "Description", "ASIN", "Product Description", "Manufacturer"])

    # Iterate over each page
    for page in range(1, num_pages + 1):
        # Generate the URL for the current page
        page_url = url + "&page=" + str(page)

        # Send a GET request to the page URL
        response = requests.get(page_url)

        # Create a BeautifulSoup object with the response content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all the product items on the page
        product_items = soup.find_all("div", class_="s-result-item")

        # Iterate over each product item and extract the required information
        for item in product_items:
            # Extract the product URL
            product_url_element = item.find("a", class_="a-link-normal s-no-outline")
            product_url = "https://www.amazon.in" + product_url_element["href"] if product_url_element else None

            # Extract the product name
            product_name_element = item.find("span", class_="a-size-medium a-color-base a-text-normal")
            product_name = product_name_element.text.strip() if product_name_element else None

            # Extract the product price
            product_price_element = item.find("span", class_="a-price-whole")
            product_price = product_price_element.text.strip() if product_price_element else None

            # Extract the product rating
            product_rating_element = item.find("span", class_="a-icon-alt")
            product_rating = product_rating_element.text.strip() if product_rating_element else None

            # Extract the number of reviews
            product_reviews_element = item.find("span", class_="a-size-base")
            product_reviews = product_reviews_element.text.strip() if product_reviews_element else None

            if product_url:
                try:
                    # Send a GET request to the product URL
                    product_response = requests.get(product_url)
                    product_soup = BeautifulSoup(product_response.content, "html.parser")

                    # Extract the description
                    description_element = product_soup.find("div", id="feature-bullets")
                    description = description_element.text.strip() if description_element else None

                    # Extract the ASIN
                    asin_element = product_soup.find("th", text="ASIN")
                    asin = asin_element.find_next("td").text.strip() if asin_element else None

                    # Extract the product description
                    product_desc_element = product_soup.find("div", id="productDescription")
                    product_desc = product_desc_element.text.strip() if product_desc_element else None

                    # Extract the manufacturer
                    manufacturer_element = product_soup.find("a", id="bylineInfo")
                    manufacturer = manufacturer_element.text.strip() if manufacturer_element else None

                    # Write the extracted information to the CSV file
                    writer.writerow([product_url, product_name, product_price, product_rating, product_reviews, description, asin, product_desc, manufacturer])
                except requests.exceptions.RequestException as e:
                    print(f"Error occurred while scraping product: {product_url}")
                    print(e)
            else:
                print("Product URL not found. Skipping...")

# Print a message indicating the successful saving of data
print("Data has been saved to product_data.csv file.")
