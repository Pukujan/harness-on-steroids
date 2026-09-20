# ChatGPT Work desktop only (`codex_work_desktop`)

Sessions: **87**
- with wait: **31**
- with js: **5**
- with send_message: **25**
- with spawn/send (multi-agent): **26**
- with apply_patch: **1**

## first tool

| tool | sessions |
| --- | --- |
| exec | 78 |
| create_thread | 3 |
| shell_command | 2 |

## tools

| tool | count |
| --- | --- |
| exec | 7582 |
| wait | 457 |
| js | 81 |
| send_message | 70 |
| shell_command | 44 |
| wait_agent | 37 |
| list_agents | 9 |
| spawn_agent | 5 |
| create_thread | 3 |
| send_message_to_thread | 3 |
| multi_agent_v1 | 3 |
| view_image | 2 |
| apply_patch | 2 |
| interrupt_agent | 1 |
| read_thread_terminal | 1 |

## bigrams

| bigram | count |
| --- | --- |
| exec -> exec | 7217 |
| wait -> wait | 235 |
| exec -> wait | 217 |
| wait -> exec | 211 |
| js -> js | 58 |
| exec -> send_message | 53 |
| send_message -> exec | 38 |
| shell_command -> shell_command | 35 |
| exec -> js | 23 |
| js -> exec | 23 |
| wait_agent -> wait_agent | 18 |
| wait -> send_message | 9 |
| send_message -> wait_agent | 7 |
| wait_agent -> list_agents | 5 |
| wait_agent -> exec | 5 |
| exec -> wait_agent | 5 |
| wait_agent -> send_message | 5 |
| send_message -> wait | 4 |
| list_agents -> wait_agent | 4 |
| exec -> list_agents | 3 |
