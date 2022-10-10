# -*- coding : utf-8-*-
from matplotlib import pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
import networkx as nx
from readcxl import cxl2graph,get_name


def ranking(nodes_c,rev=True):
    """根据节点中心性输出从大到小的排列
    输入为节点和重要性的字典，输出为排列后的节点和数值
    """
    dic2asc = sorted(nodes_c, key=nodes_c.__getitem__, reverse=rev)
    nodes_c_value = []
    for k in dic2asc:
        nodes_c_value.append(nodes_c[k])
    return dic2asc,nodes_c_value


def cal_ci_centrality(G,l):
    ci_dict = {}
    for node in G.nodes:
        ci = 0
        neighbor = nx.single_source_shortest_path_length(G, node)
        for item in neighbor:
            if neighbor[item] == l: ci += G.degree(item) - 1
            # if neighbor[item] == l: print('     ',get_name([item],name_dict))
        ci = (G.degree(node) - 1) * ci
        # print(node_name, ci)
        ci_dict[node] = ci

    return ci_dict




"""读数据"""
filename = "微积分核心概念和关系细节图.cxl"
G, name_dict = cxl2graph(filename)


"""test-度中心性"""
# c_degree = nx.degree_centrality(G)
# centrality_degree, centrality_degree_value = ranking(c_degree)
# centrality_degree = get_name(centrality_degree, name_dict)
# print('度中心性排序：',centrality_degree)
# print(c_degree)
# 迭代删点
giant_degree = []
G_degree = G.to_undirected()
total_steps = G_degree.number_of_nodes()-1
for p in range(total_steps):
    print('----STEP %d------'%(p))
    # max = 0
    print('剩余节点数：',G_degree.number_of_nodes())
    largest = max(nx.connected_components(G_degree), key=len)
    largest_connected_subgraph = G_degree.subgraph(largest)
    gc = largest_connected_subgraph.number_of_nodes()
    print('GC：',gc)
    giant_degree.append(gc)

    c_degree = nx.degree_centrality(G_degree)
    centrality_degree, centrality_degree_value = ranking(c_degree)

    G_degree.remove_node(centrality_degree[0])
    print('移除:',get_name([centrality_degree[0]],name_dict))







"""计算CI"""

# 设置球的半径
l=2

# 转为无向图
G_percolation = G.to_undirected()
giant = []
# 迭代删点
total_steps = G_percolation.number_of_nodes()-1
for p in range(total_steps):
    print('============STEP %d============='%(p))
    # max = 0
    print('剩余节点数：',G_percolation.number_of_nodes())
    largest = max(nx.connected_components(G_percolation), key=len)
    largest_connected_subgraph = G_percolation.subgraph(largest)
    gc = largest_connected_subgraph.number_of_nodes()
    print('GC：',gc)
    giant.append(gc)

    # ci_dict = {}
    # for node in G_percolation.nodes:
    #     ci = 0
    #     node_name = get_name([node],name_dict)
    #
    #     # print(G.degree(node))
    #     neighbor = nx.single_source_shortest_path_length(G_percolation,node)
    #     for item in neighbor:
    #         if neighbor[item]==l: ci += G_percolation.degree(item)-1
    #         # if neighbor[item] == l: print('     ',get_name([item],name_dict))
    #     ci = (G_percolation.degree(node)-1)*ci
    #     print(node_name,ci)
    #     ci_dict[node]=ci

    ci_dict = cal_ci_centrality(G_percolation,l)

    ci_rank , ci_value = ranking(ci_dict)
    G_percolation.remove_node(ci_rank[0])
    print('移除:',get_name([ci_rank[0]],name_dict))




'''自适应'''
# 转为无向图
G_percolation = G.to_undirected()
giant_auto = []
# 迭代删点
total_steps = G_percolation.number_of_nodes()-1
for p in range(total_steps):
    print('============STEP %d============='%(p))
    # max = 0
    print('剩余节点数：',G_percolation.number_of_nodes())
    largest = max(nx.connected_components(G_percolation), key=len)
    largest_connected_subgraph = G_percolation.subgraph(largest)
    gc = largest_connected_subgraph.number_of_nodes()
    print('GC：',gc)
    giant_auto.append(gc)
    # l = nx.diameter(largest_connected_subgraph)/2
    l = 1
    print(l)

    ci_dict = cal_ci_centrality(G_percolation,l)

    ci_rank , ci_value = ranking(ci_dict)
    G_percolation.remove_node(ci_rank[0])
    print('移除:',get_name([ci_rank[0]],name_dict))


"""介数中心性"""
giant_betweenness = []
G_betweenness = G.to_undirected()
total_steps = G_betweenness.number_of_nodes()-1
for p in range(total_steps):
    print('============Betweenness %d=============' % (p))
    largest = max(nx.connected_components(G_betweenness), key=len)
    largest_connected_subgraph = G_betweenness.subgraph(largest)
    gc = largest_connected_subgraph.number_of_nodes()
    print('GC：',gc)
    giant_betweenness.append(gc)

    c_betweenness = nx.betweenness_centrality(G_betweenness)
    centrality_betweenness, centrality_betweenness_value = ranking(c_betweenness)

    G_betweenness.remove_node(centrality_betweenness[0])
    print('移除:', get_name([centrality_betweenness[0]], name_dict))
# np.save("betweenness.npy", giant_betweenness)









    #CI计算考虑转换成函数，可能以后也会用到
x = range(total_steps)


plt.rcParams['font.sans-serif']=['SimHei']

plt.rcParams['axes.unicode_minus'] = False
plt.plot(x,giant,label='ci')
plt.plot(x,giant_betweenness,'r',label='betweenness')
plt.xlabel('P')
plt.ylabel('GC')
plt.title(filename[0:-4])
plt.legend(loc=0,ncol=1)
plt.show()