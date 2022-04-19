class Snake:
    def __init__(self, length, x):
       self.body = []
       for i in range(length):
            self.body.append([i+2 , 5])
       self.direct = 0
       self.bound = x

    def move(self):
        self.body.pop()
        self.eat()

    def eat(self):
        if self.direct == 0:
            if self.body[0][0] == 0:
                self.body.insert(0, [self.bound, self.body[0][1]])
            else:
                self.body.insert(0, [self.body[0][0] - 1, self.body[0][1]])
        elif self.direct == 1:
            if self.body[0][0] == self.bound:
                self.body.insert(0, [0, self.body[0][1]])
            else:
                self.body.insert(0, [self.body[0][0] + 1, self.body[0][1]])
        elif self.direct == 2:
            if self.body[0][1] == 0:
                self.body.insert(0, [self.body[0][0], self.bound])
            else:
                self.body.insert(0, [self.body[0][0], self.body[0][1] - 1])
        elif self.direct == 3:
            if self.body[0][1] == self.bound:
                self.body.insert(0, [self.body[0][0], 0])
            else:
                self.body.insert(0, [self.body[0][0], self.body[0][1] + 1])

    def change_direct(self, direct):
        if direct == 0 and self.direct != 1:
            self.direct = 0
        elif direct == 1 and self.direct != 0:
            self.direct = 1
        elif direct == 2 and self.direct != 3:
            self.direct = 2
        elif direct == 3 and self.direct != 2:
            self.direct = 3