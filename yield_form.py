# BEGIN YIELD_FROM_AVERAGER
from collections import namedtuple

Result = namedtuple('Result', 'count average')


# the subgenerator
def averager():  # <1>
    total = 0.0
    count = 0
    average = None
    while True:
        # 预激会执行到这里，然后停止住，term等待从调用方传递进来得值
        term = yield  # <2>
        if term is None:  # <3>
            break
        total += term
        count += 1
        average = total / count
    # 这个值会传递到委托方里面去
    return Result(count, average)  # <4>


# the delegating generator
def grouper(results, key):  # <5>
    # 这里的循环有什么作用吗？
    # while True:  # <6>
    results[key] = yield from averager()  # <7>


# the client code, a.k.a. the caller
def main(data):  # <8>
    results = {}
    # 直接循环字典，这种用法还是不错得，可以循环取里面得键和值
    for key, values in data.items():
        group = grouper(results, key)  # <9>
        # 预激委托方。委托方会直接预激子生成器
        next(group)  # <10>
        # 预激活之后，后面调用方使用得send会直接和子生成器打交道，子生成器得返回值也会直接返回给调用方
        for value in values:
            group.send(value)  # <11>
        # 手动结束子生成器
        group.send(None)  # important! <12>

    # print(results)  # uncomment to debug
    report(results)


# output report
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            result.count, group, result.average, unit))


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}

if __name__ == '__main__':
    main(data)

# END YIELD_FROM_AVERAGER