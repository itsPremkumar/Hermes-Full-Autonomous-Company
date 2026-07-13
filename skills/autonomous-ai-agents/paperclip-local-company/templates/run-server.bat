@echo off
REM Known-good Windows launcher for the Paperclip server (tsx on source).
REM Uses native C:\ paths (no MSYS rewriting) and the .bin/tsx shim.
cd /d C:\one\paperclip-company\paperclip\server
set PORT=3100
set HOST=0.0.0.0
set SERVE_UI=true
set BETTER_AUTH_SECRET=paperclip-dev-secret-change-me
set PAPERCLIP_DEPLOYMENT_MODE=authenticated
set PAPERCLIP_DEPLOYMENT_EXPOSURE=private
set PAPERCLIP_PUBLIC_URL=http://localhost:3100
set PAPERCLIP_HOME=C:\one\paperclip-company\data\paperclip
set PAPERCLIP_MIGRATION_AUTO_APPLY=true
REM REQUIRED on Windows admin accounts (embedded Postgres refuses admin). Point at your Postgres service.
set DATABASE_URL=postgres://postgres:PASSWORD@localhost:5432/paperclip
C:\one\paperclip-company\paperclip\node_modules\.bin\tsx src/index.ts >> C:\one\paperclip-company\tsx-out.log 2>&1
echo SERVER_EXIT=%ERRORLEVEL% >> C:\one\paperclip-company\tsx-out.log
