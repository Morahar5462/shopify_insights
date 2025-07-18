Shopify Store Insights Fetcher 🛍️
This project is a Python-based application built with FastAPI that scrapes a given Shopify store's website to extract and structure key brand insights. The application is designed to be robust, scalable, and maintainable, adhering to modern software development best practices without using the official Shopify API.

✨ Features
The application extracts the following information from a target Shopify store:

Full Product Catalog: Retrieves the complete list of products from the store's /products.json endpoint.

Hero Products: Identifies products that are featured directly on the homepage.

Brand Policies: Fetches the text for Privacy, Refund/Return, and Shipping policies.

Social Media Handles: Discovers links to the brand's social profiles (Instagram, Facebook, Twitter, etc.).

Contact Details: Finds contact emails and phone numbers.

Brand Context: Grabs the "About Us" text to provide context about the brand.

Important Links: Collects key navigational links like "Contact Us," "Track Order," etc.

🛠️ Tech Stack & Design Principles
Framework: FastAPI for high-performance, asynchronous API development.

HTTP Client: HTTPX for modern, async-ready HTTP requests.

HTML Parsing: BeautifulSoup4 (with lxml) for efficient web scraping.

Data Validation: Pydantic for robust data modeling and validation.

Architecture: The application's code is organized into distinct modules for models, utilities, and the main application logic to ensure separation of concerns.

📂 Project Structure
The project is organized logically to promote modularity and readability.

/shopify_insights
  ├── main.py
  ├── utils/
  │   ├── scraper.py
  │   └── helpers.py
  ├── models/
  │   └── schema.py
  └── requirements.txt
🚀 Setup and Installation
Follow these steps to get the application running locally.

Clone the Repository

Bash

git clone <your-repo-url>
cd shopify_insights
Create a Virtual Environment (Recommended)

Bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install Dependencies

Bash

pip install -r requirements.txt
Run the Application

Bash

uvicorn main:app --reload
The server will start on http://127.0.0.1:8000. The --reload flag enables hot-reloading for development.

🎮 How to Use
Once the application is running, you can interact with it using the automatically generated documentation.

Open the API Docs: Navigate to http://127.0.0.1:8000/docs in your browser.

Test the Endpoint:

Expand the POST /insights endpoint.

Click "Try it out."

In the request body, enter the URL of a Shopify store you want to analyze.

JSON

{
  "website_url": "https://hairoriginals.com"
}
Click "Execute."

API Endpoint Details
POST /insights
Description: Accepts a Shopify store URL and returns a structured JSON of brand insights.

Request Body:

JSON

{
  "website_url": "string (must be a valid URL)"
}
Success Response (200 OK):
Returns a JSON object with all the scraped data.

JSON

{
  "product_catalog": [...],
  "hero_products": [...],
  "social_handles": {"instagram": "...", "facebook": "..."},
  "contact_details": {"emails": [...], "phones": [...]},
  "brand_context": "...",
  "policies": {"privacy_policy": "...", "refund_policy": "..."},
  "important_links": {"contact": "...", "about": "..."}
}
Error Responses:

404 Not Found: If the website is unreachable or cannot be parsed.

422 Unprocessable Entity: If the request body is invalid (e.g., not a valid URL).

500 Internal Server Error: For any unexpected errors during the scraping process.

