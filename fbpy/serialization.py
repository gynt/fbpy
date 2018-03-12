
def serialize_post(post, postswriter, commentswriter, reactionswriter, subcommentswriter, creactionswriter, subreactionswriter, attachmentswriter):
    post_id=posts["id"]
    from_id=posts["from"]["id"]


    post_fieldnames=["from","message","attachments","id","created_time"]
    post_dict = {key: post[key] for key in post if key in post_fieldnames}
    level(post_dict, post_dict["from"],["from"])
    post_dict.pop("from", None)
    post_fieldnames=post_dict.keys()
    postswriter.fieldnames=post_fieldnames
    postswriter.writerow(post_dict)

    for attachment in post["attachments"]["data"]:
        d={"post_id":post_id}
        level(d, attachment)
        attachmentfieldnames=d.keys()
        attachmentswriter.writerow(d)
    

    reaction_fieldnames=["post_id","id","name","type"]

    for reaction in post["reactions"]["data"]:
        reaction["post_id"]=post_id
        reaction_dict = {key: reaction[key] for key in post if key in reaction_fieldnames}
        level(reaction_dict, reaction_dict["from"], ["from"])
        reaction_dict.pop("from", None)
        reaction_fieldnames=reaction_dict.keys()
        reactionswriter.writerow(reaction_dict)


    subcomment_fieldnames=["post_id","comment_id","message","from","id","created_time"]
    creaction_fieldnames=["post_id","parent_comment_id","comment_id","id","name","type"]

    comment_fieldnames=["post_id","message","from","id","created_time"]

    for comment in post["comments"]["data"]:
        comment["post_id"]=post_id
        comment_dict = {key: comment[key] for key in post if key in comment_fieldnames}
        level(comment_dict, comment_dict["from"], ["from"])
        comment_dict.pop("from", None)
        comment_fieldnames=comment_dict.keys()
        commentswriter.writerow(comment_dict)
        
        for creaction in comment["reactions"]:
            creaction["post_id"]=post_id
            creaction["comment_id"]=comment["id"]
            creaction_dict = {key: creaction[key] for key in creaction if key in creaction_fieldnames}
            creactionwriter.writerow(creaction_dict)
                
        for subcomment in comment["comments"]["data"]:
            subcomment["post_id"]=post_id
            subcomment["comment_id"]=comment["id"]
            subcomment_dict = {key: subcomment[key] for key in subcomment if key in subcomment_fieldnames}
            level(subcomment_dict, subcomment_dict["from"], ["from"])
            subcomment_dict.pop("from", None)
            subcomment_fieldnames=subcomment_dict.keys()
            subcommentswriter.writerow(subcomment_dict)

            for subreaction in subcomment["reactions"]:
                subreaction["post_id"]=post_id
                subreaction["parent_comment_id"]=comment["id"]
                subreaction["comment_id"]=subcomment["id"]
                subreaction_dict = {key: subreaction[key] for key in subreaction if key in creaction_fieldnames}
                subreactionswriter.writerow(subreaction_dict)
        
        
def test_serialization():
    import csv

    with open(storagepath+"posts.csv", 'a') as posts, open(storagepath+"comments.csv", 'a') as comments, open(storagepath+"reactions.csv", 'a') as reactions, open(storagepath+"subcomments.csv", 'a') as subcomments, open(storagepath+"creactions.csv", 'a') as creactions, open(storagepath+"subreactions.csv", 'a') as subreactions, open(storagepath+"attachments.csv", 'a') as attachmentswriter:
        postswriter=csv.DictWriter(posts, fieldnames = ["from","message","attachments","id","created_time"])
        commentswriter=csv.DictWriter(comments, fieldnames = ["post_id","message","from","id","created_time"])
        reactionswriter=csv.DictWriter(reactions, fieldnames = ["post_id","id","name","type"])
        subcommentswriter=csv.DictWriter(subcomments, fieldnames = ["from","message","attachments","id","created_time"])
        creactionswriter=csv.DictWriter(creactions, fieldnames = ["from","message","attachments","id","created_time"])
        subreactionswriter=csv.DictWriter(subreactions, fieldnames = ["from","message","attachments","id","created_time"])
        attachmentswriter=csv.DictWriter(attachments, fieldnames = ["from","message","attachments","id","created_time"])

            

    
def write_comments(comments_data):
    with open('curious.csv','w', encoding='utf-8') as csvfile:
        fieldnames = ["id","message","created_time"]
        writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for comment in comments_data:
            final_dict = {key: comment[key] for key in comment if key in fieldnames}
            writer.writerow(final_dict)
    
    
