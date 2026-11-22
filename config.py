from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    db_server: str = "localhost"
    db_name: str = "AdventureWorksDW2022"
    db_user: str = "sa"
    db_password: str

    @property
    def connection_string(self) -> str:
        return (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={self.db_server};DATABASE={self.db_name};"
            f"UID={self.db_user};PWD={{{self.db_password}}};"
            "TrustServerCertificate=yes;"
        )

settings = Settings()  # type: ignore[call-arg]
