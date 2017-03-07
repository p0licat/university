#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QListWidgetItem>

#include "country.h"
#include "countryrepo.h"
#include "countryrepocontroller.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_listWidget_itemClicked(QListWidgetItem *item);

    void on_exitButton_clicked();

    void on_voteButton_clicked();

    void on_sortButton_clicked();

private:
    Ui::MainWindow *ui;
    CountryRepoController* repoController;
};

#endif // MAINWINDOW_H
