#include "countryrepocontroller.h"

CountryRepoController::CountryRepoController(std::string fileName)
{
    if ( fileName == "" )
        qDebug("File does not exist.");
    else
    {
        bool result = loadCountriesToRepo(fileName);
        if ( result == true )
            return;
    }
}

Country CountryRepoController::formatInput(QString in)
{
    std::string input = in.toStdString();
    std::string name = "";
    std::string band = "";
    std::string song = "";
    std::string scoreString = "";
    int score;

    int count = 0;
    // count 0 means the first quotation
    for (unsigned int i = 0; i < input.length(); ++i)
    {
        if (input[i] == '"' && count == 0 )
        {
            ++i;
            while ( i < input.length() && input[i] != '"' )
            {
                name += input[i];
                i++;
            }
            i++;
            count++;
        }
        else if ( input[i] == '"' && count == 1 )
        {
            ++i;
            while ( i < input.length() && input[i] != '"' )
            {
                band += input[i];
                i++;
            }
            i++;
            count++;
        }
        else if ( input[i] == '"' && count == 2 )
        {
            ++i;
            while ( i < input.length() && input[i] != '"' )
            {
                song += input[i];
                i++;
            }
            i++;
            count++;
        }
        else if ( input[i] == '"' && count == 3 )
        {
            ++i;
            while ( i < input.length() && input[i] != '"' )
            {
                scoreString += input[i];
                i++;
            }
            i++;
            count++;
        }
        else if ( isdigit(input[i]) && count == 3 )
        {
            while ( isdigit(input[i]) )
            {
                scoreString += input[i];
                ++i;
            }
            count++;
        }
    }
    score = atoi(scoreString.c_str());
    Country rVal(name, band, song, score);
    return rVal;
}

int CountryRepoController::getRepoLength()
{
    return this->repo.getLength();
}

bool CountryRepoController::loadCountriesToRepo(std::string file)
{
    QString fileName = QString::fromStdString(file);
    QFile inputFile(fileName);

    if (inputFile.exists() )
        qDebug() << "Exists.";
    if (inputFile.open(QIODevice::ReadOnly))
    {
       QTextStream in(&inputFile);
       while (!in.atEnd())
       {
          QString line = in.readLine();
          qDebug() << line;
          Country c = formatInput(line);
          QString formatted = QString::fromStdString(c.toString());
          qDebug() << "Formatted line: " + formatted;
          this->repo.insertCountry(c);
       }
       inputFile.close();
    }

    return true;
}

bool CountryRepoController::addCountryToRepo(Country country)
{
    this->repo.insertCountry(country);
    return true;
}

Country CountryRepoController::getCountryAtIndex(int index)
{
    Country ctrAtIndex = this->repo.getElementAtIndex(index);

    return ctrAtIndex;
}

void CountryRepoController::incrementCountryScore(int index)
{
    this->repo.incrementAtIndex(index);
}
