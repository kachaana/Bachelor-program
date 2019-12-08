#ifndef __PROGTEST__

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <climits>
#include <cmath>
#include <cassert>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <deque>
#include <queue>
#include <stack>
#include <algorithm>
#include <pthread.h>
#include <semaphore.h>
#include <cstdint>
#include <array>
#include <unordered_map>
#include <unordered_set>
#include <thread>
#include <mutex>
#include <memory>
#include <condition_variable>
#include <atomic>
using namespace std;


class CFITCoin;
class CCVUTCoin;
class CCustomer;

typedef struct shared_ptr<CFITCoin>                        AFITCoin;
typedef struct shared_ptr<CCVUTCoin>                       ACVUTCoin;
typedef struct shared_ptr<CCustomer>                       ACustomer;
//=================================================================================================
class CFITCoin
{
public:
    CFITCoin                      ( const vector<uint32_t> & vectors,
                                    int               distMax )
            : m_Vectors ( vectors ),
              m_DistMax ( distMax ),
              m_Count ( 0 )
    {
    }
    virtual                  ~CFITCoin                     ( void ) = default;
    vector<uint32_t>         m_Vectors;
    int                      m_DistMax;
    uint64_t                 m_Count;
};
//=================================================================================================
class CCVUTCoin
{
public:
    CCVUTCoin                     ( const vector<uint8_t> & data,
                                    int               distMin,
                                    int               distMax )
            : m_Data ( data ),
              m_DistMin ( distMin ),
              m_DistMax ( distMax ),
              m_Count ( 0 )
    {
    }
    virtual                  ~CCVUTCoin                    ( void ) = default;
    vector<uint8_t>          m_Data;
    int                      m_DistMin;
    int                      m_DistMax;
    uint64_t                 m_Count;
};
//=================================================================================================
class CCustomer
{
public:
    virtual                  ~CCustomer                    ( void ) = default;
    virtual AFITCoin         FITCoinGen                    ( void ) = 0;
    virtual ACVUTCoin        CVUTCoinGen                   ( void ) = 0;

    virtual void             FITCoinAccept                 ( AFITCoin          x ) = 0;
    virtual void             CVUTCoinAccept                ( ACVUTCoin         x ) = 0;
};

//=================================================================================================
#endif /* __PROGTEST__ */

class CProblem
{
public:
    CProblem(AFITCoin, ACustomer);

    CProblem(ACVUTCoin, ACustomer);

    AFITCoin getFITProblem( void ) const;
    ACVUTCoin getCVUTProblem( void ) const;
    bool isOwner( ACustomer ) const;
private:
    ACustomer m_Owner;
    AFITCoin  m_FITCoinProblem;
    ACVUTCoin m_CVUTCoinProblem;

};
//=================================================================================================
CProblem::CProblem(AFITCoin p, ACustomer c )
{
    m_FITCoinProblem= p;
    m_Owner = c;
    m_CVUTCoinProblem = nullptr;
}
//=================================================================================================
CProblem::CProblem(ACVUTCoin p, ACustomer c)
{
    m_CVUTCoinProblem = p;
    m_Owner = c;
    m_FITCoinProblem = nullptr;
}
//=================================================================================================
AFITCoin CProblem::getFITProblem() const
{
    return m_FITCoinProblem;
}
//=================================================================================================
ACVUTCoin CProblem::getCVUTProblem() const
{
    return m_CVUTCoinProblem;
}
//=================================================================================================
bool CProblem::isOwner(ACustomer c) const
{
    if(m_Owner == c)
        return true;
    return false;
}
//=================================================================================================
class CRig
{
public:
    static void              Solve                         ( ACVUTCoin         x );
    static void              Solve                         ( AFITCoin          x );

    CRig                          ( void );
    ~CRig                         ( void ){}
    void                     Start                         ( int               thrCnt );
    void                     Stop                          ( void );
    void                     AddCustomer                   ( ACustomer         c );
private:

    //=======================================================
    vector<thread>   								m_GenerateProducers;
    atomic<bool> 									m_StopAddGenerateProducers;
    atomic<int> 									m_GenerateProducersCnt;

    mutex			 								m_ProblemsMutex;
    condition_variable								m_FullBufferProblemsEvent;
    condition_variable								m_EmptyBufferProblemsEvent;

