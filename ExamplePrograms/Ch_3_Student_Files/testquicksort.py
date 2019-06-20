"""
File: testquicksort.py

Tests the quicksort algorithm
"""


def quicksort(lyst):
    quicksortHelper(lyst, 0, len(lyst) - 1)

# 为什么我总觉得这里的递归实现的有点奇怪？
def quicksortHelper(lyst, left, right):
    # 确实很巧妙，
    if left < right:
        # 其实这里返回的是基准点在集合中排序之后的位置
        pivotLocation = partition(lyst, left, right)
        # 递归两次？
        # 已经排序完成的就不管了
        # 对左边部分进行排序
        quicksortHelper(lyst, left, pivotLocation - 1)
        # 对右边部分进行同样的排序
        quicksortHelper(lyst, pivotLocation + 1, right)


def partition(lyst, left, right):
    # Find the pivot and exchange it with the last item
    # 找到中点
    middle = (left + right) // 2
    # 获取基准点
    pivot = lyst[middle]
    # 与最右边的项进行交换
    lyst[middle] = lyst[right]
    lyst[right] = pivot
    # Set boundary point to first position
    # 最左边的项作为边界，总感觉这里有问题
    boundary = left
    # Move items less than pivot to the left
    # 对整个区间进行扫描
    # 并不是冒泡排序，而是，将边界与其他的位置的值交换，实现了分层
    for index in range(left, right):
        # 总感觉这里是在冒泡排序？
        # 所有的值与基准点的值进行比较，所以，复杂度最小是 n
        if lyst[index] < pivot:
            swap(lyst, index, boundary)
            boundary += 1
    # Exchange the pivot item and the boundary item
    # 将边界与基准点互换
    swap(lyst, right, boundary)
    return boundary


def swap(lyst, i, j):
    """Exchanges the items at positions i and j."""
    # You could say lyst[i], lyst[j] = lyst[j], lyst[i]
    # but the following code shows what is really going on
    temp = lyst[i]
    lyst[i] = lyst[j]
    lyst[j] = temp


import random

# 使用这种方式不管怎么样看都觉得十分之奇怪
def main(size=20, sort=quicksort):
    lyst = [random.randint(1, 1000) for i in range(size)]
    print(lyst)
    # 对列表进行排序
    sort(lyst)
    print(lyst)


if __name__ == "__main__":
    main()
