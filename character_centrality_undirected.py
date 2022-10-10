# -*- coding : utf-8-*-
# @Time : 2022/6/6 4:26 下午
# @Author : yjc
# @Name : character_centrality_undirected.py

from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
import xlrd
import pandas as pd
from write import write_weight


def ranking(nodes_c:'dict',rev=True) -> 'list,list':
    """根据节点中心性输出从大到小的排列
    输入为节点和重要性的字典，输出为排列后的节点和数值
    谨慎使用
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
df = pd.read_excel('ChineseMap.xlsx')
data = df.values
# print("获取到所有的值:\n{}".format(data))
# print(data[100,1])
print('行数：', len(data))

"""生成网络，目前没有添加各种权重属性，只考虑了拓扑结构"""
characters = []
edges = []

for line in data:
    characters.append(line[0])

for line in data:
    for char in line[1]:
        if char != line[0] :
            if char in characters:
                edges.append((char, line[0]))
print('连边数：',len(edges))
# print(edges[0:10])
# print(edges[1000],edges[200])
# 存入nx网络
G = nx.DiGraph()
G.add_nodes_from(characters)
# G.add_weighted_edges_from(edges)
G.add_edges_from(edges)
# print('test:',nx.dijkstra_path(G, '手', '热'))


print('G读取完成，连边不包含打分信息。此处是无向图\n')

# 先当成无向图来做
G = nx.to_undirected(G)


# """度中心性"""
# c_degree = nx.degree_centrality(G)
# centrality_degree, centrality_degree_value = ranking(c_degree)
# print('度中心性排序：',centrality_degree[0:30])
# value = []
# for key in c_degree:
#     value.append(c_degree[key])
# write_weight(value,'chinese/degree')


# """渗流中心性"""
# # 渗流状态给的0.1能出结果，但是意义还不理解，应该怎样赋值呢？
# nx.set_node_attributes(G, 0.1, 'percolation')
# c_percolation = nx.percolation_centrality(G, attribute='percolation', states=None, weight=None)
# centrality_percolation,centrality_percolation_value = ranking(c_percolation)
# print('渗流中心性：（可能不正确）',centrality_percolation[0:20])


# """特征向量中心性"""
# c_ev = nx.eigenvector_centrality(G,max_iter=500)
# centrality_ev,centrality_ev_value = ranking(c_ev)
# print('特征向量中心性：',centrality_ev[0:30])
# value = []
# for key in c_ev:
#     value.append(c_ev[key])
# write_weight(value,'chinese/eigenvector')


# """katz中心性"""
# c_katz = nx.katz_centrality(G, max_iter=1000,weight=None)
# centrality_katz,centrality_katz_value = ranking(c_katz)
# print('katz中心性：',centrality_katz[0:20])


# """紧密中心性closeness_centrality"""
# c_clo = nx.closeness_centrality(G, u=None, distance=None, wf_improved=True)
# centrality_clo,centrality_clo_value = ranking(c_clo)
# print('closeness中心性：',centrality_clo[0:30])
# value = []
# for key in c_clo:
#     value.append(c_clo[key])
# write_weight(value,'chinese/closeness')


# """current_flow_closeness_centrality有向图好像不行"""
# # c_cfc = nx.information_centrality(G, weight=None)
# # centrality_cfc,centrality_cfc_value = ranking(c_cfc)
# # print('current_flow_closeness中心性：',centrality_cfc[0:20])


# """介数中心性"""
# c_bt = nx.betweenness_centrality(G)
# centrality_bt,centrality_bt_value = ranking(c_bt)
# print('介数中心性：',centrality_bt[0:30])
# value = []
# for key in c_bt:
#     value.append(c_bt[key])
# write_weight(value,'chinese/betweenness')


# """k-core"""
# G_kcore = G.to_undirected()
# kcore = nx.core_number(G_kcore)
# value = []
# for key in kcore:
#     value.append(kcore[key])
# write_weight(value,'chinese/kcore')


# """pagerank"""
# c_pagerank = nx.pagerank_numpy(G, alpha=0.85)
# node_ranked, value_ranked = ranking(c_pagerank)
# print('pagerank排序：',node_ranked[0:30])
# value = []
# for key in c_pagerank:
#     value.append(c_pagerank[key])
# write_weight(value,'chinese/pagerank')
# print(len(c_pagerank))


"""CI"""
l = 3
c_ci = cal_ci_centrality(G, l)
node_ranked, value_ranked = ranking(c_ci)
print('CI排序：',node_ranked[0:30])
value = []
for key in c_ci:
    value.append(c_ci[key])
write_weight(value,'chinese/ci(l=%s)'%(l))
