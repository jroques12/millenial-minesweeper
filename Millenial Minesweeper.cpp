#include <iostream>
#include <string>
#include <vector>
#include <array>
#include "M&M_Function.h"
#include "Tile.h"
//#include "Mine Games.h"
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <limits>
#include <tchar.h>
#include <windows.h>


Tile currentSpace;
gameBoard mainBoard;

char confirm;
char cursorIP;
player playerOne;
int& Xcoord = playerOne.playerTile.coordinates[0];
int& Ycoord = playerOne.playerTile.coordinates[1];

int main() {
    mainBoard.tileRandomizer();
   
    std::cout << "The rendezvous point is " << mainBoard.winningSpace[0] << " , "
        << mainBoard.winningSpace[1] << endl;
    
    minePrinting();
    printPowerup();
    
    std::cout << "Your current coordinates are : X- " << currentSpace.coordinates[0] << "Y- " << currentSpace.coordinates[1] << endl;
    std::cout << "Please enter starting coordinates (X 0/100,Y 0/100)";
    std::cin >> Xcoord >> Ycoord;

    std::cout << "Go to " << Xcoord << "," << Ycoord << " (Y/N)?" << endl;
    std::cin >> confirm;

    switch (tolower(confirm)) {

    case 'y':
    case 'Y':
            letsplay();
            while (playerOne.healthPoint > 0) {
                display(Xcoord, Ycoord);
                curs_Mov(Xcoord, Ycoord);
                
            }
        
    case 'n': 
    case 'N':
            std::cout << "Thanks for playing!" << endl;
            system("pause");
            exit(1);
        
    default:
            cout << "Sorry that was an invalid input please restart application." << endl;
            exit(3);

        }
    return 0;
    }
    
    

/* Current Issues: 
Need to find a way to deactivate power ups after they are landed on/use same method used for mines
display() function displays the y axis inverted
Need to mess around with representations of tile for smoother recognition 
when there is an input error after failing to answer a mine correctly Xcoor keeps iterating endlessly(double uninteded loop structure discovered now fixed)

*/