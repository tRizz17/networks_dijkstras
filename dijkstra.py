import sys
import json
import math  # If you want to use math.inf for infinity
from queue import PriorityQueue
from graph import Graph

def ipv4_to_value(ipv4_addr):
    dec_num = 0
    nums = [int(x) for x in ipv4_addr.split('.')]
    for num in nums:
        dec_num = dec_num << 8
        dec_num = dec_num | num
    return dec_num

def value_to_ipv4(addr):

    addr_parts = []
    mask = 0xff
    bits = 24
    while bits > -1:
        addr_parts.append((addr >> bits) & mask)
        bits -= 8
    return (f"{addr_parts[0]}.{addr_parts[1]}.{addr_parts[2]}.{addr_parts[3]}")

def get_subnet_mask_value(slash):

    subnet_bits = int(slash.split("/")[-1])
    run_of_ones = ( 1 << subnet_bits) - 1
    host_bits = 32 - subnet_bits
    mask = run_of_ones << host_bits
    return mask


def ips_same_subnet(ip1, ip2, slash):

    subnet_mask = get_subnet_mask_value(slash)

    ip1_val_subnet = ipv4_to_value(ip1) & subnet_mask
    ip2_val_subnet = ipv4_to_value(ip2) & subnet_mask

    if ip1_val_subnet == ip2_val_subnet:
        return True
    else:
        return False


def get_network(ip_value, netmask):

    network_portion = ip_value & netmask
    return network_portion


def find_router_for_ip(routers, ip):

    keys_list = list(routers.keys())

    for key in keys_list:
        if ips_same_subnet(ip, key, routers[key]["netmask"]):
            return key
    return None


def build_graph(routers):
    graph = Graph()
    for ip_addr, values in routers.items():
        graph.add_vertex(ip_addr)
        for connection, parts in values["connections"].items():
            graph.add_edge(ip_addr, (connection, parts['ad']))
    return graph


def dijkstras_shortest_path(routers, src_ip, dest_ip):
    graph = build_graph(routers)

    src_router = find_router_for_ip(routers, src_ip)
    dest_router = find_router_for_ip(routers, dest_ip)

    to_visit = PriorityQueue()
    distance = {}

    for vertex in graph.vertices():
        if vertex != src_router:
            distance[vertex] = float('inf')
            to_visit.put((distance[vertex], vertex))

    parent = {}
    parent[src_router] = None
    distance[src_router] = 0
    to_visit.put((distance[src_router], src_router))

    while to_visit:
        _, curr_router = to_visit.get()

        if curr_router == dest_router:
            if parent[curr_router]:
                path = []
                path.append(curr_router)
                while parent[curr_router] is not None:
                    path.append(parent[curr_router])
                    curr_router = parent[curr_router]
                return path[::-1]
            return []

        for neighbor in graph.neighbors(curr_router):
            nbr_ip, edge_wt = neighbor
            alt = distance[curr_router] + edge_wt
            if alt < distance[nbr_ip]:
                distance[nbr_ip] = alt
                parent[nbr_ip] = curr_router
                to_visit.put((alt, nbr_ip))
    


#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)
   
if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
