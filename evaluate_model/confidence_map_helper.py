import pandas as pd
import numpy as np

def compareLabels(df_results, df_truth, window_size=0.20):
    truth_tot = 0
    correct_tot = 0
    pred_tot = 0

    truth_pos = 0
    correct_pos = 0
    pred_pos = 0

    truth_neg = 0
    correct_neg = 0
    pred_neg = 0

    truth_pos_o = 0
    correct_pos_o = 0
    pred_pos_o = 0

    truth_nuc = 0
    correct_nuc = 0
    pred_nuc = 0

    dis_pos = 0
    dis_neg = 0
    dis_pos_o = 0
    dis_nuc = 0

    dis_pos_c = 0
    dis_neg_c = 0
    dis_pos_o_c = 0
    dis_nuc_c = 0


    for i in df_truth['image_index'].unique():
        df_truth_img = df_truth[df_truth['image_index'] == i]
        df_results_img = df_results[df_results['image_index'] == i]
        truth_tot += len(df_truth_img.index) # get total truth number
        pred_tot += len(df_results_img.index) # get total prediction number

        # seperate truth labels
        df_truth_pos = df_truth_img[df_truth_img['class']==0]
        truth_pos += len(df_truth_pos.index)
        df_truth_neg = df_truth_img[df_truth_img['class']==1]
        truth_neg += len(df_truth_neg.index)
        df_truth_pos_o = df_truth_img[df_truth_img['class']==2]
        truth_pos_o += len(df_truth_pos_o.index)
        df_truth_nuc = df_truth_img[df_truth_img['class']==3]
        truth_nuc += len(df_truth_nuc.index)

        # seperate prediction labels
        df_results_pos = df_results_img[df_results_img['class']==0]
        pred_pos += len(df_results_pos.index)
        df_results_neg = df_results_img[df_results_img['class']==1]
        pred_neg += len(df_results_neg.index)
        df_results_pos_o = df_results_img[df_results_img['class']==2]
        pred_pos_o += len(df_results_pos_o.index)
        df_results_nuc = df_results_img[df_results_img['class']==3]
        pred_nuc += len(df_results_nuc.index)

        for index_t, row_t in df_truth_pos.iterrows():
            mindis = 1
            xt, yt = row_t.x, row_t.y
            for index_p, row_p in df_results_pos.iterrows():
                xp, yp = row_p.x, row_p.y
                dis = np.linalg.norm(np.array([xt,yt])-np.array([xp,yp]))
                if dis < mindis:
                    mindis = dis
            if mindis < window_size/2:
                correct_pos += 1 # increment correct number if minimum distance to a prediction is smaller than window_size
                dis_pos_c += mindis
            dis_pos += mindis

        for index_t, row_t in df_truth_neg.iterrows():
            mindis = 1
            xt, yt = row_t.x, row_t.y
            for index_p, row_p in df_results_neg.iterrows():
                xp, yp = row_p.x, row_p.y
                dis = np.linalg.norm(np.array([xt,yt])-np.array([xp,yp]))
                if dis < mindis:
                    mindis = dis
            if mindis < window_size/2:
                correct_neg += 1
                dis_neg_c += mindis
            dis_neg += mindis

        for index_t, row_t in df_truth_pos_o.iterrows():
            mindis = 1
            xt, yt = row_t.x, row_t.y
            for index_p, row_p in df_results_pos_o.iterrows():
                xp, yp = row_p.x, row_p.y
                dis = np.linalg.norm(np.array([xt,yt])-np.array([xp,yp]))
                if dis < mindis:
                    mindis = dis
            if mindis < window_size/2:
                correct_pos_o += 1
                dis_pos_o_c += mindis
            dis_pos_o += mindis

        for index_t, row_t in df_truth_nuc.iterrows():
            mindis = 1
            xt, yt = row_t.x, row_t.y
            for index_p, row_p in df_results_nuc.iterrows():
                xp, yp = row_p.x, row_p.y
                dis = np.linalg.norm(np.array([xt,yt])-np.array([xp,yp]))
                if dis < mindis:
                    mindis = dis
            if mindis < window_size/2:
                correct_nuc += 1
                dis_nuc_c += mindis
            dis_nuc += mindis
    correct_tot = correct_pos + correct_neg + correct_pos_o + correct_nuc
    columns = ['truth_tot', 'truth_pos', 'truth_neg', 'truth_pos_o', 'truth_nuc',
               'correct_tot', 'correct_pos', 'correct_neg', 'correct_pos_o', 'correct_nuc', 
               'pred_tot', 'pred_pos', 'pred_neg', 'pred_pos_o', 'pred_nuc',
               'dis_pos', 'dis_neg', 'dis_pos_o', 'dis_nuc', 
               'dis_pos_c', 'dis_neg_c', 'dis_pos_o_c', 'dis_nuc_c'] 
    df = pd.DataFrame(index=np.arange(1), columns=columns)
    df['truth_tot']=truth_tot
    df['correct_tot']=correct_tot
    df['pred_tot']=pred_tot

    df['truth_pos']=truth_pos
    df['correct_pos']=correct_pos
    df['pred_pos']=pred_pos

    df['truth_neg']=truth_neg
    df['correct_neg']=correct_neg
    df['pred_neg']=pred_neg

    df['truth_pos_o']=truth_pos_o
    df['correct_pos_o']=correct_pos_o
    df['pred_pos_o']=pred_pos_o

    df['truth_nuc']=truth_nuc
    df['correct_nuc']=correct_nuc
    df['pred_nuc']=pred_nuc

    df['dis_pos']=dis_pos
    df['dis_neg']=dis_neg
    df['dis_pos_o']=dis_pos_o
    df['dis_nuc']=dis_nuc

    df['dis_pos_c']=dis_pos_c
    df['dis_neg_c']=dis_neg_c
    df['dis_pos_o_c']=dis_pos_o_c
    df['dis_nuc_c']=dis_nuc_c
    return df

