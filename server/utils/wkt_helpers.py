
def get_wkt_multipolygons(polygons: list) -> str:
    polygons_str = []
    for polygon in polygons:
        s = ', '.join([f"{p[0]} {p[1]}" for p in polygon])
        polygons_str.append(f"(({s}))")
    return f"MULTIPOLYGON({', '.join(polygons_str)})"
