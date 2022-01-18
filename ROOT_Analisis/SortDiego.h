#ifndef _Sort_h_
#define _Sort_h_

#include <vector>
#include <algorithm>


template<typename T>
struct ByFirst {
  bool operator()(const std::pair<T, T>& p1, const std::pair<T, T>& p2) const
  { return p1.first < p2.first; }
};

template<typename T>
struct ByLast {
  bool operator()(const std::pair<T, T>& p1, const std::pair<T, T>& p2) const
  { return p1.first > p2.first; }
};


template<typename T>
void
Sort(std::vector<T>& x, std::vector<T>& y)
{
  const std::size_t n = x.size();
  std::vector<std::pair<T, T> > v(n);
  for (unsigned int i = 0; i < n; ++i)
    v[i] = std::make_pair(x[i], y[i]);
  std::sort(v.begin(), v.end(), ByFirst<T>());
  for (unsigned int i = 0; i < n; ++i) {
    x[i] = v[i].first;
    y[i] = v[i].second;
  }
}

template<typename T>
void
SortL(std::vector<T>& x, std::vector<T>& y)
{
  const std::size_t n = x.size();
  std::vector<std::pair<T, T> > v(n);
  for (unsigned int i = 0; i < n; ++i)
    v[i] = std::make_pair(x[i], y[i]);
  std::sort(v.begin(), v.end(), ByLast<T>());
  for (unsigned int i = 0; i < n; ++i) {
    x[i] = v[i].first;
    y[i] = v[i].second;
  }
}



template<typename T>
void
Sort(std::vector<T>& x, std::vector<T>& y, std::vector<T>& z, std::vector<T>& w)
{
  const std::size_t n = x.size();
  std::vector<std::pair<T, T> > v1(n), v2(n), v3(n);
  for (unsigned int i = 0; i < n; ++i) {
    v1[i] = std::make_pair(x[i], y[i]);
    v2[i] = std::make_pair(x[i], z[i]);
    v3[i] = std::make_pair(x[i], w[i]);
  }
  
  std::sort(v1.begin(), v1.end(), ByFirst<T>());
  std::sort(v2.begin(), v2.end(), ByFirst<T>());
  std::sort(v3.begin(), v3.end(), ByFirst<T>());
  
  for (unsigned int i = 0; i < n; ++i) {
    x[i] = v1[i].first;
    y[i] = v1[i].second;
    z[i] = v2[i].second;
    w[i] = v3[i].second;
  }
}

template<typename T>
void
SortL(std::vector<T>& x, std::vector<T>& y, std::vector<T>& z, std::vector<T>& w)
{
  const std::size_t n = x.size();
  std::vector<std::pair<T, T> > v1(n), v2(n), v3(n);
  for (unsigned int i = 0; i < n; ++i) {
    v1[i] = std::make_pair(x[i], y[i]);
    v2[i] = std::make_pair(x[i], z[i]);
    v3[i] = std::make_pair(x[i], w[i]);
  }
  
  std::sort(v1.begin(), v1.end(), ByLast<T>());
  std::sort(v2.begin(), v2.end(), ByLast<T>());
  std::sort(v3.begin(), v3.end(), ByLast<T>());
  
  for (unsigned int i = 0; i < n; ++i) {
    x[i] = v1[i].first;
    y[i] = v1[i].second;
    z[i] = v2[i].second;
    w[i] = v3[i].second;
  }
}

template<typename T>
void
Sort(std::vector<T>& x, std::vector<T>& y, std::vector<T>& z, std::vector<T>& w, std::vector<T>& w1, std::vector<T>& w2)
{
  const std::size_t n = x.size();
  std::vector<std::pair<T, T> > v1(n), v2(n), v3(n), v4(n), v5(n);
  for (unsigned int i = 0; i < n; ++i) {
    v1[i] = std::make_pair(x[i], y[i]);
    v2[i] = std::make_pair(x[i], z[i]);
    v3[i] = std::make_pair(x[i], w[i]);
    v4[i] = std::make_pair(x[i], w1[i]);
    v5[i] = std::make_pair(x[i], w2[i]);
  }
  
  std::sort(v1.begin(), v1.end(), ByLast<T>());
  std::sort(v2.begin(), v2.end(), ByLast<T>());
  std::sort(v3.begin(), v3.end(), ByLast<T>());
  std::sort(v4.begin(), v4.end(), ByLast<T>());
  std::sort(v5.begin(), v5.end(), ByLast<T>());
  
  for (unsigned int i = 0; i < n; ++i) {
    x[i] = v1[i].first;
    y[i] = v1[i].second;
    z[i] = v2[i].second;
    w[i] = v3[i].second;
    w1[i] = v4[i].second;
    w2[i] = v5[i].second;
  }
}

template<typename T>
void
Sort(std::vector<T>& x, std::vector<T>& y, std::vector<T>& z, std::vector<T>& w, std::vector<T>& w1, std::vector<T>& w2, std::vector<T>& w3)
{
  const std::size_t n = x.size();
  std::vector<std::pair<T, T> > v1(n), v2(n), v3(n), v4(n), v5(n), v6(n);
  for (unsigned int i = 0; i < n; ++i) {
    v1[i] = std::make_pair(x[i], y[i]);
    v2[i] = std::make_pair(x[i], z[i]);
    v3[i] = std::make_pair(x[i], w[i]);
    v4[i] = std::make_pair(x[i], w1[i]);
    v5[i] = std::make_pair(x[i], w2[i]);
    v6[i] = std::make_pair(x[i], w3[i]);
  }
  
  std::sort(v1.begin(), v1.end(), ByLast<T>());
  std::sort(v2.begin(), v2.end(), ByLast<T>());
  std::sort(v3.begin(), v3.end(), ByLast<T>());
  std::sort(v4.begin(), v4.end(), ByLast<T>());
  std::sort(v5.begin(), v5.end(), ByLast<T>());
  std::sort(v6.begin(), v6.end(), ByLast<T>());
  
  for (unsigned int i = 0; i < n; ++i) {
    x[i] = v1[i].first;
    y[i] = v1[i].second;
    z[i] = v2[i].second;
    w[i] = v3[i].second;
    w1[i] = v4[i].second;
    w2[i] = v5[i].second;
    w3[i] = v6[i].second;
  }
}




#endif