def checkYolo(conf_thres_pos = 0.001, conf_thres_neg = 0.001, conf_thres_nuc = 0.001, conf_thres_pos_o = 0.001, df_yolo = None, df_results = None):
    columns = ['image_index','class', 'x', 'y']
    df_results_tot = pd.DataFrame(index=np.arange(0), columns=columns)
    for i in df_yolo.image_index.unique():
        df_yolo_pos = df_yolo[(df_yolo['class']==0) & (df_yolo['image_index']==i) & (df_yolo['confidence']>conf_thres_pos)]
        df_yolo_neg = df_yolo[(df_yolo['class']==1) & (df_yolo['image_index']==i) & (df_yolo['confidence']>conf_thres_neg)]
        df_yolo_pos_o = df_yolo[(df_yolo['class']==2) & (df_yolo['image_index']==i) & (df_yolo['confidence']>conf_thres_pos_o)]
        df_yolo_nuc = df_yolo[(df_yolo['class']==3) & (df_yolo['image_index']==i) & (df_yolo['confidence']>conf_thres_nuc)]
#         df_yolo_pos = df_yolo_pos.append(df_yolo_pos_o, ignore_index=True)
        
        df_results_pos = df_results[(df_results['class']==0) & (df_results['image_index']==i)]
        df_results_neg = df_results[(df_results['class']==1) & (df_results['image_index']==i)]
        df_results_pos_o = df_results[(df_results['class']==2) & (df_results['image_index']==i)]
        df_results_nuc = df_results[(df_results['class']==3) & (df_results['image_index']==i)]
