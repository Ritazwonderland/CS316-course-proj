from sqlalchemy import create_engine, text


class DB:
    """Hosts all functions for querying the database.

    Use the execute() method if you want to execute a single SQL
    statement (which will be in a transaction by itself.

    If you want to execute multiple SQL statements in the same
    transaction, use the following pattern:

    >>> with app.db.engine.begin() as conn:
    >>>     # everything in this block executes as one transaction
    >>>     value = conn.execute(text('SELECT...'), bar='foo').first()[0]
    >>>     conn.execute(text('INSERT...'), par=value)
    >>>     conn.execute(text('UPDATE...'), par=value)
    >>>

    """
    def __init__(self, app):
        self.engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    def execute(self, query, args=None):
        if args is None:
            args = {}
        print(f"Executing query: {query}")
        print(f"With args: {args}")
        with self.engine.connect() as conn:
            result = conn.execute(text(query), args)
            return result.fetchall()
