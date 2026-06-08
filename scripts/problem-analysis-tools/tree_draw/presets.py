def segment_size_from_array(raw: str) -> int:
    values = [item for item in raw.replace(",", " ").split() if item]
    if not values:
        raise ValueError("--array 不能为空。")
    return len(values)
