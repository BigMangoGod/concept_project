# -*- coding : utf-8-*-
from matplotlib import pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
import networkx as nx
from readcxl import cxl2graph,get_name
import pandas as pd


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
        # node_name = get_name([node], name_dict)

        # print(G.degree(node))
        neighbor = nx.single_source_shortest_path_length(G, node)
        for item in neighbor:
            if neighbor[item] == l: ci += G.degree(item) - 1
            # if neighbor[item] == l: print('     ',get_name([item],name_dict))
        ci = (G.degree(node) - 1) * ci
        # print(node_name, ci)
        ci_dict[node] = ci

    return ci_dict


"""读数据"""
filename = 'ChineseMap.xlsx'
df = pd.read_excel(filename)
data = df.values
print('行数：', len(data))

"""生成网络，目前没有添加各种权重属性，只考虑了拓扑结构"""
characters = []
edges = []
for line in data:
    # print(line[1])
    characters.append(line[0])
    for char in line[1]:
        if char != line[0]:
            edges.append((char,line[0],line[2]))
print('连边数：',len(edges))
# 存入nx网络
G = nx.DiGraph()
G.add_nodes_from(characters)
G.add_weighted_edges_from(edges)
# print('test:',nx.dijkstra_path(G, '手', '热'))



"""当作无向图处理"""
G = G.to_undirected()
print('G读取完成，连边不含打分信息，以无向图处理。\n')


"""度中心性"""
giant_degree = []
rank_degree =[]
G_degree = G
total_steps = G_degree.number_of_nodes()-1
for p in range(total_steps):
    print('============DEGREE %d=============' % (p))
    largest = max(nx.connected_components(G_degree), key=len)
    largest_connected_subgraph = G_degree.subgraph(largest)
    gc = largest_connected_subgraph.number_of_nodes()
    giant_degree.append(gc)

    c_degree = nx.degree_centrality(G_degree)
    centrality_degree, centrality_degree_value = ranking(c_degree)

    G_degree.remove_node(centrality_degree[0])
    rank_degree.append(centrality_degree[0])

np.save("data/chinese_ci/gc_degree.npy", giant_degree)
np.save("data/chinese_ci/rank_degree.npy", rank_degree)





# """clossness中心性"""
# giant_clossness = []
# rank_clossness = []
# G_clossness = G
# total_steps = G_clossness.number_of_nodes()-1
# for p in range(total_steps):
#     print('============CLOSSNESS %d=============' % (p))
#     largest = max(nx.connected_components(G_clossness), key=len)
#     largest_connected_subgraph = G_clossness.subgraph(largest)
#     gc = largest_connected_subgraph.number_of_nodes()
#     print('GC：',gc)
#     giant_clossness.append(gc)
#
#     c_clossness = nx.closeness_centrality(G_clossness)
#     centrality_clossness, centrality_clossness_value = ranking(c_clossness)
#
#     G_clossness.remove_node(centrality_clossness[0])
#     rank_clossness.append(centrality_clossness[0])
#
# np.save("data/chinese_ci/gc_closeness.npy", giant_clossness)
# np.save("data/chinese_ci/rank_closeness.npy", rank_clossness)


# """特征向量中心性"""
# giant_eigenvector = []
# rank_eigenvector = []
# G_eigenvector = G
# total_steps = G_eigenvector.number_of_nodes()-1
# for p in range(total_steps):
#     print('============EigenVector %d=============' % (p))
#     largest = max(nx.connected_components(G_eigenvector), key=len)
#     largest_connected_subgraph = G_eigenvector.subgraph(largest)
#     gc = largest_connected_subgraph.number_of_nodes()
#     print('GC：',gc)
#     giant_eigenvector.append(gc)
#
#     c_eigenvector = nx.eigenvector_centrality(G_eigenvector,max_iter=2000)
#     centrality_eigenvector, centrality_eigenvector_value = ranking(c_eigenvector)
#
#     G_eigenvector.remove_node(centrality_eigenvector[0])
#     rank_eigenvector.append(centrality_eigenvector[0])
#
# np.save("data/chinese_ci/gc_eigenvector.npy", giant_eigenvector)
# np.save("data/chinese_ci/rank_eigenvector.npy", rank_eigenvector)
#

