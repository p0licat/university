#ifndef COUNTRYREPOCONTROLLER_H
#define COUNTRYREPOCONTROLLER_H

#include "countryrepo.h"
#include <string>
#include <fstream>
#include <regex>

#include <QDebug>
#include <QString>
#include <QFile>

class CountryRepoController {
private:
    CountryRepo repo;
public:
    CountryRepoController() {}
    CountryRepoController(std::string fileName);
    ~CountryRepoController() {}

    bool addCountryToRepo(Country country);
    Country getCountryAtIndex(int index);
    bool loadCountriesToRepo(std::string fileName);
    Country formatInput(QString input);
    int getRepoLength();
    void incrementCountryScore(int index);
};

#endif // COUNTRYREPOCONTROLLER_H
