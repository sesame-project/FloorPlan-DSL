def build_shape_graph(model, output_path):
    '''
    Shape graph: shape relationships
    '''
    context = [ 
        "https://raw.githubusercontent.com/opengeospatial/ogc-geosparql/master/1.1/contexts/sf-context.json",
        {
            "@base" : "http://exsce-floorplan.org/",
            'points' : {
                "@id" : "http://exsce-floorplan.org/points",
                "@container" : "@list",
                "@type" : "@id"
                }
            }
    ]

    graph = []

    for space in model.spaces:

        space_polygon = {
            "@id" : "polygon-{name}".format(name=space.name),
            "@type" : "Polygon",
            "points" : ["point-shape-{name}-{i}".format(name=space.name, i=i) for i, _ in enumerate(space.get_shape().get_points())]
        }

        graph.append(space_polygon)

        for i, wall in enumerate(space.walls):
            wall_polygon = {
                "@id" : "polygon-{name}-wall-{i}".format(name=space.name, i=i),
                "@type" : "Polygon",
                "points" : ["point-corner-{name}-wall-{i}-{j}".format(name=space.name, i=i, j=j) for j in range(4)]
            }

            graph.append(wall_polygon)

    shape_json_ld = {
        "@context" : context,
        "@graph" : graph,
        "@id" : "{name}-shape".format(name=model.name)
    }

    return shape_json_ld