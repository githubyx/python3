#coding=utf-8
from sklearn import neighbors
import numpy as np
from PIL import Image
import os
from sklearn.svm import SVC
from sklearn.externals import joblib
'''
根据pic下的目录的照片进行分类你 训练模型保存于train_model
'''
def get_bin_table(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

def ImageToMatrix(filename):
    image = Image.open(filename)
    width,height =image.size
    imgry = image.convert('L')
    data = np.array(imgry)
    new_data = np.reshape(data,(1,width*height))
    return new_data
#将验证码的图片拆分 灰度化
def countPic(imgfilename):
    image = Image.open('temp/%s'%imgfilename)
    imgNameList=[]
    for i in range(3):
        x = 10 + i * 20
        imagec = image.crop((x, 0, x + 20, 20))
        imgry = imagec.convert('L')
        table = get_bin_table()
        out = imgry.point(table, '1')
        fileStr = imgfilename.split('.')[0]
        out.save("temp/%s_%s.gif" % (fileStr,i))
        imgNameList.append("temp/%s_%s.gif" % (fileStr,i))
    return imgNameList

def loadData():
    trainingFileList=[]
    dirs = os.listdir("pic")
    y = []
    for i in dirs:
        for j in range(10):
            y.append(i)
    for parent, dirnames, filenames in os.walk("pic"):
        for filename in filenames:
            trainingFileList.append(os.path.join(parent,filename))
    m = len(trainingFileList)
    trainingMat = np.zeros((m, 400))
    for i in range(m):
        trainingMat[i, :] = ImageToMatrix(trainingFileList[i])
    data=np.array(trainingMat)
    tar=np.array(y)
    # print data,tar
    return data,tar

def savaModel():
    data, tar = loadData()
    clf = SVC()
    clf.fit(data, tar)
    joblib.dump(clf, "train_model")

def predict(path):
    clf = joblib.load('train_model')
    test = ImageToMatrix(path)
    predictLabel = clf.predict(test)
    return predictLabel[0]

#计算验证码的结果
def countSum(path):
    imgList=countPic(path)
    a=int(predict(imgList[0]))
    pro=predict(imgList[1])
    b = int(predict(imgList[2]))
    print(a,pro,b)
    if pro=='add' or pro==b'add':
        return a+b
    elif pro=='sub' or pro==b'sub':
        return a-b
    elif pro == 'mul'or pro == b'mul':
        return a*b
    else:
        return 0.1
if __name__ == '__main__':
    savaModel()


