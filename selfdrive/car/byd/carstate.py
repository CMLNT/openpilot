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

    #####################################################################
    # wheelSpeeds       各车轮速度
    # vEgoRaw           车原始轮速
    # vEgo  aEgo        车速和加速度 根据update_speed_kf 算法计算
    # standstill        车停止状态根据左前和右后轮速度都为0 判断
    #####################################################################

    ret.wheelSpeeds = self.get_wheel_speeds(
      cp.vl["Wheel_Speeds"]["FL"],
      cp.vl["Wheel_Speeds"]["FR"],
      cp.vl["Wheel_Speeds"]["RL"],
      cp.vl["Wheel_Speeds"]["RR"],
    )   
    ret.vEgoRaw = (ret.wheelSpeeds.fl + ret.wheelSpeeds.fr + ret.wheelSpeeds.rl + ret.wheelSpeeds.rr) / 4.    
    ret.vEgo, ret.aEgo = self.update_speed_kf(ret.vEgoRaw)
    ret.standstill = cp.vl["Wheel_Speeds"]["FL"] == 0.0 and cp.vl["Wheel_Speeds"]["RR"] == 0.0


    #####################################################################
    # gas                          车油门踏板位置 0.0-1.0
    # gasPressed               油门踏板踩下状态 油门踏板位置大于 0
    # brake @5 :Float32;            这是用户踏板（只属于用户操作）
    # brakePressed @6 :Bool;        这是用户踏板是否被按下（只属于用户操作）
    # regenBraking @45 :Bool;       这是用户踏板的再生制动功能（只属于用户操作）
    # parkingBrake @39 :Bool;       手刹是否拉起
    # brakeHoldActive @38 :Bool;    刹车保持功能是否激活
    

    ret.gas = cp.vl["PEDAL"]["Throttle_Pedal"]
    ret.gasPressed = bool(ret.gas > 0)  #需要再次确认
    ret.brake = cp.vl["PEDAL"]["Brake_Pedal"]
    ret.brakePressed = bool(ret.brake > 0)  #需要再次确认
    #再生制动未采集
    #刹车保持
    #####################################################################

    ####################################################################
    # steeringAngleDeg @7 :Float32; # 方向盘角度，单位：度
    # steeringAngleOffsetDeg @37 :Float32; # 多个传感器之间的偏移量（如果有多个传感器）
    # steeringRateDeg @15 :Float32; # 方向盘转角速率，单位：度/秒
    # steeringTorque @8 :Float32; # 方向盘扭矩（TODO: 标准化单位）
    # steeringTorqueEps @27 :Float32; # 方向盘扭矩误差（TODO: 标准化单位）
    # steeringPressed @9 :Bool; # 用户是否使用方向盘
    # steerFaultTemporary @35 :Bool; # 临时EPS故障
    # steerFaultPermanent @36 :Bool; # 永久EPS故障
    # stockAeb @30 :Bool; # 原装AEB（自动紧急制动）状态
    # stockFcw @31 :Bool; # 原装FCW（前向碰撞预警）状态
    # espDisabled @32 :Bool; # ESP（电子稳定控制系统）是否禁用
    # accFaulted @42 :Bool; # 自适应巡航控制系统（ACC）是否故障
    # carFaultedNonCritical @47 :Bool; # 某个ECU（电子控制单元）发生故障，但车辆仍可控制
    
    ret.steeringAngleDeg = cp.vl["Steering"]["Steering_Angle"]
    #ret.steeringTorque = cp.vl["Steering"]["Steering_Torque"]   #需要再次确认
    ####################################################################



    ####################################################################
    # cruiseState @10 :CruiseState;# 巡航状态对象
    # enabled @0 :Bool;            # 巡航控制是否启用
    # speed @1 :Float32;           # 巡航速度
    # speedCluster @6 :Float32;    # 在仪表盘上显示的设定速度
    # available @2 :Bool;          # 巡航控制是否可用
    # speedOffset @3 :Float32;     # 速度偏移量
    # standstill @4 :Bool;         # 车辆是否完全停止
    # nonAdaptive @5 :Bool;        # 是否为非自适应巡航模式
    ret.cruiseState.enabled = cp.vl["Steering_Torque"]["Cruise_Activated"]
    #ret.cruiseState.speed = 
    ret.cruiseState.speedCluster = cp.vl["Dash_State2"]["Cruise_Set_Speed"]



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