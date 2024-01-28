from djitellopy import Tello
class track:
    
    def rotate(self, me, qudrant):
        # Primary
        if qudrant == 6:
            me.rotate_counter_clockwise(10)
        elif qudrant == 4:
            me.rotate_clockwise(10)
        elif qudrant == 8:
            me.move("up", 20)
        elif qudrant == 2:
            me.move("down", 20)
        
        # Seconday 
        if qudrant == 7:
            me.move("down", 20)
            me.rotate_clockwise(10)
            
        elif qudrant == 9:
            me.move("down", 20)
            me.rotate_counter_clockwise(10)
            
        elif qudrant == 1:
            me.move("up", 20)
            me.rotate_clockwise(10)
        
        elif qudrant == 3:
            me.move("up", 20)
            me.rotate_counter_clockwise(10)            
            
    def follow(self, me, qudrant):
        return 0