# -*- coding : utf-8-*-
from matplotlib import pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
import networkx as nx
from readcxl import cxl2graph,get_name,cxl2graph_better


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

def adaptive_centrality(Graph,func,func_name):
    """
    中心性，考虑有无向
    返回最大联通团大小的变化和移除节点的排序
    """
    giant = []
    rank = []
    G = Graph
    total_steps = G.number_of_nodes() - 1
    for p in range(total_steps):
        print('============%s %d=============' % (func_name,p))
        largest = max(nx.connected_components(G), key=len)
        largest_connected_subgraph = G.subgraph(largest)
        gc = largest_connected_subgraph.number_of_nodes()
        print('GC：', gc)
        giant.append(gc)

        centrality = func(G)
        ranked_node, ranked_value = ranking(centrality)

        G.remove_node(ranked_node[0])
        print('移除:', get_name([ranked_node[0]], name_dict))
        rank.append(ranked_node[0])
    # np.save("betweenness.npy", giant_betweenness)
    return giant,rank


"""读数据"""
# filename = "圆的周长和面积.cxl"
# filename = "第四章：认识关系和运算之减法.cxl"
# filename = "平面几何.cxl"
filename = "微积分核心概念和关系细节图.cxl"
G, name_dict = cxl2graph_better(filename)


"""各种中心性"""
G_undirected = G.to_undirected()
gc_degree,rank_degree = adaptive_centrality(G_undirected,nx.degree_centrality,'degree')

G_undirected = G.to_undirected()
gc_betweenness, rank_betweenness = adaptive_centrality(G_undirected,nx.betweenness_centrality,'betweenness')

G_undirected = G.to_undirected()
gc_closeness, rank_closeness = adaptive_centrality(G_undirected,nx.closeness_centrality,'closeness')

# G_undirected = G.to_undirected()
# adaptive_centrality(G_undirected,nx.eigenvector_centrality(max_iter=500),'eigenvector')

G_undirected = G.to_undirected()
gc_pagerank, rank_pagerank = adaptive_centrality(G_undirected,nx.pagerank_numpy,'pagerank')


"""补充特征向量中心性"""
gc_eigenvector = []
rank_eigenvector = []
G_undirected = G.to_undirected()
total_steps = G_undirected.number_of_nodes() - 1
for p in range(total_steps):
    print('============eigenvector %d=============' % (p))
    largest = max(nx.connected_components(G_undirected), key=len)
    largest_connected_subgraph = G_undirected.subgraph(largest)
    gc = largest_connected_subgraph.number_of_nodes()
    print('GC：', gc)
    gc_eigenvector.append(gc)

    centrality = nx.eigenvector_centrality(G_undirected,max_iter=4000)
    ranked_node, ranked_value = ranking(centrality)

    G_undirected.remove_node(ranked_node[0])
    print('移除:', get_name([ranked_node[0]], name_dict))
    rank_eigenvector.append(ranked_node[0])
# np.save("betweenness.npy", giant_betweenness)


"""CI"""
# 设置球的半径
l=2

# 转为无向图
G_percolation = G.to_undirected()
gc_ci_2 = []
rank_ci_2 = []
# 迭代删点
total_steps = G_percolation.number_of_nodes()-1
for p in range(total_steps):
    print('============CI %d============='%(p))
    # max = 0
    print('剩余节点数：',G_percolation.number_of_nodes())
    largest = max(nx.connected_components(G_percolation), key=len)
    largest_connected_subgraph = G_percolation.subgraph(largest)
    gc = largest_connected_subgraph.number_of_nodes()
    print('GC：',gc)
    gc_ci_2.append(gc)
    if nx.diameter(largest_connected_subgraph) < 2: l=0
    ci_dict = cal_ci_centrality(G_percolation,l)

    ci_rank , ci_value = ranking(ci_dict)
    G_percolation.remove_node(ci_rank[0])
    rank_ci_2.append(ci_rank[0])
    print('移除:',get_name([ci_rank[0]],name_dict))

"""CI"""
# 设置球的半径
l=3

