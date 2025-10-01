from app import app
from models import db, User_entry

admin_username = 'admin'
admin_password = 'pass@123'

with app.app_context():
    existing_user = User_entry.query.filter_by(username=admin_username).first()
    if existing_user:
        print("Admin user already exists!")
    else:
        admin_user = User_entry(
            id='admin_user',
            username=admin_username,
            password=admin_password,  # Plain text password
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user added successfully!")
