# -*- coding: utf-8
"""
    flask_kqmaps
    ~~~~~~~~~~~~~~~~~~
    KQWebMap API for Flask. http://oa.kqgeo.com:20258/kqgis_2d/ http://oa.kqgeo.com:20258/examples/manual/developManual.html 
        (Embedded version v8.4)
    author: jnjn@163.com
    build: 20210923
"""
from jinja2 import Environment, PackageLoader

import flask
from flask import Blueprint
import pkg_resources
import string

DEF_STYLE='{"color": "blue", "weight": 2, "opacity": 0.65}'

class KQIcon(object):
    def __init__(self, id=None, **kwargs):
        self.parent=None

        if id:
            self.id=id
            def_options={
                "iconUrl" : "http://oa.kqgeo.com:20258/images/purple.png", 
                "iconSize" : [20,18], 
                "iconAnchor" : [10,9]
                }
            for opt in def_options:
                if not opt in kwargs:
                    kwargs[opt] = def_options[opt]
            self.options=kwargs
        else:
            raise ValueError("please specify icon url")
    def jsonoptions(self):
        return flask.json.dumps(self.options)

    def html(self):
        return flask.Markup(self.parent.parent.templates['iconjs'].render(icon=self))

class KQLayer(object):
    def __init__(self, name, ltype, id = None, isbasemap=False, options = None):
        self.name = name
        self.parent=None
        self.options = options
        self.ltype = ltype
        self.isbasemap = isbasemap
        self.id = id

        if not isinstance(self.name, str):
            raise TypeError("name must be type str, not {}", type(self.name))
        if not self.name:
            raise ValueError("name must contain at least one character.")
        if " " in self.name:
            raise ValueError("name may not contain spaces; they are not supported in id values in HTML5.")
        if self.name[0] not in string.ascii_letters:
            raise ValueError("name must start with a lower or uppercase letter as it is used as a JavaScript variable name")
    def jsonoptions(self):
        return flask.json.dumps(self.options)
    def html(self):
        return flask.Markup(self.parent.parent.templates['layerjs'].render(layer=self))    

class KQLayerGroup(KQLayer):
    def __init__(self, name, ltype="LG", id = None, isbasemap=False, options = None):
        super().__init__(name, ltype, id, isbasemap, options)
        if name:
            self.markers={}
            self.plines={}
            self.polygons={}
            self.imageTs={}
            self.geojsons={}
            self.layernames=[]
            self.js=""
            
    def add_marker(self, coord=None, icon=None, id=None, popup=None, ps=""):
        if coord:
            if not icon:
                icon="DEF_ICON"
            if not id:
                id = str(len(self.markers))
            if popup:
                ps += '.bindPopup("{}")'.format(popup)        
            self.markers[id] = 'var marker_{}_{} = L.marker({}, {{icon: icon_{}}}){};'.format(self.name, id, coord, icon, ps)
            self.layernames.append("marker_{}_{}".format(self.name,id))
    def add_polyline(self, coords=None, color="blue", id=None, popup=None, ps=""):
        if coords:
            if not id:
                id = str(len(self.plines))
            if popup:
                ps += '.bindPopup("{}")'.format(popup)  
            self.plines[id] = 'var pline_{}_{} = L.polyline({}, {{color: "{}"}}){};'.format(self.name, id, coords, color, ps)
            self.layernames.append("pline_{}_{}".format(self.name,id))
    def add_polygon(self, coords=None, color="blue", id=None, popup=None, ps=""):
        if coords:
            if not id:
                id = str(len(self.polygons))
            if popup:
                ps += '.bindPopup("{}")'.format(popup)                
            self.polygons[id] = 'var polygon_{}_{} = L.polygon({}, {{color: "{}"}}){};'.format(self.name, id, coords, color, ps)
            self.layernames.append("polygon_{}_{}".format(self.name,id))
    def add_imageTransform(self, anchors=None, url="", id=None, popup=None, ps="", **kwargs):
        #anchors: TopLeft, TopRight, BottomRight, BottomLeft
        if anchors and url and len(anchors)==4:
            if not id:
                id = str(len(self.imageTs))
            if popup:
                ps += '.bindPopup("{}")'.format(popup)                
            self.imageTs[id] = 'var imageT_{}_{} = L.imageTransform("{}", {}, {}){};'.format(self.name, id, url, anchors, '{{{}}}'.format(','.join(['{}: {}'.format(k,kwargs[k]) for k in kwargs])), ps)
            self.layernames.append("imageT_{}_{}".format(self.name,id))
    def add_geojson(self, data=None, style=DEF_STYLE, id=None, popup=None, ps=""):
        if data:
            if not id:
                id = str(len(self.geojsons))
            if popup:
                ps += '.bindPopup("{}")'.format(popup)
            self.geojsons[id] = 'var geojson_{}_{} = L.geoJSON({}, {{style: {}}}){};'.format(self.name, id, data, style, ps)
            self.layernames.append("geojson_{}_{}".format(self.name,id))

    def jsonoptions(self):
        return ""
    def html(self):
        js=list(self.markers.values()) + list(self.plines.values()) + list(self.polygons.values()) + list(self.imageTs.values()) + list(self.geojsons.values())
        self.js="\n".join(js)
        return flask.Markup(self.parent.parent.templates['layergroupjs'].render(lg=self))        

