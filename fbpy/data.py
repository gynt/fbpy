from fbpy.logger import *


def level(result, dic, address=[], log=True):
    for key in dic.keys():
        value=dic[key]
        address.append(key)
        if isinstance(value, dict):
            level(result, value, address)
        elif isinstance(value, list):
            if len(value) == 1:
                level(result, value[0], address)
            else:
                if log:
                    result["pager_log"]="key: {} actually had more than one value: {}".format(key, len(value))
        else:
            result["_".join(address)]=value
        del address[-1]
    return result


def determine_fieldnames(levelled_posts):
    fieldnames=[]
    for post in levelled_posts:
        fieldnames.extend(list(post.keys()))
    return list(set(fieldnames))


def complete(data_paging, access_manager):
    if not "data" in data_paging:
        return
    if not isinstance(data_paging, dict):
        warning("Not a dictionary: {}".format(data_paging))
        return

    pagecount=0
    
    nextpage = data_paging
    while "paging" in nextpage and "next" in nextpage["paging"]:
        req = access_manager.make_request(nextpage["paging"]["next"])

        if req.code!=200:
            warning("Aborting, because received code: " + req.code + " and response: " + json.dumps(req.content, indent=2))
            return
        nextpage = req.content
        for i in nextpage["data"]:
            data_paging["data"].append(i)
        pagecount+=1
        debug("Going to next page: {}".format(pagecount))

    for el in data_paging["data"]:
        for key in el.keys(): #["comments"]["data"]
            complete(el[key], access_manager)



class Page(object):

    def __init__(self, page):
        self.page = page
        if not isinstance(page, dict):
            raise Exception()
        if not "paging" in page:
            raise Exception()

    def has_next(self):
        return "paging" in self.page

    def next(self, access_manager):
        req = access_manager.make_request(self.page["paging"]["next"])

        if req.code!=200:
            warning("Wrong code: {}".format(req.code))
            return

        return Page(req.content)
    
