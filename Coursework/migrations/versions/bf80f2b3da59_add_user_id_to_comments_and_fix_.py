# bf80f2b3da59_add_user_id_to_comments_and_fix_relationships.py

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = 'bf80f2b3da59'
down_revision = '6fd2f77999cf'
branch_labels = None
depends_on = None

def upgrade():
    # Drop the comment table if it exists
    op.drop_table('comment')

    # Recreate the comment table with the new user_id column and foreign key
    op.create_table(
        'comment',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('post_id', sa.Integer(), sa.ForeignKey('post.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=False)
    )

def downgrade():
    # Drop the comment table as part of downgrade
    op.drop_table('comment')
