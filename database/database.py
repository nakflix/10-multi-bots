import pymongo


class Database:
    """
    One Database instance per bot, so each bot can use a completely
    different MongoDB connection/database. An instance is attached to
    each Bot as `client.db` (see levi.py), and plugins call it via the
    `client` object they already receive in every handler, e.g.:

        await client.db.add_user(user_id)
    """

    def __init__(self, uri: str, database_name: str):
        self._client = pymongo.MongoClient(uri)
        self.db = self._client[database_name]
        self.user_data = self.db['users']

    async def present_user(self, user_id: int) -> bool:
        found = self.user_data.find_one({'_id': user_id})
        return bool(found)

    async def add_user(self, user_id: int):
        self.user_data.insert_one({'_id': user_id})
        return

    async def full_userbase(self):
        user_docs = self.user_data.find()
        return [doc['_id'] for doc in user_docs]

    async def del_user(self, user_id: int):
        self.user_data.delete_one({'_id': user_id})
        return