class KQMap(object):
    def __init__(self, name, width="100%", height="80vh", options=None, drawControl=False, data_url=None, onclick=None, cursor = None, **kwargs):
        # can use common map properties as ** kwargs such as: center = [32, 117], zoom = 10, zoomControl=False, attributionControl=False
        self.name = name
        if not isinstance(self.name, str):
            raise TypeError("name must be type str, not {}", type(self.name))
        if not self.name:
            raise ValueError("name must contain at least one character.")
        if " " in self.name:
            raise ValueError("name may not contain spaces; they are not supported in id values in HTML5.")
        if self.name[0] not in string.ascii_letters:
            raise ValueError("name must start with a lower or uppercase letter as it is used as a JavaScript variable name")
        
        self.options = options
        self.parent = None
        self.layers = {}
        self.icons = {}
        self.width = width
        self.height = height
        self.drawControl = drawControl
        self.onclick = onclick
        self.cursor = cursor

        self.mapproperties = kwargs
        
        self.add_icon(KQIcon(id="DEF_ICON"))

    def add_icon(self, icon):
        if isinstance(icon, KQIcon):
            self.icons[icon.id] = icon
            icon.parent = self
        else:
            raise TypeError("must be icon type")

    def add_layer(self, layer, label=""):
        if isinstance(layer, KQLayer):
            self.layers[layer.name]=layer
            layer.parent = self
            if layer.id == None:
                layer.id = "Layer_{}".format(len(self.layers))
        elif isinstance(layer, KQLayerGroup):
            self.layers[layer.name]=layer
        else:
            raise TypeError("must be layer type")

    def html_div(self):
        return self.parent.templates['amap'].render(map=self)

    def html_js(self):
        def_values={
            "center": [30.543, 114.397],
            "zoom": 2,
            "zoomControl": False,
            "attributionControl": False,
            }
        for dv in def_values:
            if not dv in self.mapproperties:
                self.mapproperties[dv]=def_values[dv]
        self.jsonproperties = flask.json.dumps(self.mapproperties)

        if not "layers" in self.mapproperties:
            ll=[]
            for layer in self.layers:
                ll.append(self.layers[layer].id)
            layersprop=", layers: [{}]".format(", ".join(ll).replace('"',''))
        self.jsonproperties =self.jsonproperties[:-1] + layersprop + self.jsonproperties[-1:]
        return self.parent.templates['mapjs'].render(kqmap=self)

class GenKQMap(KQMap):
    class_ = "visualization"
    type_ = "Generic"

