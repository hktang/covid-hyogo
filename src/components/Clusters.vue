<template>
  <div>
    <div id="cluster-graph" style="width:900px;height:500px;"></div>
  </div>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "ClustersChart",
  data: () => ({
    width: null,
    height: null,
    chartWidth: null,
    chartHeight: null,
    margin: null,
    svg: null,
    chartLayer: null,
    color: null,
    circle_radius: 12,
    labels: null,
    groups: null,
    nodes: null,
    links: null
  }),
  mounted() {
    this.svg = d3.select("#cluster-graph").append("svg");
    this.color = d3.scaleOrdinal(d3.schemeCategory10);
    this.labels = [
      "Kindergarten",
      "Hospital",
      "Live House",
      "mnop",
      "qrst",
      "uvwx",
      "Unknown"
    ];
    this.setSize();
    this.drawChart();
  },
  methods: {
    setSize() {
      this.width = document.querySelector("#cluster-graph").clientWidth;
      this.height = document.querySelector("#cluster-graph").clientHeight;

      this.margin = { top: 0, left: 0, bottom: 0, right: 0 };

      this.chartWidth = this.width - (this.margin.left + this.margin.right);
      this.chartHeight = this.height - (this.margin.top + this.margin.bottom);

      this.svg.attr("width", this.width).attr("height", this.height);

      this.chartLayer = this.svg.append("g").classed("chartLayer", true);

      this.chartLayer
        .attr("width", this.chartWidth)
        .attr("height", this.chartHeight)
        .attr(
          "transform",
          "translate(" + [this.margin.left, this.margin.top] + ")"
        );
    },
    drawChart() {
      this.groups = this.labels.length;

      this.nodes = d3.range(0, 100).map(d => ({
        id: d,
        group: d % this.groups
      }));

      this.links = d3.range(100).map(i => ({
        source: i % this.groups,
        target: i
      }));

      let simulation = d3
        .forceSimulation()
        .force(
          "link",
          d3
            .forceLink()
            .id(function(d) {
              return d.index;
            })
            .distance(18)
        )
        .force("collide", d3.forceCollide(this.circle_radius * 1.1))
        .force("charge", d3.forceManyBody())
        .force(
          "center",
          d3.forceCenter(this.chartWidth / 2, this.chartHeight / 2)
        )
        .force("y", d3.forceY(0))
        .force("x", d3.forceX(0));

      // circles
      let node = this.svg
        .append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(this.nodes)
        .enter()
        .append("circle")
        .attr("r", this.circle_radius)
        .style("fill", d => this.color(d.group))
        .call(
          d3
            .drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended)
        );

      let rect = this.svg
        .append("g")
        .attr("class", "rects")
        .selectAll("rect")
        .data(this.nodes)
        .enter()
        .append("rect")
        .attr("fill", "white")
        .attr("fill-opacity", 0)
        .attr("width", 75)
        .attr("height", 25)
        .call(
          d3
            .drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended)
        );

      let text = this.svg
        .append("g")
        .attr("class", "labels")
        .selectAll("text")
        .data(this.nodes)
        .enter()
        .append("text")
        .style("font-size", 24)
        .style("font-weight", 900)
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(d => this.labels[d.id]);

      let ticked = function() {
        node
          .attr("cx", function(d) {
            return d.x;
          })
          .attr("cy", function(d) {
            return d.y;
          });
        text
          .attr("x", function(d) {
            return d.x - 30;
          })
          .attr("y", function(d) {
            return d.y;
          });
        rect
          .attr("x", function(d) {
            return d.x - 30;
          })
          .attr("y", function(d) {
            return d.y - 12;
          });
      };

      simulation.nodes(this.nodes).on("tick", ticked);

      //ties the circles together
      simulation.force("link").links(this.links);

      function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.5).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
      }

      function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }
    }
  }
};
</script>

<style scoped>
#cluster-graph {
  margin: 0 auto;
}
</style>
