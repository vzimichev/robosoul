import numpy as np
import time

def interpreter(st,mtrx):
    '''gets input string and last value of servoin
        returns tuple of updated values servo
        if str='start' to initials
        if str='a=12 c=13' returns (12,90,13,90,90,90,1)
        if str='(12,90,13,90,90,90,1)' returns the same
        if str='(12,90,13,90)' returns the same
        if str='a=12 c=13 then e=50 then f=40 then start' compile the algorythm
        if str='a=5 c=3 then while a=6 b=2 and a=4 b=4' compile
        if str='a=5 c=3 then wait 3 then b=5' compile
    '''
    old=[*mtrx[-1]]
    if st=='start':
        mtrx = np.vstack([mtrx,[90,90,90,90,90,90,1]])
        return mtrx
    if st=='jackson':
        mtrx = interpreter('start then for 1 b=120 d=120 and a=120 c=120 and wait 1 and a=60 c=60 and b=60 d=60',mtrx)
        return mtrx
    if st=='walk':
        mtrx = interpreter('start then for 1 e=80 g=3 and f=80 b=70 a=70 and a=50 and d=70 f=90 e=90 c=70 and e=110 f=110 b=100 a=90 d=90 and c=100 e=120 b=120 g=1 and b=130 d=110 a=120 c=120 and c=140 e=90 f=90 g=3 and e=80 f=80 d=80 b=90 a=60 c=80',mtrx)
        return mtrx
    
    if st[0:4]=='wait':
        time.sleep(int(st[5]))
        mtrx=interpreter(st[11:],mtrx)
        return mtrx
    
    if st[0:5]=='while':
        for i in range(100):
            for j in st[6:].split(' and '):
                mtrx=interpreter(j,mtrx)
    
    if st[0:3]=='for':
        for l in range(int(st[4])): 
            for j in st[6:].split(' and '):
                mtrx=interpreter(j,mtrx)
        return mtrx
    
    try: #12,13,15
        q = list(int(i) for  i in st.split(','))
        for j in range(len(q),7): q.append(old[j])
        old = [q[k] for k in range(len(q))]
        mtrx = np.vstack([mtrx,old])
        return mtrx
    except ValueError:
        try: #a=12 b=13
            q = old
            tmp = list(st.split())
            for i in tmp: 
                q[ord(str(i).split('=')[0])-97]=int(str(i).split('=')[1])
            old = [q[k] for k in range(len(q))]
            mtrx = np.vstack([mtrx,old])
            return mtrx
        except IndexError: #a=12 b=13 then b=15
            for j in st.split(' then '):
                mtrx = interpreter(str(j),mtrx)
            return mtrx
        
if __name__ == "__main__":
    matrix = np.array([[90,90,90,90,90,90,1]])
    inp = input()
    matrix = interpreter(inp,[[*matrix[-1]]])
    np.savetxt('matrix.txt',matrix,fmt='%s',delimiter='\t')

