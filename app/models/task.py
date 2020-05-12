from . import db
from sqlalchemy.event import listen

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.DateTime(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())

    @classmethod
    def new(cls, title, description, deadline):
        return Task(title=title, description=description, deadline= deadline)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def __str__(self):
        return self.title

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline
        }

def insert_tasks(*args, **kwargs):
    db.session.add(
        Task(title='Title 1', description='Description',
            deadline='2020-05-08 12:00:00')
    )
    db.session.add(
        Task(title='Title 2', description='Description',
            deadline='2020-05-08 12:00:00')
    )
    db.session.commit()

listen(Task.__table__, 'after_create', insert_tasks)