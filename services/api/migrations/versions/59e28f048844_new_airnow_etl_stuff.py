"""new airnow etl stuff

Revision ID: 59e28f048844
Revises: 55036a2dee06
Create Date: 2023-02-09 00:04:45.063306

"""
import sqlalchemy as sa
from alembic import op
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = "59e28f048844"
down_revision = "55036a2dee06"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table("stations_airnow_temp")
    op.drop_table("readings_airnow_temp")
    op.drop_table("readings_airnow")
    op.add_column("stations_airnow", sa.Column("status", sa.String(), nullable=True))
    op.add_column(
        "stations_airnow", sa.Column("elevation", sa.Numeric(11, 4), nullable=True)
    )
    op.add_column("stations_airnow", sa.Column("country", sa.String(), nullable=True))
    op.create_table(
        "stations_airnow_temp",
        sa.Column(
            "station_temp_pk",
            sa.Integer(),
            primary_key=True,
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("station_id", sa.String(), nullable=False),
        sa.Column("aqs_id", sa.String(), nullable=True),
        sa.Column("full_aqs_id", sa.String(), nullable=True),
        sa.Column("parameter", sa.String(), nullable=True),
        sa.Column("monitor_type", sa.String(), nullable=True),
        sa.Column("site_code", sa.String(), nullable=True),
        sa.Column("site_name", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("agency_id", sa.String(), nullable=True),
        sa.Column("agency_name", sa.String(), nullable=True),
        sa.Column("epa_region", sa.String(), nullable=True),
        sa.Column("latitude", sa.Numeric(10, 6), nullable=True),
        sa.Column("longitude", sa.Numeric(10, 6), nullable=True),
        sa.Column("elevation", sa.Numeric(10, 6), nullable=True),
        sa.Column("gmt_offset", sa.Numeric(10, 6), nullable=True),
        sa.Column("country_fips", sa.String(), nullable=True),
        sa.Column("cbsa_id", sa.String(), nullable=True),
        sa.Column("cbsa_name", sa.String(), nullable=True),
        sa.Column("state_aqs_code", sa.String(), nullable=True),
        sa.Column("state_abbrev", sa.String(), nullable=True),
        sa.Column("county_code", sa.String(), nullable=True),
        sa.Column("county_name", sa.String(), nullable=True),
    )
    op.create_table(
        "readings_airnow",
        sa.Column("station_id", sa.String(), nullable=False),
        sa.Column("reading_datetime", sa.DateTime(), nullable=False),
        sa.Column(
            "data_datetime",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("pm25_conc", sa.Numeric(7, 3), nullable=True),
        sa.Column("pm25_aqi", sa.Integer(), nullable=True),
        sa.Column("pm25_cat", sa.Integer(), nullable=True),
        sa.Column("pm10_conc", sa.Numeric(7, 3), nullable=True),
        sa.Column("pm10_aqi", sa.Integer(), nullable=True),
        sa.Column("pm10_cat", sa.Integer(), nullable=True),
        sa.Column("o3_conc", sa.Numeric(7, 3), nullable=True),
        sa.Column("o3_aqi", sa.Integer(), nullable=True),
        sa.Column("o3_cat", sa.Integer(), nullable=True),
        sa.Column("co_conc", sa.Numeric(7, 3), nullable=True),
        sa.Column("co_aqi", sa.Integer(), nullable=True),
        sa.Column("co_cat", sa.Integer(), nullable=True),
        sa.Column("no2_conc", sa.Numeric(7, 3), nullable=True),
        sa.Column("no2_aqi", sa.Integer(), nullable=True),
        sa.Column("no2_cat", sa.Integer(), nullable=True),
        sa.Column("so2_conc", sa.Numeric(7, 3), nullable=True),
        sa.Column("so2_aqi", sa.Integer(), nullable=True),
        sa.Column("so2_cat", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("station_id", "reading_datetime"),
    )
    op.create_table(
        "readings_airnow_temp",
        sa.Column(
            "readings_temp_pk",
            sa.Integer(),
            sa.Identity(start=1, cycle=False),
            primary_key=True,
        ),
        sa.Column("latitude", sa.String(), nullable=False),
        sa.Column("longitude", sa.String(), nullable=False),
        sa.Column("timestamp_utc", sa.String(), nullable=False),
        sa.Column("pollutant", sa.String(), nullable=True),
        sa.Column("concentration", sa.String(), nullable=True),
        sa.Column("unit", sa.String(), nullable=True),
        sa.Column("aqi", sa.String(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("site_name", sa.String(), nullable=True),
        sa.Column("site_agency", sa.String(), nullable=True),
        sa.Column("aqs_id", sa.String(), nullable=True),
        sa.Column("full_aqs_id", sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("stations_airnow_temp")
    op.drop_table("stations_airnow")
    op.create_table(
        "stations_airnow",
        sa.Column("station_id", sa.String(), nullable=False),
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
        sa.Column("station_id", sa.String(), nullable=False),
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
