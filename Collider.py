import math

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D) #спизжено с гитхаба

class Box_Collider():
    def __init__(self,x,y,height,width,rotation):
        self.x=x
        self.y=y
        self.height = height
        self.width=width
        self.rotation = rotation

    def get_vertex(self):
        x1,y1=self.x + self.width*math.cos(self.rotation),self.y + self.length*math.cos(self.rotation)
        x2, y2 = self.x - self.width * math.cos(self.rotation), self.y + self.length * math.cos(self.rotation)
        x3, y3 = self.x + self.width * math.cos(self.rotation), self.y - self.length * math.cos(self.rotation)
        x4, y4 = self.x - self.width * math.cos(self.rotation), self.y - self.length * math.cos(self.rotation)
        return((x1,y1),(x2,y2),(x3,y3),(x4,y4))

    def hit(self, other_collider):
        if isinstance(other_collider, Box_Collider):
            vertex_other_collider = other_collider.get_vertex()
            vertex_self = self.get_vertex()
            if ((self.x - other_collider.x)**2 + (self.y - other_collider.y)**2) ** 0.5 > max(self.width, self.height, other_collider.width, other_collider.height)*2:
                return False
            else:
                for t1 in range(3):
                    for t11 in  range(t1,3):
                        for t2 in range(3):
                            for t22 in range(t2, 3):
                                if intersect(t1,t11,t2,t22):
                                    return True
            return False

        else:
            pass


            '''relative_rotation = self.rotation - other_collider.rotation #В СО связанной со 2 коробкой
            relative_x = self.x - other_collider.x
            relative_y = self.y - other_collider.y

            x1, y1 = relative_x + self.width * math.cos(relative_rotation), relative_y+ self.length * math.cos(relative_rotation)
            x2, y2 = relative_x - self.width * math.cos(relative_rotation), relative_y + self.length * math.cos(relative_rotation)
            x3, y3 = relative_x + self.width * math.cos(relative_rotation), relative_y - self.length * math.cos(relative_rotation)
            x4, y4 = relative_x - self.width * math.cos(relative_rotation), relative_y - self.length * math.cos(relative_rotation)
            if min_vertex[0] <= other_collider.width or min_vertex[1] <= other_collider.height:
                return True
            else:
                False'''

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
