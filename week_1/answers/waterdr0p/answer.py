#!/usr/bin/env python3
# coding: utf-8
# 2015-12-25 14:30:23
# getrandbits   #重复率10.71%

from random import getrandbits
from time import time, ctime
from os import popen
from os.path import getsize, exists
from platform import platform
from sys import exit


def gen_qq_numbers(m, n, k, output):
    """
    用于生成QQ号的函数, 即[m, n]区间内k个不重复的等概率随机数。
    :param m: int, 所生成的QQ号须大于正整数 m, 大于等于10000
    :param n: int, 所生成的QQ号须小于正整数 n, 小于等于999999999
    :param k: int, 一共生成 k 个QQ号
    :param output: string, 文件名，生成结果保存至output中， 每行一个QQ号
    """
    global t0
    lenbits = len(bin(n)[2:])
    # 0xffffff = 16777215 -> 1556.2MB
    block = 0xffffff
    processed = 0
    s = set()
    endflag = False
    with open(output, 'w'):
        pass
    if k < block:
        endflag = True
        block = k

    while processed != k and (not endflag):
        ele = getrandbits(lenbits)
        if ele >= m and ele <= n:
            s.add(str(ele)+'\n')

        if len(s) % block == 0:
            t1 = time()
            try:
                processed += uniprocess(s, output)
            except:
                print('Memory Error! Try again!')
                block = int(block*0.9)
            s = set()
            print('processed: {}\tused: {}s\tsum: {}s'.format(
                        processed,
                        round(time() - t1, 2),
                        round(time()-t0, 2)))
            if (k - processed) < block*1.5:
                endflag = True
                break

    if endflag:
        t1 = time()
        s = set()
        lastpad = k - processed + int(block*0.1)
        last = k - processed
        while len(s) != lastpad:
            s.add(str(getrandbits(lenbits))+'\n')
        try:
            processed += uniprocess(s, output, end=last)
        except:
            print('Memory Error! Try again!')
            tmpSet = set([s.pop() for i in range(int(len(s)/2))])
            processed += uniprocess(s, output, end=int(last/2))
            last = k - processed
            processed += uniprocess(tmpSet, output, end=last)
        print('''processed: {}\tused: {}s\tsum: {}s'''.format(
            processed,
            round(time() - t1, 2),
            round(time()-t0, 2)))
    print('processed', processed, 'items !\n')


def uniprocess(inputX, output, end=False):
    """文本数据去重
    :param inputX: set，需要去重处理的集合
    :param output: string,文件名，处理后写集合的文件
    :param end: 末尾处理标志，值为False 或 未处理的数据个数
    """
    rf = open(output)
    done = False
    size = len(inputX)*2
    while not done:
        # readlines(10**8) --> 708MB
        block = set(rf.readlines(size))
        inputX -= block
        if not block:
            done = True
    wf = open(output, 'a+')
    if not end:
        wf.write(''.join(inputX))
        return len(inputX)
    else:
        wf.write(''.join(list(inputX)[:end]))
        return end
    wf.close()


def main(FN0, FN1):
    '''实现并、交、差setA - setB运算
    2.a.txt 中有 1 亿个， b.txt 中有 100 万个乱序排列的QQ号
    输出结果至union.txt, intersection.txt, difference.txt
    :param FN0: string , 需要处理的文件名, 较小的文件
    :param FN1: string , 需要处理的文件名，较大的文件
    '''
    if (not exists(FN0)) and (not exists(FN1)):
        print('OSError: file "%s" or  "%s" not exists, please check !')
        exit()
    if getsize(FN0) > getsize(FN1):
        FN0, FN1 = FN1, FN0
    rf1 = open(FN1)
    wf_int = open('intersection.txt', 'w+')
    # 948.9/8MB
    size = 0xffffff

    # intersection
    t1 = time()
    rf0 = open(FN0)
    while True:
        set_int = set()
        block0 = set(rf0.readlines(size))
        while True:
            block1 = set(rf1.readlines(size))
            tmp = block0 & block1
            set_int.update(tmp)
            block0 -= tmp
            if not block1:
                break
        wf_int.write(''.join(set_int))
        if not block0:
            break
    print('intersection used:\t%ss' % round(time() - t1, 2))

    # difference
    t1 = time()
    rf1.seek(0)
    wf_int.seek(0)
    wf_dif = open('difference.txt', 'w+')
    while True:
        block0 = set(rf1.readlines(size))
        done = len(block0)
        while True:
            block1 = set(wf_int.readlines(size))
            block0 -= block1
            if not block1:
                break
        wf_dif.write(''.join(block0))
        if not done:
            break
    print('difference used:\t%ss' % round(time() - t1, 2))
    rf1.close()
    wf_dif.close()

    # union
    t1 = time()
    rf0.seek(0)
    os_type = platform().lower()
    if 'windows' in os_type:
        popen('copy difference.txt union.txt').read()
    else:
        popen('cp difference.txt union.txt').read()
    with open('union.txt', 'a+') as wf_uni:
        wf_uni.write(rf0.read())
    print('union used:\t\t%ss' % round(time() - t1, 2))
    wf_int.close()

if __name__ == '__main__':
    t0 = time()
    print('start at:', ctime())
    gen_qq_numbers(10000, 999999999, 10**8, 'a.txt')
    gen_qq_numbers(10000, 999999999, 10**6, 'b.txt')
    main('b.txt', 'a.txt')
    print('seconds used:\t\t%ss' % round(time() - t0, 2))
