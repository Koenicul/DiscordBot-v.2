from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine('sqlite:///data.sqlite', echo=False)

class Player (Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hp = Column(Integer)
    maxhp = Column(Integer)
    level = Column(Integer)
    exp = Column(Integer)   
    gold = Column(Integer)
    attack = Column(Integer)
    defense = Column(Float)
    speed = Column(Integer)

    playerItems = relationship("PlayerItem", backref="player")
    equips = relationship("Equipment", backref="player")

    def __init__(self, id, name, hp, maxhp, level, exp, gold, attack, defense, speed):
        self.id = id
        self.name = name
        self.hp = hp
        self.maxhp = maxhp
        self.level = level
        self.exp = exp
        self.gold = gold
        self.attack = attack
        self.defense = defense
        self.speed = speed

class Item (Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    type = Column(String)
    effect = Column(Float)

    items = relationship("PlayerItem", backref="item")
    equips = relationship("Equipment", backref="item")

    def __init__(self, name, description, price, type, effect):
        self.name = name
        self.description = description
        self.price = price
        self.type = type
        self.effect = effect

class PlayerItem (Base):
    __tablename__ = 'playerItem'

    id = Column(Integer, primary_key=True)
    player_id  = Column(Integer, ForeignKey('player.id'))
    item_id = Column(Integer, ForeignKey('item.id'))

class Equipment (Base):
    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    item_id = Column(Integer, ForeignKey('item.id'))

Base.metadata.create_all(engine)