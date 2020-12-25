import random
import time

# In most case, heapsort sort most slowly and quicksort is the most fast except python built-in sort method
# When dealing with the list with much more repeat numbers, quicksort sort it better than others
# how can built-in method sort every list so fast

def bubble_up_helper(list, i):
    if i is not 0:
        p = (i - 1) // 2
        if list[i] > list[p]:
            temp = list[p]
            list[p] = list[i]
            list[i] = temp
            bubble_up_helper(list, p)


def bubble_down_helper(list, i, last):
    left_child = i * 2 + 1
    right_child = i * 2 + 2
    if left_child < last and list[i] < list[left_child]:
        if right_child < last and list[i] < list[right_child]:
            if list[right_child] > list[left_child]:
                temp = list[right_child]
                list[right_child] = list[i]
                list[i] = temp
                bubble_down_helper(list, right_child, last)
            else:
                temp = list[left_child]
                list[left_child] = list[i]
                list[i] = temp
                bubble_down_helper(list, left_child, last)
        else:
            temp = list[left_child]
            list[left_child] = list[i]
            list[i] = temp
            bubble_down_helper(list, left_child, last)
    elif right_child < last and list[i] < list[right_child]:
        temp = list[right_child]
        list[right_child] = list[i]
        list[i] = temp
        bubble_down_helper(list, right_child, last)


def heap_sort(list):
    for i in range(len(list)):
        bubble_up_helper(list, i)
    for i in range(len(list)):
        temp = list[len(list) - 1 - i]
        list[len(list) - 1 - i] = list[0]
        list[0] = temp
        bubble_down_helper(list, 0, len(list) - 1 - i)
    return list


def merge_sort(list):
    n = len(list)
    if n > 1:
        list1 = list[:n // 2]
        list2 = list[n // 2:]
        merge_sort(list1)
        merge_sort(list2)
        merge(list1, list2, list)
    return list


def merge(list1, list2, list):
    f1 = 0
    f2 = 0
    while f1 + f2 < len(list):
        if f1 == len(list1):
            list[f1 + f2] = list2[f2]
            f2 += 1
        elif f2 == len(list2):
            list[f1 + f2] = list1[f1]
            f1 += 1
        elif list2[f2] < list1[f1]:
            list[f1 + f2] = list2[f2]
            f2 += 1
        else:
            list[f1 + f2] = list1[f1]
            f1 += 1


def quick_sort(list1, start, end):
    if start < end:
        i = start
        j = end
        pivot = list1[start]
        swap_pivot = i
        while i < j:
            while i <= end and list1[i]<=pivot:
                swap_pivot = i
                i += 1
            while j > start and list1[j]>=pivot:
                j -= 1
            if i < j:
                temp = list1[i]
                list1[i] = list1[j]
                list1[j] = temp
                swap_pivot = i
        list1[start] = list1[swap_pivot]
        list1[swap_pivot] = pivot
        quick_sort(list1, start, swap_pivot-1)
        quick_sort(list1, swap_pivot+1, end)
    return list1

def evaluatepartial(n, k):
    list1 = [0] * (n-k)
    for i in range(n - k):
        a = random.randint(1, 1000000)
        list1[i] = a
    for j in range(k):
        shuffle_number = random.randint(0, n - k - 1)
        list1.append(list1[shuffle_number])
    list1.sort()
    for b in range(n//20):
        pos1 = random.randint(0,n-1)
        pos2 = random.randint(0,n-1)
        temp = list1[pos1]
        list1[pos1] = list1[pos2]
        list1[pos2] = temp
    return list1

def evaluateall(n, k):
    list1 = [0] * (n-k)
    for i in range(n - k):
        a = random.randint(0, 1000000)
        list1[i] = a
    for j in range(k):
        shuffle_number = random.randint(0, n - k - 1)
        list1.append(list1[shuffle_number])
    list_group = []
    for i in range(10):
        list_copy = list1.copy()
        random.shuffle(list_copy)
        list_group.append(list_copy)
    return list_group


def test(list_pool, n, k):
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sum4 = 0
    sum5 = 0
    sum6 = 0
    sum7 = 0
    sum8 = 0
    for i in list_pool:
        start_time = time.time()
        j = i.copy()
        heap_sort(j)
        end_time = time.time()
        duration1 = end_time - start_time
        sum1 = duration1 + sum1

        start_time = time.time()
        j = i.copy()
        merge_sort(j)
        end_time = time.time()
        duration2 = end_time - start_time
        sum2 = duration2 + sum2

        start_time = time.time()
        j = i.copy()
        random.shuffle(j)
        quick_sort(j, 0, len(j) - 1)
        end_time = time.time()
        duration3 = end_time - start_time
        sum3 = duration3 + sum3


        start_time = time.time()
        j = i.copy()
        j.sort()
        end_time = time.time()
        duration4 = end_time - start_time
        sum4 = duration4 + sum4


        list_partial = evaluatepartial(n,k)

        start_time = time.time()
        j = list_partial.copy()
        heap_sort(j)
        end_time = time.time()
        duration5 = end_time - start_time
        sum5 = duration5 + sum5


        start_time = time.time()
        j = list_partial.copy()
        merge_sort(j)
        end_time = time.time()
        duration6 = end_time - start_time
        sum6 = duration6 + sum6

        start_time = time.time()
        j = list_partial.copy()
        random.shuffle(j)
        quick_sort(j, 0, len(j) - 1)
        end_time = time.time()
        duration7 = end_time - start_time
        sum7 = duration7 + sum7

        start_time = time.time()
        j = list_partial.copy()
        j.sort()
        end_time = time.time()
        duration8 = end_time - start_time
        sum8 = duration8 + sum8

    print("%f heapsort %d %d" % (sum1/10, n, k))
    print("%f mergesort %d %d" % (sum2/10, n, k))
    print("%f quicksort %d %d" % (sum3/10, n, k))
    print("%f python %d %d" % (sum4/10, n, k))
    print("%f heapsort %d %d p" % (sum5/10, n, k))
    print("%f mergesort %d %d p" % (sum6/10, n, k))
    print("%f quicksort %d %d p" % (sum7/10, n, k))
    print("%f python %d %d p" % (sum8/10, n, k))

    print("\n")

def evaluate(n, k):
    test(evaluateall(n, k), n, k)

evaluate(100,0)
evaluate(1000,0)
evaluate(10000,0)
evaluate(100000,0)
evaluate(100,20)
evaluate(1000,200)
evaluate(10000,2000)
evaluate(100000,20000)
evaluate(100,70)
evaluate(1000,700)
evaluate(10000,7000)
evaluate(100000,70000)
