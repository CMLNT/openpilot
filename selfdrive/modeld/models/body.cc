#include "selfdrive/modeld/models/body.h"

#include <fcntl.h>
#include <unistd.h>

#include <cassert>
#include <cstring>

#include <eigen3/Eigen/Dense>

#include "common/clutil.h"
#include "common/params.h"
#include "common/timing.h"
#include "common/swaglog.h"

// #define DUMP_YUV

void bodymodel_init(BodyModelState* s, cl_device_id device_id, cl_context context) {
#ifdef USE_THNEED
  s->m = new BodyThneedModel("models/yolov5nn.thneed",
#else
  s->m = new ONNXModel("models/yolov5nn.onnx",
#endif
   &s->output[0], BODY_NET_OUTPUT_SIZE, USE_GPU_RUNTIME, true, false, context);
}

BodyModelResult* bodymodel_eval_frame(BodyModelState* s, VisionBuf* buf) {
  for (int y = 0; y < 416; y++) {
    for (int x = 0; x < 640; x++) {
      float val = (float)((uint8_t*)buf->addr)[3*y*buf->stride + 3*x] / 255.0f;
      s->net_input_buf[640*416*0 + (y*640 + x)] = val;
      s->net_input_buf[640*416*1 + (y*640 + x)] = val;
      s->net_input_buf[640*416*2 + (y*640 + x)] = val;
    }
  }

  double t1 = millis_since_boot();
  s->m->addImage((float*)s->net_input_buf, BODY_INPUT_SIZE);
  s->m->execute();
  double t2 = millis_since_boot();

  BodyModelResult *model_res = (BodyModelResult*)&s->output;
  model_res->gpu_execution_time = (t2 - t1) / 1000.;
  return model_res;
}

void bodymodel_publish(PubMaster &pm, uint32_t frame_id, BodyModelResult &model_res, float execution_time) {
  std::string res = parse_yolo_outputs(&model_res.preds[0]);

  // make msg
  MessageBuilder msg;
  auto event = msg.initEvent();
  event.initLogMessage(res.size());
  event.setLogMessage(res.c_str());

  pm.send("logMessage", msg);
}

void bodymodel_free(BodyModelState* s) {
  delete s->m;
}
