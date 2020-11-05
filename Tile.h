#ifndef TILE_H_INCLUDED
#define TILE_H_INCLUDED
#include<iostream>
#include<vector>
#include<string>
#include "M&M_Function.h"
#include<time.h>
#include <stdlib.h>
#include <stdio.h>
using namespace std;

class Tile
{
public:
    int coordinates[2] {0,0};
    bool itsATrapX= false;
    bool itsATrapY= false;
    bool powerUp= false;

private:




};
class player
{
public:
    Tile playerTile;
    unsigned healthPoint =3;

};
class gameBoard
{
public:


    int winningSpace[2] {10,10};
    int mineCoor[10][2];
    int powerUpCoor[10][2]
    {
        {5,7},// Power-up location no 1
        {18,3},//no 2
        {15,27},//etc...
        {19,21},
    };


    void tileRandomizer(){
        srand((unsigned) time(0));
        this->winningSpace[0]=rand()%20;
        this->winningSpace[1]=rand()%20;

        for(int i=0; i<10; i++){
            this->mineCoor[i][0]=rand()%20;
            this->mineCoor[i][1]=rand()%20;
        }
        for(int j=0; j<10; j++){
            this->powerUpCoor[j][0]=rand()%20;
            this->powerUpCoor[j][1]=rand()%20;
        }

    }






};
#endif
