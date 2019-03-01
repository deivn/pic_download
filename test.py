#! /usr/bin/env python  
# -*- coding:utf-8 -*-  
import re

string = """

            Las Vegas,
            NV
            89118
          
"""

string = string.strip().replace("\n", "").split(",")
print(string[1].split())