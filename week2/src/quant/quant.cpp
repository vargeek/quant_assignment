#include "common/common.h"
#include "quant.h"
#include "config.h"
#include "MdSpi.h"
#include "yaml-cpp/yaml.h"

using namespace std;

void quant::start() {
    try {
        Config cfg("config/config.yaml");
        MdSpi spi(cfg);
        spi.Connect();
    } catch (YAML::BadFile &e) {
        LOG_ERROR("配置文件读取失败!");
    } catch (...) {
        LOG_ERROR("启动失败!");
    }
}

void quant::stop() {
    
}
