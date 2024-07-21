from sqlite_base import cursor


class LocationLog:
    def __init__(self, id, location, previous_action, created_at):
        self.id = id
        self.location = location
        self.previous_action = previous_action
        self.created_at = created_at

    def __str__(self):
        return f"LocationLog(id={self.id}, location={self.location}, previous_action={self.previous_action}, created_at={self.created_at})"


def fetch_location_logs(limit):
    cursor.execute('''
        select * from location_logs
        order by id desc
        limit ?
    ''', (limit,))
    results = cursor.fetchall()
    return [
        LocationLog(
            id=result['id'],
            location=result['location'],
            previous_action=result['previous_action'],
            created_at=result['created_at']
        ) for result in results]

test = fetch_location_logs(50)
print(test)
