"""Update DB schema

Revision ID: db9881333638
Revises: 3357ecf8449f
Create Date: 2025-06-22 10:50:11.375486

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "db9881333638"
down_revision: Union[str, Sequence[str], None] = "3357ecf8449f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("tutorials", sa.Column("content", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("tutorials", "content")
    # ### end Alembic commands ###
