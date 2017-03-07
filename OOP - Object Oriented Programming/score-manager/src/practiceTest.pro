#-------------------------------------------------
#
# Project created by QtCreator 2016-05-25T16:36:50
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = practiceTest
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    country.cpp \
    countryrepo.cpp \
    countryrepocontroller.cpp

HEADERS  += mainwindow.h \
    country.h \
    countryrepo.h \
    countryrepocontroller.h

FORMS    += mainwindow.ui

DISTFILES += \
    countriesFile
