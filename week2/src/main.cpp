#include "common/common.h"
#include "ThostFtdcMdApi.h"
#include "quant/quant.h"
#include "spdlog/sinks/basic_file_sink.h"

int main(int argc, char **argv) {
#if DEBUG
    spdlog::set_level(spdlog::level::trace);
#endif
    quant::start();

    return 0;
}
