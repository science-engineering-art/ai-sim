from models.control import control


RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)


ctrl = control()
pos_x, pos_y, end_y, start_x, curv = 700, 410, 900, 0, 5
road_WC_id = ctrl.AddRoad((start_x, pos_y), (pos_x, pos_y))
road_CW_id = ctrl.AddRoad((pos_x, pos_y - 10), (start_x, pos_y- 10))
road_CS_id = ctrl.AddRoad((pos_x + curv, pos_y + curv), (pos_x + curv, end_y))
road_curWCS_ids = ctrl.connect_roads(road_WC_id, road_CS_id, (pos_x + curv, pos_y))


pos_x, pos_y, end_y, start_x, curv = 720, 400, 200, 1400, -5
road_EC_id = ctrl.AddRoad((start_x, pos_y), (pos_x, pos_y))
road_CE_id = ctrl.AddRoad((pos_x, pos_y + 10), (start_x, pos_y + 10))
road_CN_id = ctrl.AddRoad((pos_x + curv, pos_y + curv), (pos_x + curv, end_y))


road_curvECN_ids = ctrl.connect_roads(road_EC_id, road_CN_id, (pos_x + curv, pos_y))
road_curvECW_ids = ctrl.connect_roads(road_EC_id, road_CW_id, (pos_x, pos_y))
road_curvWCE_ids = ctrl.connect_roads(road_WC_id, road_CE_id, (pos_x, pos_y + 10))
road_curvWCN_ids = ctrl.connect_roads(road_WC_id, road_CN_id, (pos_x - curv, pos_y))
road_curvECS_ids = ctrl.connect_roads(road_EC_id, road_CS_id, (pos_x + curv, pos_y))


curv_x = -5; curv_y = -5; 
road_NE_id = ctrl.AddRoad((pos_x, end_y + curv_y), (start_x, end_y + curv_y))
road_curvCNE_ids = ctrl.connect_roads(road_CN_id, road_NE_id, (pos_x + curv_x, end_y + curv_y))


ctrl.AddExtremeRoads([road_WC_id, road_EC_id])
ctrl.CreateCorner([(road_WC_id, road_CS_id, 0), (road_EC_id, road_CN_id, 1), (road_EC_id, road_CW_id, 1),\
    (road_WC_id, road_CN_id, 0), (road_EC_id, road_CS_id,1), (road_WC_id, road_CE_id, 0)])
ctrl.roads[road_CN_id].end_conn = ctrl.roads[road_NE_id]
ctrl.curves[(road_NE_id, road_NE_id)] = road_curvCNE_ids
ctrl.Start()
