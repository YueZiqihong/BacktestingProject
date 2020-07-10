# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 00:03:33 2020

@author: lenovo
"""

from .test1 import Testobj1
from . import test1

class Testobj2:
     def __init__(self):
        self.testval2 = 13
#        self.testval3 = Testobj1().testval1
        self.testval3 = test1.Testobj1().testval1
        
    


