import sys
import json

class ConflictMerger:
    @staticmethod
    def merge_lines(base_text, a_text, b_text):
        base_lines = base_text.splitlines()
        a_lines = a_text.splitlines()
        b_lines = b_text.splitlines()

        result = []
        conflicts = []
        max_len = max(len(base_lines), len(a_lines), len(b_lines))

        for i in range(max_len):
            base_l = base_lines[i] if i < len(base_lines) else None
            a_l = a_lines[i] if i < len(a_lines) else None
            b_l = b_lines[i] if i < len(b_lines) else None

            if a_l == b_l:
                if a_l is not None:
                    result.append(a_l)
            elif a_l == base_l:
                if b_l is not None:
                    result.append(b_l)
            elif b_l == base_l:
                if a_l is not None:
                    result.append(a_l)
            else:
                conflicts.append({
                    "line": i + 1,
                    "base": base_l,
                    "agent_a": a_l,
                    "agent_b": b_l
                })
                result.append(f"<<<<<<< AGENT_A: {a_l} ======= AGENT_B: {b_l} >>>>>>>")

        return "\n".join(result), conflicts

def handle_rpc(request):
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "merge_3way",
                        "description": "Perform 3-way merge on base text, agent A edit, and agent B edit.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "base": {"type": "string"},
                                "agent_a": {"type": "string"},
                                "agent_b": {"type": "string"}
                            },
                            "required": ["base", "agent_a", "agent_b"]
                        }
                    },
                    {
                        "name": "detect_conflicts",
                        "description": "Inspect whether agent A and agent B edits contain collisions against base.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "base": {"type": "string"},
                                "agent_a": {"type": "string"},
                                "agent_b": {"type": "string"}
                            },
                            "required": ["base", "agent_a", "agent_b"]
                        }
                    }
                ]
            }
        }

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        base = args.get("base", "")
        a = args.get("agent_a", "")
        b = args.get("agent_b", "")

        merged, conflicts = ConflictMerger.merge_lines(base, a, b)
        if name == "merge_3way":
            res = {
                "merged_text": merged,
                "conflict_count": len(conflicts),
                "conflicts": conflicts
            }
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}
        elif name == "detect_conflicts":
            res = {
                "has_conflicts": len(conflicts) > 0,
                "conflict_count": len(conflicts),
                "conflicts": conflicts
            }
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()
