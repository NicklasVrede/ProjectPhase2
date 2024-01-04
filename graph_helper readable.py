import numpy as np
import networkx as nx
from scipy.spatial import Voronoi
from typing import List, Optional, Dict, Tuple 

def voronoi_to_edges(
      minimum_points:int, voronoi_points:Optional[int]=0
      ) -> Tuple[List[Tuple[int,int]],Dict[int,Tuple[float,float]]]:
  '''
   Generates a random planar graph containing at least minimum_points 
   (based on the Voronoi graph)

   Parameters:
   ----------
   minimum_points: Minimal number of points requested for the graph
   voronoi_points: Number of points in the Voronoi graph generation
   
   Return: Tuple[edges,coord_map]
   ----------
   edges: List[(int,int)]
      List containing the edges (Tuples of 2 vertices) 
      forming the 2D surface for the simulation.
      
   coord_map: Dict[int:(float,float)]
      Dictionary containing the coordinate of each vertex 
      (expressed as a tuple of float in [0,1]x[0,1])
  '''
  # Ensure minimum_points is at least 4
  if(minimum_points<4):
     raise Exception("voronoi_to_edges, the number of points must be larger than 3")
  
  # If voronoi_points is less than 4, set it to minimum_points
  if(voronoi_points<4):
     voronoi_points=minimum_points
  
  # Generate random points for Voronoi diagram
  random_points=np.random.rand(voronoi_points,2)
  
  # Create Voronoi diagram
  voronoi_diagram = Voronoi(random_points)    
    
  # Initialize empty edge list and coordinate map
  edge_list=[]
  coordinate_map={}
  index=0
  
  # Iterate over Voronoi ridges
  for ridge in voronoi_diagram.ridge_vertices:
      if -1 not in ridge:
          # Get vertex indices
          vertex_index_1, vertex_index_2 = ridge
          
          # Get vertex coordinates
          vertex_coordinates_1 = voronoi_diagram.vertices[vertex_index_1]
          vertex_coordinates_2 = voronoi_diagram.vertices[vertex_index_2]
          
          # Check if coordinates are within unit square
          if (
             0 <= vertex_coordinates_1[0] <= 1 and 
             0 <= vertex_coordinates_1[1] <= 1 and
             0 <= vertex_coordinates_2[0] <= 1 and 
             0 <= vertex_coordinates_2[1] <= 1
             ):
              
              # Add coordinates to map if not already present
              if tuple(vertex_coordinates_1) not in coordinate_map:
                 coordinate_map[tuple(vertex_coordinates_1)]=index
                 index+=1
              if tuple(vertex_coordinates_2) not in coordinate_map:
                 coordinate_map[tuple(vertex_coordinates_2)]=index
                 index+=1
              
              # Add edge to list
              edge_list.append(
                 (tuple(vertex_coordinates_1), 
                  tuple(vertex_coordinates_2))
                  )
  
  # If not enough points, recursively call function with more Voronoi points
  if len(coordinate_map) < minimum_points:
   return voronoi_to_edges(minimum_points, voronoi_points+1)
  
  # If enough points, return edge list and coordinate map
  else:
   return ([
      (coordinate_map[edge[0]],coordinate_map[edge[1]]) for edge in edge_list],
      {v: k for k, v in coordinate_map.items()}
      )
  

def is_graph_planar(edges:List[Tuple[int,int]])-> bool:
  '''  
  Verifies if the graph defined by the edges is planar
  
  Parameters:
   ----------
  edges: List[(int,int)]
      List containing the edges (Tuples of 2 vertices) forming the graph.

  Return: Bool
  '''
  # Create graph from edge list
  graph = nx.Graph(edges)
  
  # Check if graph is planar and return result
  return nx.is_planar(graph)