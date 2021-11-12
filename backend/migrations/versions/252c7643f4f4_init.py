"""init

Revision ID: 252c7643f4f4
Revises: 
Create Date: 2021-11-11 08:58:15.512329

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "252c7643f4f4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "network",
        sa.Column("hostname", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("ip", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("nodeid", sa.Integer(), nullable=False),
        sa.Column("site", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("device_type", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("platform", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.Column("model", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("image", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_network_active"), "network", ["active"], unique=False)
    op.create_index(
        op.f("ix_network_device_type"), "network", ["device_type"], unique=False
    )
    op.create_index(op.f("ix_network_hostname"), "network", ["hostname"], unique=False)
    op.create_index(op.f("ix_network_id"), "network", ["id"], unique=False)
    op.create_index(op.f("ix_network_image"), "network", ["image"], unique=False)
    op.create_index(op.f("ix_network_ip"), "network", ["ip"], unique=False)
    op.create_index(op.f("ix_network_model"), "network", ["model"], unique=False)
    op.create_index(op.f("ix_network_nodeid"), "network", ["nodeid"], unique=False)
    op.create_index(op.f("ix_network_platform"), "network", ["platform"], unique=False)
    op.create_index(op.f("ix_network_site"), "network", ["site"], unique=False)
    op.create_table(
        "interface",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("mac", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("vlan", sa.Integer(), nullable=True),
        sa.Column("cidr", sa.Integer(), nullable=True),
        sa.Column("ip", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("network_device_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["network_device_id"],
            ["network.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_interface_cidr"), "interface", ["cidr"], unique=False)
    op.create_index(
        op.f("ix_interface_description"), "interface", ["description"], unique=False
    )
    op.create_index(op.f("ix_interface_id"), "interface", ["id"], unique=False)
    op.create_index(op.f("ix_interface_ip"), "interface", ["ip"], unique=False)
    op.create_index(op.f("ix_interface_mac"), "interface", ["mac"], unique=False)
    op.create_index(op.f("ix_interface_name"), "interface", ["name"], unique=False)
    op.create_index(
        op.f("ix_interface_network_device_id"),
        "interface",
        ["network_device_id"],
        unique=False,
    )
    op.create_index(op.f("ix_interface_vlan"), "interface", ["vlan"], unique=False)
    op.create_table(
        "desktop",
        sa.Column("hostname", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("ip", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("nodeid", sa.Integer(), nullable=False),
        sa.Column("site", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("mac", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("cidr", sa.Integer(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.Column("interface_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["interface_id"],
            ["interface.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_desktop_active"), "desktop", ["active"], unique=False)
    op.create_index(op.f("ix_desktop_cidr"), "desktop", ["cidr"], unique=False)
    op.create_index(op.f("ix_desktop_hostname"), "desktop", ["hostname"], unique=False)
    op.create_index(op.f("ix_desktop_id"), "desktop", ["id"], unique=False)
    op.create_index(
        op.f("ix_desktop_interface_id"), "desktop", ["interface_id"], unique=False
    )
    op.create_index(op.f("ix_desktop_ip"), "desktop", ["ip"], unique=False)
    op.create_index(op.f("ix_desktop_mac"), "desktop", ["mac"], unique=False)
    op.create_index(op.f("ix_desktop_nodeid"), "desktop", ["nodeid"], unique=False)
    op.create_index(op.f("ix_desktop_site"), "desktop", ["site"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_desktop_site"), table_name="desktop")
    op.drop_index(op.f("ix_desktop_nodeid"), table_name="desktop")
    op.drop_index(op.f("ix_desktop_mac"), table_name="desktop")
    op.drop_index(op.f("ix_desktop_ip"), table_name="desktop")
    op.drop_index(op.f("ix_desktop_interface_id"), table_name="desktop")
    op.drop_index(op.f("ix_desktop_id"), table_name="desktop")
    op.drop_index(op.f("ix_desktop_hostname"), table_name="desktop")
    op.drop_index(op.f("ix_desktop_cidr"), table_name="desktop")
    op.drop_index(op.f("ix_desktop_active"), table_name="desktop")
    op.drop_table("desktop")
    op.drop_index(op.f("ix_interface_vlan"), table_name="interface")
    op.drop_index(op.f("ix_interface_network_device_id"), table_name="interface")
    op.drop_index(op.f("ix_interface_name"), table_name="interface")
    op.drop_index(op.f("ix_interface_mac"), table_name="interface")
    op.drop_index(op.f("ix_interface_ip"), table_name="interface")
    op.drop_index(op.f("ix_interface_id"), table_name="interface")
    op.drop_index(op.f("ix_interface_description"), table_name="interface")
    op.drop_index(op.f("ix_interface_cidr"), table_name="interface")
    op.drop_table("interface")
    op.drop_index(op.f("ix_network_site"), table_name="network")
    op.drop_index(op.f("ix_network_platform"), table_name="network")
    op.drop_index(op.f("ix_network_nodeid"), table_name="network")
    op.drop_index(op.f("ix_network_model"), table_name="network")
    op.drop_index(op.f("ix_network_ip"), table_name="network")
    op.drop_index(op.f("ix_network_image"), table_name="network")
    op.drop_index(op.f("ix_network_id"), table_name="network")
    op.drop_index(op.f("ix_network_hostname"), table_name="network")
    op.drop_index(op.f("ix_network_device_type"), table_name="network")
    op.drop_index(op.f("ix_network_active"), table_name="network")
    op.drop_table("network")
    # ### end Alembic commands ###
