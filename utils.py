
def defaultDict(d:dict,defaults:dict):
    if defaults == {} or not isinstance(d,dict) or not isinstance(defaults,dict):
        return d
    for k,v in defaults.items():
        if not k in d:
            d[k] = v
        else:
            d[k] = defaultDict(d[k],v)
    return d