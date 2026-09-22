# Imported provenance corpus inventory

This report is structure-only. The source export remains outside Git; the ignored manifest stores hashes and file sizes before parsing.

- Files: **752**
- Bytes: **668285942**
- Parse-error records: **0**
- File types: `{".json": 188, ".jsonl": 564}`
- Roles: `{"assistant": 52850, "tool": 46792, "user": 3773}`
- Event-like types: `{}`
- Categorical fields: `{"content_type": {"code": 81768, "execution_output": 5312, "image_asset_pointer": 1123, "multimodal_text": 42941, "reasoning_recap": 5700, "tether_browsing_display": 136, "text": 47190, "thoughts": 15895}, "default_model_slug": {"gpt-5-6": 3, "gpt-5-6-thinking": 117947, "gpt-5.6-luna-wm": 1, "gpt-5.6-terra-wm": 1}, "message_type": {"image": 30, "next": 117772, "stream": 555, "variant": 20}, "model_slug": {"gpt-5-4-auto-thinking": 174, "gpt-5-4-thinking": 931, "gpt-5-6": 3, "gpt-5-6-instant": 13, "gpt-5-6-thinking": 116749, "gpt-5.6-luna-wm": 1238, "gpt-5.6-sol-wm": 167, "gpt-5.6-terra-wm": 131}, "recipient": {"all": 119410, "api_tool.call_tool": 37065, "api_tool.find_in_resource": 917, "api_tool.list_resources": 3290, "api_tool.read_resource": 427, "api_tool.search_plugins": 7, "assistant": 266, "container.exec": 2807, "de1d73e.create": 14, "de1d73e.update": 14, "genui.run": 49, "genui.search": 70, "local.handoff": 294, "python": 1414, "study_os_design_bakery_com__jit_plugin.study_os_append_conversation_turn": 434, "study_os_design_bakery_com__jit_plugin.study_os_checkpoint": 14, "study_os_design_bakery_com__jit_plugin.study_os_record_attempt": 112, "study_os_design_bakery_com__jit_plugin.study_os_record_learning_event": 14, "study_os_design_bakery_com__jit_plugin.study_os_resume_learning_context": 14, "study_os_design_bakery_com__jit_plugin.study_os_start_session": 21, "study_os_design_bakery_com__jit_plugin.study_os_status": 7, "t2uay3k.sj1i4kz": 189, "turn_plan.update_turn_plan": 14, "web.run": 11935}, "resolved_model_slug": {"gpt-5-4-auto-thinking": 1105, "gpt-5-6": 3, "gpt-5-6-instant": 13, "gpt-5-6-thinking": 116812}, "status": {"cancelled": 30, "completed": 567, "done": 11468, "failed_with_in_kernel_exception": 20, "final": 250, "finished_successfully": 102962, "in_progress": 830, "pending": 50, "requested": 4686, "running": 85, "success": 3270, "waiting_for_user_response_on_plan": 5}, "thinking_effort": {"extended": 114187, "xhigh": 186}}`

## Use in the harness

The corpus is a newer provenance source for ontology and long-horizon task calibration. It is kept separate from the existing local Work gold until origin, export shape, and matched-task eligibility are verified. Derived samples must carry a source hash and must not include message bodies.
