def build_floorplan_graph(model, output_path):
    '''Returns the floorplan graph'''
    context = [
        {
            "@base": "http://exsce-floorplan.org/",
            "floorplan": "http://exsce-floorplan.org/",
            "spaces": {
                "@id": "floorplan:spaces",
                "@container": "@list",
                "@type": "@id"
            },
            "walls": {
                "@id": "floorplan:walls",    
                "@container": "@list",
                "@type": "@id"
            },
            "shape":{
                "@id": "floorplan:shape",
                "@type" : "@id"
            },
            "Wall" : "floorplan:Wall",
            "Space" : "floorplan:Space",
            "FloorPlan" : "floorplan:FloorPlan"
        }
    ]

    graph = []

    for space in model.spaces:

        for i, wall in enumerate(space.walls):

            wall_json = {
                "@id" : "space-{name}-wall-{i}".format(name=space.name, i=i),
                "@type" : "Wall",
                "shape" : "polygon-{name}-wall-{i}".format(name=space.name, i=i)
            }

            graph.append(wall_json)
        
        space_json = {
            "@id" : "space-{name}".format(name=space.name),
            "@type" : "Space",
            "walls" : ["space-{name}-wall-{i}".format(name=space.name, i=i) for i in range(len(space.walls))],
            "shape" : "polygon-{name}".format(name=space.name)
        }

        graph.append(space_json)

    graph.append({
            "@id" : "{name}".format(name=model.name),
            "@type" : "FloorPlan",
            "spaces" : ["space-{name}".format(name=space.name) for space in model.spaces]
        })

    floorplan_json_ld = {
        "@context" : context,
        "@graph" : graph
    }

    return floorplan_json_ld