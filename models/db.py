from __future__ import annotations
from .base import BaseDbModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, DateTime, Boolean, ForeignKey
import datetime

class Group(BaseDbModel):
    __tablename__ = "groups"
    
    group_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    
    messages: Mapped[list[Message]] = relationship("Message", back_populates="group")
    participants: Mapped[list[Participant]] = relationship("Participant", back_populates="group")
    topics: Mapped[list[Topic]] = relationship("Topic", back_populates="group")

class Participant(BaseDbModel):
    __tablename__ = "participants"
    
    group_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("groups.group_id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    is_bot: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_premium: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    group: Mapped[Group] = relationship("Group", back_populates="participants")
    messages: Mapped[list[Message]] = relationship("Message", back_populates="participant")

class Topic(BaseDbModel):
    __tablename__ = "topics"
    
    group_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("groups.group_id"), primary_key=True)
    topic_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    
    group: Mapped[Group] = relationship("Group", back_populates="topics")
    messages: Mapped[list[Message]] = relationship("Message", back_populates="topic")

class Message(BaseDbModel):
    __tablename__ = "messages"
    
    dt: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    group_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("groups.group_id"), nullable=False)
    message_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    message_text: Mapped[str] = mapped_column(String, nullable=False)
    is_forwarded: Mapped[bool] = mapped_column(Boolean, nullable=False)
    reply_to: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    topic_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    
    group: Mapped[Group] = relationship("Group", back_populates="messages")
    participant: Mapped[Participant] = relationship("Participant", 
                                                   foreign_keys=[group_id, user_id],
                                                   primaryjoin="and_(Message.group_id == Participant.group_id, "
                                                              "Message.user_id == Participant.user_id)",
                                                   back_populates="messages")
    topic: Mapped[Topic | None] = relationship("Topic", 
                                              foreign_keys=[group_id, topic_id],
                                              primaryjoin="and_(Message.group_id == Topic.group_id, "
                                                         "Message.topic_id == Topic.topic_id)",
                                              back_populates="messages")
