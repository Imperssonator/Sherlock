import cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract as tes

def match_yticks(labels,tick_list):
    tick_lens = [abs(tick[2]-tick[0]) for tick in tick_list]
    max_tick_len = max(tick_lens)
    score_list = []
    for tick in tick_list:
        west_pt = [min(tick[0],tick[2]), tick[1]]
        tick_len = abs(tick[2]-tick[0])
        tick_score = []
        for i,row in enumerate(labels):
            dist_vec = np.array(west_pt)-np.array([row[5],row[6]])
            dist_score = np.linalg.norm(dist_vec,2)
            len_score = max_tick_len-tick_len
            this_tick_score = dist_score+len_score
            tick_score.append(this_tick_score)
        score_list.append(tick_score)
    score_array = np.array(score_list)
    min_score_inds = score_array.argmin(axis=0)
    return(min_score_inds.tolist())

def match_xticks(labels,tick_list):
    tick_lens = [abs(tick[1]-tick[3]) for tick in tick_list]
    max_tick_len = max(tick_lens)
    score_list = []
    for tick in tick_list:
        south_pt = [tick[0], min(tick[1],tick[3])]
        tick_len = abs(tick[1]-tick[3])
        tick_score = []
        for i,row in enumerate(labels):
            dist_vec = np.array(south_pt)-np.array([row[5],row[6]])
            dist_score = np.linalg.norm(dist_vec,2)
            len_score = max_tick_len-tick_len
            this_tick_score = dist_score+len_score
            tick_score.append(this_tick_score)
        score_list.append(tick_score)
    score_array = np.array(score_list)
    min_score_inds = score_array.argmin(axis=0)
    return(min_score_inds.tolist())

def get_xticks(nbw,xax,tickMargin=11,minTickLen=0,maxGap=0):
    # Crop the black and white image so only the area around the x-axis exists
    m,n=nbw.shape
    xaxImg = np.zeros([m,n])
    xaxImg[xax[1]-tickMargin:xax[1]+tickMargin, xax[0]-1:xax[2]+1] = nbw[xax[1]-tickMargin:xax[1]+tickMargin, xax[0]-1:xax[2]+1]
    xaxImg = xaxImg.astype('uint8')
    # Hough Transform to obtain the vertical lines, then sort by x-coordinate
    xTicksHough = np.reshape(cv2.HoughLinesP(xaxImg,1,np.pi,2, minLineLength = minTickLen, maxLineGap = maxGap),(-1,4))
    # xTicksLen = np.absolute(np.diff(xTicksHough[:,[1,3]],axis=1))
    # xticksx = xTicksHough[:,0]
    xtsort = xTicksHough[xTicksHough[:,0].argsort()]
    return xtsort

def get_yticks(nbw,yax,tickMargin=11,minTickLen=0,maxGap=0):
    # Crop the black and white image so only the area around the y-axis exists
    m,n=nbw.shape
    yaxImg = np.zeros([m,n])
    yaxImg[yax[3]-1:yax[1]+1,yax[0]-tickMargin:yax[0]+tickMargin] = nbw[yax[3]-1:yax[1]+1,yax[0]-tickMargin:yax[0]+tickMargin]
    yaxImg = yaxImg.astype('uint8')
    yaxRot = ndimage.interpolation.rotate(yaxImg, -90)
    # Hough Transform to obtain the vertical lines, then sort by x-coordinate
    yTicksHoughRot = np.reshape(cv2.HoughLinesP(yaxRot,1,np.pi,1, minLineLength = minTickLen, maxLineGap = maxGap),(-1,4))
    yTicksHough = yTicksHoughRot[:,[3,0,1,2]]
    yTicksHough[:,[1,3]]=m-yTicksHough[:,[1,3]]
    yTicksList = yTicksHough.tolist()
    # yTicksLen = np.absolute(np.diff(yTicksHough[:,[0,2]],axis=1))
    # yTicksHor = [yTicksList[i] for i,len in enumerate(yTicksLen) if len>0]
    yTicksArray = np.array(yTicksList)
    # yticksy = yTicksArray[:,1]
    ytsort = yTicksArray[yTicksArray[:,1].argsort()]
    return ytsort


