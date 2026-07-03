from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
class URL(db.Model):
    __tablename__='urls'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    short_code=db.Column(db.String(10),unique=True, nullable=False)
    original_url=db.Column(db.String(255),nullable=False)
    status=db.Column(db.String(20),default='pending')

    def to_dict(self):
        return {
            'short_code': self.short_code,
            'original_url': self.original_url,
            'status': self.status
        }

