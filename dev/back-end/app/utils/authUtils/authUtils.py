from app.db import db

from sqlalchemy import text
from app.utils.utile import check_hashed_password

def authenticate_user(email, password, table_name):
    query = text(f'SELECT * FROM {table_name} WHERE Email = :email')
    result = db.session.execute(query, {"email": email}).mappings().first()
    if result and check_hashed_password(password, result.get("Password")):
        return dict(result), table_name
    return None, None
