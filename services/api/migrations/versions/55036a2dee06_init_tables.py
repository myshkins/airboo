"""init tables

Revision ID: 55036a2dee06
Revises:
Create Date: 2023-02-04 19:35:11.180413

"""
import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = "55036a2dee06"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("create extension if not exists postgis")
    op.create_table(
        "readings_airnow",
        sa.Column("station_id", sa.String(), autoincrement=False, nullable=False),
        sa.Column(
            "reading_datetime", sa.DateTime(), autoincrement=False, nullable=False
        ),
        sa.Column("request_datetime", sa.DateTime(), nullable=False),
        sa.Column("pm_10_conc", sa.Numeric(7, 3), nullable=True),
        sa.Column("pm_10_aqi", sa.Numeric(7, 3), nullable=True),
        sa.Column("pm_10_aqi_cat", sa.Numeric(2, 1), nullable=True),
        sa.Column("pm_25_conc", sa.Numeric(7, 3), nullable=True),
        sa.Column("pm_25_aqi", sa.Numeric(7, 3), nullable=True),
        sa.Column("pm_25_aqi_cat", sa.Numeric(2, 1), nullable=True),
        sa.PrimaryKeyConstraint("station_id", "reading_datetime"),
    )
    op.create_table(
        "readings_airnow_temp",
        sa.Column("station_id", sa.String(), autoincrement=False, nullable=False),
        sa.Column(
            "reading_datetime", sa.DateTime(), autoincrement=False, nullable=False
        ),
        sa.Column("request_datetime", sa.DateTime(), nullable=False),
        sa.Column("pm_10_conc", sa.Numeric(7, 3), nullable=True),
        sa.Column("pm_10_aqi", sa.Numeric(7, 3), nullable=True),
        sa.Column("pm_10_aqi_cat", sa.Numeric(2, 1), nullable=True),
        sa.Column("pm_25_conc", sa.Numeric(7, 3), nullable=True),
        sa.Column("pm_25_aqi", sa.Numeric(7, 3), nullable=True),
        sa.Column("pm_25_aqi_cat", sa.Numeric(2, 1), nullable=True),
        sa.PrimaryKeyConstraint("station_id", "reading_datetime"),
    )
    op.create_table(
        "readings_waqi",
        sa.Column("station_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("station_name", sa.String(), nullable=False),
        sa.Column(
            "reading_datetime", sa.DateTime(), autoincrement=False, nullable=False
        ),
        sa.Column("request_datetime", sa.DateTime(), nullable=False),
        sa.Column("latitude", sa.Numeric(10, 6), nullable=True),
        sa.Column("longitude", sa.Numeric(10, 6), nullable=True),
        sa.Column("pm_10", sa.Numeric(7, 3), nullable=True),
        sa.Column("pm_25", sa.Numeric(7, 3), nullable=True),
        sa.Column("co", sa.Numeric(7, 3), nullable=True),
        sa.Column("h", sa.Numeric(7, 3), nullable=True),
        sa.Column("no2", sa.Numeric(7, 3), nullable=True),
        sa.Column("o3", sa.Numeric(7, 3), nullable=True),
        sa.Column("p", sa.Numeric(7, 3), nullable=True),
        sa.Column("so2", sa.Numeric(7, 3), nullable=True),
        sa.Column("t", sa.Numeric(7, 3), nullable=True),
        sa.Column("w", sa.Numeric(7, 3), nullable=True),
        sa.Column("wg", sa.Numeric(7, 3), nullable=True),
        sa.PrimaryKeyConstraint("station_id", "reading_datetime"),
    )
    op.create_table(
        "readings_waqi_temp",
        sa.Column("station_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("station_name", sa.String(), nullable=False),
        sa.Column("latitude", sa.Numeric(10, 6), nullable=True),
        sa.Column("longitude", sa.Numeric(10, 6), nullable=True),
        sa.Column("pm_10", sa.Numeric(7, 3), nullable=True),
        sa.Column("pm_25", sa.Numeric(7, 3), nullable=True),
        sa.Column("co", sa.Numeric(7, 3), nullable=True),
        sa.Column("h", sa.Numeric(7, 3), nullable=True),
        sa.Column("no2", sa.Numeric(7, 3), nullable=True),
        sa.Column("o3", sa.Numeric(7, 3), nullable=True),
        sa.Column("p", sa.Numeric(7, 3), nullable=True),
        sa.Column("so2", sa.Numeric(7, 3), nullable=True),
        sa.Column("t", sa.Numeric(7, 3), nullable=True),
        sa.Column("w", sa.Numeric(7, 3), nullable=True),
        sa.Column("wg", sa.Numeric(7, 3), nullable=True),
        sa.Column(
            "reading_datetime", sa.DateTime(), autoincrement=False, nullable=False
        ),
        sa.Column("request_datetime", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("station_id", "reading_datetime"),
    )
    op.create_table(
        "stations_airnow",
        sa.Column("station_id", sa.String(), autoincrement=False, nullable=False),
        sa.Column("station_name", sa.String(), nullable=False),
        sa.Column("agency_name", sa.String(), nullable=False),
        sa.Column("latitude", sa.Numeric(10, 6), nullable=False),
        sa.Column("longitude", sa.Numeric(10, 6), nullable=False),
        sa.Column(
            "location_coord",
            Geometry(geometry_type="POINT"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("station_id"),
    )
    op.create_table(
        "stations_airnow_temp",
        sa.Column("station_id", sa.String(), autoincrement=False, nullable=False),
        sa.Column("station_name", sa.String(), nullable=False),
        sa.Column("agency_name", sa.String(), nullable=False),
        sa.Column("latitude", sa.Numeric(10, 6), nullable=False),
        sa.Column("longitude", sa.Numeric(10, 6), nullable=False),
        sa.Column(
            "location_coord",
            Geometry(geometry_type="POINT"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("station_id"),
    )
    op.create_table(
        "stations_waqi",
        sa.Column("station_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("station_name", sa.String(), nullable=False),
        sa.Column("latitude", sa.Numeric(10, 6), nullable=False),
        sa.Column("longitude", sa.Numeric(10, 6), nullable=False),
        sa.Column("request_datetime", sa.DateTime(), nullable=True),
        sa.Column("data_datetime", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("station_id"),
    )
    op.create_table(
        "stations_waqi_temp",
        sa.Column("station_id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("station_name", sa.String(), nullable=False),
        sa.Column("latitude", sa.Numeric(10, 6), nullable=False),
        sa.Column("longitude", sa.Numeric(10, 6), nullable=False),
        sa.Column("request_datetime", sa.DateTime(), nullable=True),
        sa.Column("data_datetime", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("station_id"),
    )


def downgrade() -> None:
    pass
    # op.drop_table("stations_waqi_temp")
    # op.drop_table("stations_waqi")
    # op.drop_table("stations_airnow_temp")
    # op.drop_table("stations_airnow")
    # op.drop_table("readings_waqi_temp")
    # op.drop_table("readings_waqi")
    # op.drop_table("readings_airnow_temp")
    # op.drop_table("readings_airnow")
    # op.drop_table("stations_airnow_2")
    # op.drop_table("stations_airnow_temp_2")
