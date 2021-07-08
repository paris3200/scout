"""Database models for scout package."""
import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    orm,
    select,
)

from . import config


class Product(config.Base):
    """Product Model."""

    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    @classmethod
    def create_product(cls: "Product", record: dict) -> "Product":
        """Creates a Product object.

         Args:
            record: Dict containing Product data. Fields (keys) should match:
                name: str, The common name of the product.  This is not the
                    specific name that a retailer gives a product.  This name is
                    shared among all retailers.
                description: str, Product description.

        Returns:
            An instantiated Retailer instance.
        """
        data_dict = {
            "name": record["name"],
            "description": record["description"],
        }

        return cls(**data_dict)


class Category(config.Base):
    """Category model."""

    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)


class ProductCategory(config.Base):
    """ProductCategory model maps products to a category id."""

    __tablename__ = "product_categories"
    id = Column(Integer, primary_key=True)
    categories_id = Column(Integer)
    product_id = Column(Integer)


class PriceSnapshot(config.Base):
    """PriceSnapshot model."""

    __tablename__ = "price_snapshot"
    id = Column(Integer, primary_key=True)
    price = Column(Numeric)
    product_id = Column(Integer, ForeignKey("product.id"))
    retailer_id = Column(Integer, ForeignKey("retailer.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def create_price_snapshot(cls, record: dict) -> "PriceSnapshot":
        """Creates a PriceSnapshot object.

         Args:
            record: Dict containing retailer data. Fields (keys) should match:
                price: decimal, Product price.
                product_id: int, Primary key from product table.
                retailer_id: int, Primary key from retailer table.
                date: str, Date the price was checked.
                    Defaults to datetime.datemine.utcnow

        Returns:
            An instantiated PriceSnapshot instance.
        """
        data_dict = {
            "price": record["price"],
            "product_id": record["product_id"],
            "retailer_id": record["retailer_id"],
            "date": record["date"],
        }

        return cls(**data_dict)

    @classmethod
    def get_price_snapshots(cls, session: orm.session.Session, product_id: int) -> list:
        """Queries the database to get all records that match a product_id.

        Args:
            session: An initialized SQLAlchemy session object.
            product_id: int, The product_id to search for.

        Returns:
            A list of database records with product_id == product_id.
        """
        return (
            session.execute(select(cls).where(cls.product_id == product_id))
            .scalars()
            .all()
        )


class URLMapping(config.Base):
    """URL_Mappings model."""

    __tablename__ = "url_mappings"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    url = Column(String, nullable=False)
    html_tag = Column(String, nullable=False)
    retailer_id = Column(Integer, ForeignKey("retailer.id"))
    unit_quanity = Column(Integer, default=1, nullable=False)

    @classmethod
    def create_URL(cls, record: dict) -> "URLMapping":
        """Creates a URLMapping object.

         Args:
            record: Dict containing url mapping data. Fields (keys) should match:
                product_id: int, Primary key from product table.
                url: str, The product url.
                html_tag: str, The html tag containing price.
                retailer_id: int, Primary key from retailer table.
                unit_quanity: int, int, number of units in product listing

        Returns:
            An instantiated Retailer instance.
        """
        data_dict = {
            "product_id": record["product_id"],
            "url": record["url"],
            "html_tag": record["html_tag"],
            "retailer_id": record["retailer_id"],
            "unit_quanity": record["unit_quanity"],
        }

        return cls(**data_dict)


class Retailer(config.Base):
    """Retailer model."""

    __tablename__ = "retailer"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    website = Column(String, nullable=False)

    @classmethod
    def create_retailer(cls, record: dict) -> "Retailer":
        """Creates a Retailer object.

         Args:
            record: Dict containing retailer data. Fields (keys) should match:
                name: str, The name of the retailer.
                website: str, The website url.

        Returns:
            An instantiated Retailer instance.
        """
        data_dict = {"name": record["name"].lower(), "website": record["website"]}

        return cls(**data_dict)
