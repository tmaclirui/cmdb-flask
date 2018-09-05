#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
class User(object):
    eye = 2
    foot = 2
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def get_name(self):
        return self.name
    def set_name(self,name):
        self.name = name
    def get_eye(self):
        return self.eye
    @classmethod
    def get_User_eye(cls):
        return cls.eye
    @staticmethod
    def get_User_foot():
        return User.foot
class Three(User):
    eye = 3
    def __init__(self,name,age):
        super(Three,self).__init__(name,age)
        self.sex = 1
    def get_name(self):
        print '三木:' + self.name         
if __name__ == "__main__":
    lirui = User('lirui',24)
    print lirui.get_name()
    lirui.set_name(name='tmac')
    lirui.set_name('Tracy')
    print lirui.get_name()
    print lirui.get_User_eye()
    print lirui.get_eye()
    print lirui.get_User_foot()
    print User.get_User_foot()
    t = Three('1',1)
    print t.get_name()
    t.set_name('aaaa')
    print t.get_name() 
