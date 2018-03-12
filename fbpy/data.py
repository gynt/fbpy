from fbpy.logger import *





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

    def has_next(self):
        return "paging" in self.page and "next" in self.page["paging"]

    def next(self, access_manager):
        req = access_manager.make_request(self.page["paging"]["next"])

        if req.code!=200:
            warning("Wrong code: {}".format(req.code))
            return

        return Page(req.content)
    
