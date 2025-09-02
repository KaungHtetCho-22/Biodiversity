import pandas as pd
import numpy as np
import joblib  # For saving and loading models
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.feature_selection import RFE
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


# Load dataset
df = pd.read_csv("pivot_table.csv") 

best_acc = 0
X_train = df.copy()
X_test = df.copy()

X_train.drop(['unique_date', 'pi_id'], axis=1, inplace=True)
X_test.drop(['unique_date', 'pi_id'], axis=1, inplace=True)
y_train = X_train.pop('biodiversity_level')
y_test = X_test.pop('biodiversity_level')

scaler = StandardScaler()
scaler.set_output(transform='pandas')
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
# print(X_train)
# print(X_test)

# Model initialization
xgb = XGBClassifier(eval_metric='logloss')

# Recursive Feature Elimination (RFE)
num_feature_list = [80, 70, 60, 50, 40, 30, 20]

# num_features = 60
for num_features in num_feature_list:
    rfe = RFE(xgb, n_features_to_select=num_features)
    X_train_rfe = rfe.fit_transform(X_train, y_train)
    X_test_rfe = rfe.transform(X_test)
    selected_features = X_train.columns[rfe.support_]
    print("Selected Features:", selected_features)

    # GridSearch for best hyperparameters
    param_grid = {
        'n_estimators': [25, 50, 100, 200],
        'max_depth': [3, 5, 7, 9],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.7, 0.9, 1.0],
        'colsample_bytree': [0.7, 0.9, 1.0]
    }

    grid_search = GridSearchCV(xgb, param_grid, cv=3, scoring='accuracy', n_jobs=-1, verbose=1)
    grid_search.fit(X_train_rfe, y_train)

    # Get best parameters
    best_params = grid_search.best_params_
    print("Best Parameters:", best_params)

    # Train the best model
    best_model = grid_search.best_estimator_
    best_model.fit(X_train_rfe, y_train)



    # Predictions
    y_pred = best_model.predict(X_test_rfe)

    # Evaluation metrics
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')
    print(f"F1 Score: {f1:.4f}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"### Classification Report, Num_features:{num_features} ###\n", classification_report(y_test, y_pred, target_names=['Score A', 'Score B', 'Score C'], digits=4))

    # if accuracy > best_acc:
    #     best_acc = accuracy
    #     # Save the trained model
    joblib.dump(best_model, f'results/weights/best_xgboost_model_{num_features}_{accuracy:.4f}_f1_{f1:.4f}.pkl')
    print(f"Model saved as best_xgboost_model_{num_features}.pkl")
    print("############################### END ############################")