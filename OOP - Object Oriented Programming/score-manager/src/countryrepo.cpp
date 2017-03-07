#include "countryrepo.h"

Country CountryRepo::getElementAtIndex(unsigned int index)
{
    std::vector<Country>::iterator it = this->countryList.begin();
    if ( index >= this->countryList.size() )
        return Country("", "", "", -1);
    it += index;
    return *it;
}

void CountryRepo::removeCountryAtIndex(int index)
{
    if ( !index <= this->countryList.size() )
        return;
    std::vector<Country>::iterator it = this->countryList.begin();
    it += index;
    this->countryList.erase(it);
    return;
}
