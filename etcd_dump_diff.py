'''
Helper code to find diff and similar keys in 2 etcd dumps.
Use this command to take the dump from etcd:
etcdctl ls --recursive -p | grep -v '/$' | xargs -n 1 -I% sh -c 'echo -n %:$; etcdctl get %;'

'''


import json
def create_dict(filepath, delimiter):
    with open(filepath) as temp_file:
        temp_dict = dict()
        for line in temp_file:
            line = line.replace('\n', '').replace('\t', '')
            if line:
                key, val = line.split(delimiter)
                temp_dict[key] = val
        return temp_dict


def find_common(dict_reg, dict_cen):
    common_keys = list(set(dict_reg) & set(dict_cen))
    result = dict()
    for item in common_keys:
        result[item] = {'central_val': dict_cen[item], 'regional_val': dict_reg[item]}
    return result


def find_common_key_diff_val(dict_reg, dict_cen):
    common_keys = list(set(dict_reg) & set(dict_cen))
    result = dict()
    for item in common_keys:
        val_reg = dict_reg[item]
        val_cen = dict_cen[item]
        if val_cen.lower() != val_reg.lower():
            result[item] = {'central_val': dict_cen[item], 'regional_val': dict_reg[item]}
    return result


if __name__ == '__main__':
    etcd_cen = create_dict('etcd_dump1.txt', ':$')
    etcd_reg = create_dict('etcd_dump2.txt', ':$')
    common_keys = find_common(etcd_reg, etcd_cen)
    common_keys_diff_val = find_common_key_diff_val(etcd_reg, etcd_cen)
    with open('Common_keys.json', 'w') as temp:
        temp.write(json.dumps(common_keys, indent=4))
    with open('Common_keys_diff_val.json', 'w') as temp:
        temp.write(json.dumps(common_keys_diff_val, indent=4))






