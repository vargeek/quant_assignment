#include "MdSpi.h"
#include "common/common.h"
#include <assert.h>
#include <iomanip>

using namespace quant;
using namespace std;

MdSpi::MdSpi(Config config):_config(config), _md(config.MarketDataPath, ios::out | ios::app) {
    _api = nullptr;
    _requestID = 0;
}

int MdSpi::_GenRequestID() {
    return _requestID++;
}

void MdSpi::Connect() {
    _ReleaseApi();

    TRACE("Initializing...");
    _api = CThostFtdcMdApi::CreateFtdcMdApi(_config.FlowPath.c_str());
    _api->RegisterSpi(this);
    _api->RegisterFront(const_cast<char *>(_config.FrontAddress.c_str()));
    _api->Init();

    TRACE("Join");
    _api->Join();
}

void MdSpi::_ReleaseApi() {
    if (_api != nullptr) {
        TRACE("release api");
        _api->RegisterSpi(nullptr);
        _api->Release();
        _api = nullptr;
    }
}
///当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。
void MdSpi::OnFrontConnected() {
    TRACE("OnFrontConnected");

    CThostFtdcReqUserLoginField req;
    memset(&req, 0, sizeof(req));
    strcpy(req.BrokerID, _config.BrokerID.c_str());
    strcpy(req.UserID, _config.UserID.c_str());
    strcpy(req.Password, _config.Password.c_str());
    int ret = _api->ReqUserLogin(&req, _GenRequestID());
    TRACE("ReqUserLogin: {}", ret);
}

///当客户端与交易后台通信连接断开时，该方法被调用。当发生这个情况后，API会自动重新连接，客户端可不做处理。
///@param nReason 错误原因
void MdSpi::OnFrontDisconnected(int nReason) {
    TRACE("OnFrontDisconnected: {}", nReason);
}

///心跳超时警告。当长时间未收到报文时，该方法被调用。
///@param nTimeLapse 距离上次接收报文的时间
void MdSpi::OnHeartBeatWarning(int nTimeLapse) {
    TRACE("OnHeartBeatWarning: {}", nTimeLapse);
}
///错误应答
void MdSpi::OnRspError(CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
    TRACE("OnRspError: ({}){}", pRspInfo->ErrorID, pRspInfo->ErrorID != 0 ? pRspInfo->ErrorMsg : "");
}

///登录请求响应
void MdSpi::OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
    TRACE("OnRspUserLogin: ({}){}", pRspInfo->ErrorID, pRspInfo->ErrorID != 0 ? pRspInfo->ErrorMsg : "");

    std::vector<char*> cstrings;
    cstrings.reserve(_config.Contract.size());

    for (size_t i = 0; i < _config.Contract.size(); ++i) {
        cstrings.push_back(const_cast<char*>(_config.Contract[i].c_str()));
    }
    if (!cstrings.empty()) {
        _api->SubscribeMarketData(&cstrings[0], cstrings.size());
        _api->SubscribeForQuoteRsp(&cstrings[0], cstrings.size());
    }

}
///订阅行情应答
void MdSpi::OnRspSubMarketData(CThostFtdcSpecificInstrumentField *pSpecificInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
    TRACE("OnRspSubMarketData: ({}){}", pRspInfo->ErrorID, pRspInfo->ErrorID != 0 ? pRspInfo->ErrorMsg : "");
}

///深度行情通知
void MdSpi::OnRtnDepthMarketData(CThostFtdcDepthMarketDataField *pData) {
    _md << setprecision(20)
        << pData->TradingDay
        << "," << pData->InstrumentID
        << "," << pData->ExchangeID
        << "," << pData->ExchangeInstID
        << "," << pData->LastPrice
        << "," << pData->PreSettlementPrice
        << "," << pData->PreClosePrice
        << "," << pData->PreOpenInterest
        << "," << pData->OpenPrice
        << "," << pData->HighestPrice
        << "," << pData->LowestPrice
        << "," << pData->Volume
        << "," << pData->Turnover
        << "," << pData->OpenInterest
        << "," << pData->ClosePrice
        << "," << pData->SettlementPrice
        << "," << pData->UpperLimitPrice
        << "," << pData->LowerLimitPrice
        << "," << pData->PreDelta
        << "," << pData->CurrDelta
        << "," << pData->UpdateTime
        << "," << pData->UpdateMillisec
        << "," << pData->BidPrice1
        << "," << pData->BidVolume1
        << "," << pData->AskPrice1
        << "," << pData->AskVolume1
        << "," << pData->BidPrice2
        << "," << pData->BidVolume2
        << "," << pData->AskPrice2
        << "," << pData->AskVolume2
        << "," << pData->BidPrice3
        << "," << pData->BidVolume3
        << "," << pData->AskPrice3
        << "," << pData->AskVolume3
        << "," << pData->BidPrice4
        << "," << pData->BidVolume4
        << "," << pData->AskPrice4
        << "," << pData->AskVolume4
        << "," << pData->BidPrice5
        << "," << pData->BidVolume5
        << "," << pData->AskPrice5
        << "," << pData->AskVolume5
        << "," << pData->AveragePrice
        << "," << pData->ActionDay << std::endl;

}

///取消订阅询价应答
void MdSpi::OnRspUnSubMarketData(CThostFtdcSpecificInstrumentField *pSpecificInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast) {
    TRACE("OnRspUnSubMarketData: ({}){}", pRspInfo->ErrorID, pRspInfo->ErrorID != 0 ? pRspInfo->ErrorMsg : "");
}

MdSpi::~MdSpi() {
    _ReleaseApi();
    _md.close();
}
