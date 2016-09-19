#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
# with_exapmle01.py
class Sample:
    def __enter__(self):
        return self

    def __exit__(self,type,value,trace):
        print "type:",type
        print "value:",value
        print "trace:",trace

    def do_something(self):
        bar = 1/0
        return bar + 10

with Sample() as sample:
    sample.do_something()
    
