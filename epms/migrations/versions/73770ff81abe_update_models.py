"""Update models

Revision ID: 73770ff81abe
Revises: 37b5b1ca47af
Create Date: 2024-07-07 11:42:08.224174

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '73770ff81abe'
down_revision = '37b5b1ca47af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('examiner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('course_code', sa.String(length=50), nullable=False))
        batch_op.alter_column('question_text',
               existing_type=mysql.TEXT(),
               type_=sa.String(length=255),
               nullable=False)
        batch_op.alter_column('uploaded_at',
               existing_type=mysql.DATETIME(),
               nullable=True)
        batch_op.alter_column('status',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
        batch_op.drop_constraint('question_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('question_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'examiner', ['examiner_id'], ['id'])
        batch_op.create_foreign_key(None, 'course', ['course_code'], ['course_code'])
        batch_op.drop_column('course_id')

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
        batch_op.add_column(sa.Column('course_id', mysql.VARCHAR(length=255), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('question_ibfk_2', 'user', ['examiner_id'], ['id'])
        batch_op.create_foreign_key('question_ibfk_1', 'course', ['course_id'], ['course_code'])
        batch_op.alter_column('status',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('uploaded_at',
               existing_type=mysql.DATETIME(),
               nullable=False)
        batch_op.alter_column('question_text',
               existing_type=sa.String(length=255),
               type_=mysql.TEXT(),
               nullable=True)
        batch_op.drop_column('course_code')

    op.drop_table('examiner')
    # ### end Alembic commands ###
