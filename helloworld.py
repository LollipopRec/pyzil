import os

class Hello:
    def __init__(self):
        #self.hello = 'a'
        pass
    
    def load_model(self, hello):
        self.model = hello
        b=122333
        print(globals())
        

    def train(self):
        print('train:', self.model)
        print(locals())

#a = Hello()
#a.load_model('fadsf')
#a.train()