# 转为无向图
G_percolation = G.to_undirected()
gc_ci_3 = []
rank_ci_3 = []
# 迭代删点
total_steps = G_percolation.number_of_nodes()-1
for p in range(total_steps):
    print('============CI %d============='%(p))
    # max = 0
    print('剩余节点数：',G_percolation.number_of_nodes())
    largest = max(nx.connected_components(G_percolation), key=len)
    largest_connected_subgraph = G_percolation.subgraph(largest)
    gc = largest_connected_subgraph.number_of_nodes()
    print('GC：',gc)
    gc_ci_3.append(gc)
    if nx.diameter(largest_connected_subgraph) < 2: l=0
    ci_dict = cal_ci_centrality(G_percolation,l)

    ci_rank , ci_value = ranking(ci_dict)
    G_percolation.remove_node(ci_rank[0])
    rank_ci_3.append(ci_rank[0])
    print('移除:',get_name([ci_rank[0]],name_dict))


"""CI"""
# 设置球的半径
l=1

# 转为无向图
G_percolation = G.to_undirected()
gc_ci_1 = []
rank_ci_1 = []
# 迭代删点
total_steps = G_percolation.number_of_nodes()-1
for p in range(total_steps):
    print('============CI %d============='%(p))
    # max = 0
    print('剩余节点数：',G_percolation.number_of_nodes())
    largest = max(nx.connected_components(G_percolation), key=len)
    largest_connected_subgraph = G_percolation.subgraph(largest)
    gc = largest_connected_subgraph.number_of_nodes()
    print('GC：',gc)
    gc_ci_1.append(gc)
    if nx.diameter(largest_connected_subgraph) < 2: l=0
    ci_dict = cal_ci_centrality(G_percolation,l)

    ci_rank , ci_value = ranking(ci_dict)
    G_percolation.remove_node(ci_rank[0])
    rank_ci_1.append(ci_rank[0])
    print('移除:',get_name([ci_rank[0]],name_dict))


'''自适应'''
# # 转为无向图
# G_percolation = G.to_undirected()
# giant_auto = []
# # 迭代删点
# total_steps = G_percolation.number_of_nodes()-1
# for p in range(total_steps):
#     print('============STEP %d============='%(p))
#     # max = 0
#     print('剩余节点数：',G_percolation.number_of_nodes())
#     largest = max(nx.connected_components(G_percolation), key=len)
#     largest_connected_subgraph = G_percolation.subgraph(largest)
#     gc = largest_connected_subgraph.number_of_nodes()
#     print('GC：',gc)
#     giant_auto.append(gc)
#     # l = nx.diameter(largest_connected_subgraph)/2
#     l = 1
#     print(l)
#
#     ci_dict = cal_ci_centrality(G_percolation,l)
#
#     ci_rank , ci_value = ranking(ci_dict)
#     G_percolation.remove_node(ci_rank[0])
#     print('移除:',get_name([ci_rank[0]],name_dict))


print('===========success==============')

print('\ndegree')
for i in range(5):
    print(get_name([rank_degree[i]],name_dict),end=" ")

print('\nbetweenness')
for i in range(5):
    print(get_name([rank_betweenness[i]],name_dict),end=" ")

print('\ncloseness')
for i in range(5):
    print(get_name([rank_closeness[i]],name_dict),end=" ")

print('\neigenvector')
for i in range(5):
    print(get_name([rank_eigenvector[i]],name_dict),end=" ")

print('\nPageRank')
for i in range(5):
    print(get_name([rank_pagerank[i]],name_dict),end=" ")

print('\nCI(l=1)')
for i in range(5):
    print(get_name([rank_ci_1[i]],name_dict),end=" ")

print('\nCI(l=2)')
for i in range(5):
    print(get_name([rank_ci_2[i]],name_dict),end=" ")

print('\nCI(l=3)')
for i in range(5):
    print(get_name([rank_ci_3[i]],name_dict),end=" ")






x = range(total_steps)


plt.rcParams['font.sans-serif']=['SimHei']

plt.rcParams['axes.unicode_minus'] = False
plt.plot(x,gc_ci_2,'b',label='ci(l=2)')
plt.plot(x,gc_betweenness,'r',label='betweenness')
plt.plot(x,gc_pagerank,'y',label='PageRank')
plt.plot(x,gc_closeness,'m',label='closeness')
plt.plot(x,gc_degree,'g',label='degree')
plt.plot(x,gc_eigenvector,'k',label='eigenvector')

# plt.plot(x,gc_ci_2,'b',label='l=2')
# plt.plot(x,gc_ci_1,'r',label='l=1')
# plt.plot(x,gc_ci_3,'y',label='l=3')

plt.xlabel('P')
plt.ylabel('GC')
plt.title(filename[0:-4])
plt.legend(loc=0,ncol=1)
plt.show()