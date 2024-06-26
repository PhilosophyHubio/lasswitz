"""manusciprt

Revision ID: 5581a543526d
Revises: 
Create Date: 2024-04-22 23:44:09.322551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5581a543526d'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('manuscript',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('zotid', sa.Integer(), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('abstract', sa.Text(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('revision', sa.Integer(), nullable=True),
    sa.Column('tag', sa.Text(), nullable=True),
    sa.Column('keywords', sa.Text(), nullable=True),
    sa.Column('date_created', sa.Text(), nullable=True),
    sa.Column('date_modified', sa.Text(), nullable=True),
    sa.Column('language', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_manuscript'))
    )
    op.create_table('user',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('displayname', sa.String(length=1024), nullable=True),
    sa.Column('givenname', sa.String(length=1024), nullable=True),
    sa.Column('familyname', sa.String(length=1024), nullable=True),
    sa.Column('initials', sa.String(length=100), nullable=True),
    sa.Column('mail', sa.String(length=200), nullable=True),
    sa.Column('telephone', sa.String(length=50), nullable=True),
    sa.Column('organization', sa.String(length=1024), nullable=True),
    sa.Column('organizationunit', sa.String(length=1024), nullable=True),
    sa.Column('preferredlanguage', sa.String(length=50), nullable=True),
    sa.Column('website', sa.String(length=2048), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    op.create_table('authorship_table',
    sa.Column('manuscript_id', sa.Uuid(), nullable=True),
    sa.Column('creator_id', sa.Uuid(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], name=op.f('fk_authorship_table_creator_id_user')),
    sa.ForeignKeyConstraint(['manuscript_id'], ['manuscript.id'], name=op.f('fk_authorship_table_manuscript_id_manuscript'))
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('authorship_table')
    op.drop_table('user')
    op.drop_table('manuscript')
    # ### end Alembic commands ###
