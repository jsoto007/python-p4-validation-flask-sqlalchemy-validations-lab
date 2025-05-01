from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates("name")
    def validates_name(self, key, name):
        if not name: 
            raise ValueError("Name cannot be empty.")
        
        found_name = db.session.query(Author.id).filter_by(name = name).first()

        if found_name is not None: 
            raise ValueError("This name already exits, Please pick a new one ")
        return name
        
    @validates("phone_number")
    def validates_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit(): 
            raise ValueError("The phone number must be 10 digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    
    @validates('content', 'summary')
    def validate_length(self, key, string):
        if( key == 'content'):
            if len(string) < 250:
                raise ValueError("Post content must be greater than or equal 250 characters long.")
        if( key == 'summary'):
            if len(string) > 250:
                raise ValueError("Post summary must be less than or equal to 250 characters long.")
        return string
    
    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction': 
            raise ValueError("Category must be Fiction or Non-Fiction.")
        
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