#         df_results_pos = df_results_pos.append(df_results_pos_o, ignore_index=True)
        
        for index_p, row_p in df_results_pos.iterrows():
            drop = True
            x,y = row_p.x, row_p.y
            for index_y, row_y in df_yolo_pos.iterrows():
                x1,x2,y1,y2 = row_y.x1,row_y.x2,row_y.y1,row_y.y2
                if (x1 <= x <= x2) & (y1 <= y <= y2):
                    drop = False
            if drop:
                df_results_pos = df_results_pos.drop(index_p)
        df_results_tot = df_results_tot.append(df_results_pos, ignore_index=True)
        
        for index_p, row_p in df_results_neg.iterrows():
            drop = True
            x,y = row_p.x, row_p.y
            for index_y, row_y in df_yolo_neg.iterrows():
                x1,x2,y1,y2 = row_y.x1,row_y.x2,row_y.y1,row_y.y2
                if (x1 <= x <= x2) & (y1 <= y <= y2):
                    drop = False
            if drop:
                df_results_neg = df_results_neg.drop(index_p)
        df_results_tot = df_results_tot.append(df_results_neg, ignore_index=True)
        
        for index_p, row_p in df_results_pos_o.iterrows():
            drop = True
            x,y = row_p.x, row_p.y
            for index_y, row_y in df_yolo_pos_o.iterrows():
                x1,x2,y1,y2 = row_y.x1,row_y.x2,row_y.y1,row_y.y2
                if (x1 <= x <= x2) & (y1 <= y <= y2):
                    drop = False
            if drop:
                df_results_pos_o = df_results_pos_o.drop(index_p)
        df_results_tot = df_results_tot.append(df_results_pos_o, ignore_index=True)
        
        for index_p, row_p in df_results_nuc.iterrows():
            drop = True
            x,y = row_p.x, row_p.y
            for index_y, row_y in df_yolo_nuc.iterrows():
                x1,x2,y1,y2 = row_y.x1,row_y.x2,row_y.y1,row_y.y2
                if (x1 <= x <= x2) & (y1 <= y <= y2):
                    drop = False
            if drop:
                df_results_nuc = df_results_nuc.drop(index_p)
        df_results_tot = df_results_tot.append(df_results_nuc, ignore_index=True)
    return df_results_tot

