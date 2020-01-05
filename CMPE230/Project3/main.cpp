#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QApplication>
#include <iostream>
using namespace std;
int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.gameStart();
    w.show();
    cout<<w.buttonContent;
    return a.exec();
}