    queue<CProblem*>  								m_Problems;

    void GenerateFITListener(ACustomer);
    void GenerateCVUTListener(ACustomer);
    //=======================================================



    //=======================================================
    vector<thread>   				m_AcceptProducers;
    atomic<bool> 					m_StopAddSolvedProblems;
    atomic<int> 					m_AcceptProducersCnt;

    mutex			 				m_SolvedProblemsMutex;
    condition_variable				m_FullBufferSolvedProblemEvent;
    condition_variable				m_EmptyBufferSolvedProblemEvent;

    queue<CProblem*>				m_SolvedProblems;

    void AcceptSolvedsListener(ACustomer);
    //=======================================================



    //=======================================================
    vector<thread>   				m_Consumers;
    atomic<bool>					m_StopAddProblems;
    atomic<int> 					m_ConsumersCnt;

    void SolveProblemsListener();
    //=======================================================


    static const int MAX_PROBLEMS = 30;
    static const int MAX_SOLVED_PROBLEMS = 30;


};
//=================================================================================================
CRig::CRig()
{
    m_StopAddGenerateProducers =
    m_StopAddProblems =
    m_StopAddSolvedProblems = false;

    m_ConsumersCnt =
    m_AcceptProducersCnt =
    m_GenerateProducersCnt = 0;
}

//=================================================================================================

void CRig::Stop(void)
{
    m_StopAddGenerateProducers = true;

    for (int i = 0; i < m_GenerateProducersCnt; i++)
        if(m_GenerateProducers[i].joinable())
            m_GenerateProducers[i].join();

    m_StopAddProblems = true;
    m_EmptyBufferProblemsEvent.notify_all();

    for (int i = 0; i < m_ConsumersCnt; i++)
        if(m_Consumers[i].joinable())
            m_Consumers[i].join();

    m_StopAddSolvedProblems = true;
    m_EmptyBufferSolvedProblemEvent.notify_all();



    for (int i = 0; i < m_AcceptProducersCnt; i++)
        if(m_AcceptProducers[i].joinable())
            m_AcceptProducers[i].join();

}
//=================================================================================================

void CRig::Start(int thrCnt )
{
    for (int i = 0; i < thrCnt; i++)
    {
        m_Consumers.push_back(thread (&CRig::SolveProblemsListener, this));
        m_ConsumersCnt++;
    }

}

