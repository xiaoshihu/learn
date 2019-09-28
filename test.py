# -*- coding: utf-8 -*-

"""
    @author: xiaoshihu
    @file: use.py
    @time: 2019/6/25 15:33
    @desc:
"""
from typing import List
import copy
# from graphviz import Digraph

class node_name:

    def __init__(self,name,port):
        self.name = name
        self.port = port

    def __repr__(self):
        return '{}-{}'.format(self.name,self.port)

    def __eq__(self, other):
        return self.name == other.name

class node:
    '''抽象出来的单板对象'''

    def __init__(self, point):
        '''
        利用传递进来的节点信息生成节点对象

        :param point: 节点信息
        '''
        self.next:List[node_name] = []
        self.parse(point)

    def parse(self,point):
        name,next = point.split('&&')
        self.name = node_name('-'.join(name.split('-')[:-1]),name.split('-')[-1])
        self.next.append(node_name('-'.join(next.split('-')[:-1]),next.split('-')[-1]))

    def addnext(self, next):
        self.next.append(next)

    def __repr__(self):
        return 'name:{},next:{}'.format(self.name,self.next)

    def __eq__(self, other):
        return self.name == other.name

class tran:
    def __init__(self,start,mylist:list):
        '''
        传递第一个节点和整个列表，初始化对象

        :param start: 第一个节点
        :param mylist: 节点列表
        '''
        # self.dot = Digraph(comment='The Round Table')
        self.strat = start
        # 对列表进行排序
        mylist.sort()
        self.mylist = mylist
        self.node_list:List[node] = []
        self.selfcheck = []
        # 这个里面保存所有的路径。
        # self.node_sort = []
        self.pre = ''
        self.deal_list()
        self.chain()
        print('alone:{}'.format(self.copy_list))
        print('self-check:{}'.format(self.selfcheck))
        # self.dot.save('round-table.gv')

    def __repr__(self):
        return '{}'.format(self.node_list)

    # 将每条光纤传递的路径都打印出来
    def chain(self):
        start_node = node(self.strat)
        start_index = self.node_list.index(start_node)
        tmp = self.node_list[start_index]
        self.node_list[start_index] = self.node_list[0]
        self.node_list[0] = tmp
        self.copy_list = copy.deepcopy(self.node_list[1:])
        self.create_chain([self.node_list[0]])

    def create_chain(self,next_node_list:List[node]):
        '''还没有达到我想要的效果，我想将所有的链条都打印出来'''
        # 不是很好弄，因为我想把分支表现出来
        # 这个前缀不是很好弄，
        if not next_node_list:
            print('{}end'.format(self.pre))
            # self.pre = self.pre[:-1]
            return
        out_str = '{}({})'.format(self.pre,next_node_list[0])
        print(out_str)
        if len(next_node_list[0].next) >1:
            self.pre += '--'
        for sig_node in next_node_list:
            next_name_list = sig_node.next
            for i in next_name_list:
                _next_node = []
                for _node in self.node_list:
                    if i == _node.name:
                        _next_node.append(_node)
                        try:
                            self.copy_list.remove(_node)
                        except:
                            pass
                        # self.dot.edge(sig_node.name,_node.name)
                # 首先将一条路径走完是正确的
                self.create_chain(_next_node)

    def deal_list(self):
        '''对传入进来的列表进行处理'''
        next:node = None
        for i in self.mylist:
            new_node = node(i)
            # 去掉自检
            if new_node.name.name == new_node.next[0].name:
                self.selfcheck.append(new_node)
                continue
            if next:
                if new_node == next:
                    next.addnext(new_node.next[0])
                    continue
            self.node_list.append(new_node)
            next = new_node

if __name__ == '__main__':
    # mylist = ['a&c', 'c&b', 'b&d', 'd&f', 'f&j','b&g','g&d','g&h','h&d','d&p','p&f']
    mylist = ['9-93&5-11sfiu-3&&9-93&13-12obu1-4','9-93&13-12obu1-2&&9-93&10-itl-1','9-93&13-12obu1-5&&9-93&13-12obu1-4','1-5&6-11sfiu-1&&9-93&5-11sfiu-1','1-5&7-itl-1&&1-5&5-13oau1-7','1-5&5-13oau1-8&&1-5&5-13oau1-1','1-5&5-13oau1-4&&1-5&6-11sfiu-3']
    start = '1-5&7-itl-1&&1-5&5-13oau1-7'
    # print(len(mylist))
    tran(start,mylist)
