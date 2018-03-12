


class Options(object):

    def __init__(self, since=None, until=None, limit=100, fields=[]):
        self.since = since
        self.until = until
        self.fields = fields
        self.limit = limit

class SubCommentOptions(Options):

    def __init__(self, since=None, until=None, limit=100, order="chronological", fields=["reactions","message","from","id","created_time"]):
        super().__init__(since, until, limit, fields)
        self.order=order

class CommentOptions(Options):

    def __init__(self, since=None, until=None, limit=100, order="chronological", fields=["reactions","message","from","id","created_time","comments"]):
        super().__init__(since, until, limit, fields)
        self.order=order

class ReactionOptions(Options):

    def __init__(self, since=None, until=None, limit=100, fields=["id","name","type"]):
        super().__init__(since, until, limit, fields)

class PostOptions(Options):

    def __init__(self, since=None, until=None, limit=1, fields=["from","message","attachments","reactions","id","created_time","comments"]):
        super().__init__(since, until, limit, fields)



def build_url(page_id, post_options=PostOptions(), reaction_options=ReactionOptions(), comment_options=CommentOptions(), subreaction_options=ReactionOptions(), subcomment_options=SubCommentOptions()):
    
    iurl = "https://graph.facebook.com/v2.10/"+page_id+"?"
    params=[]

    if post_options.since:
        params.append("since="+str(post_options.since))
    if post_options.until:
        params.append("until="+str(post_options.until))
    if post_options.limit:
        params.append("limit="+str(post_options.limit))

    
    if post_options.fields and len(post_options.fields) > 0:
        baseurl="fields="
        for field in post_options.fields:
            if post_options.fields.index(field)==0:
                baseurl+=""
            else:
                baseurl+=","
                
            if field=="comments":
                baseurl+="comments"
                
                if comment_options.order:
                    baseurl+=".order("+subcomment_options.order+")"
                if comment_options.since:
                    baseurl+=".since("+str(subcomment_options.since)+")"
                if comment_options.until:
                    baseurl+=".until("+str(subcomment_options.until)+")"
                if comment_options.limit:
                    baseurl+=".limit("+str(subcomment_options.limit)+")"
                    
                if len(comment_options.fields) > 0:
                    baseurl+="{"
                    for cfield in comment_options.fields:
                        if comment_options.fields.index(cfield)==0:
                            baseurl+=""
                        else:
                            baseurl+=","

                        if cfield=="comments":
                            baseurl+="comments"
                            
                            if subcomment_options.order:
                                baseurl+=".order("+subcomment_options.order+")"
                            if subcomment_options.since:
                                baseurl+=".since("+str(subcomment_options.since)+")"
                            if subcomment_options.until:
                                baseurl+=".until("+str(subcomment_options.until)+")"
                            if subcomment_options.limit:
                                baseurl+=".limit("+str(subcomment_options.limit)+")"
                                
                            if len(subcomment_options.fields) > 0:
                                baseurl+="{"
                                for ccfield in subcomment_options.fields:
                                    if subcomment_options.fields.index(ccfield)==0:
                                        baseurl+=""
                                    else:
                                        baseurl+=","
                                    baseurl+=ccfield
                                baseurl+="}"
                        elif cfield=="reactions":
                            baseurl+="reactions"

                            if subreaction_options.limit:
                                baseurl+=".limit("+str(subreaction_options.limit)+")"
                            
                            if len(subreaction_options.fields) > 0:
                                baseurl+="{"
                                for crfield in subreaction_options.fields:
                                    if subreaction_options.fields.index(crfield)==0:
                                        baseurl+=""
                                    else:
                                        baseurl+=","
                                    baseurl+=crfield
                                baseurl+="}"
                        else:
                            baseurl+=cfield
                    baseurl+="}"
            elif field=="reactions":
                baseurl+="reactions"

                if reaction_options.limit:
                    baseurl+=".limit("+str(reaction_options.limit)+")"
                
                if len(reaction_options.fields) > 0:
                    baseurl+="{"
                    for rfield in reaction_options.fields:
                        if reaction_options.fields.index(rfield)==0:
                            baseurl+=""
                        else:
                            baseurl+=","
                        baseurl+=rfield
                    baseurl+="}"
            else:
                baseurl+=field
        params.append(baseurl)

    iurl+="&".join(params)
    return iurl
