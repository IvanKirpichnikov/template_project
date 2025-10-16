__all__ = (
    "meta_data",
    "user_table",
    "access_token_table",
)

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, MetaData, String, Table
from sqlalchemy.orm import registry

from template_project.application.access_token.entity import AccessToken
from template_project.application.user.entity import User


meta_data = MetaData()

user_table = Table(
    "users",
    meta_data,
    Column("id", UUID, primary_key=True),
    Column("email", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("deleted_at", DateTime(timezone=True)),
    Column("created_at", DateTime(timezone=True), nullable=False),
)

access_token_table = Table(
    "access_token",
    meta_data,
    Column("id", UUID, primary_key=True),
    Column("user_id", UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("revoked", Boolean, nullable=False),
    Column("expires_in", DateTime(timezone=True), nullable=False),
    Column("deleted_at", DateTime(timezone=True)),
    Column("created_at", DateTime(timezone=True), nullable=False),
)

mapper_registry = registry()

mapper_registry.map_imperatively(User, user_table)
mapper_registry.map_imperatively(AccessToken, access_token_table)
