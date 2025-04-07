"""empty message

Revision ID: 460314abf9c7
Revises: a5cffa318ac2
Create Date: 2025-04-07 17:07:29.087985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '460314abf9c7'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('firstname', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('lastname', sa.String(length=120), nullable=False))
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('password',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)
        batch_op.drop_column('lastname')
        batch_op.drop_column('firstname')
        batch_op.drop_column('username')

    op.drop_table('post')
    # ### end Alembic commands ###
