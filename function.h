#pragma once
#include <iostream>
#include <vector>
#include <utility>
#include <cstdlib>
#include <ctime>

using namespace std;

const int MAXN = 101;   // max map size (2n+1 must be <= MAXN)

int countMount(int n, int arr[][MAXN], int dir);
int step_available(int n, int arr[][MAXN], int dir);
//void createPart(int n, int arr[][MAXN], int map[], int pos);
void createMap(int n, int arr[][MAXN]);
int return_direct(float mounts[], float steps[], float base[]);