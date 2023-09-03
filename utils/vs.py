import cv2
import numpy as np
p_color = [(0, 255, 255), (0, 191, 255),(0, 255, 102),(0, 77, 255), (0, 255, 0),
            (77,255,255), (77, 255, 204), (77,204,255), (191, 255, 77), (77,191,255), (191, 255, 77), 
            (204,77,255), (77,255,204), (191,77,255), (77,255,191), (127,77,255), (77,255,127), (255,255,70), (255,180,20), (20,180,255), (155,155,155)] 
line_color = [(0, 215, 255), (0, 255, 204), (0, 134, 255), (0, 255, 50), 
            (77,255,222), (77,196,255), (77,135,255), (191,255,77), 
            (77,255,77), (77,222,255), (255,156,127), (0,127,255), 
            (255,127,77), (0,77,255), (127,127,255), (255,0,127), 
            (0,127,0), (255,255,128), (0,0 ,50), (0,150 ,50), (255,180,20), (20,180,255)]
# BGR - blue for v =0, green for v =1, red for v =2

VISIBLE_COLOR = [[255, 0, 0], [0, 255, 0], [0, 0 , 255]]

topology_visualize = [[2, 1], [2, 3], [2, 6], [2, 15],
                    [15, 3], [15, 6], [15, 9], [15, 12], [3, 4],
                    [4, 5], [6, 7], [7, 8], [9, 10], [10, 11], [12, 13], [13, 14]]


def draw_pose(frame, poses):
    keypoint_radius=2
    line_thickness=2

    body_pair = np.array(topology_visualize) - 1
    part_line = {}
    for i, point in enumerate(poses):
        x = point[0]
        y = point[1]
        v = x * y 
        if v == 0:
            continue
        cv2.circle(frame, (int(x), int(y)), keypoint_radius, VISIBLE_COLOR[0], -1)
        part_line[i] = (x, y)
    
    for i, (start_p, end_p) in enumerate(body_pair):
        if start_p in part_line and end_p in part_line:
            start_xy = part_line[start_p]
            end_xy = part_line[end_p]
            cv2.line(frame, start_xy, end_xy, line_color[i], line_thickness)

    return frame


class PoseVisualizer:
    def __init__(self, topology, keypoint_radius=2, line_thickness=2):
        self.topology = topology
        self.keypoint_radius = keypoint_radius
        self.line_thickness = line_thickness
    def draw_humans(self, frame, poses):
        body_pair = np.array(self.topology) - 1
        for single_person_joints in poses:
            part_line = {}
            for i in range(single_person_joints.shape[0]):
                x = int(single_person_joints[i, 0])
                y = int(single_person_joints[i, 1])
                v = x*y
                if v==0:
                    continue
                cv2.circle(frame, (int(x), int(y)), self.keypoint_radius, VISIBLE_COLOR[0], -1)
                part_line[i] = (x, y)
            for i, (start_p, end_p) in enumerate(body_pair):
                if start_p in part_line and end_p in part_line:
                    start_xy = part_line[start_p]
                    end_xy = part_line[end_p]

                    cv2.line(frame, start_xy, end_xy, line_color[i], self.line_thickness)
        return frame
