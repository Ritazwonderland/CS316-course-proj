from flask import current_app as app
from sqlalchemy import text

class Feedback:
    def __init__(self, id, uid, pid, sid, review, time_reviewed):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.review = review
        self.time_reviewed = time_reviewed

    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute("""
SELECT id, uid, pid, sid, review, time_reviewed
FROM Feedback
WHERE uid = :user
ORDER BY time_reviewed desc
""",
                              {"user": uid})
        if not rows:
            return []
        else:
            return [{"id":row[0], "uid":row[1], "pid":row[2], "sid":row[3], "review":row[4], "time_reviewed":row[5]} for row in rows]

    @staticmethod
    def update(id, uid, pid, sid, review, time_reviewed):   
        with app.db.engine.begin() as conn:
            conn.execute(text('''
                INSERT INTO Feedback (id, uid, pid, sid, review, time_reviewed)
                VALUES (:vall, :user, :prod, :sell, :rev, :time)
                ON CONFLICT (uid, pid, sid)
                DO UPDATE
                SET id = :vall, review = :rev, time_reviewed = :time
                RETURNING *;
            '''), {
                "vall": id,
                "user": uid,
                "prod": pid,
                "sell": sid,
                "rev": review,
                "time": time_reviewed
            })

    @staticmethod
    def delete(uid, pid, sid):   
        with app.db.engine.begin() as conn:
            conn.execute(text('''
                DELETE FROM FEEDBACK
                WHERE uid = :user and pid = :prod and sid = :sell
                RETURNING *;
            '''), {
                "user": uid,
                "prod": pid,
                "sell": sid
            })

    @staticmethod
    def psummary():
        rows = app.db.execute("""
        SELECT pid, count(*) as num
        FROM FEEDBACK
        GROUP BY pid
        ORDER BY num desc
        """)
        return [{"pid": row[0], "num": row[1]} for row in rows]

    @staticmethod
    def ssummary():
        rows = app.db.execute("""
        SELECT sid, count(*) as num
        FROM FEEDBACK
        GROUP BY sid
        ORDER BY num desc
        """)
        return [{"sid": row[0], "num": row[1]} for row in rows]

