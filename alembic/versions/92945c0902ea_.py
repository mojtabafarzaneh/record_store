"""empty message

Revision ID: 92945c0902ea
Revises: 85346db2b822
Create Date: 2024-06-24 15:00:26.619566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92945c0902ea'
down_revision: Union[str, None] = '85346db2b822'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
