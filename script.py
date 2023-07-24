from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Publisher, Book, Shop, Stock, Sale

# Database connection parameters
db_username = 'postgres'
db_password = '09051945pi'
db_host = 'localhost:5432'
db_name = 'pppp'


# Create a database engine
engine = create_engine(f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}")

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


def get_shops(publisher_name):
    publisher = session.query(Publisher).filter(Publisher.name == publisher_name).first()
    if publisher_name.isdigit():
        publisher = session.query(Publisher).filter(Publisher.id == publisher_name).first()
        query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
            join(Stock, Book.id == Stock.id_book).\
            join(Sale, Stock.id == Sale.id_stock).\
            join(Shop, Stock.id_shop == Shop.id).\
            filter(Book.id_publisher == publisher.id)
        for title, shop_name, price, date_sale in query:
            print(f"{title} | {shop_name} | {price} | {date_sale.strftime('%d-%m-%Y')}")
    else:
        query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale). \
            join(Stock, Book.id == Stock.id_book). \
            join(Sale, Stock.id == Sale.id_stock). \
            join(Shop, Stock.id_shop == Shop.id). \
            filter(Book.id_publisher == publisher.id)
        for title, shop_name, price, date_sale in query:
            print(f"{title} | {shop_name} | {price} | {date_sale.strftime('%d-%m-%Y')}")


# Close the session
session.close()
if __name__ == '__main__':
    publisher_name = input("Enter the name or identifier of the publisher: ")
    get_shops(publisher_name)