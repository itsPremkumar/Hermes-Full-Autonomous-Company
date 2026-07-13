# Safe-mode pitfall (MCP write tools blocked by default)

## Symptom
MCP client connects fine, but every useful action returns:
`Error: Runtime "mcp" is in safe mode and cannot <operation>. Set ALLOW_UNSAFE_MCP_TOOLS=1 to enable this intentionally.`

## Root cause
The server's capability table marks the `mcp` runtime with `safeMode: true`. A guard function
(`assertSafeMutationAllowed`) throws `ForbiddenError` for any mutation unless the env flag is set.
Read tools (read_*, list_*, health_check, get_*) are NOT gated and work normally.

## Affected tools (example: Automated-Video-Generator)
Blocked: write_input_script, delete_input_script, upload_asset, delete_asset, delete_output,
update_env_config, run_pipeline_command.
Allowed: read_input_script, list_output_videos, read_output_file, validate_input_script,
health_check, get_workspace_paths, list_jobs, list_voices, list_local_assets, search_free_video,
download_free_video, get_system_info, read_env_config (masked), etc.

## Fix / enable
One-off:   `ALLOW_UNSAFE_MCP_TOOLS=1 npm run mcp`
Client cfg: add `"env": { "ALLOW_UNSAFE_MCP_TOOLS": "1" }` to the mcpServers entry.

## Why this matters for docs
The flag is usually UNDOCUMENTED in README — the #1 reason a user thinks "MCP is broken".
Always document it next to the MCP setup section, and explain the safe-by-default rationale
(filesystem write protection for untrusted agents).
