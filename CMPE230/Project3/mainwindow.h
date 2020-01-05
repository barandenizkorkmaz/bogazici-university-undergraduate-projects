#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTest>
#include <QPushButton>
#include <QLabel>
#include "qlabel.h"
#include <list>
#include <string>

using namespace std;

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void gameStart();
    int counter=0;
    int pairCounter=0;
    int tryCounter=0;
    vector<QPushButton*>* buttons=new vector<QPushButton*>;
    vector<QPushButton*>* pairedButtons=new vector<QPushButton*>;
    string buttonContent[24]={"Z","Z","Z","Z","Z","Z","Z","Z","Z","Z","Z","Z","Z","Z","Z","Z","Z","Z","Z","Z","Z","Z","Z","Z"};
    list<string> myLetters={"A","B","C","D","E","F","G","H","I","J","K","L"};
    void checkLetters(vector<QPushButton*>* buttons);

private slots:
    void on_pushButton_clicked();
    void on_pushButton_2_clicked();
    void on_pushButton_3_clicked();
    void on_pushButton_4_clicked();
    void on_pushButton_5_clicked();
    void on_pushButton_6_clicked();
    void on_pushButton_7_clicked();
    void on_pushButton_8_clicked();
    void on_pushButton_9_clicked();
    void on_pushButton_10_clicked();
    void on_pushButton_11_clicked();
    void on_pushButton_12_clicked();
    void on_pushButton_13_clicked();
    void on_pushButton_14_clicked();
    void on_pushButton_15_clicked();
    void on_pushButton_16_clicked();
    void on_pushButton_17_clicked();
    void on_pushButton_18_clicked();
    void on_pushButton_19_clicked();
    void on_pushButton_20_clicked();
    void on_pushButton_21_clicked();
    void on_pushButton_22_clicked();
    void on_pushButton_23_clicked();
    void on_pushButton_24_clicked();
    void on_pushButton_25_clicked();


private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
