#include "config.h"
#include "yaml-cpp/yaml.h"

using namespace quant;
using namespace std;

Config::Config(const string& filename) {
    YAML::Node config = YAML::LoadFile(filename);
    if (!config["simnow"]) {
        return;
    }

    YAML::Node simnow = config["simnow"].as<YAML::Node>();
    if (simnow["BrokerID"]) {
        BrokerID = simnow["BrokerID"].as<string>();
    }

    if (simnow["UserID"]) {
        UserID = simnow["UserID"].as<string>();
    }

    if (simnow["Password"]) {
        Password = simnow["Password"].as<string>();
    }

    if (simnow["FrontAddress"]) {
        FrontAddress = simnow["FrontAddress"].as<string>();
    }

    if (simnow["FlowPath"]) {
        FlowPath = simnow["FlowPath"].as<string>();
    }
    
    if (simnow["MarketDataPath"]) {
        MarketDataPath = simnow["MarketDataPath"].as<string>();
    }

    if (simnow["Contract"]) {
        Contract = simnow["Contract"].as<vector<string>>();
    }
}
