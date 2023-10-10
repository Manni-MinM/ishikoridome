"""added new salt model for national_id_salt and extended length of national_id

Revision ID: efca5a609c91
Revises: d819db9415d1
Create Date: 2023-10-10 21:31:49.631377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efca5a609c91'
down_revision = 'd819db9415d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('national_id_salt', sa.LargeBinary(length=16), nullable=False))
        batch_op.alter_column('national_id',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_data', schema=None) as batch_op:
        batch_op.alter_column('national_id',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=10),
               existing_nullable=False)
        batch_op.drop_column('national_id_salt')

    # ### end Alembic commands ###
