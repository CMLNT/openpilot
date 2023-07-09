# 导入
from selfdrive.car.interfaces import CarStateBase
# 导入
from selfdrive.car.byd.values import CAR, DBC, CarControllerParams
# 导入CANDefine模块
from opendbc.can.can_define import CANDefine
from cereal import car

class CarState(CarStateBase):
  def __init__(self, CP):
    super().__init__(CP)
    # 识别车辆指纹？
    can_define = CANDefine(DBC[CP.carFingerprint]["pt"])


  def update(self, cp, cp_adas, cp_cam):
    ret = car.CarState.new_message()


    #   vEgo @1 :Float32;          # 速度的最佳估计值
    #   aEgo @16 :Float32;         # 加速度的最佳估计值
    #   vEgoRaw @17 :Float32;      # 来自CAN传感器的未经滤波的速度值
    #   vEgoCluster @44 :Float32;  # 车辆仪表盘显示的速度的最佳估计值，用于用户界面
    #   standstill @18 :Bool;      # 表示车辆是否处于静止状态
    #   gas @3 :Float32;        # this is user pedal only
    #   gasPressed @4 :Bool;    # this is user pedal only


    # car wheelSpeeds       各车轮速度
    # car vEgoRaw           车原始轮速
    # car vEgo  aEgo        车速和加速度 根据update_speed_kf 算法计算
    # car standstill        车停止状态根据左前和右后轮速度都为0 判断  
    ret.wheelSpeeds = self.get_wheel_speeds(
      cp.vl["Wheel_Speeds"]["FL"],
      cp.vl["Wheel_Speeds"]["FR"],
      cp.vl["Wheel_Speeds"]["RL"],
      cp.vl["Wheel_Speeds"]["RR"],
    )   
    ret.vEgoRaw = (ret.wheelSpeeds.fl + ret.wheelSpeeds.fr + ret.wheelSpeeds.rl + ret.wheelSpeeds.rr) / 4.    
    ret.vEgo, ret.aEgo = self.update_speed_kf(ret.vEgoRaw)
    ret.standstill = cp.vl["Wheel_Speeds"]["FL"] == 0.0 and cp.vl["Wheel_Speeds"]["RR"] == 0.0

    # car  gas              车油门踏板位置 0.0-1.0
    # car  gasPressed       油门踏板踩下状态 油门踏板位置大于 0
    ret.gas = cp.vl["PEDAL"]["Throttle_Pedal"]
    ret.gasPressed = bool(ret.gas > 0)











# 检查项目
  @staticmethod
  def get_can_parser(CP):
    signals = [
      # sig_name, 信号地址
    #   ("WHEEL_SPEED_FL", "WHEEL_SPEEDS_FRONT"),
    ]

    checks = [
      # 信号地址, 信号值
    #   ("STEER_ANGLE_SENSOR", 100),

    ]


  @staticmethod
  def get_cam_can_parser(CP):


  @staticmethod
  def get_adas_can_parser(CP):
  

  @staticmethod
  def get_body_can_parser(CP):
  

  @staticmethod
  def get_loopback_can_parser(CP):