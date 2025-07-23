# !/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：TCP-IP-Python-V4-controller
@File ：parse_json.py
@IDE ：PyCharm
@Author ：mbf
@Date ：2025/7/22 下午6:07
'''

import json


def parse_alias(alias):
    parts = alias.split('_')
    id_part = parts[0] if len(parts) > 0 else None
    type_part = parts[1] if len(parts) > 1 else None
    reposition_part = parts[2] if len(parts) > 2 else None

    reposition = reposition_part if reposition_part and 'reposition' in reposition_part else None
    type_ = type_part if type_part and 'reposition' not in type_part else None

    # 如果 alias 本身就是 reposition，则 type 为 reposition-数字，id 需要从前面推断或设为 None
    if reposition_part:
        type_ = reposition_part
        id_ = id_part  # 可能是上一级的 id，这里保留原始 id_part
    elif type_part:
        id_ = id_part
        type_ = type_part
        # reposition 是独立的字段
        reposition = reposition_part if reposition_part else None
    else:
        id_ = id_part
        type_ = None
        reposition = None

    # 如果没有显式 reposition 字段，但 type 是 upload/detect，尝试从 alias 推断 reposition
    if not reposition and type_ and 'reposition' not in type_:
        for part in parts:
            if 'reposition' in part:
                reposition = part
                break

    # 如果仍然没有 reposition，则置空
    if not reposition:
        reposition = None

    return {
        "id": id_part,
        "type": type_part,
        "reposition": reposition,
        "alias": alias
    }


def main(original_json, output_json):
    # 原始数据
    with open(original_json, "r", encoding="utf-8") as f:
        original_data = json.load(f)

    #

    output = []

    for item in original_data:
        alias = item.get("alias")
        joint = item.get("joint", [])
        parsed = parse_alias(alias)
        output.append({
            "alias": alias,
            "id": parsed["id"],
            "type": parsed["type"],
            "reposition": parsed["reposition"],
            "joint": joint
        })

    # 写入 output_json.json
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("已生成 handlebar_json.json")


if __name__ == '__main__':
    original_json = ""
    output_json = "./point_json/handlebar_json.json"
    main(original_json, output_json)

    # original_data = [
    #   {
    #     "id": "5993b7a9-d0c3-4bfc-b7ba-836659805569",
    #     "alias": "1-2_upload-2_reposition-1",
    #     "pose": [3.9983, -445.455566, 411.148163, 28.390125, -68.045593, 51.276779],
    #     "name": "P1",
    #     "tool": 0,
    #     "user": 0,
    #     "joint": [291.359467, -117.27977, 78.786201, -299.601654, 61.913452, -111.490601]
    #   },
    #   {
    #     "id": "5651914b-4cf2-4678-bed0-4439daad423a",
    #     "alias": "1-2_detect-2-A_reposition-2",
    #     "pose": [-376.781342, -237.698151, 411.125671, 28.402454, -68.04734, -7.001745],
    #     "name": "P2",
    #     "tool": 0,
    #     "user": 0,
    #     "joint": [233.090164, -117.281967, 78.783813, -299.60199, 61.915787, -111.490494]
    #   }
    # ]


