from gui import MazeGUI, show_path_window
from runner import Runner
import copy

def Astar(result, data=False):
    map = result['cell_state']
    origin = Runner(result['start'], result['end'])
    queue = []
    visited = {}
    lowest_completed = None
    #Insert to queue
    queue.append(origin)
    visited[origin.position] = 0

    while queue:
        #FIND LOWEST FSCORE
        lowest = get_lowest_runner(queue)
        queue.remove(lowest)

        if lowest.gscore > visited.get(lowest.position, float("inf")):
            continue
        

        if data:
            print("--------------------\nDepth: {}\nInstances in Queue: {}\nCompleted: {}".format(len(lowest.log), len(queue), lowest_completed != None))
            if lowest_completed != None:
                print("Lowest Score: {}".format(lowest_completed.fscore))


        #POPULATE
        to_append = []
        for vector in lowest.find_paths(map):
            child = copy.deepcopy(lowest)
            child.move(vector, map)
            to_append.append(child)

        #CULL
        to_append = [
                        child
                        for child in to_append
                        if child.gscore < visited.get(child.position, float("inf"))
                    ]

        #TRACK VISITED
        for child in to_append:
            if child.gscore < visited.get(child.position, float("inf")):
                visited[child.position] = child.gscore

        #Check exceeding fscore
        if lowest_completed != None:
            to_append = [
                            child
                            for child in to_append
                            if child.gscore <= lowest_completed.fscore
                        ]

        #CHECK FINISHED
        for child in to_append:
            if child.hscore > 0:
                continue
            if lowest_completed == None or lowest_completed.fscore > child.fscore:
                lowest_completed = child

        queue.extend(to_append)
    if data:
        print("--------------------")
    return lowest_completed


#Linear Search
def get_lowest_runner(runners):
    if len(runners) <= 0:
        return
    min_runner = runners[0]
    for runner in runners:
        if runner.fscore < min_runner.fscore:
            min_runner = runner
    return min_runner

def main():
    app = MazeGUI()

    shortest_run = Astar(app.result, True)

    if shortest_run:
        print(shortest_run.log)
        show_path_window(app.result["cell_state"], shortest_run.log)
    else:
        print("No path found")

if __name__ == "__main__":
    main()