import random
from ast import literal_eval
from room import Room
from player import Player
from world import World
from util import Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

map = {}

# convenience method to remove some verbosity for travel
def travel_to(direction):
    player.travel(direction)

# method to create a new room map for all rooms in the graph
def initialize_room_map():
    # create a variable to hold the current room
    current = player.current_room
    # create an empty dictionary to hold the keys and values
    # from the room and directions
    room_map = {}

    # initialize the dictionary to hold values such as { 'n' : '?' }
    # for all directions leading from the current room
    for direction in current.get_exits():
        room_map[direction] = '?'
        map[current.id] = room_map

# method to pick an unvisited random room
def unvisited_exit_from_room():
    # set up the player's current room in a variable
    current = player.current_room
    # create an empty array to hold the unvisited rooms
    unvisited = []

    # loop through all the directions the player can go from the current room,
    # and only append the rooms that still have a '?'
    for direction in player.current_room.get_exits():
        if map[current.id][direction] == '?':
            unvisited.append(direction)

    # return a randomly chosen room from the array 
    return random.choice(unvisited)


# ---------BFS---------
def find_unvisited_room(id):
    # create a queue (BFS requires a queue)
    # and enqueue the starting vertex in a list (to keep track of the traveled path)
    # create a visited set to keep track of visited nodes
    q = Queue()
    q.enqueue([id])
    visited = set()

    # while the queue still has items
    while q.size() > 0:
        # grab the first item in the queue
        path = q.dequeue()
        # and grab the vertex from the last index in the path
        room = path[-1]

        # if the room isn't in the visited set
        if room not in visited:
            # if an array of only '?' values has items,
            # immediately return the path
            if list(map[room].values()).count('?') != 0:
                return path
            # add it
            visited.add(room)

            # grab the values from the map pertaining to the current room id
            # and add them to the path and enqueue the whole path for all rooms
            for next_room in map[room].values():
                q.enqueue(path + [next_room])
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
