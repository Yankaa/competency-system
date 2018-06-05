from typing import TypeVar, List, Callable, NoReturn
from scipy.cluster.hierarchy import linkage, fcluster
from numpy import array, ndarray, linalg, dot


def _mean(vectors: List[ndarray]) -> ndarray:
    vector = array(vectors).mean(axis=0)
    return vector / linalg.norm(vector)


def similarity(a: ndarray, b: ndarray) -> float:
    return dot(a, b)


threshold = 0.8


# should have `vector` and `amount` fields
T = TypeVar('T')


def mean_vector(cluster: List[T]) -> ndarray:
    return _mean([object.vector * (object.amount or 1) for object in cluster])


def clusters_init(objects: List[T], union_cluster: Callable[[List[T]], T]):
    vectors = array([object.vector for object in objects])
    hierarchy = linkage(vectors, method='average')
    cluster_indexes: ndarray = fcluster(hierarchy, t=1-threshold, criterion='distance')
    clusters: List[List[T]] = [[] for _ in range(max(cluster_indexes))]
    for object, cluster_index in zip(objects, cluster_indexes):
        clusters[cluster_index-1].append(object)
    for cluster in clusters:
        amount = len(cluster)
        if amount > 1:
            vector = mean_vector(cluster)
            competency = union_cluster(cluster)
            competency.vector = vector
            competency.amount = amount
        else:
            cluster[0].amount = 1


def clusters_append(old_objects: List[T], new_objects: List[T], append_to_cluster: Callable[[T, T], NoReturn]):
    for new_object in new_objects:
        best_similarity, best_object = max((similarity(new_object.vector, old_object.vector), old_object) for old_object in old_objects)
        if best_similarity < threshold:
            new_object.amount = 1
            old_objects.append(new_object)
        else:
            best_object.vector = mean_vector([best_object, new_object])
            best_object.amount += 1
            append_to_cluster(best_object, new_object)


def clusters_update(objects: List[T], union_cluster: Callable[[List[T]], T], append_to_cluster: Callable[[T, T], None]):
    old_objects = []
    new_objects = []

    for object in objects:
        (old_objects if object.amount != 0 else new_objects).append(object)

    if old_objects:
        clusters_append(old_objects, new_objects, append_to_cluster)
    else:
        clusters_init(new_objects, union_cluster)
