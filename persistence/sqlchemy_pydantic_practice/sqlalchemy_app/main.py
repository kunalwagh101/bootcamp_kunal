from database import SessionLocal, engine
from models import Base, User ,Post
from pydantic import BaseModel, EmailStr, ValidationError
from typing import Optional ,List
from sqlalchemy import delete
Base.metadata.create_all(bind=engine)
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import ssl
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker



class UserSchema(BaseModel):
    """Define a Simple SQLAlchemy Model with Pydantic"""

    name : Optional[str]
    email: Optional[EmailStr]

    class Config:
        from_attributes = True  

class PostSchema(BaseModel):
    """Pydantic model for Post."""
    title: str
    content: str
    user_id: int
    owner: Optional[UserSchema] = None

    class Config:
        from_attributes = True



"""
No 1.2 Insert a New User: 

Create a SQLAlchemy session.
Validate user data with Pydantic before inserting.
Commit the new user to the database.
"""

db = SessionLocal()

def create_user(user:dict):
    """ creating new user """ 
    try :
        data  =  UserSchema(**user)
    except ValidationError as e :
            logger.error(f"Validation Error occured {e}")
 
    user_data =  User(name = data.name , email = data.email)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return  user_data


"""
No 1.3 Fetch Users from the Database

Retrieve all users from the database.
Convert database results to a list of Pydantic models.
Display the users in a structured format.
"""
def fetch_all_user() :
    """ Retrieve ,Convert , Displays the users info """
    all_users  = db.query(User).all()
    pydantic = [ UserSchema.model_validate(i, from_attributes=True) for i in all_users]
    
    for user in pydantic :
         print( f"User info = {user.model_dump()}")

    return pydantic
    
""" 
==== Intermediate Level (Filtering, Updating, and Deleting Data) ===
"""


"""
No 2.1 
Filter Users Based on Email

Create a function to fetch a user by email.
Return a UserSchema response if the user exists.
Handle cases where the user is not found.
"""

def get_user_email(data:Optional[dict]) :
    """ Create, Returns , Handle finding user via email """

    if not isinstance(data ,str):
        user = db.query(User).filter(User.email == data["email"] ).first()
    else : 
        user = db.query(User).filter(User.email == data ).first()

    if not user :
        logger.info(f"User not found !")
        return None
    user_schema  = UserSchema.model_validate(user)
    logger.info("Fetched user: %s", user_schema.model_dump())
    return user_schema


"""
No. 2.2  Update User Email

Implement a function to update a user's email.
Ensure changes persist in the database.
Return a success message if updated successfully.
"""

def update_email(data :Optional[dict] ,  new_email:EmailStr):
    """ It ensures, updates and return a updated email with success message ! """

    if not isinstance(data ,str):
        user = db.query(User).filter(User.email == data["email"]).first()
        
    else :       
        user = db.query(User).filter(User.email == data ).first()

    if not user :
        logger.info(f"User not found !")
  
        return None   
    try : 
        user.email  = new_email
        db.commit()
        db.refresh(user)
        logger.info("User email updated successfully: %s", user)
        return "User email updated successfully."
    
    except ValidationError as e :
        db.rollback()
        logger.error(f"Validation error occured : {e}!")
        return None

"""
No 2.3 Delete a User

Write a function to remove a user from the database.
Use SQLAlchemy's delete() method.
Confirm deletion before committing.
"""

def delete_user(email: EmailStr):
    """
    Delete a user from the database based on the provided email.
    """

   
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.info("User with email '%s' not found.", email)
        return f"User with email '{email}' not found."
    
    try:
    
        user_remove = delete(User).where(User.email == email)
        db.execute(user_remove)
        db.commit()
        logger.info("User with email '%s' deleted successfully.", email)
        return f"User with email '{email}' deleted successfully."
    except Exception as e:
        db.rollback()
        logger.error("Error deleting user: %s", e)
        return f"Error deleting user: {e}"



"""
=======  Advanced Level (Relationships, Async Queries, and Transactions)  ===== 
"""


"""
No 3.1 Add a Post Table and Create a Relationship

Define a new Post model with a foreign key to User.
Establish a relationship between User and Post.
Ensure users can have multiple posts.
     
"""
     
