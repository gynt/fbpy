from fbpy.access import AccessManager
from fbpy.options import *
from fbpy.data import complete, Page

access_manager = AccessManager()

#nos/posts?fields=comments{comments{id,reactions,message,from,created_time},reactions,message,from,id,created_time},message,attachments,reactions,id,created_time&limit=1
#posts_id?fields=comments{comments{id,reactions,message,from,created_time},reactions,message,from,id,created_time},message,attachments,reactions,id,created_time&limit=1

from fbpy.logger import *


def fetch_posts(page_id, amount = 99999999, post_options=PostOptions(), reaction_options=ReactionOptions(), comment_options=CommentOptions(), subreaction_options=ReactionOptions(), subcomment_options=CommentOptions()):
    
    url=build_url(page_id+"/posts", post_options, reaction_options, comment_options, subreaction_options, subcomment_options)
    result = access_manager.make_request(url)

    #posts = []

    if result.code != 200:
        raise Exception("Error: {}".format(result.code))

    return result.content
    
    #return posts

def extract_posts(posts, amount = 99999999):
    count = 0

    page=result.content

    while count < amount:

        for post in page["data"]:
            #debug(post["id"])
            if "data" in post:
                for key in post["data"].keys():
                    complete(post["data"][key], access_manager) #["comments"]
            count+=1
            yield post
            if count > amount - 1:
                return
            #posts.append(post)
            #if len(posts) > amount - 1:
                #return posts

        p = Page(page)
        if p.has_next():
            page = p.next(access_manager).page
        else:
            debug("No more posts")
            break    

import json

def fetch_post(post_id, post_options=PostOptions(), reaction_options=ReactionOptions(), comment_options=CommentOptions(), subreaction_options=ReactionOptions(), subcomment_options=CommentOptions()):
    
    url=build_url(post_id, post_options, reaction_options, comment_options, subreaction_options, subcomment_options)
    result = access_manager.make_request(url)

    if result.code != 200:
        raise Exception("Error: " + result.code)

    return result.content

def extract_comments_for_post(post, amount=99999999, include_subcomments=True):

    count = 0

    page = post["comments"]

    while count < amount:

        for comment in page["data"]:
            #debug(comment["id"])
            if "comments" in comment:
                #complete(comment["comments"], access_manager)
                comment["comments"]=list(extract_subcomments_for_comment(comment))
                    
            count+=1
            yield comment
            if count > amount - 1:
                return

        p = Page(page)
        if p.has_next():
            page = p.next(access_manager).page
        else:
            debug("No more comments")
            break    

def extract_subcomments_for_comment(post, amount=99999999):
    
    count = 0

    page = post["comments"]

    while count < amount:

        for comment in page["data"]:
            #debug(comment["id"])
            #if "comments" in comment:
                #complete(comment["comments"], access_manager)
                    
            count+=1
            yield comment
            if count > amount - 1:
                return

        p = Page(page)
        if p.has_next():
            page = p.next(access_manager).page
        else:
            debug("No more comments")
            break  
