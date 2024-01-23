from sklearn.metrics import accuracy_score

def accuracy_train_val_test(model, X_train, y_train, X_val, y_val, X_test, y_test):
    pred = model.predict(X_train)
    acc_train = accuracy_score(y_train, pred)
    
    pred = model.predict(X_val)
    acc_val = accuracy_score(y_val, pred)

    pred = model.predict(X_test)
    acc_test = accuracy_score(y_test, pred)

    print('Acc. TRAIN:', acc_train)
    print('Acc. VALIDATION:', acc_val)
    print('Acc. TEST:', acc_test)
    
    return