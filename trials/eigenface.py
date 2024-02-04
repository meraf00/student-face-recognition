import numpy as np
from collections import Counter


def knn_classifier(projections, labels, x, k=5, log=False):
    distances = [np.linalg.norm(x - pi) for pi in projections]
    indices = np.argsort(distances)[:k]

    k_nearest_labels = [labels[i] for i in indices]
    majority_vote = Counter(k_nearest_labels).most_common(1)

    label = majority_vote[0][0]

    if log:
        print(majority_vote)

    return label, distances[indices[0]]


def calculate_pca(X, num_components):
    n, _ = X.shape

    num_components = min(num_components, n)

    mean = np.mean(X, axis=0)

    centered_data = X - mean

    L = np.dot(centered_data, centered_data.T)

    eigenvalues, eigenvectors = np.linalg.eig(L)

    eigenvectors = np.dot(centered_data.T, eigenvectors)

    for i in range(n):
        eigenvectors[:, i] = eigenvectors[:, i] / np.linalg.norm(eigenvectors[:, i])

    idx = np.argsort(-eigenvalues)
    eigenvalues, eigenvectors = eigenvalues[idx], eigenvectors[:, idx]

    return eigenvalues[:num_components], eigenvectors[:, :num_components], mean


def project(W, X, mean):
    return np.dot(X - mean, W)


def reconstruct(W, Y):
    return np.dot(Y, W.T)


def compute_threshold(projections):
    n = len(projections)

    max_dist = float("-inf")

    for i in range(n):
        for j in range(i + 1, n):
            dist = np.linalg.norm(projections[i] - projections[j])
            max_dist = max(max_dist, dist)

    return max_dist


def closest_face(projections, projection_labels, p):
    distances = [np.linalg.norm(p - pi) for pi in projections]

    sorted_distances_idx = np.argsort(distances)

    return (
        projection_labels[sorted_distances_idx[0]],
        distances[sorted_distances_idx[0]],
    )


class EigenFaces:
    def __init__(self, num_components=100, k=5):
        self.num_components = num_components
        self.k = k

    def fit(self, x_train, y_train):
        self.projection_labels = y_train

        self.eigenvalues, self.eigenvectors, self.mean_face = calculate_pca(
            x_train, self.num_components
        )

        projections = []

        for image in x_train:
            projections.append(
                project(self.eigenvectors, image.reshape(1, -1), self.mean_face)
            )

        self.projections = np.array(projections)

        self.threshold = compute_threshold(projections)

        return self

    def transform(self, X, log=False):
        y_pred = []

        for image in X:
            image = image.reshape(1, -1)

            p = project(self.eigenvectors, image, self.mean_face)

            prediction, dist = knn_classifier(
                self.projections, self.projection_labels, p, self.k, log
            )

            reconstructed = reconstruct(self.eigenvectors, p)

            rec_dist = np.linalg.norm((image - self.mean_face) - reconstructed)

            if rec_dist >= self.threshold:
                y_pred.append("NotFace")

            elif dist >= self.threshold:
                y_pred.append("NewFace")

            else:
                y_pred.append(prediction)

        return np.array(y_pred)
