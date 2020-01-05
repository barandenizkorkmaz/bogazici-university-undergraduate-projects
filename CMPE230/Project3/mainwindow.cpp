#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <iostream>
using namespace std;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::gameStart(){
    for(string letters:myLetters){
        int index1=rand()%24;
        while(true){
            if(buttonContent[index1]=="Z"){
                buttonContent[index1]=letters;
                break;
            }
            index1+=1;
            index1=index1%24;
        }
        int index2=rand()%24;
        while(true){
            if(buttonContent[index2]=="Z"){
                buttonContent[index2]=letters;
                break;
            }
            index2+=1;
            index2=index2%24;
        }
    }
}

void MainWindow::checkLetters(vector<QPushButton *>* buttons){
    this->setDisabled(true);
    QTest::qWait(500);
    this->setDisabled(false);
    if(buttons->at(0)->text()==buttons->at(1)->text()){
        buttons->at(0)->setVisible(false);
        buttons->at(1)->setVisible(false);
        pairedButtons->push_back(buttons->at(0));
        pairedButtons->push_back(buttons->at(1));
        pairCounter++;
        //tryCounter++;
        ui->label->setText(QString::number(pairCounter));
    }
    else{
        buttons->at(0)->setText(tr("X"));
        buttons->at(0)->setDisabled(false);
        buttons->at(1)->setText(tr("X"));
        buttons->at(1)->setDisabled(false);
        //tryCounter++;
    }
    buttons->clear();
    counter=0;



}

