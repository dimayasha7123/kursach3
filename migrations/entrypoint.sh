#!/bin/bash

DBSTRING="host=db user=postgres password=postgres7123 dbname=active_citizen sslmode=disable"

goose postgres "$DBSTRING" up