# E-commerce Product Recommendation System (Kilimall Beauty & Health)

## Project Overview:

This project is all about making online shopping easier and more personalized. Imagine a huge store like Kilimall, with thousands of products. How do you find exactly what you're looking for, or discover new items you might love?

That's where this system comes in. It's a **recommendation engine** built specifically for beauty and health products. By understanding product details like names, categories, and reviews, it suggests personalized items, making the shopping experience smoother and more engaging for users.

**Key achievements of this project include:**
* **Mastering Web Data:** Successfully gathering product information from a dynamic e-commerce website.
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

**2. Data Refinement (Crucial Step!):**
    * **How:** Real-world category data can be inconsistent. I have built a custom function that uses keywords in product names to accurately clean and map vague or inconsistent categories (e.g., ensuring a "men's hair clipper" is correctly classified under "Men's Grooming" even if initially listed broadly).
    * **Benefit:** Helps in  Transforming raw, messy, data that was scraped into highly precise and usable categories, which is vital for accurate recommendations.
    * 

* **3. Robust Data Preparation:**
    * **How:** Before building the recommendation engine, I processed the data by handling any missing information, converting text (like "KSh 999") into usable numbers, and standardizing numerical values using **RegX**.
    * **Benefit:** Ensures the data is clean and in the right format for the machine learning model.

* **4. Content-Based Recommendation Engine:**
    * **How:** I analyzesd the *description and type* (content) of products. Using techniques like TF-IDF (Term Frequency-Inverse Document Frequency) and Cosine Similarity, I measured how "similar" different products are based on their features.
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

## 📂 Project Structure
