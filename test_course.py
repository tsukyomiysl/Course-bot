import pytest_asyncio
import pytest
from base import base
import psycopg
from models.payload import PayLoad
from models.db import Agent
db = "postgres"

@pytest_asyncio.fixture
async def drop_db():
    try:
        connect = await psycopg.AsyncConnection.connect(dbname=db, autocommit=True)
        cursor = connect.cursor()
        await cursor.execute("CREATE DATABASE test_course")
    except psycopg.errors.DuplicateDatabase:
        pass

    yield
    await cursor.execute("DROP DATABASE IF EXISTS test_course")
    if connect :
        await connect.close()
    
@pytest.mark.asyncio
async def test_payload():

    pay = PayLoad(user_id=1, item_id=42)
    pay2 = PayLoad.unpack(pay.pack())
    assert pay2.user_id == pay.user_id
    assert pay2.item_id == pay.item_id


@pytest.mark.asyncio
async def test_confirm(drop_db):
    try:
        new_agent = Agent("test_course")
        await new_agent.get_connection()
        
        user_id = 1
        item_id = 2
        charge = "jwivj1"
        result1 = await new_agent.add_confirm(user_id, item_id, charge)
        assert result1[0] > 0

        result2  = await new_agent.get_confirm(user_id)
        assert result2[1:] == ( user_id, item_id, charge,)
    finally:
        await new_agent.pool.close()

@pytest.mark.asyncio
async def test_duoble(drop_db):
    try:
        new_agent = Agent("test_course")
        await new_agent.get_connection()
        user_id = 1
        item_id = 3
        charge1 = "hvwrvrbor3"
        charge2 = "hvwhvvhirbor3"

        result1 = await new_agent.add_confirm(user_id, item_id, charge1)
        result2 = await new_agent.add_confirm(user_id, item_id, charge2)
        result3 = await new_agent.get_confirm(user_id)
        assert result1
        assert not result2
        assert result3[1:] == ( user_id, item_id, charge1,)
    finally:
        await new_agent.pool.close()
