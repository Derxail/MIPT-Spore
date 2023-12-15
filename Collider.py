class Box_Collider():
    def __init__(self,x,y,height,width,rotation):
        self.x=x
        self.y=y
        self.height = height
        self.width=width
        self.rotation = rotation

    def hit(self, other_collider):
        type_other_collider = isinstance(other_collider, Box_Collider)


class Circle_Collider():
    def __init__(self,x,y,radius):
        self.x=x
        self.y=y
        self.radius = radius

    def hit(self, other_collider):
        if isinstance(other_collider, Circle_Collider):
            if ((Circle_Collider.x-self.x)**2 + (Circle_Collider.y-self.y)**2)**(0.5) < Circle_Collider.r-self.r:
                return True
            else:
                return False
        else:
            pass
