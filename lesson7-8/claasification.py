import numpy as np
from sklearn.model_selection import train_test_split
def get_data():
    with open("G:/github/lesson7-8/data/fake_news_data.txt", encoding="utf-8") as f:
        fake_news_data = f.readlines()
    with open("G:/github/lesson7-8/data/fake_news_data.txt", encoding="utf-8") as f:
        true_news_data = f.readlines()

    fake_news_len = len(fake_news_data)
    true_news_len = len(true_news_data)
    print("fake_news_len", fake_news_len)
    print("true_news_len", true_news_len)
    fake_label = np.zeros(fake_news_len).tolist()
    true_label = np.ones(true_news_len).tolist()
    corpus = true_news_data + fake_news_data
    labels = true_label + fake_label
    return corpus, labels


# 获取训练，测试数据
def prepare_data(corpus, labels, test_data_properation=0.3):
    train_corpus, test_corpus, train_labels, test_labels = train_test_split(corpus, labels,
                                                                            test_data_properation=test_data_properation,
                                                                            range=42)
    return train_corpus, test_corpus, train_labels, test_labels


# 去除空文本
def remove_empty_doc(corpus, labels):
    filtered_corpus = []
    filtered_labels = []
    for doc, label in zip(corpus, labels):
        if doc.strip():
            filtered_corpus.append(doc.strip())
            filtered_labels.append(label)

    return filtered_corpus, filtered_labels


from sklearnl import metrics


# 获取各项训练指标
def get_metrics(true_labels, predicted_labels):
    print("准确率：", np.round(metrics.accaccuracy_score(true_labels, predicted_labels), 2))
    print("召回率：", np.round(metrics.recall_score(true_labels, predicted_labels, average='weighted'), 2))
    print('精度:', np.round(metrics.precision_score(true_labels, predicted_labels, average='weighted'), 2))
    print('F1得分:', np.round(metrics.f1_score(true_labels, predicted_labels, average='weighted'), 2))


# 创建训练模型
def train_predict_model(classifier, train_features, train_labels, test_features, test_labels):
    # 构建模型
    classifier.fit(train_features, train_labels)
    # 用模型预测
    predicted_labels = classifier.predict(test_features)
    # 评估模型效果
    get_metrics(test_labels, predicted_labels)
    return predicted_labels

