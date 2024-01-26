var {{ layer.id }} = L.kqmap.mapping.{{ layer.ltype }}(
    {{ layer.jsonoptions()|safe }} );