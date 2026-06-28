def format_sources(sources):
    """
    Formats the sources retrieved from the metadata.
    """
    if not sources:
        return "Không tìm thấy tài liệu phù hợp (Chống ảo giác)"

    formatted = []
    for idx, src in enumerate(sources, 1):
        if isinstance(src, dict):
            title = (
                src.get("title")
                or src.get("filename")
                or src.get("name")
                or f"Tài liệu {idx}"
            )
            content = src.get("content") or src.get("text") or ""
            # Truncate content to keep the table clean
            if content:
                content = content.strip()
                content_snippet = (
                    content[:120] + "..." if len(content) > 120 else content
                )
                formatted.append(f'{idx}. **{title}**: *"{content_snippet}"*')
            else:
                formatted.append(f"{idx}. **{title}**")
        else:
            formatted.append(f"{idx}. {src}")

    return "<br>".join(formatted)