def putBackYOLO(df_results = None, df_yolo = None, conf_thres_pos = 0.24, conf_thres_neg = 0.1, conf_thres_nuc = 0.12, conf_thres_pos_o = 0.06, window_size = 0.15):
    columns = ['image_index','class', 'x', 'y']
    df_results_tot = pd.DataFrame(index=np.arange(0), columns=columns)
    for i in df_results.image_index.unique():
        df_yolo_pos = df_yolo[(df_yolo['class']==0) & (df_yolo['image_index']==i) & (df_yolo['confidence']>conf_thres_pos)]
        df_yolo_neg = df_yolo[(df_yolo['class']==1) & (df_yolo['image_index']==i) & (df_yolo['confidence']>conf_thres_neg)]
        df_yolo_pos_o = df_yolo[(df_yolo['class']==2) & (df_yolo['image_index']==i) & (df_yolo['confidence']>conf_thres_pos_o)]
        df_yolo_nuc = df_yolo[(df_yolo['class']==3) & (df_yolo['image_index']==i) & (df_yolo['confidence']>conf_thres_nuc)]
        
        df_results_pos = df_results[(df_results['class']==0) & (df_results['image_index']==i)]
        df_results_neg = df_results[(df_results['class']==1) & (df_results['image_index']==i)]
        df_results_pos_o = df_results[(df_results['class']==2) & (df_results['image_index']==i)]
        df_results_nuc = df_results[(df_results['class']==3) & (df_results['image_index']==i)]
        
        for index_y, row_y in df_yolo_pos.iterrows():
            putBack = True
            xy,yy = (row_y.x1+row_y.x2)/2, (row_y.y1+row_y.y2)/2
            for index_p, row_p in df_results_pos.iterrows():
                xp, yp = row_p.x, row_p.y
                if np.linalg.norm(np.array([xy,yy])-np.array([xp,yp])) <= window_size/2:
                    putBack = False
            if putBack:
                columns = ['image_index','class', 'x', 'y']
                df = pd.DataFrame(index=np.arange(1), columns=columns)
                df.image_index = i
                df['class'] = 0
                df.x = xy
                df.y = yy
                df_results_pos = df_results_pos.append(df, ignore_index=True)
        df_results_tot = df_results_tot.append(df_results_pos, ignore_index=True)
        
        for index_y, row_y in df_yolo_neg.iterrows():
            putBack = True
            xy,yy = (row_y.x1+row_y.x2)/2, (row_y.y1+row_y.y2)/2
            for index_p, row_p in df_results_neg.iterrows():
                xp, yp = row_p.x, row_p.y
                if np.linalg.norm(np.array([xy,yy])-np.array([xp,yp])) <= window_size/2:
                    putBack = False
            if putBack:
                columns = ['image_index','class', 'x', 'y']
                df = pd.DataFrame(index=np.arange(1), columns=columns)
                df.image_index = i
                df['class'] = 1
                df.x = xy
                df.y = yy
                df_results_neg = df_results_neg.append(df, ignore_index=True)
        df_results_tot = df_results_tot.append(df_results_neg, ignore_index=True)
        
        for index_y, row_y in df_yolo_pos_o.iterrows():
            putBack = True
            xy,yy = (row_y.x1+row_y.x2)/2, (row_y.y1+row_y.y2)/2
            for index_p, row_p in df_results_pos.iterrows():
                xp, yp = row_p.x, row_p.y
                if np.linalg.norm(np.array([xy,yy])-np.array([xp,yp])) <= window_size/2:
                    putBack = False
            if putBack:
                columns = ['image_index','class', 'x', 'y']
                df = pd.DataFrame(index=np.arange(1), columns=columns)
                df.image_index = i
                df['class'] = 2
                df.x = xy
                df.y = yy
                df_results_pos_o = df_results_pos_o.append(df, ignore_index=True)
        df_results_tot = df_results_tot.append(df_results_pos_o, ignore_index=True)
        
        for index_y, row_y in df_yolo_nuc.iterrows():
            putBack = True
            xy,yy = (row_y.x1+row_y.x2)/2, (row_y.y1+row_y.y2)/2
            for index_p, row_p in df_results_nuc.iterrows():
                xp, yp = row_p.x, row_p.y
                if np.linalg.norm(np.array([xy,yy])-np.array([xp,yp])) <= window_size/2:
                    putBack = False
            if putBack:
                columns = ['image_index','class', 'x', 'y']
                df = pd.DataFrame(index=np.arange(1), columns=columns)
                df.image_index = i
                df['class'] = 3
                df.x = xy
                df.y = yy
                df_results_nuc = df_results_nuc.append(df, ignore_index=True)
        df_results_tot = df_results_tot.append(df_results_nuc, ignore_index=True)
    return df_results_tot

