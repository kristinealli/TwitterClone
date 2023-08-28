#Populate tea database with fake information using the SQLAlchemy ORM

import random
import string
import hashlib
import secrets
from datetime import datetime, timedelta
from faker import Faker  
from flying_saucers.src.models import Tea, Rating, User, Collection, Supplier, Variety, tea_collection_association_table, db
from flying_saucers.src import create_app

TEA_COUNT = 40
USER_COUNT = 5
RATING_COUNT = 100
COLLECTION_COUNT = 15
MAX_TEAS_PER_COLLECTION = 40

assert RATING_COUNT <= (TEA_COUNT * USER_COUNT)
fake = Faker()

#Hashed and Salted Password of Length N | 8 <= N <= 15
def random_passhash():
    raw = ''.join(
        random.choices(
            string.ascii_letters + string.digits + '!@#$%&',  
            k=random.randint(8, 15)  
        )
    )
    salt = secrets.token_hex(16)
    return hashlib.sha512((raw + salt).encode('utf-8')).hexdigest()


#Delete all rows from database tables
def truncate_tables():
    db.session.execute(tea_collection_association_table.delete())
    Tea.query.delete()
    Rating.query.delete()
    User.query.delete()
    Collection.query.delete()
    Supplier.query.delete()
    Variety.query.delete()
    db.session.commit()
    

    
def main(): 
    app = create_app()
    app.app_context().push()
    truncate_tables()
    
    last_tea = None
    for _ in range (TEA_COUNT):
        last_tea = Tea(
            blend_name=fake.unique.word(),  # Fake unique blend names
            tasting_notes=fake.sentence(),
            date_of_purchase=fake.date_time_this_decade(),
            price=random.uniform(5, 20),  # Random price between 5 and 20
            origin=fake.word(),
            caffeine=random.choice([True, False]),  # Random caffeine value
            variety_type=fake.word(),
            brewing_temp_F=random.randint(160, 212),   # Random temperature range
            brewing_temp_C=random.randint(71, 100),   # Random temperature range
            brewing_time_min=random.randint(2, 5),   # Random brewing time
            tsp_per_cup=random.randint(1, 2)   # Random tsp_per_cup
        )
        db.session.add(last_tea)
    db.session.commit()
    
    last_user = None
    for _ in range(USER_COUNT): 
        last_user = User(
            username = fake.unique.first_name().lower() + str(random.randint(1,150)),
            password = random_passhash()
        )
        db.session.add(last_user)
    db.session.commit()
    
    last_rating = None
    for _ in range (RATING_COUNT): 
        last_rating = Rating(
            date_created = fake.date_time_this_decade(),
            review_comments = fake.sentence(),
            ranking = random.randint(1,5),
            tea_id = random.randint(1, TEA_COUNT),
            author_user_id = random.randint(1, USER_COUNT)
        )
        db.session.add(last_rating)
    db.session.commit()
    
    last_collection = None
    collections = []
    for _ in range(COLLECTION_COUNT): 
        last_collection = Collection(
            collection_id = fake.unique.word(),
            date_created = fake.date_time_this_decade(),
            user_id = random.randint(1, USER_COUNT)
        )
        collections.append(last_collection)
        db.session.add(last_collection)
    db.session.commit()
    
    tea_collection_groups = set()
    for collection in collections:
        num_teas = random.randint(1, MAX_TEAS_PER_COLLECTION)
        selected_teas = random.sample(range(1, TEA_COUNT + 1), num_teas)
        for tea_id in selected_teas:
            tea_collection_groups.add(
                (tea_id, collection.user_id, collection.id))

    new_collection = [{"user_id": value[1], "tea_id": value[0],"collection_id": value[2]} for value in tea_collection_groups]
    insert_collection = tea_collection_association_table.insert().values(new_collection)
    db.session.execute(insert_collection)
    db.session.commit()
        
main()
    