#ifndef M M FUNCTION H
#define M M FUNCTION H
#include "Tile.h"
#include <vector>
#include <iostream>
#include <array>
#include <string>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <limits>
using namespace std;
extern Tile currentSpace;
extern char cursorIP;
extern gameBoard mainBoard;
extern player playerOne;

void didWinGame(int& Xcoord, int& Ycoord)
{
    if(Xcoord == mainBoard.winningSpace[0] && Ycoord == mainBoard.winningSpace[1])
    {
        cout<<"Congratulations you found the rendezvous point and are being taken to safety!!"<<endl;
        cout<<"Thank you so much for playing we hope you enjoyed!!"<<endl;
        system("pause");
        exit(0);
    }
}
void evalPowerUpSpace(int& Xcoord, int&Ycoord)
{
    for(int n =0; n<10; n++)
    {
        if(Xcoord==mainBoard.powerUpCoor[n][0] && Ycoord==mainBoard.powerUpCoor[n][1])
        {
            playerOne.healthPoint++;
            cout<<"Power Up Space! You now have "<<playerOne.healthPoint<<" health left "<<endl;
            
            system("pause");
        }
    }
}
inline void minePrinting()
{

    std::cout<<"Mines are at the following locations: "<<endl;
    for(int l=0; l<10; l++)
    {
        cout<<mainBoard.mineCoor[l][0]<<" , "<<mainBoard.mineCoor[l][1]<<" ||"<<endl
            ;
    }


}
inline void display(int &Xcoord, int& Ycoord)
{
    for(int height = 0; height<20; height++){
        for( int length =0; length<20; length++){
            if(Xcoord==length && Ycoord == height){
                cout<<"X";
            }
            else {
                cout<<"7";
            }
        }
        cout<<endl;
    }

}
inline void ifDead()
{

    if (playerOne.healthPoint==0)
    {
        cout<<"You ran out of health and died D: oh no! Better luck next time!"<<endl;
        system("pause");
        exit(2);
    }
}
void trapQuest1()
{


    int sunDist=93;
    int questAns;

    cout<<"You have tripped a mine! Don't move! "<<endl;
    cout<<"Fill in the blank. The Sun is ___ million miles from Earth. "<<endl;

    //cin.clear();
    //fflush(stdin);
    //cin.ignore();
    cin>>questAns;

    if (questAns!=sunDist)
    {
        cout<<"Sorry that was an incorrect answer and the mine blew up. "<<endl;
        playerOne.healthPoint--;
        cout<<"You now have "<<playerOne.healthPoint<<" health points left."<<endl;
        system("pause");

    }
    else
    {
        cout<<"Nice job, everyone knows land mines calm down with astronomy facts! "<<endl;
        system("pause");
    }

}
void isTrapSpace(int& Xcoord, int& Ycoord)
{
    for(int iter=0; iter<10; iter++)
    {
        if(Xcoord==mainBoard.mineCoor[iter][0] && Ycoord==mainBoard.mineCoor[iter][1])
        {
            mainBoard.mineCoor[iter][0]=102;
            mainBoard.mineCoor[iter][1]=102;
            trapQuest1();
            cout<<"Where would you like to go next?"<<endl;
        }

    }
}
void letsplay()
{
    std::cout<<"-----Find the rendezvous coordinates without killing yourself."<<std::endl;
    std::cout<<"----------------------------------Use WASD to move your player"<<endl;
    std::cout<<"-----------------Each space you move to may be a blank, a mine"<<endl;
    std::cout<<"-or power-up. If you land on a mine you must complete the task"<<endl;
    std::cout<<"---------in order to stay alive, you can only survive 3 mines."<<endl;
    std::cout<<"---------Power-ups will either give you hp or a mine location "<<endl;
}
void printPowerup()
{
    cout<<"Power up coordinates are :"<<endl;
    for(int p =0; p<10; p++)
    {

        cout<<mainBoard.powerUpCoor[p][0]<<" , "<<mainBoard.powerUpCoor[p][1]<<"||"<<endl;
    }
}
void curs_Mov(int& Xcoord,int& Ycoord)
{


    cin>>cursorIP;

    switch(cursorIP)/*moves cursor using WASD*/
    {

    case 'W':
    case'w' :
        ++Ycoord;
        didWinGame(Xcoord,Ycoord);
        isTrapSpace(Xcoord,Ycoord);
        evalPowerUpSpace(Xcoord,Ycoord);
        display(Xcoord,Ycoord);
        break;

    case 'A':
    case'a' :
            --Xcoord;
        didWinGame(Xcoord,Ycoord);
        isTrapSpace(Xcoord,Ycoord);
        evalPowerUpSpace(Xcoord,Ycoord);
        display(Xcoord,Ycoord);
        break;

    case 'S':
    case's' :
        --Ycoord;
        didWinGame(Xcoord,Ycoord);
        isTrapSpace(Xcoord,Ycoord);
        evalPowerUpSpace(Xcoord,Ycoord);
        display(Xcoord,Ycoord);
        break;

    case 'D':
    case'd' :
            ++Xcoord;
        didWinGame(Xcoord,Ycoord);
        isTrapSpace(Xcoord,Ycoord);
        evalPowerUpSpace(Xcoord,Ycoord);
        display(Xcoord,Ycoord);
        break;

    default:
        std::cout<<"Input Error"<<endl;//Error for not using WASD
        
        break;
    }
    if(Xcoord<0||Xcoord>20)  //sets map boundaries
    {
        Xcoord<0? Xcoord=20 : Xcoord=0;

    }
    if(Ycoord<0||Ycoord>20)  //sets map boundaries
    {
        Ycoord<0 ? Ycoord=20 : Ycoord=0;

    }
    //display(Xcoord,Ycoord);
    cout<<"Player One is at space "<<Xcoord<<" , "<<Ycoord<<endl;


}








#endif