# """介数中心性"""
# giant_betweenness = []
# rank_betweenness = []
# G_betweenness = G
# total_steps = G_betweenness.number_of_nodes()-1
# for p in range(total_steps):
#     print('============Betweenness %d=============' % (p))
#     largest = max(nx.connected_components(G_betweenness), key=len)
#     largest_connected_subgraph = G_betweenness.subgraph(largest)
#     gc = largest_connected_subgraph.number_of_nodes()
#     print('GC：',gc)
#     giant_betweenness.append(gc)
#
#     c_betweenness = nx.betweenness_centrality(G_betweenness)
#     centrality_betweenness, centrality_betweenness_value = ranking(c_betweenness)
#
#     G_betweenness.remove_node(centrality_betweenness[0])
#     rank_betweenness.append(centrality_betweenness[0])
#
# np.save("data/chinese_ci/gc_betweenness.npy", giant_betweenness)
# np.save("data/chinese_ci/rank_betweenness.npy", rank_betweenness)

# """PageRank"""
# giant_pagerank = []
# rank_pagerank = []
# G_pagerank = G
# total_steps = G_pagerank.number_of_nodes() - 1
# for p in range(total_steps):
#     print('============PageRank %d=============' % (p))
#     largest = max(nx.connected_components(G_pagerank), key=len)
#     largest_connected_subgraph = G_pagerank.subgraph(largest)
#     gc = largest_connected_subgraph.number_of_nodes()
#     print('GC：', gc)
#     giant_pagerank.append(gc)
#
#     c_pagerank = nx.pagerank_numpy(G_pagerank, alpha=0.85)
#     centrality_pagerank, centrality_betweenness_value = ranking(c_pagerank)
#
#     G_pagerank.remove_node(centrality_pagerank[0])
#     rank_pagerank.append(centrality_pagerank[0])
#
# np.save("data/chinese_ci/gc_pagerank.npy", giant_pagerank)
# np.save("data/chinese_ci/rank_pagerank.npy", rank_pagerank)


# """计算CI"""
# # 设置球的半径
# l = 3
# # 转为无向图
# G_percolation = G
# giant_ci = []
# rank_ci = []
# # 迭代删点
# total_steps = G_percolation.number_of_nodes()-1
# for p in range(total_steps):
#     print('============STEP %d============='%(p))
#     # max = 0
#     # print('剩余节点数：',G_percolation.number_of_nodes())
#     largest = max(nx.connected_components(G_percolation), key=len)
#     largest_connected_subgraph = G_percolation.subgraph(largest)
#     gc = largest_connected_subgraph.number_of_nodes()
#     print('GC：',gc)
#     giant_ci.append(gc)
#
#     ci_dict = cal_ci_centrality(G_percolation,l)
#
#     ci_rank , ci_value = ranking(ci_dict)
#     G_percolation.remove_node(ci_rank[0])
#     rank_ci.append(ci_rank[0])
#     print('移除:',ci_rank[0])
#
#
# np.save("data/chinese_ci/gc_ci_3.npy", giant_ci)
# np.save("data/chinese_ci/rank_ci_3.npy", giant_ci)


# x = range(total_steps)
#
#
# plt.rcParams['font.sans-serif']=['SimHei']
#
# plt.rcParams['axes.unicode_minus'] = False
# plt.plot(x[0:1000],giant_ci[0:1000],'b',label='ci')
# plt.plot(x[0:1000],giant_degree[0:1000],'r',label='degree')
# plt.plot(x[0:1000],giant_betweenness[0:1000],'y',label='betweenness')
# plt.plot(x[0:1000],giant_clossness[0:1000],'g',label='closeeness')
# plt.plot(x[0:1000],giant_eigenvector[0:1000],'m',label='eigenvector')
# # plt.plot(x,giant_ci,'b',label='ci')
# # plt.plot(x,giant_degree,'r',label='degree')
# # plt.plot(x,giant_betweenness,'y',label='betweenness')
# # plt.plot(x,giant_clossness,'g',label='closeeness')
# # plt.plot(x,giant_eigenvector,'m',label='eigenvector')
#
# plt.xlabel('P')
# plt.ylabel('GC')
# plt.title(filename[0:-4])
# plt.legend(loc=0,ncol=1)
# plt.show()