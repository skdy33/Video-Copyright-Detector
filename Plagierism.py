# Input data의 파일형식에 따라 FPS가 안맞을수도 있다.
# 안 맞는 경우 파일형식의(예.avi) Header의 문제인데, 실험 때는 그냥 되는 파일형식으로 convert해서 사용하자.

class plagierism:
    """
    원본 영상을 받는다.
    input : 
    self = str of the video
    out = str of the name of the output video, including 
    """
    codec = {'mp4':'H264','avi':'XVID'}
    
    def WriterChecker(self):
        if (self.cap.isOpened()!=1):
            print("Refresh opener")
            return 0
        if (self.out.isOpened()!=1):
            print("Refresh writer")
            return 0
        return 1
    
        
    
    def __init__(self,video,out):

        self._fileName = video
        self._outFile = out
        self.cap = cv2.VideoCapture(video)
        print(self.cap.isOpened())
        #Checking
        if (cap.isOpened()==False):
            print ("Problem reading a video file")
            return 
        
        #the property of the video
        self.width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.FPS = cap.get(cv2.CAP_PROP_FPS)

            
        # For later issue. If we wanna keep our output w/ a same extension
        out_file, out_extension = out.split('.')
        dec = self.codec.get(out_extension,1)

        if dec == 1:
            return
        print (dec)
        try:    
            fourcc = cv2.VideoWriter_fourcc(*'XVID') # 일단 output은 무조건 .avi
        except:
            print ("I said write the name of the output including extension")
            return 
        # Output은 무조건 .avi
        self.out = cv2.VideoWriter(out_file+'_m.avi',fourcc,self.FPS,(640,480))
        if (self.out.isOpened()==False):
            print ("There might be a existing file that has your target name.")
            return 
        
    """
    writer class
    name : str of the name of the file that'll be the modified one.
    """
    def writer(self,name):
        return
        
    """
    영상의 절단 후 재배포
    """    
    def Cutting(self):
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret == True:
                frame = frame[int(height/8):int(height/8*7),int(width/8):int(width/8*7)]
                frame = cv2.resize(frame,(640,480))
                self.out.write(frame)
                cv2.imshow('frame',frame)
            else:
                break
                
        cap.release()
        out.release()
        cv2.destroyAllWindows()
            
    """
    영상 아래에 임의의 영상 혹은 사진 끼워넣기
    data : String of background에 깔릴 영상(or 사진) location
    """
    def Padding(self,data):
        back = cv2.VideoCapture(data)
        
        #checking
        if (back.isOpened()!=True):
            print ("Prob opening background video or image")
            return
        
        BackWidth = int(back.get(cv2.CAP_PROP_FRAME_WIDTH))
        BackHeight = int(back.get(cv2.CAP_PROP_FRAME_HEIGHT))
        BackFPS = back.get(cv2.CAP_PROP_FPS)
        
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret == True:
                # 여기서 back frame을 계속 읽어줘야해. 나중에 regarding complexity 우리가 picture 의 경우는 fixation 할 수 있지만
                # 지금은 일단 편의를 위해 닫히면 계속 새로 open 하도록 할게
                if back.isOpened() == True:
                    BackRet, BackFrame = back.read()
                    if BackRet == 1:
                        pass
                    else :
                        back.release()
                        back = cv2.VideoCapture(data)
                        BackRet, BackFrame = back.read()
                else :
                    back.release()
                    back = cv2.VideoCapture(data)
                    BackRet, BackFrame = back.read()

                        
                # padding은 일단 1/2 사이즈로 줄여서 넣어볼게.
                frame = cv2.resize(frame,(int(BackWidth/2),int(BackHeight/2)))
                BackFrame[int(BackHeight/4):int(BackHeight/4*3),int(BackWidth/4):int(BackWidth/4*3)] = frame
                BackFrame = cv2.resize(BackFrame,(640,480))
                self.out.write(BackFrame)
                cv2.imshow('frame',BackFrame)
            else:
                cap.release()
                out.release()
                back.release()
                break
                
        cap.release()
        out.release()
        back.release()
        cv2.destroyAllWindows()
        
        
    
    """
    영상 일부분만 배포
    s = starting point. 몇 초 후 부터 녹화할것인가. 초 단위
    d = duration. 몇 분을 녹화할 것인가. 초 단위
    """
    def Slicing(self,s,d):
        # sec to frame
        start = int(s * self.FPS)
        fin = int(d * self.FPS)
        
        #Checking before writing
        if (WriterChecker()==0):
            return
        
        #Frame counter
        cnt = 0
        
        #Write
        while(self.cap.isOpened()):
            if (cnt < s):
                continue
            if (cnt > d):
                break
                
            ret, frame = self.cap.read()
            if ret == True:
                cnt +=1
                frame = cv2.resize(frame,(640,480))
                self.out.write(frame)
                cv2.imshow('frame',frame)
            else:
                break
                
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
        return

    """
    영상 화질 낮추기
    일단 (640,480) 으로 나오는 걸로 한다.
    이것보다 더 극단적으로 낮추고 싶으면 writer 정의할 때 작게해야 하는데,
    이건 writer function 정의하고 그거 이용하면 쉬울거다.
    그러면 writer refresh func 에는 해상도 default var 로 주면 될 것 같다.
    """
    def Dequalify(self):
        
        #Checking before writing
        if (WriterChecker()==0):
            return
        
        #write
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret == True:
                frame = cv2.resize(frame,(640,480))
                self.out.write(frame)
                cv2.imshow('frame',frame)
            else:
                break

        return

    """
    좌우 대칭
    flip
    """
    def Flip(self):
        #Checking before writing
        if (WriterChecker()==0):
            return
        
        #write
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret == True:
                frame = cv2.resize(frame,(640,480))
                frame = cv2.flip(frame)
                self.out.write(frame)
                cv2.imshow('frame',frame)
            else:
                break

        return
    
    """
    속도 빠르게 만들기.
    x : times faster(slower). 
    이것도 writer 재정의야.
    일단은 hard coding,
    refreshing writing func 만들면 그걸로 대신 사용.
    """
    def SpeedUp(self,x):
        
        # self.out 재정의
        if (self.out.isOpened()):
            self.out.release()
            
        out_file = self._outFile.split('.')[0]
        
        #FPS 재정의
        FPS = self.FPS * x
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID') # 일단 output은 무조건 .avi
        self.out = cv2.VideoWriter(out_file+'_m.avi',fourcc,FPS,(640,480))
        
        #check
        if (WriterChecker()==0):
            return 0
        
        #write
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret == True:
                frame = cv2.resize(frame,(640,480))
                frame = cv2.flip(frame)
                self.out.write(frame)
                cv2.imshow('frame',frame)
            else:
                break
        
        
        
    
    """
    음성 바꾸기
    opencv로 음성 안들어옴.
    """
    def AudioChg(self):
        return    
    
    """
    조도 변화
    a = param
    b = bias
    """
    def Jodo(self,a=2,b=3):
        #Checking before writing
        if (WriterChecker()==0):
            return
        
        #write
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret == True:
                frame = cv2.resize(frame,(640,480))
                frame = frame*a + b
                self.out.write(frame)
                cv2.imshow('frame',frame)
            else:
                break

        return
