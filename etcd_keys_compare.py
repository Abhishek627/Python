import json


'''
Find common and different keys between 2 etcd dumps (gotten using etcdctcl cli)

'''

def create_dict(filepath,delimiter):
    with open(filepath) as temp_file:
        temp_dict=dict()
        for line in temp_file:
            line=line.replace('\n','').replace('\t','')
            if line:
                key,val=line.split(delimiter)
                temp_dict[key]=val
        return temp_dict

def find_common(dict_reg,dict_cen):
    common_keys=list(set(dict_reg) & set(dict_cen))
    result=dict()
    for item in common_keys:
        result[item]={'central_val':dict_cen[item],'regional_val':dict_reg[item]}
    return result

def find_common_key_diff_val(dict_reg,dict_cen):
    common_keys=list(set(dict_reg) & set(dict_cen))
    result=dict()
    for item in common_keys:
        val_reg= dict_reg[item]
        val_cen= dict_cen[item]
        if val_cen.lower()!= val_reg.lower():
            result[item]={'central_val':dict_cen[item],'regional_val':dict_reg[item]}
    return result


if __name__ == '__main__':
    etcd_cen=create_dict('/Users/shabhishek/Desktop/etcd_central_latest.txt',':$')
    etcd_reg=create_dict('/Users/shabhishek/Desktop/etcd_regional_latest.txt',':$')
    common_keys= find_common(etcd_reg,etcd_cen)
    common_keys_diff_val=find_common_key_diff_val(etcd_reg,etcd_cen)
    with open('/Users/shabhishek/Desktop/Common_keys.json','w') as temp:
        temp.write(json.dumps(common_keys,indent=4))
    with open('/Users/shabhishek/Desktop/Common_keys_diff_val.json','w') as temp:
        temp.write(json.dumps(common_keys_diff_val,indent=4))
    # print json.dumps(common_keys,indent=4)
    # print json.dumps(common_keys_diff_key,indent=4)


