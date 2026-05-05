from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import FastAPI, Request

from ..core.config import get_settings


class MongoDB:
    _client: AsyncIOMotorClient | None = None  # ✅ class-level singleton
    _db: AsyncIOMotorDatabase | None = None

    @classmethod
    def _connect_to_db(cls):
        """
        Create ONE MongoDB client (singleton).
        """
        if cls._client is None:
            settings = get_settings()

            mongodb_uri = (
                'mongodb+srv://'
                + settings.mongodb_user
                + ':'
                + settings.mongodb_pass
                + '@'
                + settings.cluster
                + '.'
                + settings.project_string
                + '.mongodb.net/'
            )
            # print("URI",mongodb_uri)

            cls._client = AsyncIOMotorClient(mongodb_uri)   # creates new mongodb connection
            cls._db = cls._client.get_default_database(settings.database)   # gets the default database using the connection url

    # START the MongoDB Connection
    @classmethod
    async def startup(cls, app: FastAPI):
        """
        Attach DB to FastAPI app state.
        """
        cls._connect_to_db()

        # attach to app state
        app.state.mongo_client = cls._client
        app.state.db = cls._db

        # ✅ health check
        await app.state.db.command("ping")

        print("\n\t✅ MongoDB connected.\n")

    # SHUTDOWN the MongoDb Connection
    @classmethod
    async def shutdown(cls, app: FastAPI):
        """
        Close MongoDB connection.
        """
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None

        print("\n\t❌ MongoDB disconnected.\n")


    # FETCHING Interface to interact with DB
    @classmethod
    def get_db(cls, request: Request) -> AsyncIOMotorDatabase:
        """
        Dependency for routes.
        """
        return request.app.state.db