def checkYolo_checkAllBoxes(conf_thres_pos = 0.001, conf_thres_neg = 0.001, conf_thres_nuc = 0.001, conf_thres_pos_o = 0.001, df_yolo = None, df_results = None):
    columns = ['image_index','class', 'x', 'y']
    df_results_tot = pd.DataFrame(index=np.arange(0), columns=columns)
    for i in df_yolo.image_index.unique():
        df_yolo_pos = df_yolo[(df_yolo['image_index']==i) & (df_yolo['confidence']>conf_thres_pos)]
        df_yolo_neg = df_yolo[(df_yolo['image_index']==i) & (df_yolo['confidence']>conf_thres_neg)]
        df_yolo_pos_o = df_yolo[(df_yolo['image_index']==i) & (df_yolo['confidence']>conf_thres_pos_o)]
        df_yolo_nuc = df_yolo[(df_yolo['image_index']==i) & (df_yolo['confidence']>conf_thres_nuc)]
        
        df_results_pos = df_results[(df_results['class']==0) & (df_results['image_index']==i)]
        df_results_neg = df_results[(df_results['class']==1) & (df_results['image_index']==i)]
        df_results_pos_o = df_results[(df_results['class']==2) & (df_results['image_index']==i)]
        df_results_nuc = df_results[(df_results['class']==3) & (df_results['image_index']==i)]
        
        for index_p, row_p in df_results_pos.iterrows():
            drop = True
            x,y = row_p.x, row_p.y
            for index_y, row_y in df_yolo_pos.iterrows():
                x1,x2,y1,y2 = row_y.x1,row_y.x2,row_y.y1,row_y.y2
                if (x1 <= x <= x2) & (y1 <= y <= y2):
                    drop = False
            if drop:
                df_results_pos = df_results_pos.drop(index_p)
        df_results_tot = df_results_tot.append(df_results_pos, ignore_index=True)
        
        for index_p, row_p in df_results_neg.iterrows():
            drop = True
            x,y = row_p.x, row_p.y
            for index_y, row_y in df_yolo_neg.iterrows():
                x1,x2,y1,y2 = row_y.x1,row_y.x2,row_y.y1,row_y.y2
                if (x1 <= x <= x2) & (y1 <= y <= y2):
                    drop = False
            if drop:
                df_results_neg = df_results_neg.drop(index_p)
        df_results_tot = df_results_tot.append(df_results_neg, ignore_index=True)
        
        for index_p, row_p in df_results_pos_o.iterrows():
            drop = True
            x,y = row_p.x, row_p.y
            for index_y, row_y in df_yolo_pos_o.iterrows():
                x1,x2,y1,y2 = row_y.x1,row_y.x2,row_y.y1,row_y.y2
                if (x1 <= x <= x2) & (y1 <= y <= y2):
                    drop = False
            if drop:
                df_results_pos_o = df_results_pos_o.drop(index_p)
        df_results_tot = df_results_tot.append(df_results_pos_o, ignore_index=True)
        
        for index_p, row_p in df_results_nuc.iterrows():
            drop = True
            x,y = row_p.x, row_p.y
            for index_y, row_y in df_yolo_nuc.iterrows():
                x1,x2,y1,y2 = row_y.x1,row_y.x2,row_y.y1,row_y.y2
                if (x1 <= x <= x2) & (y1 <= y <= y2):
                    drop = False
            if drop:
                df_results_nuc = df_results_nuc.drop(index_p)
        df_results_tot = df_results_tot.append(df_results_nuc, ignore_index=True)
    return df_results_tot

# compares prediction with groud truth, categorizes each prediction as correct or incorrect, and each annotated point as
# predicted and not predicted

