from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, ForeignKey
import enum

db = SQLAlchemy()

# Enum para los tipos de media
class Mediatype(enum.Enum):
    video = 'video'
    imagen = 'imagen'

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), unique=True)
    firstname: Mapped[str] = mapped_column(String(120))
    lastname: Mapped[str] = mapped_column(String(120))
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # relations
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    following = relationship('Follower', foreign_keys='Follower.user_from_id', back_populates='follower')
    followers = relationship('Follower', foreign_keys='Follower.user_to_id', back_populates='followed')

    # serialize
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    
    # relation
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(120), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    # relations
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Enum] = mapped_column(Enum(Mediatype), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    # relation
    post = relationship('Post', back_populates='media')

class Follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True, nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True, nullable=False)

    # relations
    follower = relationship('User', foreign_keys=[user_from_id], back_populates='following')
    followed = relationship('User', foreign_keys=[user_to_id], back_populates='followers')
