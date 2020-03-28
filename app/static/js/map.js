// World Map
import {legend} from "@d3/color-legend"
d3 = require("d3@5")
width  = 1500;
height = 750;
projection = d3.geoEqualEarth()
path = d3.geoPath(projection)
outline = ({type: "Sphere"})
countries = topojson.feature(world, world.objects.countries) // replace with our data
world = FileAttachment("countries-50m.json").json() // replace with our data
topojson = require("topojson-client@3") 


let svg = d3.create("svg").style("display", "block").attr("viewBox", [0, 0, width, height]);
  
defs = svg.append("defs");
defs.append("path")
	.attr("id", "outline")
	.attr("d", path(outline));
  
defs.append("clipPath")
	.attr("id", "clip")
  	.append("use")
	.attr("xlink:href", new URL("#outline", location));
  
let g = svg.append("g")
	.attr("clip-path", `url(${new URL("#clip", location)})`); 

g.append("use")
	.attr("xlink:href", new URL("#outline", location))
	.attr("fill", "white");
  
g.append("g")
	.selectAll("path")
	.data(countries.features) // replace with our data
	.join("path")
	.attr("fill", d => color(data.get(d.properties.name))) // replace with our data
	.attr("d", path)
	.append("title")
	.text(d => `${d.properties.name}${data.has(d.properties.name) ? data.get(d.properties.name) : "N/A"}`); // replace with our data
  
g.append("path")
	.datum(topojson.mesh(world, world.objects.countries, (a, b) => a !== b)) // replace with our data
	.attr("fill", "none")
	.attr("stroke", "white")
	.attr("stroke-linejoin", "round")
	.attr("d", path);
  
svg.append("use")
	.attr("xlink:href", new URL("#outline", location))
	.attr("fill", "none")
	.attr("stroke", "black");
