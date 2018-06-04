

l = [['1','2','3'],['a','b','c'],['x','y','z']]

d = {'a':[1,2,3],'b':[4,5,6],'c':[7,8,9]}

def merge(d):
    l = list(d.keys())
    res_d = []
    res = mergeRecur(l,d[l[0]],d,1)
    for e1 in res:
        d_res = {}
        for i,e2 in enumerate(e1.split("|")):
            d_res[l[i]] = e2
        res_d.append(d_res)
    return res, res_d


def mergeRecur(l,l1,d,i):

    new_l = []

    for e1 in l1:
        for e2 in d[l[i]]:
            new_l.append(str(e1) + "|" + str(e2))
    if i == len(l) - 1:
    	return new_l
    else:
    	return mergeRecur(l,new_l,d,i+1)

res, res_d = merge(d)
print (res)
print (res_d)
#print(len(merge(d)))