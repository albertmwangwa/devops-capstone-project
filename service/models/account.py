"""Account Model"""

from datetime import datetime

from service import db


class Account(db.Model):
    """Account class"""

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone_number = db.Column(db.String(32))
    address = db.Column(db.String(200))  # Added this field
    disabled = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Account {self.name}>"

    def serialize(self):
        """Serialize to dict"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "disabled": self.disabled,
            "date_joined": self.date_joined.isoformat() if self.date_joined else None,
        }

    def deserialize(self, data):
        """Deserialize from dict"""
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.phone_number = data.get("phone_number")
            self.address = data.get("address")  # Handle address field
            self.disabled = data.get("disabled", False)
        except KeyError as error:
            raise ValueError(f"Missing required field: {error}")

    @classmethod
    def all(cls):
        """Return all accounts"""
        return cls.query.all()

    @classmethod
    def find(cls, account_id):
        """Find account by id"""
        return cls.query.get(account_id)

    def update(self):
        """Update account in database"""
        db.session.commit()

    def delete(self):
        """Delete account from database"""
        db.session.delete(self)
        db.session.commit()
