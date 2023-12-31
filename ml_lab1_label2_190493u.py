# -*- coding: utf-8 -*-
"""ML-lab1-label2-190493U.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QqmD1pkPsLyfV_UWYTjHkmVLQjF8p1Qh
"""

from google.colab import drive
drive.mount('/content/drive')

"""Import necssary libraries and modules"""

#import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

from sklearn.metrics import mean_squared_error, r2_score

train_path = '/content/drive/MyDrive/Colab Notebooks/ML/Lab 1/train.csv'
valid_path = '/content/drive/MyDrive/Colab Notebooks/ML/Lab 1/valid.csv'
test_path = '/content/drive/MyDrive/Colab Notebooks/ML/Lab 1/test.csv'

train_data = pd.read_csv(train_path)
valid_data = pd.read_csv(valid_path)
test_data = pd.read_csv(test_path)

"""Drop the columns where there are null values for the lables in the training dataset"""

train_null_counts = train_data.isnull().sum()
print("train null counts : \n {}".format(train_null_counts))

train_data = train_data.dropna(subset=train_data.columns[-4:], how='any')

train_data = train_data.fillna(train_data.mean())

valid_data = valid_data.fillna(valid_data.mean())

test_data = test_data.fillna(test_data.mean())

"""Separate features and labels in the train, valid and test datasets"""

train_features = train_data.iloc[:, :-4]
train_labels = train_data.iloc[:, -4:]

valid_features = valid_data.iloc[:, :-4]
valid_labels = valid_data.iloc[:, -4:]

test_features = test_data.iloc[:, :-4]
test_labels = test_data.iloc[:, -4:]

train_label2 = train_labels.iloc[:,1]

valid_label2 = valid_labels.iloc[:,1]

test_label2 = test_labels.iloc[:,1]

"""# Predicting Label 2 without Feature Engineering

Predict label 2 without feature engineering steps and techniques

Make copies of the features and labels of the datasets to be used in the models without feature engineering
"""

train_features_copy = train_features.copy()
train_labels_copy = train_labels.copy()

valid_features_copy = valid_features.copy()
valid_labels_copy = valid_labels.copy()

test_features_copy = test_features.copy()
test_labels_copy = test_labels.copy()

train_label2_copy = train_label2.copy()

valid_label2_copy = valid_label2.copy()

test_label2_copy = test_label2.copy()

"""Standardize the features of all datasets"""

scaler = StandardScaler()
train_features_copy = scaler.fit_transform(train_features_copy)
valid_features_copy = scaler.transform(valid_features_copy)
test_features_copy = scaler.transform(test_features_copy)

"""Use the raw scaled features to train the best model which is KNN Regressor"""

best_model = KNeighborsRegressor()

best_model.fit(train_features_copy, train_label2_copy)

"""Used the trained model on all features to predict the valid and get metrics"""

y_pred_base_train = best_model.predict(train_features_copy)

mse = mean_squared_error(train_label2_copy, y_pred_base_train)
r2s = r2_score(train_label2_copy, y_pred_base_train)

print(f"Metrics for KNeighborsRegressor on train data:")
print(f"Mean Squared Error: {mse:.2f}")
print(f"R2 Score: {r2s:.2f}")
print("\n")

y_pred_base_valid = best_model.predict(valid_features_copy)

mse = mean_squared_error(valid_label2_copy, y_pred_base_valid)
r2s = r2_score(valid_label2_copy, y_pred_base_valid)

print(f"Metrics for KNeighborsRegressor on valid data:")
print(f"Mean Squared Error: {mse:.2f}")
print(f"R2 Score: {r2s:.2f}")
print("\n")

"""Predict the label 2 on test data"""

y_pred_base_test = best_model.predict(test_features_copy)

"""# Predicting Label 2 with Feature Engineering

Predict label 2 with feature engineering steps and techniques

## Feature Engineering

Use feature selection based on correlation matrix and feature extraction based on PCA

### Feature Selection

Visualize the distribution of the training label 2
"""

labels, counts = np.unique(train_label2, return_counts=True)

plt.figure(figsize=(10, 6))
plt.xticks(labels)
plt.bar(labels, counts)
plt.xlabel('Target Label 2')
plt.ylabel('Frequency')
plt.title('Distribution of Target Label 2')
plt.show()