def iso_lines(lines,minspace=5):
    # take an array of lines (x1, y1, x2, y2) and remove lines that are less than <minspace> away from each other.
    for x1,y1,x2,y2 in lines:
        for index, (x3,y3,x4,y4) in enumerate(lines):

            if y1==y2 and y3==y4: # Horizontal Lines
                diff = abs(y1-y3)
            elif x1==x2 and x3==x4: # Vertical Lines
                diff = abs(x1-x3)
            else:
                diff = 0

            if diff < minspace and diff is not 0:
                del lines[index]
    return np.array(lines)

def med_spaced(lines,buff,col):
    # take an array of lines and return only those that are "about (within <buff>)" the median spacing from each other
    ind_set = set()
    diffs1 = np.diff(lines[:,col],n=1,axis=0).tolist()
    dmed = np.median(diffs1)
    for i, d in enumerate(diffs1):
        if d>dmed-buff and d<dmed+buff:
            ind_set.add(i)
            ind_set.add(i+1)
    return lines[list(ind_set),:]    
    
def get_xaxis(HoughP,nbw):
    xax_perf = np.array([1, 0.7, 0.8])
    xScores = list()
    
    for i,linepts in enumerate(HoughP):
        linevec = linepts[2:4]-linepts[0:2]
        linemag = np.linalg.norm(linevec,2)
        cosScore = np.dot(linevec/linemag, np.array([1,0]))**2
        fracLenScore = float(np.absolute(linevec[0]))/nbw.shape[1]
        fracYcScore = float(linepts[1])/nbw.shape[0]
        lineFeat = np.array([cosScore, fracLenScore, fracYcScore])
        distFeat = np.linalg.norm(lineFeat-xax_perf,2)
        xScores.append(distFeat)
    xaxLine = xScores.index(min(xScores))
    return HoughP[xaxLine,:]

def get_yaxis(HoughP,nbw):
    yax_perf = np.array([0, 0.7, 0.2])
    yScores = list()
    
    for i,linepts in enumerate(HoughP):
        linevec = linepts[2:4]-linepts[0:2]
        linemag = np.linalg.norm(linevec,2)
        cosScore = np.dot(linevec/linemag, np.array([1,0]))**2
        fracLenScore = float(np.absolute(linevec[1]))/nbw.shape[0]
        fracXcScore = float(linepts[0])/nbw.shape[1]
        lineFeat = np.array([cosScore, fracLenScore, fracXcScore])
        distFeat = np.linalg.norm(lineFeat-yax_perf,2)
        yScores.append(distFeat)
    yaxLine = yScores.index(min(yScores))
    return HoughP[yaxLine,:]

if __name__ == '__main__':
    img = cv2.imread('isotherm1.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    r, bw = th3 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    nbw = (255-bw)

    # lines = cv2.HoughLines(nbw,1,np.pi/180,200)
    linesP = cv2.HoughLinesP(nbw, 1, np.pi/2, 2, minLineLength=nbw.shape[1]/10,
                             maxLineGap=3)[0]

    xax_perf = np.array([1, 0.7, 0.8])
    yax_perf = np.array([0, 0.7, 0.2])

    xScores = [xaxScore(pts) for pts in linesP]
    # print('---')
    yScores = [yaxScore(pts) for pts in linesP]
    xaxLine = xScores.index(min(xScores))
    yaxLine = yScores.index(min(yScores))

    imlabel = img.copy()
    for x1, y1, x2, y2 in linesP[[xaxLine, yaxLine], :]:
        cv2.line(imlabel, (x1, y1), (x2, y2), (255, 0, 0), 2)
        print(x1, y1, x2, y2)
