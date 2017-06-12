import numpy as np

def clean_ocr_results(ocr,charspace = 7,neg_charspace = -3):
    no_newlines=ocr.split('\n')
    good_list = [l.split(' ') for l in no_newlines]
    list_nums = [[l[0], int(l[1]), int(l[2]), int(l[3]), int(l[4])]  for l in good_list]
    xdiffs = [[i, j+1, next[1]-cur[3]] for i,cur in enumerate(list_nums[:-1]) for j,next in enumerate(list_nums[1:])]
    close_diffs = [d for d in xdiffs if d[2]>neg_charspace and d[2]<charspace and yoverlap(d[0],d[1],list_nums)]

    # Get rid of repetitions
    close_diffs = [d for d in close_diffs if d[0]!=d[1]]

    # Get rid of duplicates in first column
    cd1 = [i[0] for i in close_diffs]
    _,keepers = np.unique(np.array(cd1),return_index=True)
    keepers = keepers.tolist()
    close_diffs = np.array(close_diffs)[keepers,:]
    
    # Get rid of duplicates in second column
    cd_flip = np.flipud(close_diffs)
    cd2 = [i[1] for i in cd_flip]
    _,keepersflip = np.unique(np.array(cd2),return_index=True)
    keepersflip = keepersflip.tolist()
    cd_final = np.array(cd_flip)[keepersflip,:].tolist()
    
    words = word_list(list_nums,cd_final)
    return words

def yoverlap(ind1,ind2,list_nums,min_overlap=0.3):
    # At least 30% of one character's bounding box y-range must overlap with the other's
    y1low=list_nums[ind1][2]
    y1high=list_nums[ind1][4]
    y2low = list_nums[ind2][2]
    y2high = list_nums[ind2][4]
    y1_range = range(y1low,y1high)
    y2_range = range(y2low,y2high)
    overlap = [val for val in y1_range if val in y2_range]
    max_overlap_frac = max(float(len(overlap))/float(len(y1_range)),
                           float(len(overlap))/float(len(y2_range))
                          )
    if max_overlap_frac>min_overlap:
        over=True
    else:
        over=False
    '''
    overlap_frac_1=(y1high-y2low)/(y1high-y1low)  # How much of first char overlaps with second
    overlap_frac_2=(y2
    

    if y2low in range(y1low-buffer,y1high+buffer) or y2high in range(y1low-buffer,y1high+buffer):
        over=True
    else:
        over=False
    '''
    return over

def make_word(letters,start,close_diffs):
    letter_inds = []
    letter_inds.append(start)
    start_diffs = [i[0] for i in close_diffs]
    if start in start_diffs:
        start_ind = start_diffs.index(start)
        run = True
        while run:
            letter_inds.append(close_diffs[start_ind][1])
            if start_ind+1>=len(close_diffs):
                run=False
            else:
                if close_diffs[start_ind][1] == close_diffs[start_ind+1][0]:
                    start_ind+=1
                else:
                    run = False
    return letter_inds

def word_list(letters,close_diffs):
    words = []
    letters_copy = letters[:]
    while letters_copy:
        orig_ind = letters.index(letters_copy[0])
        new_word_inds = make_word(letters,orig_ind,close_diffs)
#         print(new_word_inds)
        for i in new_word_inds:
            letters_copy.remove(letters[i])

        new_word_list = [letters[i] for i in new_word_inds]
        new_word = list()
        new_word.append("".join([l[0] for l in new_word_list]))
        new_word_boxes = [i[1:] for i in new_word_list]
        new_box_array = np.array(new_word_boxes)
        new_word.append(new_box_array[:,0].min(axis=0))
        new_word.append(new_box_array[:,1].min(axis=0))
        new_word.append(new_box_array[:,2].max(axis=0))
        new_word.append(new_box_array[:,3].max(axis=0))
        words.append(new_word)
    for w in words:
        w[0]=w[0].replace(',','')
    return words