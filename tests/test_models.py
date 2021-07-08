"""Test Cases for database models."""
import datetime
import random
from decimal import Decimal

import factory
import pytest
import pytz
from sqlalchemy import create_engine, orm

from scout import config, models
from scout.db_util import ENGINE

# DB Setup
engine = create_engine("sqlite://")
Session = orm.scoped_session(orm.sessionmaker(bind=engine))
config.Base.metadata.create_all(engine)


# Fixture definitions used in individual tests
@pytest.fixture(scope="module")
def connection() -> None:
    """Create an isolated connection that closes itself after each test."""
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="function")
def session(connection: orm.session.Session) -> None:
    """Create an isolated session that levereages our connection each test."""
    transaction = connection.begin()
    session = Session()
    yield session
    session.close()
    transaction.rollback()


class RetailerFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for Retailer Model."""

    class Meta:
        model = models.Retailer
        sqlalchemy_session = Session

    id = factory.LazyAttribute(lambda _: random.randrange(1000, 9999))
    name = factory.Faker("company")
    website = factory.Faker("domain_name")


def test_engine_created_with_url_from_config() -> None:
    """It loads url from config."""
    assert str(ENGINE.url) == "sqlite:///scout.db"


class PriceSnapshotFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for PriceSnapshot  Model."""

    class Meta:
        model = models.PriceSnapshot
        sqlalchemy_session = Session

    id = factory.LazyAttribute(lambda _: random.randrange(1000, 9999))
    price = factory.LazyAttribute(lambda _: Decimal(random.randrange(0, 200)))
    product_id = factory.LazyAttribute(lambda _: random.randrange(1000, 9999))
    retailer_id = factory.LazyAttribute(lambda _: random.randrange(1000, 9999))
    date = factory.LazyFunction(datetime.datetime.utcnow)


class TestRetailerModel:
    """Tests for Retailer Model."""

    def test_create_retailer_returns_retailer_object(self: "TestRetailerModel") -> None:
        """It creates a Retailer object."""
        name = "Company Name"
        website = "https://www.website.com"

        input_dict = {"name": name, "website": website}

        test_obj = models.Retailer.create_retailer(input_dict)

        assert test_obj.name == name.lower()
        assert test_obj.website == website


class TestProductModel:
    """Tests for Product Model."""

    def test_create_product_returns_product_object(self: "TestProductModel") -> None:
        """It creates a Product object."""
        name = "Product Name"
        description = "Product Description"

        input_dict = {"name": name, "description": description}

        test_obj = models.Product.create_product(input_dict)

        assert test_obj.name == name
        assert test_obj.description == description


class TestPriceSnapshotModel:
    """Tests for PriceSnapshot Model."""

    def test_create_pricesnapshot_returns_product_object(
        self: "TestPriceSnapshotModel",
    ) -> None:
        """It creates a PriceSnapshot object."""
        price = Decimal(9.99)
        product_id = 100
        retailer_id = 1
        date = "2021-04-06 17:00:00+00:00"

        input_dict = {
            "price": price,
            "product_id": product_id,
            "retailer_id": retailer_id,
            "date": date,
        }

        test_obj = models.PriceSnapshot.create_price_snapshot(input_dict)
        assert test_obj.price == price
        assert test_obj.product_id == product_id
        assert test_obj.retailer_id == retailer_id
        assert test_obj.date == str(
            datetime.datetime(2021, 4, 6, 17, 0, 0, tzinfo=pytz.utc)
        )

    def test_get_pricesnapshots_returns_records_matching_product_id(
        self: "TestPriceSnapshotModel", session: orm.session.Session
    ) -> None:
        """It returns all records matching the product_id."""
        snapshot1 = PriceSnapshotFactory.create()
        snapshot2 = PriceSnapshotFactory.create()
        snapshot3 = PriceSnapshotFactory.create()

        snapshot1.product_id = 1
        snapshot2.product_id = 2
        snapshot3.product_id = 3
        results = models.PriceSnapshot.get_price_snapshots(session, 3)
        assert results == [snapshot3]


class TestURLMappingModel:
    """Tests for the URLMapping model."""

    def test_create_urlmapping_returns_urlmapping_object(
        self, session: orm.session.Session
    ) -> None:
        """It creates an URLMapping object."""
        product_id = 100
        url = "www.retailer.com"
        html_tag = "<div class='price'>"
        retailer_id = RetailerFactory.create()
        unit_quanity = 1

        test_dict = {
            "product_id": product_id,
            "url": url,
            "html_tag": html_tag,
            "retailer_id": retailer_id,
            "unit_quanity": unit_quanity,
        }

        test_obj = models.URLMapping.create_URL(test_dict)

        assert test_obj.product_id == product_id
        assert test_obj.url == url
        assert test_obj.html_tag == html_tag
        assert test_obj.retailer_id == retailer_id
        assert test_obj.unit_quanity == unit_quanity
