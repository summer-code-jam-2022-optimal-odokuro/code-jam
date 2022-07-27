import random
def mapgen():
    map=[]
    for h in range(0,25):
        if h==6 or h==7 or h==8 or h==11 or h==12 or h==13 or h==16 or h==17 or h==18:
            a=0
            mapvertical=[]
            while a<80:
                maphorizontal=[]
                lowlim=random.randint(1,10)
                highlim=random.randint(70,78)
                b=0
                while b<80:
                    if a==0 or a==79:
                        if b==38 or b==39 or b==40 or b==41:
                            maphorizontal.append(' ')
                        else:
                            maphorizontal.append(('#'))
                    elif a==38 or a==39 or a==40 or a==41:
                        if b==0 or b==79:
                            maphorizontal.append(' ')
                        else:
                            maphorizontal.append((' '))
                    else:
                        if b < lowlim or b >highlim:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append((' '))
                    b+=1

                mapvertical.append(maphorizontal)
                a+=1


            g=random.randint(25,30)
            while g>0:
                rocksize=random.randint(5,7)
                rocklocx=random.randint(0,70)
                rocklocy=random.randint(0,70)
                while rocklocy<3 and rocklocx<41 and rocklocx>32 or rocklocy>70 and rocklocx<41 and rocklocx>32 or rocklocx>65 and rocklocy<41 and rocklocy>32 or rocklocx>65 and rocklocy<41 and rocklocy>32:
                    rocklocx=random.randint(0,70)
                    rocklocy=random.randint(0,70)
                for v in range(0, rocksize):
                    for t in range(0, random.randint((rocksize-2),(rocksize+2))):
                        (mapvertical[rocklocy+v])[rocklocx+t]='#'
                g-=1

            map.append(mapvertical)
        if h==0:
            a=0
            mapvertical=[]
            while a<80:
                maphorizontal=[]
                lowlim=random.randint(1,10)
                highlim=random.randint(70,78)
                b=0
                while b<80:
                    if a==79:
                        if b==38 or b==39 or b==40 or b==41:
                            maphorizontal.append(' ')
                        else:
                            maphorizontal.append(('#'))
                    elif a==38 or a==39 or a==40 or a==41:
                        if b==79:
                            maphorizontal.append(' ')
                        elif b==0:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append((' '))
                    elif a==0:
                        maphorizontal.append('#')
                    else:
                        if b < lowlim or b >highlim:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append((' '))
                    b+=1

                mapvertical.append(maphorizontal)
                a+=1


            g=random.randint(25,30)
            while g>0:
                rocksize=random.randint(5,7)
                rocklocx=random.randint(0,70)
                rocklocy=random.randint(0,70)
                while rocklocy<3 and rocklocx<41 and rocklocx>32 or rocklocy>70 and rocklocx<41 and rocklocx>32 or rocklocx>65 and rocklocy<41 and rocklocy>32 or rocklocx>65 and rocklocy<41 and rocklocy>32:
                    rocklocx=random.randint(0,70)
                    rocklocy=random.randint(0,70)
                for v in range(0, rocksize):
                    for t in range(0, random.randint((rocksize-2),(rocksize+2))):
                        (mapvertical[rocklocy+v])[rocklocx+t]='#'
                g-=1

            map.append(mapvertical)
        if h==4:
            a=0
            mapvertical=[]
            while a<80:
                maphorizontal=[]
                lowlim=random.randint(1,10)
                highlim=random.randint(70,78)
                b=0
                while b<80:
                    if a==79:
                        if b==38 or b==39 or b==40 or b==41:
                            maphorizontal.append(' ')
                        else:
                            maphorizontal.append(('#'))
                    elif a==38 or a==39 or a==40 or a==41:
                        if b==0:
                            maphorizontal.append(' ')
                        elif b==79:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append((' '))
                    elif a==0:
                        maphorizontal.append('#')
                    else:
                        if b < lowlim or b >highlim:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append((' '))
                    b+=1

                mapvertical.append(maphorizontal)
                a+=1


            g=random.randint(25,30)
            while g>0:
                rocksize=random.randint(5,7)
                rocklocx=random.randint(0,70)
                rocklocy=random.randint(0,70)
                while rocklocy<3 and rocklocx<41 and rocklocx>32 or rocklocy>70 and rocklocx<41 and rocklocx>32 or rocklocx>65 and rocklocy<41 and rocklocy>32 or rocklocx>65 and rocklocy<41 and rocklocy>32:
                    rocklocx=random.randint(0,70)
                    rocklocy=random.randint(0,70)
                for v in range(0, rocksize):
                    for t in range(0, random.randint((rocksize-2),(rocksize+2))):
                        (mapvertical[rocklocy+v])[rocklocx+t]='#'
                g-=1

            map.append(mapvertical)
        if h==20:
            a=0
            mapvertical=[]
            while a<80:
                maphorizontal=[]
                lowlim=random.randint(1,10)
                highlim=random.randint(70,78)
                b=0
                while b<80:
                    if a==0:
                        if b==38 or b==39 or b==40 or b==41:
                            maphorizontal.append(' ')
                        else:
                            maphorizontal.append('#')
                    elif a==38 or a==39 or a==40 or a==41:
                        if b==79:
                            maphorizontal.append(' ')
                        elif b==0:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append(' ')
                    elif a==79:
                        maphorizontal.append('#')
                    else:
                        if b < lowlim or b >highlim:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append(' ')
                    b+=1

                mapvertical.append(maphorizontal)
                a+=1


            g=random.randint(25,30)
            while g>0:
                rocksize=random.randint(5,7)
                rocklocx=random.randint(0,70)
                rocklocy=random.randint(0,70)
                while rocklocy<3 and rocklocx<41 and rocklocx>32 or rocklocy>70 and rocklocx<41 and rocklocx>32 or rocklocx>65 and rocklocy<41 and rocklocy>32 or rocklocx>65 and rocklocy<41 and rocklocy>32:
                    rocklocx=random.randint(0,70)
                    rocklocy=random.randint(0,70)
                for v in range(0, rocksize):
                    for t in range(0, random.randint((rocksize-2),(rocksize+2))):
                        (mapvertical[rocklocy+v])[rocklocx+t]='#'
                g-=1

            map.append(mapvertical)
        if h==24:
            a=0
            mapvertical=[]
            while a<80:
                maphorizontal=[]
                lowlim=random.randint(1,10)
                highlim=random.randint(70,78)
                b=0
                while b<80:
                    if a==0:
                        if b==38 or b==39 or b==40 or b==41:
                            maphorizontal.append(' ')
                        else:
                            maphorizontal.append('#')

                    elif a==38 or a==39 or a==40 or a==41:
                        if b==0:
                            maphorizontal.append(' ')
                        elif b==79:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append(' ')
                    elif a ==79:
                        maphorizontal.append('#')

                    else:
                        if b < lowlim or b >highlim:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append(' ')

                    b+=1

                mapvertical.append(maphorizontal)
                a+=1


            g=random.randint(25,30)
            while g>0:
                rocksize=random.randint(5,7)
                rocklocx=random.randint(0,70)
                rocklocy=random.randint(0,70)
                while rocklocy<3 and rocklocx<41 and rocklocx>32 or rocklocy>70 and rocklocx<41 and rocklocx>32 or rocklocx>65 and rocklocy<41 and rocklocy>32 or rocklocx>65 and rocklocy<41 and rocklocy>32:
                    rocklocx=random.randint(0,70)
                    rocklocy=random.randint(0,70)
                for v in range(0, rocksize):
                    for t in range(0, random.randint((rocksize-2),(rocksize+2))):
                        (mapvertical[rocklocy+v])[rocklocx+t]='#'
                g-=1

            map.append(mapvertical)
        if h==1 or h==2 or h==3:
            a=0
            mapvertical=[]
            while a<80:
                maphorizontal=[]
                lowlim=random.randint(1,10)
                highlim=random.randint(70,78)
                b=0
                while b<80:
                    if a==79:
                        if b==38 or b==39 or b==40 or b==41:
                            maphorizontal.append(' ')
                        else:
                            maphorizontal.append('#')
                    elif a==38 or a==39 or a==40 or a==41:
                        if b==79 or b==0:
                            maphorizontal.append(' ')
                        else:
                            maphorizontal.append(' ')
                    elif a==0:
                        maphorizontal.append('#')
                    else:
                        if b < lowlim or b >highlim:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append(' ')
                    b+=1

                mapvertical.append(maphorizontal)
                a+=1


            g=random.randint(25,30)
            while g>0:
                rocksize=random.randint(5,7)
                rocklocx=random.randint(0,70)
                rocklocy=random.randint(0,70)
                while rocklocy<3 and rocklocx<41 and rocklocx>32 or rocklocy>70 and rocklocx<41 and rocklocx>32 or rocklocx>65 and rocklocy<41 and rocklocy>32 or rocklocx>65 and rocklocy<41 and rocklocy>32:
                    rocklocx=random.randint(0,70)
                    rocklocy=random.randint(0,70)
                for v in range(0, rocksize):
                    for t in range(0, random.randint((rocksize-2),(rocksize+2))):
                        (mapvertical[rocklocy+v])[rocklocx+t]='#'
                g-=1

            map.append(mapvertical)
        if h==21 or h==22 or h==23:
            a=0
            mapvertical=[]
            while a<80:
                maphorizontal=[]
                lowlim=random.randint(1,10)
                highlim=random.randint(70,78)
                b=0
                while b<80:
                    if a==0:
                        if b==38 or b==39 or b==40 or b==41:
                            maphorizontal.append(' ')
                        else:
                            maphorizontal.append('#')
                    elif a==38 or a==39 or a==40 or a==41:
                        if b==79 or b==0:
                            maphorizontal.append(' ')
                        else:
                            maphorizontal.append(' ')
                    elif a==79:
                        maphorizontal.append('#')
                    else:
                        if b < lowlim or b >highlim:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append(' ')
                    b+=1

                mapvertical.append(maphorizontal)
                a+=1


            g=random.randint(25,30)
            while g>0:
                rocksize=random.randint(5,7)
                rocklocx=random.randint(0,70)
                rocklocy=random.randint(0,70)
                while rocklocy<3 and rocklocx<41 and rocklocx>32 or rocklocy>70 and rocklocx<41 and rocklocx>32 or rocklocx>65 and rocklocy<41 and rocklocy>32 or rocklocx>65 and rocklocy<41 and rocklocy>32:
                    rocklocx=random.randint(0,70)
                    rocklocy=random.randint(0,70)
                for v in range(0, rocksize):
                    for t in range(0, random.randint((rocksize-2),(rocksize+2))):
                        (mapvertical[rocklocy+v])[rocklocx+t]='#'
                g-=1

            map.append(mapvertical)
        if h==5 or h==10 or h==15:
            a=0
            mapvertical=[]
            while a<80:
                maphorizontal=[]
                lowlim=random.randint(1,10)
                highlim=random.randint(70,78)
                b=0
                while b<80:
                    if a==79 or a==0:
                        if b==38 or b==39 or b==40 or b==41:
                            maphorizontal.append(' ')
                        else:
                            maphorizontal.append('#')
                    elif a==38 or a==39 or a==40 or a==41:
                        if b==79:
                            maphorizontal.append(' ')
                        elif b==0:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append(' ')
                    else:
                        if b < lowlim or b >highlim:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append(' ')
                    b+=1

                mapvertical.append(maphorizontal)
                a+=1


            g=random.randint(25,30)
            while g>0:
                rocksize=random.randint(5,7)
                rocklocx=random.randint(0,70)
                rocklocy=random.randint(0,70)
                while rocklocy<3 and rocklocx<41 and rocklocx>32 or rocklocy>70 and rocklocx<41 and rocklocx>32 or rocklocx>65 and rocklocy<41 and rocklocy>32 or rocklocx>65 and rocklocy<41 and rocklocy>32:
                    rocklocx=random.randint(0,70)
                    rocklocy=random.randint(0,70)
                for v in range(0, rocksize):
                    for t in range(0, random.randint((rocksize-2),(rocksize+2))):
                        (mapvertical[rocklocy+v])[rocklocx+t]='#'
                g-=1

            map.append(mapvertical)
        if h==9 or h==14 or h==19:
            a=0
            mapvertical=[]
            while a<80:
                maphorizontal=[]
                lowlim=random.randint(1,10)
                highlim=random.randint(70,78)
                b=0
                while b<80:
                    if a==79 or a==0:
                        if b==38 or b==39 or b==40 or b==41:
                            maphorizontal.append(' ')
                        else:
                            maphorizontal.append('#')
                    elif a==38 or a==39 or a==40 or a==41:
                        if b==0:
                            maphorizontal.append(' ')
                        elif b==79:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append(' ')
                    else:
                        if b < lowlim or b >highlim:
                            maphorizontal.append('#')
                        else:
                            maphorizontal.append(' ')
                    b+=1

                mapvertical.append(maphorizontal)
                a+=1


            g=random.randint(25,30)
            while g>0:
                rocksize=random.randint(5,7)
                rocklocx=random.randint(0,70)
                rocklocy=random.randint(0,70)
                while rocklocy<3 and rocklocx<41 and rocklocx>32 or rocklocy>70 and rocklocx<41 and rocklocx>32 or rocklocx>65 and rocklocy<41 and rocklocy>32 or rocklocx>65 and rocklocy<41 and rocklocy>32:
                    rocklocx=random.randint(0,70)
                    rocklocy=random.randint(0,70)
                for v in range(0, rocksize):
                    for t in range(0, random.randint((rocksize-2),(rocksize+2))):
                        (mapvertical[rocklocy+v])[rocklocx+t]='#'
                g-=1

            map.append(mapvertical)
    return(map)