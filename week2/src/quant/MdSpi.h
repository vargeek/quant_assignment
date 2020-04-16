#ifndef __MD_SPI_H__
#define __MD_SPI_H__

#include "ThostFtdcMdApi.h"
#include "config.h"
#include <iostream>
#include <fstream>

namespace quant {
class MdSpi: public CThostFtdcMdSpi {
    public:
    MdSpi(Config config);
    ~MdSpi();
    void Connect();

    private:
    Config _config;
    CThostFtdcMdApi *_api;
    int _requestID;
    std::ofstream _md;
    
    void _ReleaseApi();
    int _GenRequestID();

    void OnFrontConnected() override;
    void OnFrontDisconnected(int nReason) override;
    void OnHeartBeatWarning(int nTimeLapse) override;
    void OnRspError(CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) override;
    void OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) override;
    void OnRspSubMarketData(CThostFtdcSpecificInstrumentField *pSpecificInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) override;
    void OnRspUnSubMarketData(CThostFtdcSpecificInstrumentField *pSpecificInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) override;
    void OnRtnDepthMarketData(CThostFtdcDepthMarketDataField *pDepthMarketData) override;
};
}

#endif // #ifndef __MD_SPI_H__