def evaluate_prediction(df_results, df_truth, window_size=0.20):
    truth_tot = 0
    correct_tot = 0
    pred_tot = 0

    truth_pos = 0
    correct_pos = 0
    pred_pos = 0

    truth_neg = 0
    correct_neg = 0
    pred_neg = 0

    truth_pos_o = 0
    correct_pos_o = 0
    pred_pos_o = 0

    truth_nuc = 0
    correct_nuc = 0
    pred_nuc = 0

    dis_pos = 0
    dis_neg = 0
    dis_pos_o = 0
    dis_nuc = 0

    dis_pos_c = 0
    dis_neg_c = 0
    dis_pos_o_c = 0
    dis_nuc_c = 0


    for i in df_truth['image_index'].unique():
        df_truth_img = df_truth[df_truth['image_index'] == i]
        df_results_img = df_results[df_results['image_index'] == i]
        truth_tot += len(df_truth_img.index) # get total truth number
        pred_tot += len(df_results_img.index) # get total prediction number

        # seperate truth labels
        df_truth_pos = df_truth_img[df_truth_img['class']==0]
        truth_pos += len(df_truth_pos.index)
        df_truth_neg = df_truth_img[df_truth_img['class']==1]
        truth_neg += len(df_truth_neg.index)
        df_truth_pos_o = df_truth_img[df_truth_img['class']==2]
        truth_pos_o += len(df_truth_pos_o.index)
        df_truth_nuc = df_truth_img[df_truth_img['class']==3]
        truth_nuc += len(df_truth_nuc.index)

        # seperate prediction labels
        df_results_pos = df_results_img[df_results_img['class']==0]
        pred_pos += len(df_results_pos.index)
        df_results_neg = df_results_img[df_results_img['class']==1]
        pred_neg += len(df_results_neg.index)
        df_results_pos_o = df_results_img[df_results_img['class']==2]
        pred_pos_o += len(df_results_pos_o.index)
        df_results_nuc = df_results_img[df_results_img['class']==3]
        pred_nuc += len(df_results_nuc.index)

        for index_t, row_t in df_truth_pos.iterrows():
            mindis = 1
            xt, yt = row_t.x, row_t.y
            for index_p, row_p in df_results_pos.iterrows():
                xp, yp = row_p.x, row_p.y
                dis = np.linalg.norm(np.array([xt,yt])-np.array([xp,yp]))
                if dis < mindis:
                    mindis = dis
            if mindis < window_size/2:
                correct_pos += 1 # increment correct number if minimum distance to a prediction is smaller than window_size
                dis_pos_c += mindis
            dis_pos += mindis

        for index_t, row_t in df_truth_neg.iterrows():
            mindis = 1
            xt, yt = row_t.x, row_t.y
            for index_p, row_p in df_results_neg.iterrows():
                xp, yp = row_p.x, row_p.y
                dis = np.linalg.norm(np.array([xt,yt])-np.array([xp,yp]))
                if dis < mindis:
                    mindis = dis
            if mindis < window_size/2:
                correct_neg += 1
                dis_neg_c += mindis
            dis_neg += mindis

        for index_t, row_t in df_truth_pos_o.iterrows():
            mindis = 1
            xt, yt = row_t.x, row_t.y
            for index_p, row_p in df_results_pos_o.iterrows():
                xp, yp = row_p.x, row_p.y
                dis = np.linalg.norm(np.array([xt,yt])-np.array([xp,yp]))
                if dis < mindis:
                    mindis = dis
            if mindis < window_size/2:
                correct_pos_o += 1
                dis_pos_o_c += mindis
            dis_pos_o += mindis

        for index_t, row_t in df_truth_nuc.iterrows():
            mindis = 1
            xt, yt = row_t.x, row_t.y
            for index_p, row_p in df_results_nuc.iterrows():
                xp, yp = row_p.x, row_p.y
                dis = np.linalg.norm(np.array([xt,yt])-np.array([xp,yp]))
                if dis < mindis:
                    mindis = dis
            if mindis < window_size/2:
                correct_nuc += 1
                dis_nuc_c += mindis
            dis_nuc += mindis
    correct_tot = correct_pos + correct_neg + correct_pos_o + correct_nuc
    columns = ['truth_tot', 'truth_pos', 'truth_neg', 'truth_pos_o', 'truth_nuc',
               'correct_tot', 'correct_pos', 'correct_neg', 'correct_pos_o', 'correct_nuc', 
               'pred_tot', 'pred_pos', 'pred_neg', 'pred_pos_o', 'pred_nuc',
               'dis_pos', 'dis_neg', 'dis_pos_o', 'dis_nuc', 
               'dis_pos_c', 'dis_neg_c', 'dis_pos_o_c', 'dis_nuc_c'] 
    df = pd.DataFrame(index=np.arange(1), columns=columns)
    df['truth_tot']=truth_tot
    df['correct_tot']=correct_tot
    df['pred_tot']=pred_tot

    df['truth_pos']=truth_pos
    df['correct_pos']=correct_pos
    df['pred_pos']=pred_pos

    df['truth_neg']=truth_neg
    df['correct_neg']=correct_neg
    df['pred_neg']=pred_neg

    df['truth_pos_o']=truth_pos_o
    df['correct_pos_o']=correct_pos_o
    df['pred_pos_o']=pred_pos_o

    df['truth_nuc']=truth_nuc
    df['correct_nuc']=correct_nuc
    df['pred_nuc']=pred_nuc

    df['dis_pos']=dis_pos
    df['dis_neg']=dis_neg
    df['dis_pos_o']=dis_pos_o
    df['dis_nuc']=dis_nuc

    df['dis_pos_c']=dis_pos_c
    df['dis_neg_c']=dis_neg_c
    df['dis_pos_o_c']=dis_pos_o_c
    df['dis_nuc_c']=dis_nuc_c
    return df