import pymysql
import queue
from contextlib import contextmanager
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class ConnectionPool:
    def __init__(self, size=10):
        self.size = size
        self.pool = queue.Queue(maxsize=size)
        self._initialize_pool()

    def _create_connection(self):
        return pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            port=settings.DB_PORT,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def _initialize_pool(self):
        for _ in range(self.size):
            try:
                self.pool.put(self._create_connection())
            except Exception as e:
                logger.error(f"Failed to initialize connection: {e}")
                # Don't fail completely on startup if one connection fails, 
                # but log it. We will handle failures dynamically.

    def get_connection(self):
        try:
            conn = self.pool.get(timeout=5)
            # Ping to check if connection is still alive
            conn.ping(reconnect=True)
            return conn
        except queue.Empty:
            logger.warning("Connection pool empty, creating a new temporary connection")
            return self._create_connection()

    def release_connection(self, conn):
        try:
            self.pool.put(conn, block=False)
        except queue.Full:
            # If the pool is full (e.g. from temporary connections), close the excess connection
            conn.close()

db_pool = ConnectionPool(size=10)

@contextmanager
def get_db_connection():
    """Context manager to safely get and release connections."""
    conn = db_pool.get_connection()
    try:
        yield conn
    finally:
        db_pool.release_connection(conn)
