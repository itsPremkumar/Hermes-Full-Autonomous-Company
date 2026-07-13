@echo off
set PGDATA=C:\Program Files\PostgreSQL\17\data
set PGBIN=C:\Program Files\PostgreSQL\17\bin
set HBA=%PGDATA%\pg_hba.conf

REM Backup (idempotent)
if not exist "%HBA%.bak2" copy "%HBA%" "%HBA%.bak2" >nul

REM Allow local TCP trust so we can create the role/db without the postgres password.
REM On Windows psql uses TCP (host), so change the 127.0.0.1 line, NOT the local line.
powershell -NoProfile -Command "(Get-Content '%HBA%') -replace 'host    all             all             127.0.0.1/32            scram-sha-256','host    all             all             127.0.0.1/32            trust' | Set-Content '%HBA%'"

net stop postgresql-x64-17
net start postgresql-x64-17
ping -n 4 127.0.0.1 >nul

"%PGBIN%\psql.exe" -U postgres -h 127.0.0.1 -w -c "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='paperclip') THEN CREATE ROLE paperclip LOGIN PASSWORD 'paperclippw' SUPERUSER; END IF; END $$;"
"%PGBIN%\psql.exe" -U postgres -h 127.0.0.1 -w -c "SELECT 1 FROM pg_database WHERE datname='paperclip';" | findstr "1" >nul && echo DB_EXISTS || "%PGBIN%\psql.exe" -U postgres -h 127.0.0.1 -w -c "CREATE DATABASE paperclip OWNER paperclip;"

REM Restore secure hba
copy /Y "%HBA%.bak2" "%HBA%" >nul
net stop postgresql-x64-17
net start postgresql-x64-17

echo SETUP_DONE
