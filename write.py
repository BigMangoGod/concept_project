import xlwt


def write_weight(list,name,column=0):
    """写入权重列表，顺序默认为原表顺序"""
    f = xlwt.Workbook('encoding = utf-8') #设置工作簿编码
    sheet1 = f.add_sheet('sheet1',cell_overwrite_ok=True) #创建sheet工作表
    list1 = list#要写入的列表的值
    for i in range(len(list1)):
        sheet1.write(i+1,column,list1[i]) #写入数据参数对应 行, 列, 值
    sheet1.write(0, column, name)
    f.save('data/%s.xls' % (name))#保存.xls到当前工作目录


