import time, cv2
from threading import Thread
class track:
    
    def rotate(me, qudrant):
        # Primary
        if qudrant == 6:
            me.rotate_clockwise(20)
        elif qudrant == 4:
            me.rotate_counter_clockwise(20)
        elif qudrant == 8:
            me.send_rc_control(0,0,40,0)
            time.sleep(1)
            me.send_rc_control(0,0,0,0)
        elif qudrant == 2:
            me.send_rc_control(0,0,-40,0)
            time.sleep(1)
            me.send_rc_control(0,0,0,0)
        
        # Seconday 
        if qudrant == 7:
            me.send_rc_control(0,0,40,0)
            time.sleep(1)
            me.send_rc_control(0,0,0,0)
            me.rotate_counter_clockwise(20)
            
        elif qudrant == 9:
            me.send_rc_control(0,0,40,0)
            time.sleep(1)
            me.send_rc_control(0,0,0,0)
            me.rotate_clockwise(20)
            
        elif qudrant == 1:
            me.send_rc_control(0,0,-40,0)
            time.sleep(1)
            me.send_rc_control(0,0,0,0)
            me.rotate_counter_clockwise(20)
        
        elif qudrant == 3:
            me.send_rc_control(0,0,-40,0)
            time.sleep(1)
            me.send_rc_control(0,0,0,0)
            me.rotate_clockwise(20)        
            
    def follow(me, qudrant):
        # Primary
        if qudrant == 6:
            me.send_rc_control(20,0,0,0)
            time.sleep(1)
            me.send_rc_control(0,0,0,0)
        elif qudrant == 4:
            me.send_rc_control(-20,0,0,0)
            time.sleep(1)
            me.send_rc_control(0,0,0,0)
        elif qudrant == 8:
            me.send_rc_control(0,0,20,0)
            time.sleep(1)
            me.send_rc_control(0,0,0,0)
        elif qudrant == 2:
            me.send_rc_control(0,0,-20,0)
            time.sleep(1)
            me.send_rc_control(0,0,0,0)
    
        # Secondary
        if qudrant == 7:
            me.send_rc_control(-20,0,-20,0)
            time.sleep(1)
            me.send_rc_control(0,0,0,0)
            
        elif qudrant == 9:
            me.send_rc_control(20,0,-20,0)
            time.sleep(1)
            me.send_rc_control(0,0,0,0)
            
        elif qudrant == 1:
            me.send_rc_control(-20,0,20,0)
            time.sleep(1)
            me.send_rc_control(0,0,0,0)
        
        elif qudrant == 3:
            me.send_rc_control(20,0,20,0)
            time.sleep(1)
            me.send_rc_control(0,0,0,0)
            
    def sling_shot(me, qudrant):
        keepRecording = True
        frame_read = me.get_frame_read()

        def videoRecorder():
            # create a VideoWrite object, recoring to ./video.avi
            # 创建一个VideoWrite对象，存储画面至./video.avi
            height, width, _ = frame_read.frame.shape
            video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

            while keepRecording:
                video.write(frame_read.frame)
                time.sleep(1 / 30)

            video.release()

        # we need to run the recorder in a seperate thread, otherwise blocking options
        #  would prevent frames from getting added to the video
        # 我们需要在另一个线程中记录画面视频文件，否则其他的阻塞操作会阻止画面记录
        recorder = Thread(target=videoRecorder)
        recorder.start()
        
        while me.get_height() < 200:
            me.send_rc_control(0,10,10,0)
            me.send_rc_control(0,0,0,0)
        while me.get_height() > 50:
            me.send_rc_control(0,-10,-10,0)
            
        keepRecording = False
        recorder.join()