//=================================================================================================
void CRig::AddCustomer( ACustomer c )
{
    if(m_StopAddGenerateProducers)
        return;

    m_GenerateProducers.push_back(thread (&CRig::GenerateFITListener, this, c));
    m_GenerateProducersCnt++;

    m_GenerateProducers.push_back(thread (&CRig::GenerateCVUTListener, this, c));
    m_GenerateProducersCnt++;

    m_AcceptProducers.push_back(thread (&CRig::AcceptSolvedsListener, this, c));
    m_AcceptProducersCnt++;

}
//=================================================================================================
void CRig::GenerateFITListener(ACustomer c)
{
    while(true)
    {
        AFITCoin problem = c->FITCoinGen();

        unique_lock<mutex> lockProblems(m_ProblemsMutex);
        m_FullBufferProblemsEvent.wait(lockProblems, [this]
                                       {
                                           return m_Problems.size() < MAX_PROBLEMS;
                                       }
        );

        if(problem == nullptr)
        {

            lockProblems.unlock();
            m_FullBufferProblemsEvent.notify_all();
            m_EmptyBufferProblemsEvent.notify_one();
            return;
        }
        m_Problems.push(new CProblem(problem, c));
        lockProblems.unlock();
        m_EmptyBufferProblemsEvent.notify_one();

    }
}
//=================================================================================================
void CRig::GenerateCVUTListener(ACustomer c)
{
    while(true)
    {
        ACVUTCoin problem = c->CVUTCoinGen();
        unique_lock<mutex> lockProblems(m_ProblemsMutex);
        m_FullBufferProblemsEvent.wait(lockProblems, [this]
                                       {
                                           return m_Problems.size() < MAX_PROBLEMS;
                                       }
        );
        if(problem == nullptr)
        {

            lockProblems.unlock();
            m_EmptyBufferProblemsEvent.notify_one();
            m_FullBufferProblemsEvent.notify_all();
            return;
        }

        m_Problems.push(new CProblem(problem,c));
        lockProblems.unlock();
        m_EmptyBufferProblemsEvent.notify_one();

    }
}
//=================================================================================================
void CRig::SolveProblemsListener(void)
{
    while(true)
    {
        unique_lock<mutex> lockProblems(m_ProblemsMutex);
        m_EmptyBufferProblemsEvent.wait(lockProblems, [this]
                                        {
                                            return m_Problems.empty() == false   || m_StopAddProblems == true ;
                                        }
        );

        if(m_StopAddProblems == true && m_Problems.empty() == true ){

            lockProblems.unlock();
            m_EmptyBufferProblemsEvent.notify_all();
            return;
        }


        CProblem* problem = m_Problems.front();
        m_Problems.pop();

        lockProblems.unlock();
        m_FullBufferProblemsEvent.notify_one();
        if(problem -> getCVUTProblem() != nullptr)
        {

            Solve(problem -> getCVUTProblem());
        }
        if(problem -> getFITProblem() != nullptr)
        {

            Solve(problem -> getFITProblem());
        }

        unique_lock<mutex> lockSolvedProblems(m_SolvedProblemsMutex);
        m_FullBufferSolvedProblemEvent.wait(lockSolvedProblems, [this]
                                            {
                                                return m_SolvedProblems.size() < MAX_SOLVED_PROBLEMS;
                                            }
        );

        m_SolvedProblems.push(problem);
        lockSolvedProblems.unlock();
        m_EmptyBufferSolvedProblemEvent.notify_one();


    }
}
//=================================================================================================
void CRig::AcceptSolvedsListener(ACustomer c)
{
    while(true)
    {

        unique_lock<mutex> lockSolvedProblems(m_SolvedProblemsMutex);
        m_EmptyBufferSolvedProblemEvent.wait(lockSolvedProblems, [this]
                                             {
                                                 return m_SolvedProblems.empty() == false || m_StopAddSolvedProblems == true;
                                             }
        );

        if(m_StopAddSolvedProblems == true && m_SolvedProblems.empty() == true)
        {
            lockSolvedProblems.unlock();
            m_EmptyBufferSolvedProblemEvent.notify_all();
            return;
        }

        CProblem* problem = m_SolvedProblems.front();
        if( problem-> isOwner(c)  == false)
        {


            lockSolvedProblems.unlock();
            m_EmptyBufferSolvedProblemEvent.notify_one();
            continue;
        }


        if(problem -> getCVUTProblem() != nullptr)
        {

            c->CVUTCoinAccept(problem -> getCVUTProblem());
            cout << problem -> getCVUTProblem() ->m_Count << endl;

        }
        if(problem -> getFITProblem() != nullptr)
        {
            c->FITCoinAccept(problem -> getFITProblem());
            cout << problem -> getFITProblem() ->m_Count << endl;
        }
        m_SolvedProblems.pop();
        lockSolvedProblems.unlock();
        m_FullBufferSolvedProblemEvent.notify_one();

    }
}
//=================================================================================================

int binomialCoeff(int n, int k)
{
    uint64_t tmp;
    uint64_t **array = new uint64_t*[n + 1];
    for(int i = 0; i <= n ; i++)
        array[i] = new uint64_t[k + 1];
    for(int i = 0; i <= n; i++)
        array[i][0] = 1;
    for(int i = 1; i <= n; i++)
        for(int j = 1; j <= k; j++)
            array[i][j] = array[i-1][j-1] * i / j;
    tmp = array[n][k];
    for(int i = 0; i <= n; i++)
        delete [] array[i];
    delete  [] array;
    return tmp;
}

//=================================================================================================
string getString(uint8_t numb)
{
    string tmp = "";
    for(int i = 0; i < 8; i++)
    {
        if(1 & numb)
            tmp += "1";
        else
            tmp += "0";
        numb >>= 1;
    }
    reverse(tmp.begin(), tmp.end());
    return tmp;
}

