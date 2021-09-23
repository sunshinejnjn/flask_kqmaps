
  {% for icon in kqmap.icons %}
  {{ kqmap.icons[icon].html() }}
  {% endfor %}


  {% for layer in kqmap.layers %}
  {{ kqmap.layers[layer].html() }}
  {% endfor %}

  var baseMaps = {
    {% for layer in kqmap.layers %}
    {% if kqmap.layers[layer].isbasemap %}
        "{{ kqmap.layers[layer].name }}": {{ kqmap.layers[layer].id }},
    {% endif %}
    {% endfor %}
  };

  var overlays = {
    {% for layer in kqmap.layers %}
    {% if not kqmap.layers[layer].isbasemap %}
        "{{ kqmap.layers[layer].name }}": {{ kqmap.layers[layer].id }},
    {% endif %}
    {% endfor %}
  };

  var {{ kqmap.name }} = L.map("{{ kqmap.name }}", {{ kqmap.jsonproperties }});

  {% if ((kqmap.cursor is defined) and (kqmap.cursor != None) and (kqmap.cursor != '')) %}
  $('#{{ kqmap.name }}').css('cursor', '{{ kqmap.cursor }}');
  {% endif %}

  L.control.layers(baseMaps, overlays).addTo({{ kqmap.name }}).setPosition("topleft");

  {% if kqmap.drawControl %}
  // 创建一个绘制图层
  var editableLayers = new L.FeatureGroup();
  {{ kqmap.name }}.addLayer(editableLayers);

  // 绘制控件参数配置
  var options = {
    position: 'topleft',
    draw: {
      polyline: {}, // 线
      polygon: {}, // 面
      circle: {}, // 圆
      rectangle: {}, // 矩形
      marker: {}, // 标记点
      circlemarker: {}
    },
    edit: {
      featureGroup: editableLayers,
      remove: true
    }
  };

  // 创建并添加绘制控件
  var drawControl = new L.Control.Draw(options);
  {{ kqmap.name }}.addControl(drawControl);

  // 监听绘制事件
  {{ kqmap.name }}.on(L.Draw.Event.CREATED, function (e) {
    var type = e.layerType, layer = e.layer;
    editableLayers.addLayer(layer);
  });
  {% endif %}

  {% if (( kqmap.onclick != None ) and ( kqmap.onclick != "" )) %}
  {{ kqmap.name }}.on('click', function (e) {
    doOnClick(e.latlng);
  });
  function doOnClick(latlon) {
    var lat = latlon.lat;
    var lon = latlon.lng;
    {{ kqmap.onclick }}
    }

  {% endif %}