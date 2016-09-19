#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
# with_exapmle01.py
class Sample:
    def __enter__(self):
        print "In__enter__()"
        return "Foo"
    def __exit__(self,type,value,trace):
        print "In__exit__()"
def get_sample():
    return Sample()

with get_sample() as sample:
    print "sample:",sample
    
