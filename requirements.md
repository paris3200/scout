# Requirements

* Scrape multiple websites for a item prices.
* Store pricing data in database.
* Track the average price of an item.
* Calculate unit price with bulk discounts.


# Data Model

* DB Models
    * Product
        * id
        * name
        * description

    * Categories
        * id
        * description

    * Product Categories
        * product_id
        * categories_id

    * Price Snapshot
        * id
        * product_id
        * price
        * unit_price
        * date
        * retailer

    * URL_mappings
        * product_id
        * retailer_id
        * url
        * html_tag
        * unit_quanity

    * Retailer
        * id
        * Name
        * website


* Scraper Helper
    * Beautiful Soup helper

* Config
    * Constants

* CLI
    * Db connections object
    * Main Function


# Happy Path
 1. Spin up, read config and instantiate logger.
 2. Read database to get urls and html tags.
 3. Scrape websites for prices.
 4. Write price info to database.
 5. Calculate average price.
 6. Exit
