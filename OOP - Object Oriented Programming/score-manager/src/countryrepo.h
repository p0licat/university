#ifndef COUNTRYREPO_H
#define COUNTRYREPO_H

#include "country.h"
#include <vector>

class CountryRepo {
private:
    std::vector<Country> countryList;
public:
    CountryRepo() {}
    CountryRepo(int length) { this->countryList.resize(length); }
    ~CountryRepo() {}

    int getLength() { return this->countryList.size(); }
    void insertCountry (Country c) { this->countryList.push_back(c); }
    void removeCountryAtIndex(int index);
    Country getElementAtIndex(unsigned int index);
    void clearAll() { this->countryList.clear(); }
    void incrementAtIndex(int index) {
        if ( index < (int)countryList.size() )
            countryList[index].setScore(countryList[index].getScore() + 1);
    }
};

#endif // COUNTRYREPO_H
