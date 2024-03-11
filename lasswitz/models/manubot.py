from __future__ import annotations
from typing import List

from sqlalchemy import (
    Table,
    ForeignKey,
    Column,
    Index,
    Integer,
    String,
    Text,
    DateTime,
    Uuid
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

import uuid

from .meta import Base

authorship_table = Table(
    "authorship_table",
    Base.metadata,
    Column("manuscript_id", ForeignKey("manuscript.id")),
    Column("creator_id", ForeignKey("user.id")),
)


class Manuscript(Base):
    __tablename__ = 'manuscript'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=lambda: uuid.uuid4().hex)
    zotid = Column(Integer, nullable=True)
    title = Column(Text)
    abstract = Column(Text, nullable=True)
    body = Column(Text, nullable=True)
    revision = Column(Integer)
    tag = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
    date_created = Column(DateTime)
    date_modified = Column(DateTime)
    language = Column(Text)
    creators: Mapped[List[AcademicPerson]] = relationship(back_populates="manuscripts", secondary=authorship_table)
    # links: Mapped[List["Relationship"]] = relationship(back_populates="manuscript")


class AcademicPerson(Base):
    __tablename__ = 'user'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=lambda: uuid.uuid4().hex)
    username = Column(String(length=100))
    displayname = Column(String(length=1024))
    givenname = Column(String(length=1024))
    familyname = Column(String(length=1024))
    initials = Column(String(length=100))
    mail = Column(String(length=200))
    telephone = Column(String(length=50))
    organization = Column(String(length=1024))
    organizationunit = Column(String(length=1024))
    preferredlanguage = Column(String(length=50))
    website = Column(String(length=2048))
    manuscripts: Mapped[List[Manuscript]] = relationship(secondary=authorship_table, back_populates='creators')


#    dn: cn=Barbara Jensen,ou=Product Development,dc=siroe,dc=com
#    objectClass: top
#    objectClass: person
#    objectClass: organizationalPerson
#    objectClass: inetOrgPerson
#    cn: Barbara Jensen
#    cn: Babs Jensen
#    displayName: Babs Jensen
#    sn: Jensen
#    givenName: Barbara
#    initials: BJJ
#    title: manager, product development
#    uid: bjensen
#    mail: bjensen@siroe.com
#    telephoneNumber: +1 408 555 1862
#    facsimileTelephoneNumber: +1 408 555 1992
#    mobile: +1 408 555 1941
#    roomNumber: 0209
#    carLicense: 6ABC246
#    o: Siroe
#    ou: Product Development
#    departmentNumber: 2604
#    employeeNumber: 42
#    employeeType: full time
#    preferredLanguage: fr, en-gb;q=0.8, en;q=0.7
#    labeledURI: http://www.siroe.com/users/bjensen My Home Page


# class Relationship(Base):
#     __tablename__ = 'links'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     kind = Column(String(length=100))
#     manuscript_id: Mapped[Uuid] = mapped_column(ForeignKey("manuscripts.id"))
#     manuscript: Mapped[Manuscript] = relationship(back_populates='links')
#     target: Mapped[Manuscript] = relationship(back_populates="relationship")