from sqlalchemy import CHAR, Column, DateTime, Enum, ForeignKey, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Token(Base):
    """
    班级管理员token表
    """
    __tablename__ = 'token'

    token_id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    admin_name = Column(CHAR(10), nullable=False)
    token = Column(CHAR(50), nullable=False)
    comment = Column(TINYTEXT)

    def __repr__(self):
        return f"<Token {self.admin_name} {self.token}>"


class Counselor(Base):
    __tablename__ = 'counselor'

    counselor_id = Column(INTEGER(11), primary_key=True)
    counselor_name = Column(CHAR(20), nullable=False)
    token_id = Column(ForeignKey('token.token_id'), index=True)
    counselor_qq = Column(BIGINT(20))
    counselor_qq_name = Column(CHAR(20))

    token = relationship('Token')
    classes = relationship('Clas', back_populates='counselor')

    def __repr__(self):
        return f"<辅导员 {self.counselor_name}>"


class Clas(Base):
    """
    班级信息表
    """
    __tablename__ = 'class'

    class_id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    class_name = Column(CHAR(20), nullable=False)
    token_id = Column(ForeignKey('token.token_id'), nullable=False, index=True)
    counselor_id = Column(ForeignKey('counselor.counselor_id'), index=True)
    class_group_name = Column(CHAR(50), nullable=False)
    class_group_number = Column(BIGINT(20), nullable=False)
    not_prompt = Column(Enum('是', '否'), nullable=False, server_default=text("'否'"))
    cube_id = Column(INTEGER(11))

    counselor = relationship('Counselor', back_populates='classes', uselist=False)
    students = relationship('Student', back_populates='_class')
    token = relationship('Token')

    def __repr__(self):
        return f"<班级 {self.class_name} >"


class Finish(Base):
    """
    打卡完成记录表
    """
    __tablename__ = 'finish'

    finish_id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    class_id = Column(ForeignKey('class.class_id'), nullable=False, index=True)
    time = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    _class: Clas = relationship('Clas')

    def __repr__(self):
        return f"<打卡完成 {self.time.strftime('%Y-%m-%d')} {self._class.class_name} >"


class Student(Base):
    """
    学生信息表
    """
    __tablename__ = 'students'

    student_number = Column(INTEGER(11), primary_key=True)
    class_id = Column(ForeignKey('class.class_id'), index=True)
    student_name = Column(CHAR(10), nullable=False)
    student_qq = Column(BIGINT(20))
    cube_id = Column(INTEGER(11))

    _class = relationship('Clas', back_populates='students', uselist=False)

    def __repr__(self):
        return f"<Student {self.student_name}>"


class Log(Base):
    """
    日志表
    """
    __tablename__ = 'log'

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    receiver = Column(TINYTEXT, nullable=False)
    message = Column(Text, nullable=False)
    time = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    def __repr__(self):
        return f"<日志 {self.time} {self.receiver}>"


class AutoPunch(Base):
    """
    自动打卡表
    """
    __tablename__ = 'auto_punch'

    auto_punch_id = Column(INTEGER(11), primary_key=True)
    auto_punch_token = Column(CHAR(40), nullable=False, unique=True)
    comment = Column(CHAR(40), nullable=False)
    skip = Column(Enum('是', '否'), nullable=False, server_default=text("'否'"))


class CubePunchState(Base):
    """
    班级魔方考勤状态枚举
    """
    __tablename__ = 'cube_punch_state'

    cube_punch_state_id = Column(INTEGER(11), primary_key=True)
    cube_punch_state_name = Column(CHAR(10), nullable=False)


class CubeAutoPunch(Base):
    """
    班级魔方自动标记
    """
    __tablename__ = 'cube_auto_punch'

    id = Column(INTEGER(11), primary_key=True)
    student_number = Column(ForeignKey('students.student_number'), nullable=False, index=True)
    cube_punch_state_id = Column(ForeignKey('cube_punch_state.cube_punch_state_id'), nullable=False, index=True)
    skip = Column(Enum('是', '否'), nullable=False, server_default=text("'否'"))
    comment = Column(CHAR(10), nullable=False)

    cube_punch_state: CubePunchState = relationship('CubePunchState')
    student: Student = relationship('Student')
