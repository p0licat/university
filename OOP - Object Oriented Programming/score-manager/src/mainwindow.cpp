#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    repoController = new CountryRepoController("countriesFile");

    for (int i = 0; i < repoController->getRepoLength(); ++i)
    {
        Country current = repoController->getCountryAtIndex(i);
        QString score = QString::fromStdString(std::to_string(current.getScore()));
        QString textInserted = QString::fromStdString(current.getName()) + " " + score;
        ui->listWidget->insertItem(i, textInserted);

    }
}

MainWindow::~MainWindow()
{
    delete ui;
    delete repoController;
}

void MainWindow::on_listWidget_itemClicked(QListWidgetItem *item)
{
    int row = this->ui->listWidget->row(item);
    Country country = this->repoController->getCountryAtIndex(row);
    this->ui->lineEditName->setText(QString::fromStdString(country.getName()));
    this->ui->lineEditBand->setText(QString::fromStdString(country.getBand()));
    this->ui->lineEditSong->setText(QString::fromStdString(country.getSongTitle()));
    this->ui->lineEditScore->setText(QString::fromStdString(std::to_string(country.getScore())));
}

void MainWindow::on_exitButton_clicked()
{
    QApplication::quit();
}

void MainWindow::on_voteButton_clicked()
{
    if (this->ui->lineEditName->text() != "" )
    {
        QList<QListWidgetItem*> list = this->ui->listWidget->selectedItems();
        int row = this->ui->listWidget->row(list[0]);
        this->repoController->incrementCountryScore(row);
        this->ui->lineEditScore->setText(QString::fromStdString(std::to_string(
                                                                 this->repoController->getCountryAtIndex(row).getScore())));
    }
    else
        return;
}

void MainWindow::on_sortButton_clicked()
{
    this->ui->listWidget->sortItems(Qt::AscendingOrder);
}
