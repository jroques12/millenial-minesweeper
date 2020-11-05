#ifndef STONE_ARCHIVE_H_INCLUDED
#define STONE_ARCHIVE_H_INCLUDED
#include <iostream>
#include <string>
#include <vector>
#include <array>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <fstream>
using namespace std;

class Stone
{

public:


    string stoneName="Not Entered";
    vector<string> keyWord;
    string color="Not Entered";
    string description="Not Entered";
    string elementAffinity="Not Entered";


    int hardScale;
    int atomicNumber;

    Stone()
    {
        extern vector<Stone> dataBase;
        static string currentInput;
        static string origFile;
        static ofstream outFile;
        static ifstream inFile;

        inFile.open("Stone_Archive.txt");

        cout<<"What is the name of the stone?"<<endl;
        cin.ignore();
        getline(cin,this->stoneName);


        cout<<"Stone name is "<<this->stoneName<<endl;//initialize stoneName
keyEntry:

        cout<<"What keyword would you like associated with it?"<<endl;
        getline(cin,currentInput);
        this->keyWord.push_back(currentInput);//adds keywords to string object vector
        cout<<"Would you like to add another keyword?(y/n)"<<endl;
        getline(cin,currentInput);
        if(currentInput=="y"||currentInput=="Y")
        {
            goto keyEntry;
        }
        cout<<"All keywords associated with "<<this->stoneName<<" are: "<<endl;
        for(size_t i =0; i!= keyWord.size(); i++)
        {
            cout<<keyWord[i]<<" , ";

        }
        cout<<endl;

        cout<<"What color or colors are in this stone?"<<endl;//initialize color member
        cin>>this->color;
        cout<<this->stoneName<<" has a color of "<<this->color<<endl;

        dataBase.push_back(*this);
        outFile.open("Stone_Archive.txt",std::ios_base::app);
        if(outFile.is_open())
        {
            outFile<<origFile<<endl;
            outFile<<"Stone Name: "<<this->stoneName<<endl;
            outFile<<"Keywords :";
            for(size_t i =0; i!= keyWord.size(); i++)
            {
                outFile<<keyWord[i]<<" | ";
            }
            outFile<<endl;


            outFile<<"Color: "<<this->color<<endl;
            outFile<<"----------------------------"<<endl;
        }
        inFile.close();
        outFile.close();
    }
};



#endif // STONE_ARCHIVE_H_INCLUDED
