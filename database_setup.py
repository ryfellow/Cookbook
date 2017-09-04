from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    difficulty = Column(String(250), nullable=False)
    category = Column(String(250), nullable=False)
    ing1Title = Column(String(250), nullable=False)
    ing1Amt = Column(String(12), nullable=False)
    ing1Unit = Column(String(5), nullable=False)
    ing2Title = Column(String(250), nullable=False)
    ing2Amt = Column(String(12), nullable=False)
    ing2Unit = Column(String(5), nullable=False)
    ing3Title = Column(String(250), nullable=True)
    ing3Amt = Column(String(12), nullable=True)
    ing3Unit = Column(String(5), nullable=True)
    ing4Title = Column(String(250), nullable=True)
    ing4Amt = Column(String(12), nullable=True)
    ing4Unit = Column(String(5), nullable=True)
    ing5Title = Column(String(250), nullable=True)
    ing5Amt = Column(String(12), nullable=True)
    ing5Unit = Column(String(5), nullable=True)
    ing6Title = Column(String(250), nullable=True)
    ing6Amt = Column(String(12), nullable=True)
    ing6Unit = Column(String(5), nullable=True)
    ing7Title = Column(String(250), nullable=True)
    ing7Amt = Column(String(12), nullable=True)
    ing7Unit = Column(String(5), nullable=True)
    ing8Title = Column(String(250), nullable=True)
    ing8Amt = Column(String(12), nullable=True)
    ing8Unit = Column(String(5), nullable=True)
    ing9Title = Column(String(250), nullable=True)
    ing9Amt = Column(String(12), nullable=True)
    ing9Unit = Column(String(5), nullable=True)
    ing10Title = Column(String(250), nullable=True)
    ing10Amt = Column(String(12), nullable=True)
    ing10Unit = Column(String(5), nullable=True)
    ing11Title = Column(String(250), nullable=True)
    ing11Amt = Column(String(12), nullable=True)
    ing11Unit = Column(String(5), nullable=True)
    ing12Title = Column(String(250), nullable=True)
    ing12Amt = Column(String(12), nullable=True)
    ing12Unit = Column(String(5), nullable=True)
    ing13Title = Column(String(250), nullable=True)
    ing13Amt = Column(String(12), nullable=True)
    ing13Unit = Column(String(5), nullable=True)
    ing14Title = Column(String(250), nullable=True)
    ing14Amt = Column(String(12), nullable=True)
    ing14Unit = Column(String(5), nullable=True)
    ing15Title = Column(String(250), nullable=True)
    ing15Amt = Column(String(12), nullable=True)
    ing15Unit = Column(String(5), nullable=True)
    step1 = Column(String(250), nullable=False)
    step2 = Column(String(250), nullable=False)
    step3 = Column(String(250), nullable=False)
    step4 = Column(String(250), nullable=True)
    step5 = Column(String(250), nullable=True)
    step6 = Column(String(250), nullable=True)
    step7 = Column(String(250), nullable=True)
    step8 = Column(String(250), nullable=True)
    step9 = Column(String(250), nullable=True)
    step10 = Column(String(250), nullable=True)
    step11 = Column(String(250), nullable=True)
    step12 = Column(String(250), nullable=True)
    step13 = Column(String(250), nullable=True)
    step14 = Column(String(250), nullable=True)
    step15 = Column(String(250), nullable=True)
    postDate = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        return {
            'title': self.title,
            'id': self.id,
            'description': self.description,
            'difficulty': self.difficulty,
            'category': self.category,
            'ing1Title': self.ing1Title,
            'ing1Amt': self.ing1Amt,
            'ing1Unit': self.ing1Unit,
            'ing2Title': self.ing2Title,
            'ing2Amt': self.ing2Amt,
            'ing2Unit': self.ing2Unit,
            'ing3Title': self.ing3Title,
            'ing3Amt': self.ing3Amt,
            'ing3Unit': self.ing3Unit,
            'ing4Title': self.ing4Title,
            'ing4Amt': self.ing4Amt,
            'ing4Unit': self.ing4Unit,
            'ing5Title': self.ing5Title,
            'ing5Amt': self.ing5Amt,
            'ing5Unit': self.ing5Unit,
            'ing6Title': self.ing6Title,
            'ing6Amt': self.ing6Amt,
            'ing6Unit': self.ing6Unit,
            'ing7Title': self.ing7Title,
            'ing7Amt': self.ing7Amt,
            'ing7Unit': self.ing7Unit,
            'ing8Title': self.ing8Title,
            'ing8Amt': self.ing8Amt,
            'ing8Unit': self.ing8Unit,
            'ing9Title': self.ing9Title,
            'ing9Amt': self.ing9Amt,
            'ing9Unit': self.ing9Unit,
            'ing10Title': self.ing10Title,
            'ing10Amt': self.ing10Amt,
            'ing10Unit': self.ing10Unit,
            'ing11Title': self.ing11Title,
            'ing11Amt': self.ing11Amt,
            'ing11Unit': self.ing11Unit,
            'ing12Title': self.ing12Title,
            'ing12Amt': self.ing12Amt,
            'ing12Unit': self.ing12Unit,
            'ing13Title': self.ing13Title, 
            'ing13Amt': self.ing13Amt,
            'ing13Unit': self.ing13Unit,
            'ing14Title': self.ing14Title,
            'ing14Amt': self.ing14Amt,
            'ing14Unit': self.ing14Unit,
            'ing15Title': self.ing15Title, 
            'ing15Amt': self.ing15Amt,
            'ing15Unit': self.ing15Unit,
            'step1': self.step1,
            'step2': self.step2,
            'step3': self.step3,
            'step4': self.step4,
            'step5': self.step5,
            'step6': self.step6,
            'step7': self.step7,
            'step8': self.step8,
            'step9': self.step9,
            'step10': self.step10,
            'step11': self.step11,
            'step12': self.step12,
            'step13': self.step13,
            'step14': self.step14,
            'step15': self.step15,
        }

engine = create_engine('sqlite:///cbdb.db')


Base.metadata.create_all(engine)