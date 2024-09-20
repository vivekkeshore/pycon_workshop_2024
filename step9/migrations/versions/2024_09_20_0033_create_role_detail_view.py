"""create role detail view

Revision ID: 86693e020849
Revises: 2049d9a0e4ae
Create Date: 2024-09-20 00:33:09.557127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '86693e020849'
down_revision: Union[str, None] = '2049d9a0e4ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

create_view_query = """
CREATE OR REPLACE VIEW users.role_detail_view AS
SELECT
    u.email,
    r.name,
    r.description,
    ur.user_id,
    ur.role_id,
    ur.is_active
FROM
    users.role r
JOIN
    users.user_role ur ON r.id = ur.role_id
JOIN 
    users.user u ON u.id = ur.user_id;
"""

delete_view_query = """
DROP VIEW IF EXISTS users.role_detail_view;
"""


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(create_view_query)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(delete_view_query)
    # ### end Alembic commands ###