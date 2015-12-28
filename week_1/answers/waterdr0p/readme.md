#PEP8 风格检查
pip3 install pylint
pylint mymodule.py
pip install pep8
pep8 qq_getrandbits.py > pep8.txt

#优化结论
len函数：len(largeSet) 在海量循环时，并不会比计数器更消耗资源，且代码量更少
集合操作：海量数据集合操作时，占用内存不能太小，导致频繁IO,性能下降; 也不能太大，导致集会计算性能下降
file.write(): wf.write(''.join(list(inputX)[:end])) 比wf.writelines(list(inputX)[:end]))远远优化的多

#python3 64bit window 运行最佳结果
start at: Sun Dec 27 22:24:33 2015
processed: 16777215     used: 9.66s     sum: 30.75s
processed: 33272733     used: 18.29s    sum: 70.09s
processed: 49492755     used: 26.49s    sum: 117.86s
processed: 65438592     used: 34.4s     sum: 173.34s
processed: 81119224     used: 42.66s    sum: 237.17s
processed: 100000000    used: 71.3s     sum: 308.46s
processed 100000000 items !

processed: 1000000      used: 1.31s     sum: 312.77s
processed 1000000 items !

intersection used:      47.23s
difference used:        61.31s
union used:             15.75s
seconds used:           437.18s

#1亿数据生成算法描述
随机数生成：random.getrandbits(30)
内存管理：每次循环生成block 变量大小的数据，block = 0xffffff = 16777215约1556.2MB
重复过滤：block大小的数据使用s = set() 来过滤重复
重复过滤：集合 s 数据写入output文件中，写之前，循环遍历setB=set(output.readlines(size))，并使用s - setB 来去重，遍历完成后写数据

#交并差算法描述
交：两个文件使用双重while循环，遍历s.update(set(rf0.readlines(size)) & set(rf1.readlines(size)))来处理交集，内层循环完毕写文件
差：两个文件使用双重while循环，
外层循环block0 = set(rf0.readlines(size))
遍历block1 = set(rf1.readlines(size)))
 block0 -= block1 来处理差集，内层循环完毕写文件
并：difference.txt+b.txt直接合并
