class Point:
    def __init__(self,x,y):
        self.__x=x
        self.__y=y

    def setX(self,x):
        self.__x=x
    def setY(self,y):
        self.__y=y

    def get(self):
        return self.__x , self.__y

    def move(self,dx,dy):
        self.__x += dx
        self.__y += dy

