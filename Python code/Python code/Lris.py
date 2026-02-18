# 1. 导入所需库

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# 2. 加载 Iris 鸢尾花数据集

iris = load_iris()
X = iris.data
y = iris.target

df = pd.DataFrame(X, columns=iris.feature_names)
df["label"] = y

print("数据集前 5 行：")
print(df.head())

# 3. 划分训练集和测试集（留出法）

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 4. 定义三种经典分类模型

models = {
    "Logistic Regression": LogisticRegression(max_iter=200),
    "SVM": SVC(kernel="rbf", gamma="scale"),
    "KNN": KNeighborsClassifier(n_neighbors=5)
}

# 5. 验证方法一：留出法

print("\n=== Hold-out Validation Results ===")
holdout_results = {}

for name, model in models.items():
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", model)
    ])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    holdout_results[name] = acc

    print(f"{name}: Accuracy = {acc:.4f}")

# 6. 验证方法二：K 折交叉验证

print("\n=== K-Fold Cross Validation (k=5) ===")
kf = KFold(n_splits=5, shuffle=True, random_state=42)
kfold_results = {}

for name, model in models.items():
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", model)
    ])

    scores = cross_val_score(pipeline, X, y, cv=kf)
    kfold_results[name] = scores.mean()

    print(f"{name}: Mean Accuracy = {scores.mean():.4f}")

# 7. 验证方法三：分层 K 折交叉验证

print("\n=== Stratified K-Fold Cross Validation (k=5) ===")
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
skfold_results = {}

for name, model in models.items():
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", model)
    ])

    scores = cross_val_score(pipeline, X, y, cv=skf)
    skfold_results[name] = scores.mean()

    print(f"{name}: Mean Accuracy = {scores.mean():.4f}")

# 8. 结果对比表格

results_df = pd.DataFrame({
    "Hold-out": holdout_results,
    "K-Fold": kfold_results,
    "Stratified K-Fold": skfold_results
})

print("\n=== 模型性能对比结果 ===")
print(results_df)

# 9. 结果可视化（柱状图）

results_df.plot(kind="bar", figsize=(10, 6))
plt.title("Comparison of Three Classification Algorithms")
plt.ylabel("Accuracy")
plt.ylim(0.8, 1.0)
plt.xticks(rotation=0)
plt.grid(axis="y")
plt.show()
