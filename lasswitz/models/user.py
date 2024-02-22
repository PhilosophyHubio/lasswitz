from sqlalchemy import (
    Column,
    Index,
    Integer,
    String,
    Text,
    Uuid,
)

from .meta import Base


class AcademicPerson(Base):
    __tablename__ = 'user'
    id = Column(Uuid, primary_key=True)
    username = Column(String(length=100))
    displayname = Column(String(length=1024))
    givenname = Column(String(length=1024))
    familyname = Column(String(length=1024))
    initials = Column(String(length=100))
    mail = Column(String(length=100))
    telephone = Column(String(length=50))
    organization = Column(String(length=1024))
    organizationunit = Column(String(length=1024))
    preferredlanguage = Column(String(length=50))
    website = Column(String(length=2048))


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