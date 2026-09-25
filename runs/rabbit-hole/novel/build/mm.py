"""Small helpers that emit Meaning Model JSON records for this run's models."""
import json

PROV = ["rabbit-hole-run; authored by the calling LLM under the human's delegation"]
UNK = {"kind": "unknown"}


def event(eid, boundary, description=None, interval=None, participants=None, process_ids=None, region=None):
    e = {"id": eid, "boundary": boundary, "interval": interval, "participants": participants or {},
         "process_ids": process_ids or [], "observation_process_ids": [], "region": region,
         "substrate": None, "provenance": PROV}
    if description:
        e["description"] = description
    return e


def iv(start, end):
    return {"start": start, "end": end}


def rel(rid, kind, src, tgt, description):
    return {"id": rid, "kind": kind, "source_event_id": src, "target_event_id": tgt,
            "description": description, "authority": None, "uncertainty": UNK, "provenance": PROV}


def referent(rid, boundary, continuity, life_event):
    return {"id": rid, "boundary": boundary, "continuity_criterion": continuity,
            "lifecycle_event_id": life_event, "interval": None, "authority": None,
            "uncertainty": UNK, "provenance": PROV}


def binding(bid, referent_id, event_id, role="subject", btype="lifecycle_subject"):
    return {"id": bid, "binding_type": btype, "role": role, "referent_id": referent_id,
            "target": {"kind": "event", "event_id": event_id}, "interval": None,
            "authority": None, "uncertainty": UNK, "provenance": PROV}


def cut(cid, parent, question, unit, answers, note="authored, not measured"):
    tot = round(sum(w for _, w in answers), 9)
    assert abs(tot - 1.0) < 1e-9, (cid, tot)
    assert any(k == "remainder" for k, _ in answers), cid
    return {"id": cid, "parent_event_id": parent, "question": question, "unit": unit,
            "answers": [{"key": k, "weight": w} for k, w in answers], "provenance": PROV + [note]}


def scalar(pid, lo, hi, init, unit, role, support, frame="story-world", update="observed"):
    return {"id": pid, "value_type": {"kind": "scalar", "bounds": {"minimum": lo, "maximum": hi}},
            "initial_value": {"kind": "scalar", "value": init}, "unit": unit, "update_mode": update,
            "reference_frame": frame, "scale": {"semantic_role": role}, "support": support,
            "uncertainty": UNK, "axes": [], "access_scopes": [], "provenance": PROV}


def dump(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
