from sqlite_base import cursor

class Purpose:
    def __init__(self, id, type, content, created_at):
        self.id = id
        self.type = type
        self.content = content
        self.created_at = created_at

    def __str__(self):
        return f"Purpose(id={self.id}, type={self.type}, content={self.content}, created_at={self.created_at})"

def get_purpose(purpose_type):
    cursor.execute('''
        select * from purposes
        where type = ?
        order by id desc
        limit 1
    ''', (purpose_type, ))
    result = cursor.fetchone()
    return Purpose(id=result['id'], type=result['type'], content=result['content'], created_at=result['created_at'])