//=================================================================================================
int getKomb(int k, int f)
{
    int tmp = 0;
    int min;
    k < f ? min = k : min = f;
    for(int i = 0; i <= min; i++)
        tmp+=binomialCoeff(f, i);
    return tmp;
}
//=================================================================================================
int distance(string suf, string pref)
{
    int **array = new int*[suf.size() + 1];
    for(int i = 0; i <= (int)suf.size() ; i++)
        array[i] = new int[pref.size() + 1];
    int delta = 0;
    for(int i = 0; i <= (int)suf.size() ; i++)
        array[i][pref.size()] = suf.size() - i;
    for(int j = 0; j <= (int)pref.size(); j++)
        array[suf.size()][j] = pref.size() - j;
    for(int i = (int)suf.size() - 1; i >= 0; i--)
        for(int j = pref.size() - 1; j >= 0; j--)
        {
            if( suf.at(i) == pref.at(j))
                delta = 0;
            else
                delta = 1;
            array[i][j] = min(delta + array[i+1][j+1], min(1 + array[i+1][j], 1 + array[i][j+1])) ;
        }
    int tmp= array[0][0];
    for(int i = 0; i <= (int)suf.size(); i++)
        delete [] array[i];
    delete  [] array;
    return tmp;
}

//=================================================================================================

void CRig::Solve( AFITCoin x)
{
    vector<uint32_t> vectorsNew;
    uint32_t firstV = x->m_Vectors.front();
    uint32_t firstVNeg = ~firstV;
    uint64_t one = 1,  tmp, numb, numbNeg, powT;

    if(x->m_Vectors.size() == 1)
    {
        uint64_t out = 0, komb = 0;
        for(int i = 0; i <= x->m_DistMax; i++)
        {
            komb = binomialCoeff(32, i);
            out += komb;
        }
        x->m_Count = out;
        return;
    }

    for( int n : x->m_Vectors)
    {
        firstV &= n;
        tmp = ~n;
        firstVNeg &= tmp;
    }
    tmp = 0;
    int counter = 0;
    uint32_t tmpV;
    int max = 0; // length of new vector

    if(firstVNeg == 0 && firstV == 0)
    {
        vectorsNew = x->m_Vectors;
    }
    else
        for( auto & n: x->m_Vectors)
        {
            numb = firstV;
            numbNeg = firstVNeg;
            tmpV = n;
            for(int i = 0; i < 32; i++)
            {
                if((one & numb) == 0 && (one & numbNeg) == 0)
                {

                    powT = pow(2, counter) * (tmpV & one);
                    tmp += powT;
                    counter++;
                }
                numb = numb >> 1;
                numbNeg = numbNeg >> 1;
                tmpV = tmpV >> 1;
            }
            max = counter;
            counter = 0;
            vectorsNew.push_back(tmp);
            tmp = 0;
        }

    //********GENERATE ALL COMBINATIONS***********//

    uint32_t MAX = UINT32_MAX;
    MAX = MAX >> (32 - max);
    uint32_t tmpK = 0;
    int dist = 0, distTMP = 0;
    uint32_t o = 1;
    for(uint32_t i = 0; i <= MAX; i++)
    {
        for(auto & n : vectorsNew)
        {
            tmpK = n ^ i;
            for(int k = 0; k < max; k++)
            {
                if(o & tmpK )
                    distTMP++;
                tmpK = tmpK >> 1;
            }
            if(distTMP >= dist)
                dist = distTMP;
            distTMP = 0;
        }
        if(dist == x->m_DistMax)
            x->m_Count++;
        else if (dist < x->m_DistMax)
            x->m_Count += getKomb( x->m_DistMax - dist, 32 - max);
        dist = 0;
    }
}


//=================================================================================================

void CRig::Solve( ACVUTCoin x )
{
    int size = x->m_Data.size() * 8;
    string str = "";
    reverse(x->m_Data.begin(),x->m_Data.end());
    for(auto n : x->m_Data)
        str += getString(n);
    string suf = "", pref = "";
    int d;
    for(int s = 0; s < size; s++)
        for(int p = size - 1; p >= 0; p--)
        {
            suf = str.substr(0, s);
            pref = str.substr(p, size - 1);
            d = distance(suf, pref);
            if(d >= x->m_DistMin && d <= x->m_DistMax)
                x->m_Count++;
        }
}

//=================================================================================================

#ifndef __PROGTEST__
#include "test.inc"
#endif /* __PROGTEST__ */


