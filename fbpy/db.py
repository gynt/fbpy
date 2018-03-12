

import sqlite3

class DB(object):

    def __init__(self, path):
        self.conn=sqlite3.connect(path)
        #tables=self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='table_name';").fetchall()
        #if len(tables)==0:
        self.init_db()

    def close(self):
        self.conn.commit()
        self.conn.close()
        
    def init_db(self):
        posts="""CREATE TABLE IF NOT EXISTS posts (
                                                id integer PRIMARY KEY,
                                                post_id text,
                                                from_name text,
                                                from_id text,
                                                message text, 
                                                created_time text
                                                );"""
        attachments="""CREATE TABLE IF NOT EXISTS attachments (
                                                id integer PRIMARY KEY,
                                                post_id text,
                                                description text,
                                                media_image_height integer,
                                                media_image_src text,
                                                media_image_width integer,
                                                target_id text,
                                                target_url text,
                                                title text,
                                                type text,
                                                url text
                                                );"""
        reactions="""CREATE TABLE IF NOT EXISTS reactions (
                                                id integer PRIMARY KEY,
                                                post_id text,
                                                uid text,
                                                type text,
                                                name text
                                                );"""
        creactions="""CREATE TABLE IF NOT EXISTS creactions (
                                                id integer PRIMARY KEY,
                                                post_id text,
                                                comment_id text,
                                                uid text,
                                                type text,
                                                name text
                                                );"""
        subcreactions="""CREATE TABLE IF NOT EXISTS subcreactions (
                                                id integer PRIMARY KEY,
                                                post_id text,
                                                comment_id text,
                                                subcomment_id text,
                                                uid text,
                                                type text,
                                                name text
                                                );"""
        comments="""CREATE TABLE IF NOT EXISTS comments(
                                                id integer PRIMARY KEY,
                                                post_id text,
                                                comment_id text,
                                                from_id text,
                                                from_name text,
                                                message text,
                                                created_time
                                                );"""
        subcomments="""CREATE TABLE IF NOT EXISTS subcomments(
                                                id integer PRIMARY KEY,
                                                post_id text,
                                                comment_id text,
                                                subcomment_id text,
                                                from_id text,
                                                from_name text,
                                                message text,
                                                created_time
                                                );"""

        for i in [posts, attachments, reactions, creactions, subcreactions, comments, subcomments]:
            cursor=self.conn.cursor()    
            cursor.execute(i)
        self.conn.commit()
        
    def get_cursor(self):
        return self.conn.cursor()


def precompile(table, headers):
    return """INSERT INTO """+table+""" ("""+','.join(headers)+""") VALUES ("""+','.join(['?']*len(headers))+""");"""

def serialize_post_db(db, post):
    cursor=db.get_cursor()

    spost=precompile('posts',['post_id','from_name','from_id','message','created_time'])
    cursor.execute(spost, [post["id"],post["from"]["name"],post["from"]["id"],post["message"],post["created_time"]])

    for attachment in post['attachments']['data']:
        r={"post_id":post['id']}
        level(r, attachment)
        sattachment=precompile('attachments', list(r.keys()))
        cursor.execute(sattachment, list(r.values()))

    for reaction in post['reactions']['data']:
        r={"post_id":post['id']}
        level(r, reaction)
        r['uid']=r['id']
        del r['id']
        sreaction=precompile('reactions', list(r.keys()))
        cursor.execute(sreaction, list(r.values()))

    scomment=precompile('comments',["post_id","comment_id","from_id","from_name","created_time","message"])
    ssubcomment=precompile('subcomments',["post_id","comment_id","subcomment_id","from_id","from_name","created_time","message"])

    screaction=precompile('creactions',["post_id","comment_id","uid","name","type"])
    ssubcreaction=precompile('subcreactions',["post_id","comment_id","subcomment_id","uid","name","type"])

    for comment in post['comments']['data']:
        cursor.execute(scomment, [post["id"], comment["id"], comment["from"]["id"], comment["from"]["name"], comment["created_time"], comment["message"]])

        if 'reactions' in comment:

            for creaction in comment['reactions']['data']:
                cursor.execute(screaction, [post["id"], comment["id"], creaction["id"], creaction["name"], creaction["type"]])

        if 'comments' in comment:
            
            for subcomment in comment['comments']['data']:
                cursor.execute(ssubcomment, [post["id"], comment["id"], subcomment["id"], subcomment["from"]["id"], subcomment["from"]["name"], subcomment["created_time"], subcomment["message"]])

                if 'reactions' in subcomment:

                    for subcreaction in subcomment['reactions']['data']:
                        cursor.execute(ssubcreaction, [post["id"], comment["id"], subcomment["id"], subcreaction["id"], subcreaction["name"], subcreaction["type"]])

    db.conn.commit()
