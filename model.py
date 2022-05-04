from sqlalchemy import CHAR, Column, DateTime, Enum, ForeignKey, Table, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

t_class_info = Table(
    'class_info', metadata,
    Column('class_id', INTEGER(11), server_default=text("'0'")),
    Column('class_name', CHAR(20)),
    Column('token_id', INTEGER(11)),
    Column('token', CHAR(50))
)

t_student_info = Table(
    'student_info', metadata,
    Column('student_number', INTEGER(11)),
    Column('class_id', INTEGER(11)),
    Column('student_name', CHAR(10)),
    Column('student_qq', BIGINT(20)),
    Column('class_name', CHAR(20))
)


class Token(Base):
    __tablename__ = 'token'

    token_id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    admin_name = Column(CHAR(10), nullable=False)
    token = Column(CHAR(50), nullable=False)
    comment = Column(TINYTEXT)

    def __repr__(self):
        return f"<Token {self.admin_name} {self.token}>"


class Clas(Base):
    __tablename__ = 'class'

    class_id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    class_name = Column(CHAR(20), nullable=False)
    token_id = Column(ForeignKey('token.token_id'), nullable=False, index=True)
    class_group_name = Column(CHAR(50), nullable=False)
    not_prompt = Column(Enum('是', '否'), nullable=False, server_default=text("'否'"))

    token = relationship('Token')

    def __repr__(self):
        return f"<Class {self.class_name}>"


class Finish(Base):
    __tablename__ = 'finish'

    finish_id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    class_id = Column(ForeignKey('class.class_id'), nullable=False, index=True)
    time = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    _class: Clas = relationship('Clas')

    def __repr__(self):
        return f"<打卡完成 {self.time.strftime('%Y-%m-%d')} {self._class.class_name} >"


class Student(Base):
    __tablename__ = 'students'

    student_number = Column(INTEGER(11), primary_key=True)
    class_id = Column(ForeignKey('class.class_id'), index=True)
    student_name = Column(CHAR(10), nullable=False, server_default=text("''"))
    student_qq = Column(BIGINT(20))

    _class = relationship('Clas')

    def __repr__(self):
        return f"<Student {self.student_name}>"
