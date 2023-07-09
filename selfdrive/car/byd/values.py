# 每一个都有的
from cereal import car
#加载 DBC 文件
from selfdrive.car import dbc_dict





# 每一个都有的
Ecu = car.CarParams.Ecu




# 定义车型号代码，采用比亚迪厂家车型定义
class CAR:
    HA2HE = "BYD_QIN_PLUS_DMI_2021_120KM"
    SA3HE = "BYD_SONG_PLUS_DMI_2021_110KM_PRO_PLUS_4G"




# 定义车顶对应的 DBC 文件
DBC = {
  CAR.HA2HE: dbc_dict('BYD_QIN_PLUS_DMI_2021_120KM_PRO', None),
  CAR.SA3HE: dbc_dict('BYD_SONG_PLUS_DMI_2021_110KM_PRO_PLUS_4G', None),

}