#pragma once
#include <iostream>
#include <fstream>
#include<string>
#include <vector>
#include <utility>
#include <cstdlib>
#include <ctime>

using namespace std;

const int MAXN = 101;   // max map size (2n+1 must be <= MAXN)
const int MAX_LINE = 100;
int countMount(int n, int arr[][MAXN], int dir);
int step_available(int n, int arr[][MAXN], int dir);
//void createPart(int n, int arr[][MAXN], int map[], int pos);
void readBase(string fileName, int n);
void writeBase(string fileName, int n);
void createMap(int n, int arr[][MAXN]);
int return_direct(int n, float mounts[], float steps[], float base[]);
void returnBase(int n, int arr[][MAXN], float preBase, float base[]);