def create_muiti_post(user_email , posts_data: List[dict]):

    """ generate new post  """
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        logger.error(f"User with email  not found. {user_email}" )
        return None
    
    created_posts = []

    for post_data in posts_data:
        new_post = Post(
            title=post_data.get("title"),
            content=post_data.get("content"),
            owner=user 
        )
        db.add(new_post)
        created_posts.append(new_post)

    try:
        db.commit() 
        for post in created_posts:
            db.refresh(post)
        logger.info(f"User  now has new posts:  {user.email}, {created_posts}",)

        return created_posts
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating posts for user {user.email}, {e} ", )
        return None
    



"""
No 3.2 Fetch a User and Their Posts

Implement a query to get a user along with their posts.
Convert results into nested Pydantic models.
Return a structured JSON response.
"""


def fetch_user_with_posts(email: EmailStr):
    """
    Retrieve a user along with their posts.

    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.info("User with email '%s' not found.", email)
        return None

    user_schema = UserSchema.model_validate(user, from_attributes=True)
    logger.info("Fetched user with posts: %s", user_schema.model_dump())
    return user_schema.model_dump()



def create_bulk_users(users_data: List[dict]):
    """
    Bulk insert multiple users using transactions to ensure atomicity.

    """
    created_users = []
    try:
        for user in users_data:
            validated = UserSchema(**user)
            new_user = User(name=validated.name, email=validated.email)
            db.add(new_user)
            created_users.append(new_user)
        db.commit()
        for user in created_users:
            db.refresh(user)
        logger.info("Bulk user insert successful: %s", created_users)
        return [UserSchema.model_validate(u, from_attributes=True).model_dump() for u in created_users]
    except Exception as e:
        db.rollback()
        logger.error("Error during bulk user insert: %s", e)
        return None
    
"""
No3.4 Convert Everything to Async (Using SQLAlchemy 2.0)

Use asyncpg for PostgreSQL with async SQLAlchemy.
Modify queries to work with async sessions.
Ensure async-safe user retrieval and insertion.

"""

ssl_context = ssl.create_default_context()
ASYNC_DATABASE_URL = "postgresql+asyncpg://neondb_owner:EuZaD9pNP4sd@ep-billowing-hill-a5nnoisq.us-east-2.aws.neon.tech/neondb"
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True, connect_args={"ssl": ssl_context})
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

async def async_create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Async tables created.")


async def main():
    await async_create_tables()
    new_user = await async_create_user({"name": "AsyncUser", "email": "async@example.com"})
    print("Created user:", new_user)

async def async_create_user(user: dict):
    async with AsyncSessionLocal() as session:
        try:
            data = UserSchema(**user)
        except ValidationError as e:
            logger.error("Validation Error occurred: %s", e)
            return None
        new_user = User(name=data.name, email=data.email)
        session.add(new_user)
        try:
            await session.commit()
            await session.refresh(new_user)
            logger.info("User created asynchronously: %s", new_user)
            return new_user
        except Exception as e:
            await session.rollback()
            logger.error("Error creating user asynchronously: %s", e)
            return None
        
import asyncio




async def async_fetch_user(email: EmailStr):
    """Asynchronously retrieve a user by email."""
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select  
        result = await session.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        if not user:
            logger.info("User with email '%s' not found (async).", email)
            return None
        user_schema = UserSchema.model_validate(user, from_attributes=True)
        logger.info("Fetched user asynchronously: %s", user_schema.model_dump())
        return user_schema.model_dump()


if __name__ == "__main__" :
    user = { "name":"Tiger" , "email" :"tiger@gmail.com"}

    created_user = create_user(user)
    user_email = get_user_email("tiger@gmail.com")
    update_email = update_email("tiger@gmail.com" , "newtiger@gmail.com")
    print("Get user via email : ",user_email)
    delete_user("tiger@gmail.com")
    fetch_all_user()
    posts_to_create = [
        {"title": "First Post", "content": "This is the content of the first post."},
        {"title": "Second Post", "content": "This is the content of the second post."},
    ]
    
    created = create_muiti_post("newtiger@gmail.com", posts_to_create)

    bulk_users = [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": "bob@example.com"},
    ]
    print(create_bulk_users(bulk_users))
    print(fetch_user_with_posts("newtiger@gmail.com"))

    asyncio.run(main())
    asyncio.run(async_create_tables())
    asyncio.run(async_create_user({"name": "AsyncUser", "email": "async@example.com"}))
    asyncio.run(async_fetch_user("async@example.com"))  






   