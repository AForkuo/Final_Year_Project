"""Initial migration

Revision ID: 37b5b1ca47af
Revises: 
Create Date: 2024-07-07 04:12:29.539684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37b5b1ca47af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('examiner_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.String(length=255), nullable=False),
    sa.Column('question_text', sa.Text(), nullable=True),
    sa.Column('file_name', sa.String(length=255), nullable=True),
    sa.Column('file_path', sa.String(length=255), nullable=True),
    sa.Column('uploaded_at', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.course_code'], ),
    sa.ForeignKeyConstraint(['examiner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('schedule_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invigilator_assignment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.Column('schedule_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invigilator_assignment')
    op.drop_table('venue')
    op.drop_table('question')
    # ### end Alembic commands ###
