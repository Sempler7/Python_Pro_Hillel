from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData

engine = create_engine("postgresql+psycopg2://user:password@localhost/online_shop")
metadata = MetaData()

products = Table("products", metadata,
                 Column("id", Integer, primary_key=True),
                 Column("name", String),
                 Column("price", Float),
                 Column("category", String),
                 Column("stock", Integer)
                 )

metadata.create_all(engine)

# Використовуємо контекстний менеджер
with engine.connect() as conn:
    # CREATE
    conn.execute(products.insert().values(name="Ноутбук ASUS", price=25000, category="electronics", stock=15))
    conn.commit()

    # READ
    result = conn.execute(products.select())
    for row in result:
        print(row)

    # UPDATE
    conn.execute(products.update().where(products.c.name == "Ноутбук ASUS").values(stock=14))
    conn.commit()

    # DELETE
    conn.execute(products.delete().where(products.c.stock <= 0))
    conn.commit()
