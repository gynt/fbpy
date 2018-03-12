from fbpy.access import AccessManager
from fbpy.options import *
from fbpy.data import complete, Page

access_manager = AccessManager()

#nos/posts?fields=comments{comments{id,reactions,message,from,created_time},reactions,message,from,id,created_time},message,attachments,reactions,id,created_time&limit=1
#posts_id?fields=comments{comments{id,reactions,message,from,created_time},reactions,message,from,id,created_time},message,attachments,reactions,id,created_time&limit=1

from fbpy.logger import *


def get_posts_for_page(page_id, amount = 1, post_options=PostOptions(), reaction_options=ReactionOptions(), comment_options=CommentOptions(), subreaction_options=ReactionOptions(), subcomment_options=CommentOptions()):
    
    url=build_url(page_id, post_options, reaction_options, comment_options, subreaction_options, subcomment_options)
    result = access_manager.make_request(url)

    posts = []

    if result.code != 200:
        raise Exception("Error: {}".format(result.code))
    
    page=result.content

    while len(posts) < amount:

        for post in page["data"]:
            debug(post["id"])
            if "data" in post:
                for key in post["data"].keys():
                    complete(post["data"][key], access_manager) #["comments"]          
            posts.append(post)
            if len(posts) > amount - 1:
                return posts

        p = Page(page)
        if p.has_next():
            page = p.next(access_manager).page
        else:
            info("No more posts")
            break
    
    return posts


def get_comments_for_post(post_id, post_options=PostOptions(), reaction_options=ReactionOptions(), comment_options=CommentOptions(), subreaction_options=ReactionOptions(), subcomment_options=CommentOptions()):
    
    url=build_url(post_id, post_options, reaction_options, comment_options, subreaction_options, subcomment_options, False)
    result = access_manager.make_request(url)

    posts = []

    if result.code == 200:
        page=result.content

        complete(page)

        for post in page["comments"]["data"]:
            if "data" in post:
                for key in post["data"].keys():
                    complete(post["data"][key]) #["comments"]          
            posts.append(post)
        return posts
    else:
        raise Exception("Error: " + result[0])