class KQMaps(object):

    def __init__(self, app=None):

        self.app = app

        self.maps = {}
        self.config = None
        self.template_env = None
        self.templates = {}

        if self.app is not None:
            self.init_app(self.app)
    
    def init_app(self, app):
        # type: (flask.Flask) -> bool
        """Initializes the extension against the app"""
        if isinstance(app, flask.Flask):
            self.app = app
            self.config = app.config

            blueprint = Blueprint(
                'kqmaps',
                __name__,
                template_folder='templates',
                static_folder='static',
                static_url_path=app.static_url_path + '/kqmaps')

            app.register_blueprint(blueprint)
            
            self.config.setdefault("KQMAPS_VERSION", "current")
            self.app.after_request(self._after_request)
            self.app.context_processor(self.template_variables)

            # establish route for static javascript
            self.app.add_url_rule("/kqmap.init.js", "kqmap_init_js", self._get_static_init)

            # initialize templates
            self.template_env = Environment(loader=PackageLoader('flask_kqmaps', 'templates'))
            self.templates['init'] = self.template_env.get_template("init_kqmap.js")
            self.templates['script'] = self.template_env.get_template("script.js")
            self.templates['mapjs'] = self.template_env.get_template("mapjs.js")
            self.templates['iconjs'] = self.template_env.get_template("icon.js")
            self.templates['layerjs'] = self.template_env.get_template("layer.js")
            self.templates['layergroupjs'] = self.template_env.get_template("layergroup.js")
            self.templates['kqmap'] = self.template_env.get_template("maps.html")
            self.templates['amap'] = self.template_env.get_template("map.html")
            return True
        raise TypeError("app must be type flask.Flask, not {}".format(type(app)))

    def template_variables(self):
        if self.maps:
            return {'kqmap_init': self._get_init_markup(), 'kq_easymaps': self._get_easymaps_markup(), 'kq_maps': self._get_maps_markup(), 'kq_scripts': self._get_scripts_markup()}
        return {}

    def _after_request(self, resp):
        # type: (flask.Response) -> flask.Response
        """Cleans out the maps variable between requests. In debug mode, it will check if Javascript dependencies have been met,
        and that all map divs are included in templates, a warning will be logged if not. However, easymaps mode would be fine 
        even a warning is fired."""
        if self.app.debug and self.maps:
            resp_data = resp.get_data().decode()
            for x in self.maps.keys():
                if "data-map-name=\"{}\"".format(x) not in resp_data:
                    self.app.logger.warning("Map \"{}\" not included on template.".format(x))

        self.maps = {}
        return resp

    def _get_easymaps_markup(self):
        return flask.Markup(self.templates['kqmap'].render(maps=self.maps,
                                                          config=self.config,
                                                          include_tags=True))

    def _get_maps_markup(self):
        return {n: flask.Markup(c.html_div()) for n, c in self.maps.items()}

    @staticmethod
    def _get_static_init():
        return flask.send_file(pkg_resources.resource_stream("flask_kqmaps", "static/maps.init.js"),
                               attachment_filename="maps.init.js")

    def _get_init_markup(self):
        if "KQ_RELEASE_JS" in self.config:
            kq_release_js = self.config['KQ_RELEASE_JS']
        else:
            kq_release_js = None
        if "KQ_ES_JS" in self.config:
            kq_es_js = self.config['KQ_ES_JS']
        else:
            kq_es_js = None
        return flask.Markup(self.templates['init'].render(maps=self.maps,
                                                          config=self.config,
                                                          include_tags=True, kq_release_js=kq_release_js, kq_es_js=kq_es_js))
    def _get_scripts_markup(self):
        return flask.Markup(self.templates['script'].render(maps=self.maps,
                                                          config=self.config,
                                                          include_tags=True))

    def register(self, map):
        # type: (KQMap) -> bool
        """Registers a map in the app"""
        if isinstance(map, KQMap):
            if map.name not in self.maps:
                    map.parent = self
                    self.maps[map.name] = map
                    return True
            raise KeyError("map with this name {} already exists".format(map.name))
        raise TypeError("map must be subclass of GenericMap, not {}".format(type(map)))