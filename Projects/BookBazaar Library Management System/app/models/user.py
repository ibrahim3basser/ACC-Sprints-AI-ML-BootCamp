class User:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    @staticmethod
    def from_db_row(row):
        return User(
            id=row['id'],
            username=row['username'],
            email=row['email']
        )

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }