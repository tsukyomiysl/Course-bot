from psycopg_pool import AsyncConnectionPool
import psycopg
from dataclasses import dataclass
from psycopg.errors import UniqueViolation

@dataclass
class Agent():
    def __init__(self, db_path):
        self.db = db_path
        self.pool = AsyncConnectionPool(
            conninfo=f'dbname={self.db}',
            kwargs={"autocommit":True},
            min_size = 1,
            max_size=4,
            open=False
        )
    async def get_connection(self):
        await self.pool.open()
        async with self.pool.connection() as conn:
            cursor = conn.cursor()
            await cursor.execute("""
        CREATE TABLE IF NOT EXISTS confirms (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        item_id BIGINT NOT NULL,
        charge_id TEXT NOT NULL UNIQUE,
        UNIQUE (user_id, item_id)
        )
        """)

            
    async def add_confirm(self, user_id , item_id, charge_id):
        try:
            async with self.pool.connection() as conn:
                async with conn.transaction():
                    cursor = conn.cursor()
                    await cursor.execute("INSERT INTO confirms (user_id, item_id, charge_id) VALUES (%s,%s,%s) RETURNING id ",(user_id, item_id, charge_id,))
                    result = await cursor.fetchone()
                    return result
        except psycopg.errors.UniqueViolation:
            return None
        

    async def get_confirm(self, user_id):
        async with self.pool.connection() as conn:
            cursor = conn.cursor()
            await cursor.execute("SELECT * FROM confirms WHERE user_id = %s",(user_id,))
            result = await cursor.fetchone()
            return result
    
