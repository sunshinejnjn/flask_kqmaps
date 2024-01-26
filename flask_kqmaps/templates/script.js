<script type="text/javascript">
     window.onload = onload();
     function onload() {
       // 初始化地图
       {% for map in maps %}
       {{ maps[map].html_js()|safe }}
       {% endfor %}
     }
</script>