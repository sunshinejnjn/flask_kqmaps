<script>window.lib_path = "/static/kqmaps/kqwebclient/leaflet/3rd_libs"</script>
<script type="text/javascript" include="leaflet.draw,leaflet.easybutton,fontawesome,imagetransform"
  src="/static/kqmaps/kqwebclient/leaflet/include-leaflet.js"></script>
<script src="{% if ((kq_release_js is defined) and (not kq_release_js is none)) %}{{ kq_release_js }}{% else %}/static/kqmaps/kqwebclient/leaflet/kq-release.js{% endif %}"></script>
<style>
  {% for map in maps %}
  #{{ map }} { 
    width: {{ maps[map].width }};
    height: {{ maps[map].height }};
  }
  {% endfor %}

  #maptools {
    margin: 8px 7px;
    position: absolute;
    left: 0px;
    top: 0px;
    font-size: 12px;
    z-index: 99999;
  }

  #maptools #pane {
    width: 200px;
    color: white;
    opacity: 0.8;
    border-radius: 4px;
    background-color: #0C0C0C;
    box-shadow: 2px 2px 2px #888888;
    padding: 10px;
    height: 80px;
  }

  #maptools .label {
    font-weight: bold;
  }

  #maptools .content {
    padding-left: 2px;
    color: white;
    background-color: #0C0C0C;
    border-radius: 4px;
    border: 1px solid white;
    /*text-align: center;*/
  }

  #maptools .label {
    padding-right: 2px;
  }

  #maptools input {
    width: 140px;
  }

  #maptools button {
    width: 48%;
    margin: 5px 0;
  }

  .k-notification-info {
    background-color: rgba(0, 0, 0, 0.5);
    border: none;
    padding: 8px 12px;
  }
</style>