#302930, Patryk Tomaszewski

from typing import List, Set, Dict, NamedTuple
from collections import deque
import networkx as nx
from enum import Enum, auto



class Color(Enum):
    white = auto()
    grey = auto()
    black = auto()

class tuple_vertex(NamedTuple):
    vertex_label: int
    d: int



VertexID = int


AdjMatrix = List[List[int]]


AdjList = Dict[VertexID, List[VertexID]]

Distance = int



def neighbors(adjlist: AdjList, start_vertex_id: VertexID, max_distance: Distance) -> Set[VertexID]:

    visited = set()
    queue = []
    colors = {}
    first_tuple = tuple_vertex(start_vertex_id,0)
    for u in adjlist:
        colors[u] = Color.white

    colors[first_tuple.vertex_label] = Color.grey
    queue.append(first_tuple)

    while queue:
        u = queue.pop()
        if u.vertex_label != start_vertex_id and u.d <= max_distance:
            visited.add(u.vertex_label)


        if u.vertex_label in adjlist:
            for v in adjlist[u.vertex_label]:
                if v not in colors:
                    new = tuple_vertex(v,u.d+1)
                    queue.append(new)

                elif colors[v] == Color.white:
                    colors[v] = Color.grey
                    new = tuple_vertex(v, u.d + 1)
                    queue.append(new)

            colors[u] = Color.black

    return visited




VertexID = int
EdgeID = int


class TrailSegmentEntry(NamedTuple):
    vertexStart: VertexID
    vertexEnd: VertexID
    edge: EdgeID
    weight: float
    
Trail = List[TrailSegmentEntry]


def load_multigraph_from_file(filepath):
    G = nx.MultiDiGraph()
    
    with open(filepath) as f:
        rows=(row.strip() for row in f)
        rows = list(row for row in rows if row)
        
        
            
    for elem in rows:
        x, y, z = elem.split()
        x = int(x)
        y = int(y)
        z = float(z)
       
        G.add_weighted_edges_from([(x,y,z)])
    return G
            
        

def find_min_trail(g: nx.MultiDiGraph, v_start: VertexID, v_end: VertexID) -> Trail:
    path_list = []
    atlas_list = []
    weight_list = []
    trail = []
    add_weight = []
    
    
    for elem in nx.dijkstra_path(g,v_start,v_end):
        path_list.append(elem)
    for i in range(len(path_list)-1):
        atlas_list.append(g[path_list[i]][path_list[i+1]])
    
    for i, elem in enumerate(atlas_list):
        if len(atlas_list[i]) != 1:
            for el in range(len(atlas_list[i])):
                add_weight.append(atlas_list[i][el]['weight'])
            weight_list.append(min(add_weight))
            
        else:
            weight_list.append(atlas_list[i][0]['weight'])
    
            
    for elem in range(len(path_list)-1):
        if len(atlas_list[elem]) == 1:
             trail_elements = TrailSegmentEntry(path_list[elem], path_list[elem+1], 0, weight_list[elem])
             trail.append(trail_elements)
        else:
            sorted_tuple = []
            for idx, el in enumerate(atlas_list[elem]):
                krotka = el, atlas_list[elem][idx]['weight']
                sorted_tuple.append(krotka)
            
            sorted_tuple.sort(key=lambda x: x[1])
            x, y = sorted_tuple[0]

            trail.append(TrailSegmentEntry(path_list[elem], path_list[elem+1], x, weight_list[elem]))
            
        
        
    return trail
        
       
def trail_to_str(trail: Trail) -> str:
    trail_str = ""
    total_sum  = 0
    for i in trail:
        total_sum += i.weight
    for i in trail:
        trail_str += '{} -[{}: {}]-> '.format(i.vertexStart, i.edge, i.weight)
    trail_str += '{}  (total = {})'.format(trail[-1].vertexEnd, total_sum)
    return trail_str











   
