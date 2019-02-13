import random
import collections
import queue
import argparse
import time

# 一些全局参数
DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIME = 180
SEARCH_DURATION = 5
TRIP_DURATION = 20
DEPARTURE_INTERVAL = 5

# 具名元组，这个元组的名称就叫做Event，元组里面有三个值，这三个值都是用自己的属性的名称的
Event = collections.namedtuple('Event', 'time proc action')


# BEGIN TAXI_PROCESS
def taxi_process(ident, trips, start_time=0):  # <1>
    """Yield to simulator issuing event at each state change"""
    # 不要在用生成器的观点去考虑这个位置，这个就是一个控制点
    time = yield Event(start_time, ident, 'leave garage')  # <2>
    for i in range(trips):  # <3>
        # 乘客上下的控制点
        time = yield Event(time, ident, 'pick up passenger')  # <4>
        time = yield Event(time, ident, 'drop off passenger')  # <5>

    # 最后一个控制点
    yield Event(time, ident, 'going home')  # <6>
    # end of taxi process # <7>
# END TAXI_PROCESS


# BEGIN TAXI_SIMULATOR
class Simulator:

    def __init__(self, procs_map):
        # 优先级队列，里面元素是有优先级别的
        self.events = queue.PriorityQueue()
        self.procs = dict(procs_map)

    def run(self, end_time):  # <1>
        """Schedule and display events until time is up"""
        # schedule the first event for each cab
        # 下划线基本上就是用来作为不需要使用的参数的，跟匿名函数是差不多的作用
        # 对字典里面的东西进行排序，但是是怎么排序的呢
        # 如果sorted函数里面排序的项目是字典，那么最终会返回按照字典里面的key值排好顺序的，并且键值对变成
        # 一个元组的数列
        '''
        eg:
        test = {0: 2, 1: 4, 2: 6, 3: 8, 4: 10, 5: 12, 6: 14, 7: 16, 10: 18, 9: 20}
        sorted(test.items()) 
        >>>[(0, 2),(1, 4),(2, 6),(3, 8),(4, 10),(5, 12),(6, 14),(7, 16),(9, 20),(10, 18)]
        '''
        for _, proc in sorted(self.procs.items()):  # <2>
            first_event = next(proc)  # <3>
            self.events.put(first_event)  # <4>

        # main loop of the simulation
        sim_time = 0  # <5>
        while sim_time < end_time:  # <6>
            if self.events.empty():  # <7>
                print('*** end of events ***')
                break

            current_event = self.events.get()  # <8>
            sim_time, proc_id, previous_action = current_event  # <9>
            print('taxi:', proc_id, proc_id * '   ', current_event)  # <10>
            active_proc = self.procs[proc_id]  # <11>
            next_time = sim_time + compute_duration(previous_action)  # <12>
            try:
                next_event = active_proc.send(next_time)  # <13>
            except StopIteration:
                del self.procs[proc_id]  # <14>
            else:
                self.events.put(next_event)  # <15>
        else:  # <16>
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))
# END TAXI_SIMULATOR


def compute_duration(previous_action):
    """Compute action duration using exponential distribution"""
    if previous_action in ['leave garage', 'drop off passenger']:
        # new state is prowling
        interval = SEARCH_DURATION
    elif previous_action == 'pick up passenger':
        # new state is trip
        interval = TRIP_DURATION
    elif previous_action == 'going home':
        interval = 1
    else:
        raise ValueError('Unknown previous_action: %s' % previous_action)
    return int(random.expovariate(1/interval)) + 1


# 函数里面也指定了默认值了的
def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS,
         seed=None):
    """Initialize random generator, build procs and run simulation"""
    if seed is not None:
        # 这个东西使得随机数可以预测，但是，我需要用到随机数为什么要让这个东西可预测？
        random.seed(seed)  # get reproducible results

    # 字典推导式，看看得到的是一个什么结果，第一个参数是序号，第二个参数是还不知道，第三个参数是出租车的出发时间
    # 字典推导式我之前还没有使用过
    # 生成了一个序号对应taix生成器的键值对的字典
    taxis = {i: taxi_process(i, (i+1)*2, i*DEPARTURE_INTERVAL) for i in range(num_taxis)}
    # 这些推导式在新建数据结构的时候真的好用，以后需要自己注意一点，但是仅仅只使用于在新建数据的时候
    # taxis = {i: (i+1)*2 for i in range(10)}
    sim = Simulator(taxis)
    sim.run(end_time)


if __name__ == '__main__':

    # TODO:这个方法值得学习，以后需要传递的参数都使用这种方式
    parser = argparse.ArgumentParser(
                        description='Taxi fleet simulator.')
    # 这些就是添加的选项，前面是选项的缩写，第二项是具名元组的属性名称，第三个是默认的初始值，最后一个是说明信息
    parser.add_argument('-e', '--end-time', type=int,
                        default=DEFAULT_END_TIME,
                        help='simulation end time; default = %s'
                        % DEFAULT_END_TIME)
    parser.add_argument('-t', '--taxis', type=int,
                        default=DEFAULT_NUMBER_OF_TAXIS,
                        help='number of taxis running; default = %s'
                        % DEFAULT_NUMBER_OF_TAXIS)
    parser.add_argument('-s', '--seed', type=int, default=None,
                        help='random generator seed (for testing)')

    # 获取所有的参数，然后每一个参数就能使用属性的名称去调用，确实比之前的sys模块下面的东西好用多了，之后我的脚本其实也可以改变一下。
    # 获取的对象是一个具名元组，我之前想过用一个字典去实现类似的功能，现在看来别人有了更好的解决方法
    args = parser.parse_args()
    # 所以这里就传递了相应的参数，上面的用法还是比较好用的。
    main(args.end_time, args.taxis, args.seed)