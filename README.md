# E-commerce Product Recommendation System (Kilimall Beauty & Health)

## Project Overview:

This project is all about making online shopping easier and more personalized. Imagine a huge store like Kilimall, with thousands of products. How do you find exactly what you're looking for, or discover new items you might love?

That's where this system comes in. It's a **recommendation system** built specifically for beauty and health products. By understanding product details like names, rating, categories,sub-categories and customer reviews, it suggests personalized items, making the shopping experience smoother and more engaging for users.

**Key achievements of this project include:**
* **Mastering Web Scraping:** Successfully gathering product information from a dynamic e-commerce website.
* **Data Cleaning:** Transforming messy, real-world data into a clean, usable format.
* **Building a Content-based Recommendation system :** Creating a system that recommends products based on user input.

## The Problem I'm Solving

In today's crowded online marketplaces, shoppers often face **information overload**. They might know they want a "face cream" but get overwhelmed by hundreds of choices. Without good recommendations, users can get frustrated and leave the site without buying.

This project tackles this "discovery problem" head-on. By providing tailored suggestions, it helps users quickly find what they need or explore complementary products, ultimately **improving their shopping journey** and helping the e-commerce platform convert more sales.

## Core Features That Make It Work

This system employs several key components to deliver effective recommendations:

* **1. Web Scraping:**
    * **How:** I used powerful tools (`requests`, `BeautifulSoup`, and `Selenium`) to collect product data from Kilimall. This setup is specifically designed to handle websites that load content dynamically, ensuring I capture all necessary details.
    * **Benefit:** Gathered a rich dataset of products including names, prices, ratings, categories, sub-categories and customer reviews.

* **2. Data Refinement (Crucial Step!):**
    * **How:** Real-world category data can be inconsistent. I have built a custom function that uses keywords in product names to accurately clean and map vague or inconsistent categories (e.g., ensuring a "men's hair clipper" is correctly classified under "Men's Grooming" even if initially listed broadly).
    * **Benefit:** Helps in  Transforming raw, messy, data that was scraped into highly precise and usable categories, which is vital for accurate recommendations.
    * 

* **3. Robust Data Preparation:**
    * **How:** Before building the recommendation system, I processed the data by handling any missing information, converting text (like "KSh 999") into usable numbers, and standardizing numerical values using **RegX**.
    * **Benefit:** Ensures the data is clean and in the right format for the machine learning model.

* **4. Content-Based Recommendation Engine:**
    * **How:** I analyzed the *description and type* (content) of products. Using techniques like TF-IDF (Term Frequency-Inverse Document Frequency) and Cosine Similarity, I measured how "similar" different products are based on their features.
    * **Benefit:** Recommends products that share similar characteristics to what a user is looking for.

* **5. Hybrid Recommendation Logic:**
    * **How:** Instead of just finding similar products anywhere, our system takes user-specified `Category` and `Sub_Category` preferences into account *first*. Then, it applies content similarity **within that specific category**.
    * **Benefit:** Provides highly relevant and focused recommendations (e.g., "show me similar face creams within the 'Face' category," not just any similar product).

* **6. User-Friendly Interface (for demonstration):**
    * **How:** The Jupyter Notebook allows you to interact directly with the system. You can input your desired product category and sub-category to get immediate recommendations.
    * **Benefit:** Easy to test and see the recommendations in action.

## 🛠 Technologies Used

* **Python 3.x**
* **Web Scraping:** `requests`, `BeautifulSoup`, `selenium` (with Chrome WebDriver)
* **Data Manipulation & Analysis:** `pandas`, `numpy`
* **Natural Language Processing (NLP):** `nltk`, 
* **Machine Learning (Scikit-learn):** `TfidfVectorizer`, `cosine_similarity`, `MinMaxScaler`
* **Other:** `time`, `random`, `os`, `re`

