import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import optimize as op


loc = 'data/chinese_ci'

closeness = np.load("%s/gc_closeness.npy"%(loc))
degree = np.load("%s/gc_degree.npy"%(loc))
eigenvector = np.load("%s/gc_eigenvector.npy"%(loc))
betweenness = np.load("%s/gc_betweenness.npy"%(loc))
ci_1 = np.load("%s/gc_ci_1.npy"%(loc))
ci_3 = np.load("%s/gc_ci_3.npy"%(loc))
ci_2 = np.load("%s/gc_ci_2.npy"%(loc))


rank_ci_1 = np.load("%s/rank_ci_1.npy"%(loc))
rank_ci_3 = np.load("%s/rank_ci_3.npy"%(loc))
rank_ci_2 = np.load("%s/rank_ci_2.npy"%(loc))



x = range(4300)


# for i in range(len(betweenness)):
#     print(i,betweenness[i])


plt.rcParams['font.sans-serif']=['SimHei']


scale = 300
plt.rcParams['axes.unicode_minus'] = False
plt.plot(x[0:scale],closeness[0:scale],'b',label='clossness')
plt.plot(x[0:scale],degree[0:scale],'r',label='degree')
plt.plot(x[0:scale],eigenvector[0:scale],'y',label='eigenvector')
plt.plot(x[0:scale],betweenness[0:scale],'g',label='betweenness')
plt.plot(x[0:scale],ci_2[0:scale],'m',label='ci(l=2)')


print(rank_ci_1[0:20])
print(rank_ci_2[0:20])
print(rank_ci_3[0:20])



# plt.plot(x[0:scale],ci_1[0:scale],'g',label='l=1')
# plt.plot(x[0:scale],ci_2[0:scale],'m',label='l=2')
# plt.plot(x[0:scale],ci_3[0:scale],'b',label='l=3')






plt.xlabel('P')
plt.ylabel('GC')
# plt.title(filename[0:-4])
plt.legend(loc=0,ncol=1)
plt.show()