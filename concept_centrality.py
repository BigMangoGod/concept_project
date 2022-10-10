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


"""读数据"""
filename = "第四章：认识关系和运算之减法.cxl"
G, name_dict = cxl2graph(filename)


"""度中心性"""
c_degree = nx.degree_centrality(G)
centrality_degree, centrality_degree_value = ranking(c_degree)
centrality_degree = get_name(centrality_degree, name_dict)
print('度中心性排序：',centrality_degree)


"""渗流中心性"""
# 渗流状态给的0.1能出结果，但是与所需要的渗流概念意义不同。这里更偏向于是一种动态的重要性
# nx.set_node_attributes(G, 0.1, 'percolation')
# c_percolation = nx.percolation_centrality(G, attribute='percolation', states=None, weight=None)
# centrality_percolation,centrality_percolation_value = ranking(c_percolation)
# print('渗流中心性：（可能不正确）',centrality_percolation)


"""特征向量中心性"""
# c_ev = nx.eigenvector_centrality(G,max_iter=500)
# centrality_ev,centrality_ev_value = ranking(c_ev)
# print('特征向量中心性：',centrality_ev)


"""katz中心性"""
c_katz = nx.katz_centrality(G, max_iter=1000,weight=None)
centrality_katz,centrality_katz_value = ranking(c_katz)
centrality_katz = get_name(centrality_katz, name_dict)
print('katz中心性：',centrality_katz)


"""紧密中心性closeness_centrality"""
c_clo = nx.closeness_centrality(G, u=None, distance=None, wf_improved=True)
centrality_clo,centrality_clo_value = ranking(c_clo)
centrality_clo = get_name(centrality_clo, name_dict)
print('closeness中心性：',centrality_clo)


"""current_flow_closeness_centrality有向图好像不行"""
# c_cfc = nx.information_centrality(G, weight=None)
# centrality_cfc,centrality_cfc_value = ranking(c_cfc)
# print('current_flow_closeness中心性：',centrality_cfc[0:20])


"""介数中心性"""
c_bt = nx.betweenness_centrality(G)
centrality_bt,centrality_bt_value = ranking(c_bt)
centrality_bt = get_name(centrality_bt, name_dict)
print('介数中心性：',centrality_bt)