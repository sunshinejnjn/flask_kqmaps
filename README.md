Flask-KQMaps is a Flask Extension for KQWebMap API for Leaflet (aka KQClient for Leaflet API)
Current embedded version of KQWebMap is v8.4 (release on 02/JUL/2021)
for more information on KQWebMap API for Leaflet, please refer to: http://oa.kqgeo.com:20258/kqgis_2d/

Installation using pip:
pip install flask_kqmaps

Usage example:

Import the module:
    from flask_kqmaps import KQMaps

Initialize flask app with the extension:
    kqmaps=KQMaps()
    kqmaps.init_app(app)

In page templates:
- Put this at the end of the page "header" (or head block)
    {{ kqmap_init }}

- Put this somewhere at the end of the "body" part (with other scripts):
    {{ kq_scripts }}

- Put either {{ kq_easymaps }} or {{ kq_maps.SAMPLE_MAP }} to where you want the map to be shown on the page.
    kq_easymaps would show any registered maps and kq_maps.SAMPLE_MAP would show only the specific map named "SAMPLE_MAP".


Generate and register a map with flask_kqmaps and render with flask:
    from flask_kqmaps import *

    #Instantiate a map object
    pmap = GenKQMap(mapname, attributionControl=True, center=[32.05382, 118.77730], zoom=17, zoomControl=True)

    #Add some base map layers
    pmap.add_layer(KQLayer(name="Basemap", ltype="tiandituTileLayer", id="vec", isbasemap=True,
                           options={"layerType": "vec", "attribution": None}))
    pmap.add_layer(KQLayer(name="Label", ltype="tiandituTileLayer", id="cva", isbasemap=False,
                           options={"layerType": "cva", "attribution": None}))

    #Initialize a layergroup
    layergroups = KQLayerGroup("SampleArea", id="lgs")

    #Add Polygon(s) to the layergroup
    layergroups.add_polygon([[32.0560441,118.7789681], [32.0559059, 118.7774060], [32.0548220, 118.7776785],
        [32.0546329,118.7760735],[32.0539564,118.7761936],[32.0538436,118.7752581],
        [32.0532580,118.7753611],[32.0531416,118.7748976],[32.0520568,118.7749330],
        [32.0520459,118.7758771],[32.0523059,118.7789692]], color="light blue", id="polygon1")

    #define some icon and add it to the map for use
    picon_in = KQIcon(id="iconin", iconUrl='http://SOME_URL', iconSize=[29, 26])
    pmap.add_icon(picon_in)

    #put some markers into a marker layer(group)
    layergroup1 = KQLayerGroup("MarkerLayer", id="lgm")
    layergroup1.add_marker([32.0525987,118.7775229], icon="iconin", id="1",popup='Hello there, I'm a marker.')

    #Add the layergroups to the map
    pmap.add_layer(layergroups)
    pmap.add_layer(layergroup1)

    #register map with kqmaps
    kqmaps.register(pmap)

    #render with template
    return_page = make_response(render_template("page_template.html"))

License:
    This software is licensed under GNU GPLv3. Please make your modifications under the same license and publish them openly.
