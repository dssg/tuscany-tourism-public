#!/usr/bin/env bash

# create the pgpass file
touch ~/.pgpass
chmod 600 .pgpass

#replace the credentials below
#echo db.dssg.io:5432:dbname:username:password >> ~/.pgpass
#echo "host:port:database:username:password" >> ~/.pgpass

export PGPASSFILE=~/.pgpass


export PGHOST=$(cut -d':' -f1 $PGPASSFILE)
export PGPORT=$(cut -d':' -f2 $PGPASSFILE)
export PGDATABASE=$(cut -d':' -f3 $PGPASSFILE)
export PGUSER=$(cut -d':' -f4 $PGPASSFILE)
export PGPASSWORD=$(cut -d':' -f5 $PGPASSFILE)
export PGCONNECTION=host=$PGHOST\ port=$PGPORT\ user=$PGUSER\ password=$PGPASSWORD\ dbname=$PGDATABASE

#run the og2og2 as below
#ogr2ogr -f "PostgreSQL" PG:"$PGCONNECTION" -t_srs EPSG:4326 Com2016_WGS84_g.shp -nlt PROMOTE_TO_MULTI -lco precision=NO -lco SCHEMA=tuscany


