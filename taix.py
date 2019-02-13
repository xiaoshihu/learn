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

Event = collections.namedtuple('Event', 'time proc action')


# BEGIN TAXI_PROCESS
def taxi_process(ident, trips, start_time=0):  # <1>
    """Yield to simulator issuing event at each state change"""
    time = yield Event(start_time, ident, 'leave garage')  # <2>
    for i in range(trips):  # <3>
        time = yield Event(time, ident, 'pick up passenger')  # <4>
        time = yield Event(time, ident, 'drop off passenger')  # <5>

    yield Event(time, ident, 'going home')  # <6>
    # end of taxi process # <7>
# END TAXI_PROCESS


# BEGIN TAXI_SIMULATOR
class Simulator:

    def __init__(self, procs_map):
        self.events = queue.PriorityQueue()
        self.procs = dict(procs_map)

    def run(self, end_time):  # <1>
        """Schedule and display events until time is up"""
        # schedule the first event for each cab
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


def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS,
         seed=None):
    """Initialize random generator, build procs and run simulation"""
    if seed is not None:
        random.seed(seed)  # get reproducible results

    taxis = {i: taxi_process(i, (i+1)*2, i*DEPARTURE_INTERVAL)
             for i in range(num_taxis)}
    sim = Simulator(taxis)
    sim.run(end_time)


if __name__ == '__main__':

    # 这个方法值得学习，以后需要传递的参数都使用这种方式
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