"""Calculate the correlation matrix of the training data features"""

correlation_matrix = train_features.corr()

mask = np.triu(np.ones_like(correlation_matrix))

plt.figure(figsize=(12, 12))
sns.heatmap(correlation_matrix, cmap='coolwarm', center=0, mask=mask)
plt.title("Correlation Matrix")
plt.show()

"""Identify the features that are highly correlated with each other using the traning dataset"""

correlation_threshold = 0.9

highly_correlated = set()

for i in range(len(correlation_matrix.columns)):
    for j in range(i):
        if abs(correlation_matrix.iloc[i, j]) > correlation_threshold:
            colname = correlation_matrix.columns[i]
            highly_correlated.add(colname)

"""Remove the previously identified highly correlated features from all the datasets"""

train_features = train_features.drop(columns=highly_correlated)
valid_features = valid_features.drop(columns=highly_correlated)
test_features = test_features.drop(columns=highly_correlated)

correlation_with_target = train_features.corrwith(train_label2)

correlation_threshold = 0.05

highly_correlated_features = correlation_with_target[correlation_with_target.abs() > correlation_threshold]

train_features = train_features[highly_correlated_features.index]

valid_features = valid_features[highly_correlated_features.index]

test_features = test_features[highly_correlated_features.index]

scaler = StandardScaler()
standardized_train_features = scaler.fit_transform(train_features)
standardized_valid_features = scaler.transform(valid_features)
standardized_test_features = scaler.transform(test_features)

"""### Feature Extraction"""

variance_threshold = 0.99

pca = PCA(n_components=variance_threshold, svd_solver='full')

pca_train_result = pca.fit_transform(standardized_train_features)
pca_valid_result = pca.transform(standardized_valid_features)
pca_test_result = pca.transform(standardized_test_features)

explained_variance_ratio_reduced = pca.explained_variance_ratio_
print("Explained Variance Ratio after Dimensionality Reduction:", explained_variance_ratio_reduced)

plt.figure(figsize=(18, 10))
plt.bar(range(1, pca_train_result.shape[1] + 1), explained_variance_ratio_reduced)
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance Ratio')
plt.title('Explained Variance Ratio per Principal Component (Reduced)')
plt.show()

"""## Model Selection

Select the model that best predicts the valid and test datasets based on root mean squared error and r2 score
"""

classification_models = [
    # ('Linear Regression', LinearRegression()),
    ('K Neighbors', KNeighborsRegressor()),
    # ('Decision Tree', DecisionTreeRegressor()),
    # ('Random Forest', RandomForestRegressor()),
    # ('XGBoost', XGBRegressor())
]


num_features = pca_train_result.shape[1]
print(f"Number of features: {num_features}\n")

for model_name, model in classification_models:
    model.fit(pca_train_result, train_label2)

    y_pred_train = model.predict(pca_train_result)

    mse = mean_squared_error(train_label2, y_pred_train)
    r2s = r2_score(train_label2, y_pred_train)

    print(f"Metrics for {model_name} on train data:")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R2 Score: {r2s:.2f}")
    print("\n")

    y_pred_valid = model.predict(pca_valid_result)

    mse = mean_squared_error(valid_label2, y_pred_valid)
    r2s = r2_score(valid_label2, y_pred_valid)

    print(f"Metrics for {model_name} on validation data:")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R2 Score: {r2s:.2f}")
    print("\n")

    y_pred_test = model.predict(pca_test_result)

"""# Generate Output CSV

Define method to create the csv file
"""

def create_csv(features, pred_before_fe, pred_after_fe, destination):
  feature_count = features.shape[1]

  header_row = [f"new_feature_{i}" for i in range(1,feature_count+1)]

  df = pd.DataFrame(features, columns  = header_row)

  df.insert(loc=0, column='Predicted labels before feature engineering', value=pred_before_fe)
  df.insert(loc=1, column='Predicted labels after feature engineering', value=pred_after_fe)
  df.insert(loc=2, column='No of new features', value=np.repeat(feature_count, features.shape[0]))

  df.to_csv(destination, index=False)

"""Create CSV file"""

destination = '/content/drive/MyDrive/Colab Notebooks/ML/Lab 1/190493U_label_2.csv'

create_csv(pca_test_result, y_pred_base_test, y_pred_test, destination)