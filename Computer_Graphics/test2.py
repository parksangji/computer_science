import numpy

def globalalign(v,w,scorematrix,indel) :
    s = numpy.zeros((len(v)+1,len(w)+1),dtype= "int32")
    b = numpy.zeros((len(v)+1,len(w)+1),dtype="int32")

    for i in range(0,len(w)+1) :
        if(j==0) :
            if (i > 0) :
                s[i,j] = s[i-1,j] + indel
                b[i,j] = 1
            continue
        if(i==0) :
            s[i,j] = s[i,j-1] +indel
            b[i,j] = 2
            continue
        score = s[i-1,j-1] + scorematrix[v[i-1],w[j-1]]
        vskip = s[i-1,j] + indel
        wskip = s[i,j-1] + indel
        s[i,j] = max(vskip,wskip,score)
        if(s[i,j] == vskip) :
            b[i,j] = 1
        elif(s[i,j]== wskip) :
            b[i,j] =2
        else:
            b[i,j] = 3
    return (s,b)

