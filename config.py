class Config:
	userAgent = "Mozilla/5.0 (X11; Linux x86) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
	scheme = "zxy"
	tileSize = 256
	cacheSize = 104857600
	zoom = (1, 22)
	mapbox_api_token = "pk.eyJ1IjoiY2FydG9kYmluYyIsImEiOiJja202bHN2OXMwcGYzMnFrbmNkMzVwMG5rIn0.Zb3J4JTdJS-oYNXlR3nvnQ"
	# "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}" - ESRI Topo
	# "https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png" - wikipedia
	# "https://api.mapbox.com/raster/v1/mapbox.mapbox-terrain-dem-v1/{z}/{x}/{y}.webp?sku=101BCUxOGdxeK&access_token=pk.eyJ1IjoiY2FydG9kYmluYyIsImEiOiJja202bHN2OXMwcGYzMnFrbmNkMzVwMG5rIn0.Zb3J4JTdJS-oYNXlR3nvnQ"
	# "https://services.arcgisonline.com/arcgis/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
	# "https://api.mapbox.com/v4/mapbox.terrain-rgb/{z}/{x}/{y}.pngraw?access_token=pk.eyJ1IjoiY2FydG9kYmluYyIsImEiOiJja202bHN2OXMwcGYzMnFrbmNkMzVwMG5rIn0.Zb3J4JTdJS-oYNXlR3nvnQ",
	# "http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}"
	# "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
	# https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z} - Hybryd

	sources = [
		dict(
			name="Admin Boundaries",
			url="https://services.arcgisonline.com/arcgis/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
			scheme="zxy",
			tile_size=256,
			draw_options=dict(
				opacity=1,
				order=0
			)
		),
		dict(
			name="RGB Elevation",
			url="https://api.mapbox.com/v4/mapbox.terrain-rgb/{z}/{x}/{y}.pngraw?access_token=" + mapbox_api_token,
			scheme="zxy",
			tile_size=256,
			draw_options=dict(
				opacity=0.6,
				order=1
			)
		),
		dict(
			name="ESRI Satellite",
			url="https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
			scheme="xyz",
			tile_size=256,
			draw_options=dict(
				opacity=1,
				order=3
			)
		)
	]