void MainWindow::on_pushButton_clicked(){
    QString qstr=QString::fromStdString(buttonContent[0]);
    ui->pushButton->setText(qstr);
    ui->pushButton->setDisabled(true);
    buttons->push_back(ui->pushButton);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_2_clicked(){
    QString qstr=QString::fromStdString(buttonContent[1]);
    ui->pushButton_2->setText(qstr);
    ui->pushButton_2->setDisabled(true);
    buttons->push_back(ui->pushButton_2);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_3_clicked(){
    QString qstr=QString::fromStdString(buttonContent[2]);
    ui->pushButton_3->setText(qstr);
    ui->pushButton_3->setDisabled(true);
    buttons->push_back(ui->pushButton_3);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_4_clicked(){
    QString qstr=QString::fromStdString(buttonContent[3]);
    ui->pushButton_4->setText(qstr);
    ui->pushButton_4->setDisabled(true);
    buttons->push_back(ui->pushButton_4);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_5_clicked(){
    QString qstr=QString::fromStdString(buttonContent[4]);
    ui->pushButton_5->setText(qstr);
    ui->pushButton_5->setDisabled(true);
    buttons->push_back(ui->pushButton_5);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_6_clicked(){
    QString qstr=QString::fromStdString(buttonContent[5]);
    ui->pushButton_6->setText(qstr);
    ui->pushButton_6->setDisabled(true);
    buttons->push_back(ui->pushButton_6);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_7_clicked(){
    QString qstr=QString::fromStdString(buttonContent[6]);
    ui->pushButton_7->setText(qstr);
    ui->pushButton_7->setDisabled(true);
    buttons->push_back(ui->pushButton_7);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_8_clicked(){
    QString qstr=QString::fromStdString(buttonContent[7]);
    ui->pushButton_8->setText(qstr);
    ui->pushButton_8->setDisabled(true);
    buttons->push_back(ui->pushButton_8);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_9_clicked(){
    QString qstr=QString::fromStdString(buttonContent[8]);
    ui->pushButton_9->setText(qstr);
    ui->pushButton_9->setDisabled(true);
    buttons->push_back(ui->pushButton_9);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_10_clicked(){
    QString qstr=QString::fromStdString(buttonContent[9]);
    ui->pushButton_10->setText(qstr);
    ui->pushButton_10->setDisabled(true);
    buttons->push_back(ui->pushButton_10);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_11_clicked(){
    QString qstr=QString::fromStdString(buttonContent[10]);
    ui->pushButton_11->setText(qstr);
    ui->pushButton_11->setDisabled(true);
    buttons->push_back(ui->pushButton_11);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_12_clicked(){
    QString qstr=QString::fromStdString(buttonContent[11]);
    ui->pushButton_12->setText(qstr);
    ui->pushButton_12->setDisabled(true);
    buttons->push_back(ui->pushButton_12);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_13_clicked(){
    QString qstr=QString::fromStdString(buttonContent[12]);
    ui->pushButton_13->setText(qstr);
    ui->pushButton_13->setDisabled(true);
    buttons->push_back(ui->pushButton_13);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_14_clicked(){
    QString qstr=QString::fromStdString(buttonContent[13]);
    ui->pushButton_14->setText(qstr);
    ui->pushButton_14->setDisabled(true);
    buttons->push_back(ui->pushButton_14);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_15_clicked(){
    QString qstr=QString::fromStdString(buttonContent[14]);
    ui->pushButton_15->setText(qstr);
    ui->pushButton_15->setDisabled(true);
    buttons->push_back(ui->pushButton_15);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_16_clicked(){
    QString qstr=QString::fromStdString(buttonContent[15]);
    ui->pushButton_16->setText(qstr);
    ui->pushButton_16->setDisabled(true);
    buttons->push_back(ui->pushButton_16);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_17_clicked(){
    QString qstr=QString::fromStdString(buttonContent[16]);
    ui->pushButton_17->setText(qstr);
    ui->pushButton_17->setDisabled(true);
    buttons->push_back(ui->pushButton_17);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_18_clicked(){
    QString qstr=QString::fromStdString(buttonContent[17]);
    ui->pushButton_18->setText(qstr);
    ui->pushButton_18->setDisabled(true);
    buttons->push_back(ui->pushButton_18);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_19_clicked(){
    QString qstr=QString::fromStdString(buttonContent[18]);
    ui->pushButton_19->setText(qstr);
    ui->pushButton_19->setDisabled(true);
    buttons->push_back(ui->pushButton_19);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_20_clicked(){
    QString qstr=QString::fromStdString(buttonContent[19]);
    ui->pushButton_20->setText(qstr);
    ui->pushButton_20->setDisabled(true);
    buttons->push_back(ui->pushButton_20);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_21_clicked(){
    QString qstr=QString::fromStdString(buttonContent[20]);
    ui->pushButton_21->setText(qstr);
    ui->pushButton_21->setDisabled(true);
    buttons->push_back(ui->pushButton_21);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_22_clicked(){
    QString qstr=QString::fromStdString(buttonContent[21]);
    ui->pushButton_22->setText(qstr);
    ui->pushButton_22->setDisabled(true);
    buttons->push_back(ui->pushButton_22);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_23_clicked(){
    QString qstr=QString::fromStdString(buttonContent[22]);
    ui->pushButton_23->setText(qstr);
    ui->pushButton_23->setDisabled(true);
    buttons->push_back(ui->pushButton_23);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_24_clicked(){
    QString qstr=QString::fromStdString(buttonContent[23]);
    ui->pushButton_24->setText(qstr);
    ui->pushButton_24->setDisabled(true);
    buttons->push_back(ui->pushButton_24);
    counter++;
    if(counter==1){
        tryCounter++;
        ui->label_2->setText(QString::number(tryCounter));
    }
    if(counter==2){
        checkLetters(buttons);
    }
}
void MainWindow::on_pushButton_25_clicked(){
    for(vector<QPushButton*>::iterator itr=pairedButtons->begin();itr!=pairedButtons->end();itr++){
        (*itr)->setVisible(true);
        (*itr)->setDisabled(false);
        (*itr)->setText(tr("X"));
    }
    for(vector<QPushButton*>::iterator itr=buttons->begin();itr!=buttons->end();itr++){
        (*itr)->setVisible(true);
        (*itr)->setDisabled(false);
        (*itr)->setText(tr("X"));
    }
    buttons->clear();
    pairedButtons->clear();
    for(int i=0;i<24;i++){
        buttonContent[i]="Z";
    }
    counter=0;
    pairCounter=0;
    tryCounter=0;
    ui->label->setText(QString::number(pairCounter));
    ui->label_2->setText(QString::number(tryCounter));
    this->gameStart();
}

