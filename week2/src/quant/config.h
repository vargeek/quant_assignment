#ifndef __CONFIG_H__
#define __CONFIG_H__

#include <string>
#include <vector>

namespace quant {

class Config {
    public:
    Config(const std::string& filename);
    std::string BrokerID;
    std::string UserID;
    std::string Password;
    std::string FrontAddress;
    std::string FlowPath;
    std::string MarketDataPath;
    std::vector<std::string> Contract;
};

}

#endif // #ifndef __CONFIG_H__
