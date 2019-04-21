import argparse
import collections
import queue
import random

# 基本上这个文件都已经看懂了，但是有一点不是很清楚，就是，这里怎么就实现了并发了模拟？怎么体现事件驱动的？
# 理一下怎么是想怎么实现事件驱动，就是一个主线程里面一直有一个循环，这个循环不间断的遍历一些东西，当这些
# 东西能够使用的时候，就去处理它，这个时候会产生新的线程或者进程，然后让这些进程或者线程去处理具体的事务，之前看的
# 书上的例子都是这样写的，那就是比较传统的服务器的类型，之后接触到的异步服务器是完全不一样的，理论上只有一个线程就
# 可以实现多io类型请求的并发，先不说系统内核支持的套接字监听， 当当从生成器的特性说起，这个例子还是没有体现并发的概念
# 只有多个套接字的时候，才能很好的说明并发是怎么在一个线程里面实现的，当然，协程如果离开异步网路编程，基本上
# 也看不出什么实际的意义。所以，举例子最好是使用多个套接字，或者linux内核支持的管道和文件，就是支持系统层面上
# 的系统能提供监听操作的操作。但是异步操作一定不要去处理cpu密集型的任务，因为，是会造成阻塞的，也可以和多进程和
# 多线程结合起来使用，实现处理cpu任务密集型的任务。现在脑子里面好像是把这些东西弄清楚了。
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
    # 第二个参数应该是搭乘乘客的数量
    """Yield to simulator issuing event at each state change"""
    # 不要在用生成器的观点去考虑这个位置，这个就是一个控制点
    time = yield Event(start_time, ident, 'leave garage')  # <2>
    # 因为这里里面必要要有一个循环的事件，才能一直不停的处理，写表达式就是为了传递值
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
        # 一个元组的数列,所以这里会返回一个按照出租车序号排序的数列
        '''
        eg:
        test = {0: 2, 1: 4, 2: 6, 3: 8, 4: 10, 5: 12, 6: 14, 7: 16, 10: 18, 9: 20}
        sorted(test.items()) 
        >>>[(0, 2),(1, 4),(2, 6),(3, 8),(4, 10),(5, 12),(6, 14),(7, 16),(9, 20),(10, 18)]
        '''
        # 预激所有的出租车生成器，然后将所有包含开始时间的具名元组添加到队列里面去
        for _, proc in sorted(self.procs.items()):  # <2>
            # 第一个参数是出租车的序号，第二个参数是生成器，第一个参数后面不需要用到，所以用下划线来表示
            # 对生成器进行预激
            # first_event接受了生成器返回的值Event(start_time, ident, 'leave garage')
            # 一个具名元组，里面都是出租车开始的时间
            first_event = next(proc)  # <3>
            # 将预激的生成器送入队列里面
            # 这里之前描述错误，这里并不是生成器，
            self.events.put(first_event)  # <4>

        # main loop of the simulation
        sim_time = 0  # <5>
        # 事件会一直循环，直到大于规定的时间
        while sim_time < end_time:  # <6>
            # 如果队列空了，就退出循环
            if self.events.empty():  # <7>
                print('*** end of events ***')
                break

            # 从队列中获取最新添加进去的数据，会直接将里面的数据取出来，然后队列里面就会少一个数据
            current_event = self.events.get()  # <8>
            # 三个参数分别代表的是，时间，出租车序号，出租车的动作
            sim_time, proc_id, previous_action = current_event  # <9>
            # 这里用来区别每一个出租车的输出信息
            print('taxi:', proc_id, proc_id * '#', current_event)  # <10>
            # 获取对应序号的出租车生成器对象
            active_proc = self.procs[proc_id]  # <11>
            # 后面的函数应该是生成一个随机数
            next_time = sim_time + compute_duration(previous_action)  # <12>

            try:
                # 触发生成器进行下面的步骤，将next_time传递给函数里面的time，并且将返回的具名元组赋值给next_event
                next_event = active_proc.send(next_time)  # <13>
            except StopIteration:
                # 搭车的乘客数量够了之后，就会触发这个异常，并且从字典中将这个出租车删除掉
                del self.procs[proc_id]  # <14>
            # 在没有出现异常的情况下才会执行下面的语句
            else:
                # 将最新获取到的具名元组，也就是说明了出租车现在的运营状态
                self.events.put(next_event)  # <15>
        # 这里的else和dinally的作用有点类似
        else:  # <16>
            # 只有在循环是以正常的运行状态退出的时候，也就是while循环是条件不成立的情况下退出，for循环，是迭代完成之后
            # 退出，里面如果使用break退出的话，else里面的语句是不会执行的
            msg = '*** end of simulation time: {} events pending ***'
            # 获取队列里面的元素的个数
            print(msg.format(self.events.qsize()))


# END TAXI_SIMULATOR

# 这个应该是生成一个随机的时间，代表乘客的路程时间。
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
    return int(random.expovariate(1 / interval)) + 1


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
    taxis = {i: taxi_process(i, (i + 1) * 2, i * DEPARTURE_INTERVAL) for i in range(num_taxis)}
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
    # 这里应该是自己回去获取命令行里面输入的参数。比之前那种方式确实是要好很多。
    args = parser.parse_args()
    # 所以这里就传递了相应的参数，上面的用法还是比较好用的。
    main(args.end_time, args.taxis, args.seed)
