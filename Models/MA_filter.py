class coordinate:
    original=[0,0]
    def __init__(self,l:list[int]): 
            self.original=l
    def distance(self,l1,l2):
        return int(((l1[0]-l2[0])**2+(l1[1]-l2[1])**2)*1/2)
    def c(self,l):
        if self.original==[0,0]:
             self.original=l
        elif self.distance(self.original,l)<10000:
            self.original=[int((l[0])),int((l[1]))]
        return self.original
    def ema_filter(self,new_value, prev_ema, alpha):
        if prev_ema is None:
            return new_value
        return alpha * new_value + (1 - alpha) * prev_ema