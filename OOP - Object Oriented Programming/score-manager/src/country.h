#ifndef COUNTRY_H
#define COUNTRY_H

#include <string>
typedef std::string string;

class Country {
private:
    string name;
    string band;
    string song_title;
    int score;
public:
    Country() : name(""), band(""), song_title(""), score(-1) {}
    Country(string name, string band, string song_title, int score) :
        name(name), band(band), song_title(song_title), score(score) {}
    ~Country() {}

    //getters
    string getName() { return name; }
    string getBand() { return band; }
    string getSongTitle() { return song_title; }
    int getScore() { return score; }

    //setters
    void setName(string name) { this->name = name; }
    void setBand(string band) { this->band = band; }
    void setSongTitle(string song_title) { this->song_title = song_title; }
    void setScore(int score) { this->score = score; }

    string toString() {
        string returnValue = "";
        returnValue += "Country: ";
        returnValue += this->name + " ";
        returnValue += this->band + " ";
        returnValue += this->song_title + " ";
        returnValue += (std::to_string(this->score)) + "\n";

        return returnValue;
    }

};


#endif // COUNTRY_H