## 📂Files
- `data.py`: The script for scraping data and performing initial cleaning.
- `model.ipynb`: The main Jupyter Notebook where data is prepared, the recommendation engine is built, and recommendations are generated.
- `kilimall_beauty_health_products_scraped.csv`: Raw scraped product data.
- `unique_category_sub_category_combinations.csv`: A list of all clean and unique category/sub-category pairs, useful for input.


## 🚀 Getting Started

Follow these steps to set up and run the project on your machine:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/taylorwanyama/Recommendation-system-project.git](https://github.com/taylorwanyama/Recommendation-system-project.git)
    cd Recommendation-system-project
    ```

2.  **Install Required Libraries:**
    Ensure you have all the necessary Python libraries installed. If you have a `requirements.txt` file (which you can generate using `pip freeze > requirements.txt` after manually installing them once), run:
    ```bash
    pip install -r requirements.txt
    ```
    Otherwise, install them manually:
    ```bash
    pip install pandas numpy requests beautifulsoup4 selenium scikit-learn nltk
    ```

4.  **Install Chrome WebDriver:**
    The `data.py` script requires `chromedriver` to interact with the Chrome browser.
    * **Download:** Get the `chromedriver` version that matches your installed Chrome browser from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).
    * **Placement:** Place the downloaded `chromedriver.exe` (or `chromedriver`) file in your project directory, or in a directory that is part of your system's PATH.

5.  **Download NLTK Data:**
    The `model.ipynb` uses NLTK resources for text processing. Run these commands once in your Python environment:
    ```python
    import nltk
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    ```

## ▶️ How to Use the Recommendation System

1.  **Run the Data Scraper (Optional - if `kilimall_beauty_health_products_scraped.csv` doesn't exist or needs updating):**
    * Open your terminal or command prompt in the project folder.
    * Execute the `data.py` script:
        ```bash
        python data.py
        ```
    * This will scrape data, perform initial cleaning, and save it to `kilimall_beauty_health_products_scraped.csv`.

2.  **Launch the Recommendation Notebook:**
    * Start Jupyter Notebook from your project directory:
        ```bash
        jupyter notebook
        ```
    * In the Jupyter interface, open `model.ipynb`.
    * **Execute all cells sequentially** from top to bottom.
    * **Interactive Input:** When prompted, enter a `Category` and `Sub_Category` (e.g., `Beauty` and `Fragrance`) to receive recommendations. You can refer to `unique_category_sub_category_combinations.csv` for valid combinations.

## Data Source

The dataset for this project was diligently scraped from the "Beauty & Health" section of [Kilimall.co.ke](https://www.kilimall.co.ke/).

##  What I Learned & What Makes This Project Stand Out

This project was a deep dive into practical data science, offering insights into:

* **Real-world Web Data:** Gaining hands-on experience with challenges like dynamic content and anti-scraping measures.
* **The Power of Clean Data:** Realizing how crucial robust data cleaning (especially my custom category refinement) is for any successful machine learning project. Garbage in, garbage out!
* **Building a Smart Recommender:** Understanding how content similarity can be leveraged to provide truly personalized product suggestions.
* **Hybrid Approach Benefits:** Seeing how combining content analysis with simple filtering (by category) can yield highly relevant results for users.

## 📈 Future Enhancements

I envision several ways to expand and improve this system:

* **User Behavior Integration:** Incorporating actual user purchase history or viewing patterns to build a more advanced hybrid system (e.g., collaborative filtering).
* **Deployment:** Turning the recommendation engine into a deployable service (e.g., a simple API) for real-time recommendations.
* **Performance Metrics:** Implementing quantitative metrics to rigorously evaluate recommendation quality (e.g., precision, recall, diversity).
* **Scalability:** Optimizing the scraping and processing pipelines for even larger datasets and faster performance.

## Author

**[Taylor Wanyama]**
**([https://www.linkedin.com/in/your-linkedin-profile-url/](https://www.linkedin.com/in/taylor-wanyama-421920271/))**


