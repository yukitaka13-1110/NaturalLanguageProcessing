# -*- coding: utf-8 -*-
from NLP import Mecab,Cabocha
from collections import Counter
import itertools
import math
import os
import re


class Report:

    def __init__(self,studentID,y,m,d,subject,score,c1,c2,c3):
        self._studentID = StudentID(studentID)
        self._date = Date(y,m,d)
        self._test = Test(subject,score)
        self._comment = Comment(c1,c2,c3)

    """
    studentID
    """
    def studentID(self):
        return self._studentID.studentID

    def is_studentID_equal(self,studentID):
        return self._studentID.is_equal(studentID)

    """
    date
    """
    def is_date_in_range(self,begin,end):
        return self._date.is_in_range(begin,end)

    """
    test
    """
    def is_subject_equal(self,subject):
        return self._test.is_subject_equal(subject)

    def is_score_in_range(self,low,high):
        return self._test.is_in_range(low,high)

    def score(self):
        return self._test.score

    def subject(self):
        return self._test.subject

    """
    comment
    """
    def comment(self,num):
        return self._comment.comment(num)

    def parse_comment(self,num):
        return self._comment.parse(num)

    def parse_comment_if(self,num,wc_str):
        return self._comment.parse_if(num,wc_str)


class Date:

    def __init__(self,y,m,d):
        self._y = int(y)
        self._m = int(m)
        self._d = int(d)

    def is_in_range(self,begin,end):
        yb,mb = begin.split('/')
        ye,me = end.split('/')
        mb,me = mb.zfill(2),me.zfill(2)
        begin,end = int(yb+mb),int(ye+me)
        return begin <= int(str(self._y)+str(self._m).zfill(2)) <= end

class StudentID:

    def __init__(self,studentID):
        self._studentID = studentID

    def _get_studentID(self):
        return self._studentID
    studentID = property(_get_studentID)

    def is_equal(self,name):
        return self._studentID == name

class Test:

    def __init__(self,subject,score):
        self._subject = subject
        self._score = int(score)

    def _get_score(self):
        return self._score
    score = property(_get_score)

    def _get_subject(self):
        return self._subject
    subject = property(_get_subject)

    def is_subject_equal(self,sub):
        return self._subject == sub

    def is_in_range(self,low,high):
        return int(low) <= self._score <= int(high)

class Comment:

    def __init__(self,c1,c2,c3):
        self._c1 = str(c1)
        self._c2 = str(c2)
        self._c3 = str(c3)

    def comment(self,num):
        if num == 1:
            return self._c1
        return self._c2 if num == 2 else self._c3

    def parse(self,num):
        mc = Mecab(self.comment(num))
        return mc.parse()

    def parse_if(self,num,wc_str):
        mc = Mecab(self.comment(num))
        return mc.parse_if(wc_str)


