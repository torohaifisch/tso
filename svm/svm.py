from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn import metrics
from joblib import dump, load


def svm(filePath):
    f = open(filePath, "r")

    x = []
    y = []
    counter=0

    for i in f:
        res = i.strip().split()
        y.append(round(float(res.pop(0)),1))
        x.append(list(map(int, res)))
        counter+=1
        if counter ==  60000:
            break
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.4,random_state=109) # 70% training and 30% test


    
    model = SVR(kernel='rbf').fit(X_train, y_train)

    tests = [13, 41, 25, 3, 34, 44, 23, 31, 38, 20, 46, 10, 22, 9, 12, 24, 47, 4, 1, 28, 33, 40, 15, 39, 14, 11, 32, 19, 29, 42, 16, 26, 18, 36, 5, 27, 35, 6, 17, 43, 45, 30, 37, 8, 7, 0, 21, 2]

    print("Accuracy:",model.score(X_test, y_test))
    dump(model, 'berlinModel.joblib') 

    
svm("../dataBerlin.txt")
