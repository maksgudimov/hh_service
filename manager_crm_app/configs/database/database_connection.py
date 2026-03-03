from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from configs.database.base import Configuration



class DatabaseConnection:
    """Асинхронный коннект к БД через SQLAlchemy.

    Attributes:
        configuration (Configuration): Конфиги базы.
        engine: Асинк движок.
        async_session: Фабрика асинк сессий.
    """

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.engine = create_async_engine(
            self.configuration.get_uri(),
            echo=False,
            pool_size=5,
            max_overflow=10,
        )
        self.async_session = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def close(self) -> None:
        """
            Закрытие соединения
        """
        await self.engine.dispose()

    @property
    def session(self) -> async_sessionmaker:
        """
            Возвращает сессию
        Returns:
            AsyncSession: асинк сессия.
        """
        return self.async_session
