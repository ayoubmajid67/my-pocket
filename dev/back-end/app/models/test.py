from app.db import db

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Test {self.firstname} {self.lastname}>'