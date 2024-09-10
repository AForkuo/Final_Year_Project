"""Set cascade delete on foreign key for course_code in question table

Revision ID: 6176070550c6
Revises: 651621105ac8
Create Date: 2024-09-10 02:44:10.574696

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6176070550c6'
down_revision = '651621105ac8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_constraint('question_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['examiner_id'], ['user_id'])
        batch_op.create_foreign_key(None, 'course', ['course_code'], ['course_code'], ondelete='CASCADE')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=1000),
               type_=sa.String(length=150),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=150),
               type_=mysql.VARCHAR(length=1000),
               existing_nullable=False)

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('question_ibfk_1', 'course', ['course_code'], ['course_code'])

    # ### end Alembic commands ###
